#!/usr/bin/env python3
"""
MSME Working Capital Estimator
Starter script — 2026-10-19

Demonstrates how GST + UPI pattern data can surface short-term cash-flow gaps
for Indian MSMEs. Replace the sample dictionaries with real (anonymized) data.
"""

from datetime import datetime, timedelta
from typing import Dict, List

# ---------------------------------------------------------------------------
# Sample data — replace with real GST / UPI summaries
# ---------------------------------------------------------------------------
# Monthly GST-style sales & purchase summaries (last 3 months)
gst_data: Dict[str, Dict[str, float]] = {
    "2026-07": {"taxable_sales": 1_850_000, "taxable_purchases": 1_120_000, "gst_paid": 145_000},
    "2026-08": {"taxable_sales": 2_100_000, "taxable_purchases": 1_280_000, "gst_paid": 165_000},
    "2026-09": {"taxable_sales": 1_950_000, "taxable_purchases": 1_150_000, "gst_paid": 155_000},
}

# UPI / bank inflow-outflow pattern (last 90 days summarized)
upi_pattern: Dict[str, float] = {
    "avg_daily_inflow": 62_000,          # customer collections
    "avg_daily_outflow": 48_000,         # vendors + opex
    "pending_receivables": 920_000,      # unpaid invoices
    "upcoming_payables_30d": 680_000,    # vendor bills due soon
    "current_bank_balance": 340_000,
}

# Buyer concentration (top customer % of sales)
buyer_concentration_pct: float = 42.0  # high concentration = higher risk

# ---------------------------------------------------------------------------
def estimate_collection_period(gst_data: Dict) -> float:
    """Rough days-sales-outstanding proxy from recent sales vs receivables."""
    recent_sales = sum(m["taxable_sales"] for m in list(gst_data.values())[-2:]) / 2
    if recent_sales == 0:
        return 45.0
    # Assume pending receivables represent ~1.5 months of sales for illustration
    return (upi_pattern["pending_receivables"] / recent_sales) * 30

def project_cash_gap(days: int = 60) -> Dict:
    """Simple linear projection of cash position."""
    net_daily = upi_pattern["avg_daily_inflow"] - upi_pattern["avg_daily_outflow"]
    projected_balance = upi_pattern["current_bank_balance"] + (net_daily * days)
    # Subtract known near-term payables
    projected_balance -= upi_pattern["upcoming_payables_30d"] * 0.6  # assume 60% still outstanding
    gap = max(0, -projected_balance)
    return {
        "projected_balance_60d": round(projected_balance),
        "estimated_gap": round(gap),
        "collection_period_days": round(estimate_collection_period(gst_data), 1),
    }

def generate_recommendations(gap_info: Dict) -> List[str]:
    """Practical MSME-oriented suggestions."""
    recs = []
    if gap_info["estimated_gap"] > 200_000:
        recs.append("• Consider invoice discounting / TReDS for the ₹{:,.0f} pending receivables.".format(upi_pattern["pending_receivables"]))
    if gap_info["collection_period_days"] > 45:
        recs.append("• Collection period is elevated ({:.0f} days). Review credit terms with top buyers.".format(gap_info["collection_period_days"]))
    if buyer_concentration_pct > 35:
        recs.append("• High buyer concentration ({:.0f}%). Diversify customer base or tighten terms with the largest account.".format(buyer_concentration_pct))
    if gap_info["estimated_gap"] > 0:
        recs.append("• Review OD/CC limit with your bank; a temporary top-up could cover the ₹{:,.0f} projected gap.".format(gap_info["estimated_gap"]))
        recs.append("• Negotiate 7–15 day extension with key vendors if relationship allows.")
    else:
        recs.append("• Liquidity looks stable for the next 60 days. Consider sweeping idle balances to a high-yield account.")
    return recs

def main():
    print("=" * 60)
    print("MSME Working Capital Estimator — 2026-10-19")
    print("=" * 60)
    gap = project_cash_gap()
    print(f"\nCurrent bank balance     : ₹{upi_pattern['current_bank_balance']:,.0f}")
    print(f"Pending receivables     : ₹{upi_pattern['pending_receivables']:,.0f}")
    print(f"Upcoming payables (30d) : ₹{upi_pattern['upcoming_payables_30d']:,.0f}")
    print(f"Est. collection period  : {gap['collection_period_days']} days")
    print(f"\n60-day projected balance : ₹{gap['projected_balance_60d']:,.0f}")
    print(f"Estimated cash gap      : ₹{gap['estimated_gap']:,.0f}")
    print("\nRecommendations:")
    for r in generate_recommendations(gap):
        print(r)
    print("\n" + "=" * 60)
    print("Replace sample data with your GST / UPI figures and re-run.")
    print("This is a starter demo — production systems should use live AA + GSTN feeds.")

if __name__ == "__main__":
    main()
