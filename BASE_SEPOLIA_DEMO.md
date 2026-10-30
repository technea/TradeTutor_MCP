# Base Sepolia USDC demo

A standalone browser prototype is available at `/base-sepolia-demo.html` after this branch is deployed.

## What it does

- Connects to an injected EVM wallet only after a user click.
- Switches/adds Base Sepolia (chain ID 84532).
- Reads the connected account's USDC balance using `eth_call`.
- Uses Circle's published Base Sepolia USDC contract: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`.
- Builds an ERC-20 transfer proposal and applies local checks: valid recipient, non-zero recipient, no self-transfer, amount greater than zero, maximum 1 USDC, and sufficient balance.
- Requires a second, separate user click to call `eth_sendTransaction`; the wallet displays the final transaction confirmation.
- Rechecks chain, account, proposal age (2-minute expiry), and balance immediately before asking the wallet to submit.

## Safety boundaries

- Testnet only. The page hardcodes chain ID 84532 and the Base Sepolia USDC contract. It does not support Base mainnet.
- No private keys, seed phrases, or secrets are requested, read, or stored.
- No transaction is sent during connect, balance read, or proposal preparation.
- The demo's policy checks are client-side guardrails, not a security audit, smart-contract enforcement, recipient reputation service, or guarantee of safety.
- The user must approve the transaction in their wallet. A returned transaction hash means the wallet submitted it; it does not mean the transaction has been mined or succeeded.
- The existing production dashboard is not modified by this standalone page. Deploy the branch and open `/base-sepolia-demo.html` to test it.

## Manual test checklist

1. Open the page in a browser with MetaMask or another EIP-1193 wallet.
2. Connect a wallet and switch to Base Sepolia.
3. Confirm USDC balance appears (zero is a valid result).
4. Try malformed address, zero address, own address, zero amount, over-1-USDC amount, and amount above balance; each must be blocked.
5. Prepare a valid transfer and confirm the proposal shows the recipient, amount, chain, and token contract.
6. Change account or network after preparing; send must be disabled and proposal invalidated.
7. Prepare again, press the final confirmation button, inspect the wallet's transaction details, and reject once to confirm no transaction is submitted.
8. If test USDC is available, repeat and verify the hash on Base Sepolia explorer.

## Official token reference

Circle's USDC contract registry: https://developers.circle.com/stablecoins/usdc-contract-addresses
