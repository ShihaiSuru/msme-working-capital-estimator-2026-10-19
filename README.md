# MSME Working Capital Estimator (2026-10-19)

AI-powered tool that helps Indian MSMEs estimate short-term working capital needs and detect cash-flow gaps using GST return summaries and UPI/bank transaction patterns.

## Problem
Indian MSMEs (especially micro and small manufacturers, traders, and service providers) face chronic cash-flow volatility. Delayed customer payments, GST compliance cycles, seasonal demand, and fragmented UPI/bank data make it hard to predict when a liquidity shortfall will hit. Traditional CA reports or bank statements arrive too late for proactive financing decisions.

## Solution
This starter tool:
- Ingests simplified GST (GSTR-1/3B style) and UPI inflow/outflow summaries.
- Calculates key metrics: average collection period, payment cycle, net cash position, and projected gap over the next 30–60 days.
- Flags high-risk periods and suggests practical next steps (invoice discounting, OD/CC limit review, vendor term negotiation).

It is intentionally lightweight and demo-ready so founders can extend it with real Account Aggregator / GSTN / UPI data feeds or agentic workflows.

## Usage
```bash
python working_capital_estimator.py
```

Edit the sample data dictionaries at the top of the script with your own (anonymized) monthly figures and re-run. The script prints a clear cash-flow gap report and simple recommendations.

## Features (Starter)
- Collection period & cash conversion cycle estimates
- 60-day liquidity gap projection
- Basic risk scoring based on concentration and delay patterns
- Actionable suggestions tailored to Indian MSME financing options

## Next Steps for Production
- Connect to Account Aggregator for live bank/UPI data
- Parse real GSTR JSON exports
- Add ML forecasting (seasonality + buyer behavior)
- Integrate with invoice discounting / NBFCs for one-click offers
- WhatsApp / dashboard alerts

Built as a profile project for founders focused on practical AI cash-flow systems for Indian MSMEs.
