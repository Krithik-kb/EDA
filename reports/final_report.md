# Exploratory Data Analysis (EDA) Report: Telecom Customer Churn

## Executive Summary

Customer retention is vital to the profitability and growth of telecom service providers. This report presents a comprehensive Exploratory Data Analysis (EDA) performed on a dataset of **1000 customers** (after data cleaning) with **10 baseline attributes**. 

The main goal of this analysis is to identify the core drivers of customer churn—where the customer terminates their subscription (represented by `Churn = 1`)—and to provide data-driven recommendations to mitigate customer loss.

### Baseline Metrics
* **Total Cleaned Customers:** 1000
* **Retained Customers:** 852 (85.2%)
* **Churned Customers:** 148 (14.8%)
* **Overall Customer Churn Rate:** **14.80%**
* **Average Customer Age:** 46.5 years
* **Average Customer Tenure:** 36.2 months
* **Average Monthly Charges:** $59.19

---

## Data Cleaning & Quality Control

To ensure analysis integrity and correct model inputs, several critical data cleaning steps were performed:

1. **Duplicate Records:** Removed **15 duplicate records** from the raw dataset, ensuring each customer represents a unique record.
2. **Missing Value Imputation:**
   - **Age:** 23 missing or outlier values were imputed using the median age of valid observations.
   - **Total Charges:** 30 missing values were imputed by calculating `MonthlyCharges * Tenure` for each record, preventing skewness in financials.
3. **Outlier and Anomaly Treatment:**
   - **Age:** Addressed negative and extremely high ages (e.g. -5, 105, 120) by replacing them with the median age.
   - **Monthly Charges:** Identified and corrected 2 clear typos where Monthly Charges were listed as $999.00 and $850.00 (while actual charges are under $110). These were corrected by calculating `TotalCharges / Tenure` for those specific records.

---

## Key Insights

The analysis revealed distinct differences between customers who churn and those who remain with the service.

### 1. The Impact of Tenure (Correlation: -0.376)
Tenure is the strongest negative correlation factor with Churn. 
* **Retained Customers** have an average tenure of **39.4 months**.
* **Churned Customers** have an average tenure of **18.1 months** (less than half!).
* **Conclusion:** The risk of customer churn is extremely high in the first 1.5 to 2 years of the customer lifecycle. Once a customer passes the 3-year mark, retention stabilizes.

### 2. Contract Type Influences Customer Behavior
The structure of the customer contract is one of the most visible indicators of churn risk:
* **Month-to-month contracts** have a high churn rate of **24.70%** (accounting for most of the churned customers).
* **One-year contracts** show a churn rate of **8.26%**.
* **Two-year contracts** exhibit an exceptionally low churn rate of **1.92%**.
* **Conclusion:** Long-term contract commitments are highly effective in securing customer loyalty, whereas month-to-month contracts represent an immediate churn risk.

### 3. Support Calls as an Early Warning Indicator (Correlation: +0.179)
Customer support interactions directly signal service or billing friction:
* **Retained Customers** average **1.45 support calls**.
* **Churned Customers** average **2.07 support calls**.
* **Churn Escalation:** Churn rates increase significantly with support call counts:
  - 0 call(s): **8.57% Churn Rate** (210 customers)
  - 1 call(s): **10.21% Churn Rate** (333 customers)
  - 2 call(s): **18.15% Churn Rate** (259 customers)
  - 3 call(s): **22.06% Churn Rate** (136 customers)
  - 4 call(s): **22.22% Churn Rate** (36 customers)
  - 5 call(s): **47.62% Churn Rate** (21 customers)
  - 6 call(s): **25.00% Churn Rate** (4 customers)
  - 7 call(s): **0.00% Churn Rate** (1 customers)
* **Conclusion:** A customer who calls support 2 or more times is transitioning into a high-churn risk category and needs proactive attention.

### 4. Monthly Charges and Customer Sensitivities (Correlation: +0.115)
Financial load plays a role in retention decisions:
* **Retained Customers** pay an average monthly charge of **$58.00**.
* **Churned Customers** pay an average monthly charge of **$66.05**.
* **Conclusion:** Customers with higher-tier billing structures churn at a higher frequency. They are likely more sensitive to price hikes or perceive a lower return on investment.

### 5. Demographics and Payment Methods
* **Gender:** Churn is balanced between Male and Female customers, indicating gender is not a predictive factor.
* **Payment Method:** Bank Transfer users have the lowest churn rate, followed by Credit Card and PayPal. PayPal users are slightly more volatile, likely due to the ease of canceling automatic pre-authorizations compared to bank lines.

---

## Data-Driven Recommendations

Based on the findings above, we recommend implementing the following strategic business initiatives:

### 1. Run a Month-to-Month Contract Conversion Campaign
* **Action:** Target month-to-month contract holders with discounts or value-add features in exchange for signing a 1-year or 2-year agreement.
* **Reasoning:** Shifting a customer from month-to-month to a 1-year contract reduces churn probability by **66.6%**. Shifting them to a 2-year contract reduces it by **92.2%**.

### 2. Establish a "Proactive Customer Success" Flag
* **Action:** Implement an automated alert in the CRM system when a customer reaches **2 support calls** within a rolling 60-day window.
* **Execution:** Have a customer success representative reach out directly to resolve the technical or billing issues, offering a loyalty discount if necessary, before they call a third or fourth time.
* **Reasoning:** Churn rates double when support call counts move from 1 call (~10%) to 2 calls (~18%), and continue climbing. Catching friction early prevents churn.

### 3. Target "High Charge, Low Tenure" Customer Cohorts
* **Action:** Identify new customers (tenure < 18 months) who are on high monthly charge tiers (>$70/month) and offer them loyalty packages or review their usage to ensure they are getting full utility from their plan.
* **Reasoning:** This cohort represents the highest risk of churn, as they are paying high fees but have not yet developed long-term customer habituation.
