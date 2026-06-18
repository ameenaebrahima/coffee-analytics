# ☕ Coffee Shop Customer Analytics

> **A complete business intelligence engine** that turns raw POS transactions into customer segments, revenue insights, and actionable marketing decisions.

**Live demo →** `https://YOUR_USERNAME.github.io/coffee-analytics`

---

## 📌 The Problem

A coffee shop owner has thousands of transactions but no idea **who their best customers are**, **when they're busiest**, or **which customers are about to leave**. This project answers all three — using only data they already have in their POS system.

## 💡 The Headline Insight

> **13% of customers (the "Champions") generate 45% of all revenue.**
> Losing one Champion = losing 39 occasional visitors.

This single finding tells the owner exactly where to focus retention budget.

---

## 📊 What It Does

| Analysis | Output |
|----------|--------|
| **RFM Scoring** | Every customer scored 1–5 on Recency, Frequency, Monetary |
| **K-Means Segmentation** | 5 behavioral segments: Champions, Loyal, Potential, At Risk, Lost |
| **Product Analysis** | Best-selling items, basket patterns |
| **Time Patterns** | Peak hours (8AM rush) and busiest days |
| **Channel & Branch** | Revenue split across Dine-in, Takeaway, Talabat, Jahez |
| **Marketing Playbook** | Concrete action for each segment |

---

## 🎯 Customer Segments Found

| Segment | Customers | % of Revenue | Recommended Action |
|---------|-----------|--------------|--------------------|
| 🟢 Champions | 103 (13%) | **44.6%** | VIP perks, birthday rewards |
| 🔵 Loyal | 149 (19%) | 28.3% | Upsell food, subscription plan |
| 🟡 Potential | 363 (45%) | 25.4% | Loyalty card, 2nd-visit discount |
| 🟠 At Risk | 129 (16%) | 1.5% | Win-back SMS, "we miss you" offer |
| 🔴 Lost | 56 (7%) | 0.2% | Final reactivation, then archive |

---

## 📁 Project Structure

```
coffee-analytics/
├── data/
│   ├── generate_data.py     # Synthetic POS data generator (Bahrain market)
│   └── transactions.csv     # 57,763 transactions, 800 customers
├── src/
│   └── analytics.py         # Full BI pipeline: RFM + K-Means + insights
├── results/
│   ├── customer_segments.csv
│   └── analytics.json
├── website/
│   └── index.html           # Interactive dashboard
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/coffee-analytics.git
cd coffee-analytics
pip install -r requirements.txt

python data/generate_data.py   # Generate the dataset
python src/analytics.py        # Run the analysis
open website/index.html        # View the dashboard
```

---

## 🔬 Methodology

1. **Aggregate** — roll 57K transactions up to per-customer R/F/M metrics
2. **Score** — `pd.qcut` quintiles give each customer a 1–5 score per dimension
3. **Cluster** — `StandardScaler` + `KMeans(k=5)` group by behavioral similarity
4. **Label & act** — rank clusters by RFM, map to named segments, attach actions

This pipeline is **reproducible on any real POS export** — just swap the CSV.

---

## 🛠️ Tech Stack

`Python 3.11` · `pandas` · `NumPy` · `scikit-learn` · `Chart.js` · `HTML/CSS`

---

## 🎓 About

**Project 1 of 5** in my Business Analytics portfolio. Demonstrates:
- Real-world data analysis (Python, pandas)
- Unsupervised ML (clustering + evaluation)
- Business intelligence thinking (RFM, actionable insights)
- Data storytelling (interactive dashboard)

Built by **Amina** — Business Analytics, University of Bahrain · 2025
