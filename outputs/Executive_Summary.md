# Customer Engagement & Product Utilization Analytics

## Executive summary

The supplied `European_Bank.csv` contains 10,000 customer records from 2025 and 14 fields. It has no missing values and no duplicated customer IDs. The observed exit rate is **20.37%**. The portfolio is nearly evenly split between active members (51.51%) and inactive members (48.49%).

Engagement and product count are strongly associated with observed churn in this snapshot. Inactive customers have a **26.85%** exit rate, compared with **14.27%** for active members, a 12.58 percentage-point difference. Customers holding two products have a 7.58% exit rate, compared with 27.71% for one-product customers. The small three- and four-product groups have much higher observed exit rates (82.71% and 100%, respectively), so “more products always means lower churn” is not supported by this data. Those groups contain only 266 and 60 customers, and merit investigation before designing bundles.

Using the dataset's 75th-percentile balance (€127,644.24) and salary (€149,388.25) as value cutoffs, **2,154 inactive customers** meet at least one cutoff. Their observed exit rate is 29.06%. This is a useful outreach prioritization segment, not a prediction that these individuals will churn.

## Findings from the complete dataset

| Measure | Result |
| --- | ---: |
| Customers | 10,000 |
| Historical exited | 2,037 (20.37%) |
| Active members | 5,151 (51.51%) |
| Inactive members | 4,849 (48.49%) |
| Average products per customer | 1.53 |
| Inactive and high-value by balance or salary | 2,154 |
| Mean balance, retained | €72,745.30 |
| Mean balance, exited | €91,108.54 |

| Products held | Customers | Observed exit rate |
| ---: | ---: | ---: |
| 1 | 5,084 | 27.71% |
| 2 | 4,590 | 7.58% |
| 3 | 266 | 82.71% |
| 4 | 60 | 100.00% |

By geography, observed exit rates are 16.15% in France (5,014 customers), 32.44% in Germany (2,509), and 16.67% in Spain (2,477). Geographic differences may guide follow-up analysis, but this comparison is unadjusted for other customer characteristics.

## Recommended actions

1. Start with a service-oriented contact for inactive, high-value customers; check for unmet needs or friction before offering additional products.
2. Investigate the three- and four-product exit pattern and validate the product mapping or customer circumstances before using product count as a retention lever.
3. Consider relevant bundles for one-product customers, then test them against a control group and track retention over a defined period.
4. Build follow-up analysis that includes engagement recency, transactions, product types, tenure, and service interactions. Evaluate outcomes by geography and customer segment.

## Method and limitations

The Streamlit dashboard recomputes metrics as users filter engagement, product count, minimum balance, or minimum salary. The relationship-strength heuristic scores active status as 60 points and product breadth as up to 40 points (1 product = 0 breadth points, 4 or more = 40), with tiers of Fragile (0–39), Developing (40–69), and Strong (70–100). High-value disengaged means inactive and at or above either selected balance or salary threshold; defaults use the full dataset's 75th percentiles.

`Exited` is a historical outcome. Associations are descriptive, not causal or predictive. The active-member field is a single binary snapshot and does not reveal recency or frequency. No missing values were present in the supplied file; app handling is documented in the dashboard and README.
