import subprocess
from pathlib import Path

def trending_tokens(chain_id='56'):
    """
    Fetch trending tokens using the crypto-market-rank skill.
    chain_id: '56' for BSC, 'CT_501' for Solana, '8453' for Base, '1' for Ethereum.
    """
    # The formatter imports COMMANDS/call directly and performs one uncached request.
    chain_map = {
        'bsc': '56',
        'eth': '1',
        'ethereum': '1',
        'sol': 'CT_501',
        'solana': 'CT_501',
        'base': '8453'
    }
    
    # Use the mapped ID if it exists, otherwise use the passed ID
    actual_chain_id = chain_map.get(str(chain_id).lower(), str(chain_id))
    
    cmd = ["node", str(Path(__file__).parents[1] / "fetch_trending.mjs"), actual_chain_id]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return result.stdout

if __name__ == "__main__":
    print(trending_tokens('56'), end='')
