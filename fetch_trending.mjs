#!/usr/bin/env node
// Fetch the live Binance Trending board. This intentionally has no cache.
import { randomUUID } from 'node:crypto';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const cliPath = resolve('.agents/skills/crypto-market-rank/scripts/cli.mjs');
const { COMMANDS, call } = await import(pathToFileURL(cliPath).href);

const fetchedAt = new Date().toISOString();
const requestMarker = `${Date.now()}-${randomUUID().slice(0, 8)}`;
const params = {
  rankType: 10,
  chainId: process.argv[2] ?? '56',
  page: 1,
  size: 5,
};

function value(token, ...keys) {
  for (const key of keys) {
    if (token?.[key] !== undefined && token[key] !== null) return token[key];
  }
  return '—';
}

function formatTable(tokens) {
  const rows = tokens.slice(0, 5).map((token, index) => [
    String(index + 1),
    String(value(token, 'symbol', 'tokenSymbol')),
    String(value(token, 'name', 'tokenName', 'fullName', 'metaInfo') === '—'
      ? '—'
      : (value(token, 'name', 'tokenName', 'fullName') !== '—'
        ? value(token, 'name', 'tokenName', 'fullName')
        : value(token.metaInfo, 'name', 'tokenName'))),
    String(value(token, 'price')),
    String(value(token, 'percentChange24h', 'percentChange')),
  ]);
  const headers = ['Rank', 'Symbol', 'Name', 'Price', '24h %'];
  const widths = headers.map((header, i) => Math.max(header.length, ...rows.map(row => row[i].length)));
  const line = row => row.map((cell, i) => cell.padEnd(widths[i])).join(' | ');
  return [line(headers), widths.map(width => '-'.repeat(width)).join('-+-'), ...rows.map(line)].join('\n');
}

try {
  // COMMANDS builds the request; call() performs a new network request here.
  const result = await call(COMMANDS['token-rank'](params));
  const tokens = result?.data?.tokens;
  if (!Array.isArray(tokens)) throw new Error('Unexpected API response: data.tokens is missing or not an array');
  console.log(`Fetched at: ${fetchedAt}`);
  console.log(`Request marker: ${requestMarker}`);
  console.log(formatTable(tokens));
} catch (error) {
  console.error(`Trending token fetch failed: ${error?.message ?? error}`);
  if (error?.body) console.error(JSON.stringify(error.body, null, 2));
  process.exit(error?.exitCode || 1);
}
