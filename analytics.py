"""
Coffee Shop Customer Analytics Engine
=====================================
Full business intelligence pipeline:
  1. RFM Analysis & Customer Segmentation (K-Means)
  2. Product performance & basket analysis
  3. Time-based patterns (peak hours, days)
  4. Channel & branch performance
  5. Loyalty program impact
  6. Actionable business recommendations

Author: Amina — Business Analytics Portfolio
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
import os

pd.set_option("display.float_format", lambda x: f"{x:.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD & PREPARE
# ═══════════════════════════════════════════════════════════════════════════
df = pd.read_csv("data/transactions.csv", parse_dates=["date"])
SNAPSHOT = df["date"].max() + pd.Timedelta(days=1)
print(f"📊 Loaded {len(df):,} transactions | {df['customer_id'].nunique()} customers\n")

results = {}

# ═══════════════════════════════════════════════════════════════════════════
# 2. RFM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
rfm = df.groupby("customer_id").agg(
    recency=("date", lambda x: (SNAPSHOT - x.max()).days),
    frequency=("transaction_id", "count"),
    monetary=("amount_bhd", "sum"),
).reset_index()

# Score 1-5 using quantiles
rfm["R"] = pd.qcut(rfm["recency"], 5, labels=[5,4,3,2,1]).astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M"] = pd.qcut(rfm["monetary"], 5, labels=[1,2,3,4,5]).astype(int)
rfm["RFM_score"] = rfm["R"] + rfm["F"] + rfm["M"]

# ═══════════════════════════════════════════════════════════════════════════
# 3. K-MEANS SEGMENTATION
# ═══════════════════════════════════════════════════════════════════════════
X = rfm[["recency", "frequency", "monetary"]].copy()
X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
rfm["cluster"] = kmeans.fit_predict(X_scaled)

# Label clusters by avg RFM score
cluster_rank = rfm.groupby("cluster")["RFM_score"].mean().sort_values(ascending=False)
labels = ["Champions", "Loyal", "Potential", "At Risk", "Lost"]
label_map = {cl: labels[i] for i, cl in enumerate(cluster_rank.index)}
rfm["segment"] = rfm["cluster"].map(label_map)

seg_colors = {
    "Champions": "#16a34a", "Loyal": "#0891b2", "Potential": "#ca8a04",
    "At Risk": "#ea580c", "Lost": "#dc2626"
}
seg_actions = {
    "Champions": "Reward with VIP perks, free birthday drink, early access to new menu",
    "Loyal": "Upsell food items, introduce subscription plan, referral bonus",
    "Potential": "Loyalty card push, 2nd-visit discount, personalized offers",
    "At Risk": "Win-back SMS, 'we miss you' 25% off, ask for feedback",
    "Lost": "Final reactivation offer, then move to low-cost email only",
}

print("🎯 CUSTOMER SEGMENTS")
print("─" * 70)
seg_summary = []
for seg in labels:
    s = rfm[rfm["segment"] == seg]
    if len(s) == 0:
        continue
    row = {
        "segment": seg,
        "customers": int(len(s)),
        "pct": round(len(s)/len(rfm)*100, 1),
        "avg_recency": round(s["recency"].mean(), 0),
        "avg_frequency": round(s["frequency"].mean(), 1),
        "avg_monetary": round(s["monetary"].mean(), 2),
        "total_revenue": round(s["monetary"].sum(), 2),
        "revenue_pct": round(s["monetary"].sum()/rfm["monetary"].sum()*100, 1),
        "color": seg_colors[seg],
        "action": seg_actions[seg],
    }
    seg_summary.append(row)
    print(f"{seg:12s} | {row['customers']:3d} cust ({row['pct']:4.1f}%) | "
          f"{row['revenue_pct']:4.1f}% of revenue | BD {row['avg_monetary']:.0f} avg")

results["segments"] = seg_summary

# ═══════════════════════════════════════════════════════════════════════════
# 4. PRODUCT PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
all_items = df["items"].str.split(r" \+ ").explode().str.strip()
item_counts = all_items.value_counts()
top_products = [{"name": k, "count": int(v), "pct": round(v/len(all_items)*100, 1)}
                for k, v in item_counts.head(8).items()]
results["top_products"] = top_products

print("\n☕ TOP PRODUCTS")
print("─" * 70)
for p in top_products[:5]:
    print(f"{p['name']:20s} | {p['count']:,} sold ({p['pct']}%)")

# ═══════════════════════════════════════════════════════════════════════════
# 5. TIME PATTERNS
# ═══════════════════════════════════════════════════════════════════════════
df["weekday"] = df["date"].dt.day_name()
hourly = df.groupby("hour")["amount_bhd"].agg(["count", "sum"]).reset_index()
results["hourly"] = [{"hour": int(r["hour"]), "transactions": int(r["count"]),
                      "revenue": round(r["sum"], 2)} for _, r in hourly.iterrows()]

weekday_order = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
daily = df.groupby("weekday")["amount_bhd"].agg(["count","sum"]).reindex(weekday_order).reset_index()
results["weekday"] = [{"day": r["weekday"][:3], "transactions": int(r["count"]),
                       "revenue": round(r["sum"], 2)} for _, r in daily.iterrows()]

peak_hour = int(hourly.loc[hourly["count"].idxmax(), "hour"])
peak_day = daily.loc[daily["count"].idxmax(), "weekday"]
print(f"\n⏰ Peak hour: {peak_hour}:00 | Peak day: {peak_day}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. CHANNEL & BRANCH
# ═══════════════════════════════════════════════════════════════════════════
channel = df.groupby("channel")["amount_bhd"].agg(["count","sum"]).reset_index()
results["channels"] = [{"name": r["channel"], "transactions": int(r["count"]),
                        "revenue": round(r["sum"], 2)} for _, r in channel.iterrows()]

branch = df.groupby("branch")["amount_bhd"].agg(["count","sum"]).reset_index()
results["branches"] = [{"name": r["branch"], "transactions": int(r["count"]),
                        "revenue": round(r["sum"], 2)} for _, r in branch.iterrows()]

# ═══════════════════════════════════════════════════════════════════════════
# 7. LOYALTY IMPACT
# ═══════════════════════════════════════════════════════════════════════════
loyalty = df.groupby("loyalty_member").agg(
    customers=("customer_id", "nunique"),
    avg_spend=("amount_bhd", "mean"),
    total=("amount_bhd", "sum"),
).reset_index()
loy_member = loyalty[loyalty["loyalty_member"]==True].iloc[0]
loy_non = loyalty[loyalty["loyalty_member"]==False].iloc[0]
results["loyalty"] = {
    "member_avg": round(loy_member["avg_spend"], 3),
    "nonmember_avg": round(loy_non["avg_spend"], 3),
    "uplift_pct": round((loy_member["avg_spend"]/loy_non["avg_spend"]-1)*100, 1),
}

# ═══════════════════════════════════════════════════════════════════════════
# 8. KPI SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
results["kpis"] = {
    "total_revenue": round(df["amount_bhd"].sum(), 2),
    "total_transactions": int(len(df)),
    "unique_customers": int(df["customer_id"].nunique()),
    "avg_transaction": round(df["amount_bhd"].mean(), 3),
    "avg_basket_size": round(df["num_items"].mean(), 2),
    "peak_hour": peak_hour,
    "peak_day": peak_day[:3],
    "date_range": f"{df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}",
}

# ═══════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════
os.makedirs("results", exist_ok=True)
rfm_out = rfm.merge(df.groupby("customer_id")["persona"].first(), on="customer_id")
rfm_out.to_csv("results/customer_segments.csv", index=False)

with open("results/analytics.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n" + "═" * 70)
print("✅ Analysis complete!")
print(f"   Total revenue analyzed: BD {results['kpis']['total_revenue']:,.2f}")
print(f"   Champions are {seg_summary[0]['pct']}% of customers "
      f"but {seg_summary[0]['revenue_pct']}% of revenue")
print("📁 Exports: results/customer_segments.csv, results/analytics.json")
