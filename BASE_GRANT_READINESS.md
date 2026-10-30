# TradeTutor — Base Grant Readiness

## Product direction

**TradeTutor is an explainable AI trading research and risk-protection assistant.** It helps users research market conditions, inspect token risk, plan position sizing, and keep a human approval boundary around financial actions.

The Base-focused product direction is to make TradeTutor useful for people discovering and evaluating Base assets, then extend it into a user-authorized onchain agent workflow.

## Current verified foundation

- Existing public app: https://tradetutor-two.vercel.app/
- Source repository: https://github.com/technea/TradeTutor_MCP
- Existing Binance-powered market dashboard and token research.
- Portfolio Guardian checks configured trade-risk, daily-loss, open-position, and kill-switch limits in the Python workflow.
- Token audit routing already recognizes Base chain ID 8453.
- This feature branch adds chain-aware token search for Base (8453), BNB Chain (56), Ethereum (1), and Solana (CT_501), plus API validation of supported chain IDs.

## Not yet implemented — do not claim as completed

- Base wallet connection or smart-wallet deployment.
- USDC transfers or swaps on Base.
- Onchain execution controlled by Portfolio Guardian.
- Builder Codes integration or attributable Base activity.
- Production-grade transaction simulation, signing, or monitoring.

These must be implemented and tested before being described as live capabilities in a grant nomination or public demo.

## Proposed Base roadmap

### Milestone 1 — Base asset research
- Make Base an explicit first-class network in the dashboard.
- Verify token search and contract audit responses for Base contracts.
- Display chain, contract address, source, fetch time, and audit limitations.
- Add tests for chain selection and unsupported-chain rejection.

### Milestone 2 — User-authorized Base wallet
- Add Base wallet connection using supported Base wallet tooling.
- Read wallet address and Base network state.
- Keep private keys and signing outside TradeTutor's backend.
- Require clear user confirmation for every onchain action.

### Milestone 3 — Policy-gated USDC demo
- Build a testnet-first USDC transfer or other narrow, transparent transaction flow.
- Add policy checks for allowed contract, maximum amount, daily cap, and user authorization.
- Simulate before signing; reject failed or stale policy checks.
- Record transaction hash and policy decision.

### Milestone 4 — Attribution, testing, and launch
- Integrate Base Builder Codes if required by the applicable program.
- Deploy the public Base experience.
- Publish reproducible tests, a short demo, and onchain proof.
- Measure unique users, successful transactions, rejected unsafe requests, and repeat usage.

## Draft grant / nomination narrative

TradeTutor is building an explainable AI trading and risk-protection assistant for onchain users. Most trading agents optimize for execution; TradeTutor focuses on helping users understand what an agent proposes, what could go wrong, and whether the action fits their own risk limits.

The existing product combines market research, token-risk inspection, position sizing, portfolio protection, paper trading, and a human-confirmation boundary. The Base roadmap brings this workflow closer to Base users: first through Base-native asset discovery and contract research, then through a user-authorized wallet flow where policy checks run before a transaction can be signed.

We want to make onchain trading tools safer and easier to understand, especially for users who are new to DeFi. Our near-term goal is a public Base experience with verifiable usage, transparent security decisions, and a narrow USDC transaction demo that never takes custody of user funds.

## Proposed 4-week milestones

1. **Week 1:** Complete Base asset discovery and contract-audit UX; verify live Base responses and add automated tests.
2. **Week 2:** Add Base wallet connection and network checks; no backend custody or private-key storage.
3. **Week 3:** Implement a testnet USDC transaction demo with policy simulation, user confirmation, and audit logging.
4. **Week 4:** Integrate Builder Codes where applicable, deploy, publish a walkthrough, and report real usage metrics.

## Proposed use of a $5,000 development budget

This is a planning estimate, not a statement that the Base Builder Grants program guarantees a $5,000 award.

| Workstream | Estimate |
|---|---:|
| Base wallet and network integration | $1,000 |
| Policy-gated transaction flow | $1,200 |
| Security tests and transaction monitoring | $1,000 |
| Product UX and onboarding | $600 |
| Infrastructure and deployment | $500 |
| Documentation, demo, and launch | $700 |
| **Total** | **$5,000** |

## Success metrics

- Base wallet connections by real, unique users.
- Successful Base testnet and, after review, mainnet transactions.
- Number of unsafe or over-limit actions correctly rejected.
- Percentage of transactions with a recorded policy decision.
- Repeat users and completed research-to-action workflows.

Do not fabricate these metrics. Publish only measured results.

## Funding route notes

Base's published Builder Grants information describes a discovery- and nomination-led program. It says Base evaluates whether a project is unique, brings users onchain, and is live and making an impact; it also states grants currently range from 1–5 ETH. This is not the same as a guaranteed $5,000 application award.

Official program information: https://paragraph.com/@grants.base.eth/calling-based-builders

Base's separate Ecosystem Fund is an investment program for pre-seed and seed teams building onchain businesses: https://docs.base.org/get-started/base-ecosystem-fund

Before submitting, re-check current program terms and use only official Base channels.
