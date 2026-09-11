#!/usr/bin/env node
// Local dashboard server: browser-safe proxy for fresh public Binance data.
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { randomUUID } from 'node:crypto';

const root = resolve('.');
const rankSkill = await import(pathToFileURL(resolve(root, '.agents/skills/crypto-market-rank/scripts/cli.mjs')).href);
const tokenInfoSkill = await import(pathToFileURL(resolve(root, '.agents/skills/query-token-info/scripts/cli.mjs')).href);
const port = Number(process.env.PORT || 8787);
const symbols = new Set(['BTCUSDT', 'ETHUSDT', 'BNBUSDT']);

function send(res, status, body, contentType = 'application/json') {
  res.writeHead(status, { 'Content-Type': contentType, 'Cache-Control': 'no-store' });
  res.end(contentType === 'application/json' ? JSON.stringify(body) : body);
}

async function bodyJson(req) {
  let text = '';
  for await (const chunk of req) text += chunk;
  return text ? JSON.parse(text) : {};
}

async function binancePublic(path) {
  const hosts = ['data-api.binance.vision', 'api.binance.com', 'api1.binance.com', 'api2.binance.com', 'api3.binance.com'];
  let lastError;
  for (const host of hosts) {
    try {
      const response = await fetch(`https://${host}${path}`, {
        headers: { 'Cache-Control': 'no-cache' },
        signal: AbortSignal.timeout(8000),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(`Binance HTTP ${response.status}: ${data.msg || 'request failed'}`);
      return data;
    } catch (error) {
      lastError = error;
    }
  }
  throw new Error(`Binance public API unavailable after ${hosts.length} attempts: ${lastError?.message || 'fetch failed'}`);
}

createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (req.method === 'GET' && url.pathname === '/') {
      return send(res, 200, await readFile(resolve(root, 'index.html'), 'utf8'), 'text/html; charset=utf-8');
    }
    if (req.method === 'POST' && url.pathname === '/api/rank') {
      const params = await bodyJson(req);
      const result = await rankSkill.call(rankSkill.COMMANDS['token-rank'](params)); // One new upstream skill request per call.
      return send(res, 200, result);
    }
    if (req.method === 'POST' && url.pathname === '/api/token-search') {
      const { keyword, chainIds = '56' } = await bodyJson(req);
      if (typeof keyword !== 'string' || !keyword.trim() || keyword.length > 80) {
        return send(res, 400, { error: 'A token keyword of 1–80 characters is required.' });
      }
      const result = await tokenInfoSkill.call(tokenInfoSkill.COMMANDS.search({ keyword: keyword.trim(), chainIds }));
      return send(res, 200, result);
    }
    if (req.method === 'POST' && url.pathname === '/api/token-audit') {
      const { chainId = '56', contractAddress } = await bodyJson(req);
      if (!['56', '1', '8453', 'CT_501'].includes(String(chainId)) || typeof contractAddress !== 'string' || !contractAddress.trim()) {
        return send(res, 400, { error: 'A supported chain ID and exact contract address are required for an audit.' });
      }
      const response = await fetch('https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept-Encoding': 'identity', 'User-Agent': 'binance-web3/1.4 (Skill)', source: 'agent' },
        body: JSON.stringify({ binanceChainId: String(chainId), contractAddress: contractAddress.trim(), requestId: randomUUID() }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(`Token audit HTTP ${response.status}: ${result?.message || result?.code || 'request failed'}`);
      return send(res, 200, result);
    }
    if (req.method === 'GET' && (url.pathname === '/api/ticker' || url.pathname === '/api/depth')) {
      const symbol = String(url.searchParams.get('symbol') || '').toUpperCase();
      if (!symbols.has(symbol)) return send(res, 400, { error: `Unsupported symbol: ${symbol}` });
      const path = url.pathname === '/api/ticker'
        ? `/api/v3/ticker/24hr?symbol=${encodeURIComponent(symbol)}`
        : `/api/v3/depth?symbol=${encodeURIComponent(symbol)}&limit=10`;
      return send(res, 200, await binancePublic(path));
    }
    return send(res, 404, { error: 'Not found' });
  } catch (error) {
    console.error(error);
    return send(res, error.exitCode === 3 ? 503 : 502, { error: error.message, body: error.body });
  }
}).listen(port, '127.0.0.1', () => {
  console.log(`TradeTutor dashboard: http://127.0.0.1:${port}`);
});
