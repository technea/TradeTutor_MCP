import subprocess
import json
import os

def trending_tokens(chain_id='56'):
    """
    Fetch trending tokens using the crypto-market-rank skill.
    chain_id: '56' for BSC, 'CT_501' for Solana, '8453' for Base, '1' for Ethereum.
    """
    # Define the path to the cli.mjs script installed via npx skills
    skill_path = os.path.join(".agents", "skills", "crypto-market-rank", "scripts", "cli.mjs")
    
    # Map common names to numeric chain IDs
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
    
    # Construct the command
    args = json.dumps({
        "rankType": 10,  # 10 means Trending
        "chainId": actual_chain_id,
        "page": 1,
        "size": 20
    })
    
    cmd = ["node", skill_path, "token-rank", args]
    
    try:
        # Run the command and capture output (utf-8 encoding to avoid Windows cp1252 issues)
        result = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        # The CLI outputs JSON, parse it and return
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_output": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        print(f"Error running skill: {e.stderr}")
        return {"error": "Failed to fetch trending tokens", "details": e.stderr}
    except FileNotFoundError:
        return {"error": "Node.js is not installed or not in PATH."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(json.dumps(trending_tokens('56'), indent=2))
