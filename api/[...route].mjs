import { randomUUID } from 'node:crypto';

const rankSkill = await import('../.agents/skills/crypto-market-rank/scripts/cli.mjs');
const tokenInfoSkill = await import('../.agents/skills/query-token-info/scripts/cli.mjs');
const symbols = new Set(['BTCUSDT', 'ETHUSDT', 'BNBUSDT']);

async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  let text = '';
  for await (const chunk of req) text += chunk;
  return text ? JSON.parse(text) : {};
}

async function binancePublic(path) {
  let lastError;
  for (const host of ['data-api.binance.vision', 'api.binance.com', 'api1.binance.com', 'api2.binance.com', 'api3.binance.com']) {
    try {
      const response = await fetch(`https://${host}${path}`, { headers: { 'Cache-Control': 'no-cache' }, signal: AbortSignal.timeout(8000) });
      const data = await response.json();
      if (!response.ok) throw new Error(`Binance HTTP ${response.status}: ${data.msg || 'request failed'}`);
      return data;
    } catch (error) { lastError = error; }
  }
  throw new Error(`Binance public API unavailable after 5 attempts: ${lastError?.message || 'fetch failed'}`);
}

function send(res, status, body) {
  res.status(status).json(body);
}

export default async function handler(req, res) {
  const path = new URL(req.url, 'https://vercel.local').pathname;
  try {
    if (req.method === 'GET' && (path === '/api/ticker' || path === '/api/depth')) {
      const symbol = String(new URL(req.url, 'https://vercel.local').searchParams.get('symbol') || '').toUpperCase();
      if (!symbols.has(symbol)) return send(res, 400, { error: `Unsupported symbol: ${symbol}` });
      const endpoint = path === '/api/ticker' ? `/api/v3/ticker/24hr?symbol=${symbol}` : `/api/v3/depth?symbol=${symbol}&limit=10`;
      return send(res, 200, await binancePublic(endpoint));
    }
    if (req.method === 'POST' && path === '/api/rank') {
      return send(res, 200, await rankSkill.call(rankSkill.COMMANDS['token-rank'](await readJson(req))));
    }
    if (req.method === 'POST' && path === '/api/token-search') {
      const { keyword, chainIds = '56' } = await readJson(req);
      const supportedChains = new Set(['56', '8453', '1', 'CT_501']);
      if (typeof keyword !== 'string' || !keyword.trim() || keyword.length > 80) return send(res, 400, { error: 'A token keyword of 1-80 characters is required.' });
      if (!supportedChains.has(String(chainIds))) return send(res, 400, { error: 'Unsupported chain. Use BNB Chain (56), Base (8453), Ethereum (1), or Solana (CT_501).' });
      return send(res, 200, await tokenInfoSkill.call(tokenInfoSkill.COMMANDS.search({ keyword: keyword.trim(), chainIds: String(chainIds) })));
    }
    if (req.method === 'POST' && path === '/api/token-audit') {
      const { chainId = '56', contractAddress } = await readJson(req);
      if (!['56', '1', '8453', 'CT_501'].includes(String(chainId)) || typeof contractAddress !== 'string' || !contractAddress.trim()) return send(res, 400, { error: 'A supported chain ID and exact contract address are required for an audit.' });
      const response = await fetch('https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit', { method: 'POST', headers: { 'Content-Type': 'application/json', 'User-Agent': 'binance-web3/1.4 (Skill)', source: 'agent' }, body: JSON.stringify({ binanceChainId: String(chainId), contractAddress: contractAddress.trim(), requestId: randomUUID() }) });
      const result = await response.json();
      if (!response.ok) throw new Error(`Token audit HTTP ${response.status}: ${result?.message || result?.code || 'request failed'}`);
      return send(res, 200, result);
    }
    return send(res, 404, { error: 'Not found' });
  } catch (error) {
    console.error(error);
    return send(res, 502, { error: error.message });
  }
}
