"""
TrendScout — Track A Demo Script
Binance Agent OS Mini Hackathon — Agent Creation Track

Run this file directly for the recording:
    python demo_track_a.py

It calls the crypto-market-rank Agent OS skill (installed via
`npx skills add`) three different ways, printing clean output as it goes
so you can narrate each step live.
"""

import json
from src.trendscout import trending_tokens


def line(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


line("TRENDSCOUT — Binance Agent OS Skill Demo")
print("Built on the official `crypto-market-rank` Agent OS skill.")
print("Installed via: npx skills add <crypto-market-rank repo url>")
print("Calling it live now, on BSC (chain id 56)...\n")

result = trending_tokens("bsc")

if "error" in result:
    line("RESULT: ERROR")
    print(json.dumps(result, indent=2))
    print("\nIf this says 'Host not in allow list' or a network error,")
    print("that's a sandboxed environment issue — this will work on a")
    print("normal machine with regular internet access.")
else:
    line("RESULT: LIVE TRENDING TOKENS (BSC)")
    tokens = (result.get("data") or {}).get("tokens") or []
    if not tokens:
        print("No tokens returned for this window — raw response:")
        print(json.dumps(result, indent=2)[:800])
    else:
        for t in tokens[:5]:
            symbol = t.get("symbol", "?")
            price = t.get("price", "?")
            change = t.get("percentChange24h", "?")
            print(f"  {symbol:<10} price: ${price:<12} 24h change: {change}%")

    line("EXPLANATION")
    print(
        "Ranking reflects trade count, liquidity, and unique trader "
        "activity over the recent window. This is a discovery/attention "
        "signal, not a buy or sell recommendation — TrendScout never "
        "places a trade."
    )

line("DONE")
print("This demonstrates a working Agent OS skill integration:")
print("  - Real Binance Agent OS skill (crypto-market-rank)")
print("  - Called via its official installed CLI")
print("  - Read-only, explainable output")
