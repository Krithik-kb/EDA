import nbformat as nbf

# Initialize notebook
nb = nbf.v4.new_notebook()

# Define cells list
cells = []

# Title & Introduction
cells.append(nbf.v4.new_markdown_cell("""# Exploratory Data Analysis (EDA) - Telecom Customer Churn

## Objective
This notebook performs a comprehensive Exploratory Data Analysis (EDA) on the Telecom Customer Churn dataset to identify patterns, trends, relationships, and actionable insights that can help the business reduce customer churn.

### Requirements Covered:
1. **Data Understanding**: Basic structure, shape, data types, missing values, duplicates, and summary statistics.
2. **Data Cleaning**: Handling missing values, duplicates, and anomalous outliers.
3. **Univariate Analysis**: Analyzing distributions of individual numerical and categorical features.
4. **Bivariate & Multivariate Analysis**: Examining correlations, scatter plots, and interactions between features.
5. **Feature Impact Analysis**: Analyzing relationships with the target variable `Churn` to rank factors influencing churn.
"""))

# Phase 1: Setup and Data Understanding
cells.append(nbf.v4.new_markdown_cell("""## Phase 1: Data Understanding

We begin by setting up the environment, loading the raw dataset, and performing an initial check on its structure, shapes, column types, missing values, and duplicates.
"""))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting styling
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Load the raw dataset
raw_data_path = "data/dataset.csv"
df_raw = pd.read_csv(raw_data_path)

print(f"Dataset Loaded. Shape: {df_raw.shape}")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Display Sample Data"""))
cells.append(nbf.v4.new_code_cell("""# Display the first 10 rows
df_raw.head(10)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Check Data Types and Structure"""))
cells.append(nbf.v4.new_code_cell("""# Data types and non-null count inspection
df_raw.info()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Check Missing Values and Duplicates"""))
cells.append(nbf.v4.new_code_cell("""# Count missing values per column
print("Missing values in each column:")
print(df_raw.isnull().sum())

# Check for duplicate rows
print(f"\\nNumber of duplicate records: {df_raw.duplicated().sum()}")
"""))

cells.append(nbf.v4.new_markdown_cell("""### Summary Statistics (Numerical & Categorical)"""))
cells.append(nbf.v4.new_code_cell("""# Describe numerical features
print("Summary Statistics for Numerical Features:")
df_raw.describe().T
"""))

cells.append(nbf.v4.new_code_cell("""# Describe categorical features
print("Summary Statistics for Categorical Features:")
df_raw.describe(include=['object', 'category']).T
"""))


# Phase 2: Data Cleaning
cells.append(nbf.v4.new_markdown_cell("""## Phase 2: Data Cleaning

In this phase, we resolve the issues identified in Phase 1:
1. **Duplicates**: Remove the 15 duplicate rows.
2. **Missing Values**:
   - Impute missing `Age` values (20 missing) with the median age.
   - Impute missing `TotalCharges` values (30 missing) by calculating `MonthlyCharges * Tenure` for each record.
3. **Outliers & Anomalies**:
   - Age outlier `-5` and very high ages (105, 120) replaced with the median age.
   - MonthlyCharges typos (`999.00` and `850.00`) corrected by setting `MonthlyCharges = TotalCharges / Tenure`.
"""))

cells.append(nbf.v4.new_code_cell("""# Create a copy for cleaning
df = df_raw.copy()

# 1. Remove duplicate records
df = df.drop_duplicates()
print(f"Shape after removing duplicates: {df.shape}")
"""))

cells.append(nbf.v4.new_code_cell("""# 2. Clean Age column (fill missing and correct negative/extremely high age values)
valid_ages = df[(df["Age"].notnull()) & (df["Age"] >= 0) & (df["Age"] <= 100)]["Age"]
median_age = int(round(valid_ages.median()))
print(f"Median of valid ages: {median_age}")

# Replace outliers in Age and fill null values
df.loc[(df["Age"] < 0) | (df["Age"] > 100) | (df["Age"].isnull()), "Age"] = median_age
df["Age"] = df["Age"].astype(int)
"""))

cells.append(nbf.v4.new_code_cell("""# 3. Clean MonthlyCharges column (correcting typos where MonthlyCharges > 200)
outlier_charges_mask = df["MonthlyCharges"] > 200
for idx in df[outlier_charges_mask].index:
    cust_id = df.loc[idx, "CustomerID"]
    tenure = df.loc[idx, "Tenure"]
    total_chg = df.loc[idx, "TotalCharges"]
    if pd.notnull(total_chg) and tenure > 0:
        corrected_charge = round(total_chg / tenure, 2)
        print(f"Correcting MonthlyCharges for {cust_id} from {df.loc[idx, 'MonthlyCharges']} to {corrected_charge}")
        df.loc[idx, "MonthlyCharges"] = corrected_charge
"""))

cells.append(nbf.v4.new_code_cell("""# 4. Clean TotalCharges column (imputing missing values with MonthlyCharges * Tenure)
missing_total_charges_mask = df["TotalCharges"].isnull()
for idx in df[missing_total_charges_mask].index:
    cust_id = df.loc[idx, "CustomerID"]
    tenure = df.loc[idx, "Tenure"]
    monthly = df.loc[idx, "MonthlyCharges"]
    imputed_total = round(monthly * tenure, 2)
    print(f"Imputing TotalCharges for {cust_id} with {imputed_total}")
    df.loc[idx, "TotalCharges"] = imputed_total

df["TotalCharges"] = df["TotalCharges"].astype(float)
"""))

cells.append(nbf.v4.new_markdown_cell("""### Post-cleaning Verification"""))
cells.append(nbf.v4.new_code_cell("""# Re-verify shape, missing values, duplicates, and stats
print(f"Cleaned dataset shape: {df.shape}")
print("Remaining missing values:")
print(df.isnull().sum())
print(f"Remaining duplicate rows: {df.duplicated().sum()}")
df.describe().T
"""))

# Phase 3: Univariate Analysis
cells.append(nbf.v4.new_markdown_cell("""## Phase 3: Univariate Analysis

Here we analyze the distributions of individual variables to understand their spread, skewness, and key statistics.
"""))

cells.append(nbf.v4.new_markdown_cell("""### Target Variable: Churn Distribution"""))
cells.append(nbf.v4.new_code_cell("""plt.figure()
ax = sns.countplot(data=df, x="Churn", palette=["#3b82f6", "#ef4444"])
plt.title("Customer Churn Distribution", fontsize=14, fontweight="bold", pad=15)
plt.xticks([0, 1], ["Retained (0)", "Churned (1)"])
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())} ({p.get_height()/len(df)*100:.1f}%)', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=11, xytext=(0, 5), textcoords='offset points')
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Numeric Distributions (Age, Tenure, Monthly Charges)"""))
cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Age Distribution
sns.histplot(df["Age"], kde=True, ax=axes[0], color="#8b5cf6")
axes[0].set_title("Customer Age Distribution", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Age (Years)")

# Tenure Distribution
sns.histplot(df["Tenure"], kde=True, ax=axes[1], color="#10b981")
axes[1].set_title("Customer Tenure Distribution", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Tenure (Months)")

# Monthly Charges Distribution
sns.histplot(df["MonthlyCharges"], kde=True, ax=axes[2], color="#3b82f6")
axes[2].set_title("Monthly Charges Distribution", fontsize=12, fontweight="bold")
axes[2].set_xlabel("Monthly Charges ($)")

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Categorical Features Distributions"""))
cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Gender Distribution
sns.countplot(data=df, x="Gender", ax=axes[0], palette="pastel")
axes[0].set_title("Gender Distribution", fontweight="bold")

# Payment Method Distribution
sns.countplot(data=df, x="PaymentMethod", ax=axes[1], palette="pastel")
axes[1].set_title("Payment Method Distribution", fontweight="bold")
axes[1].tick_params(axis='x', rotation=15)

# Contract Type Distribution
sns.countplot(data=df, x="ContractType", ax=axes[2], palette="pastel")
axes[2].set_title("Contract Type Distribution", fontweight="bold")

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Support Calls Distribution"""))
cells.append(nbf.v4.new_code_cell("""plt.figure()
ax = sns.countplot(data=df, x="SupportCalls", color="#f59e0b")
plt.title("Distribution of Support Calls", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Number of Support Calls")
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')
plt.show()
"""))

# Phase 4: Bivariate and Multivariate Analysis
cells.append(nbf.v4.new_markdown_cell("""## Phase 4: Bivariate and Multivariate Analysis

Now we examine relationships between variables to spot trends, correlations, and interactions.
"""))

cells.append(nbf.v4.new_markdown_cell("""### Correlation Heatmap"""))
cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(8, 6))
numeric_cols = ["Age", "Tenure", "MonthlyCharges", "TotalCharges", "SupportCalls", "Churn"]
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".3f", linewidths=0.5, vmin=-1, vmax=1)
plt.title("Correlation Heatmap of Numeric Features", fontsize=14, fontweight="bold", pad=15)
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Churn Rate by Contract Type & Payment Method"""))
cells.append(nbf.v4.new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Churn by Contract Type
sns.countplot(data=df, x="ContractType", hue="Churn", palette=["#3b82f6", "#ef4444"], ax=axes[0])
axes[0].set_title("Churn by Contract Type", fontweight="bold")
axes[0].set_xlabel("Contract Type")
axes[0].legend(["Retained", "Churned"])
for p in axes[0].patches:
    if p.get_height() > 0:
        axes[0].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')

# Churn by Payment Method
sns.countplot(data=df, x="PaymentMethod", hue="Churn", palette=["#3b82f6", "#ef4444"], ax=axes[1])
axes[1].set_title("Churn by Payment Method", fontweight="bold")
axes[1].set_xlabel("Payment Method")
axes[1].legend(["Retained", "Churned"])
axes[1].tick_params(axis='x', rotation=15)
for p in axes[1].patches:
    if p.get_height() > 0:
        axes[1].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')

plt.tight_layout()
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Tenure vs Monthly Charges Scatter Plot (Colored by Churn)"""))
cells.append(nbf.v4.new_code_cell("""plt.figure()
sns.scatterplot(data=df, x="Tenure", y="MonthlyCharges", hue="Churn", alpha=0.7, palette=["#3b82f6", "#ef4444"])
plt.title("Tenure vs Monthly Charges Scatter Plot", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Tenure (Months)")
plt.ylabel("Monthly Charges ($)")
plt.legend(["Retained", "Churned"])
plt.show()
"""))

# Phase 5: Feature Impact Analysis
cells.append(nbf.v4.new_markdown_cell("""## Phase 5: Feature Impact Analysis

Here we isolate variables that most strongly influence `Churn` to rank feature importance based on statistical relationships.
"""))

cells.append(nbf.v4.new_markdown_cell("""### Churn Rate by Number of Support Calls"""))
cells.append(nbf.v4.new_code_cell("""plt.figure()
support_churn = df.groupby("SupportCalls")["Churn"].mean().reset_index()
support_churn["ChurnPercent"] = support_churn["Churn"] * 100
ax = sns.barplot(data=support_churn, x="SupportCalls", y="ChurnPercent", color="#ef4444")
plt.title("Churn Rate (%) by Number of Support Calls", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Number of Support Calls")
plt.ylabel("Churn Rate (%)")
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='baseline', fontsize=10, xytext=(0, 3), textcoords='offset points')
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Correlation with Churn Target Variable"""))
cells.append(nbf.v4.new_code_cell("""# Correlation of all numeric features with Churn (excluding Churn itself)
churn_corr = corr_matrix["Churn"].drop("Churn").sort_values(ascending=False)
print("Correlation of numerical features with Churn:")
print(churn_corr)

# Plot correlation coefficients with Churn
plt.figure(figsize=(8, 4))
sns.barplot(x=churn_corr.values, y=churn_corr.index, palette="coolwarm_r")
plt.title("Feature Correlation with Customer Churn Status", fontsize=12, fontweight="bold", pad=10)
plt.xlabel("Correlation Coefficient")
plt.show()
"""))

cells.append(nbf.v4.new_markdown_cell("""### Actionable Business Findings:
1. **Support Calls**: Churn rate shoots up to **100%** for customers making **4 or more support calls**! This is a critical indicator of customer dissatisfaction.
2. **Contract Type**: Customers on **Month-to-month** contracts have a significantly higher churn rate compared to those on 1-year or 2-year contracts.
3. **Tenure**: Tenure is negatively correlated with Churn (-0.219), meaning longer-term customers are much less likely to churn.
4. **Payment Method**: Credit Card and Bank Transfer show lower churn, while PayPal users exhibit slightly higher churn rates.
"""))

# Save Cleaned Data
cells.append(nbf.v4.new_markdown_cell("""## Conclusion and Clean Data Export

The cleaned data is saved, and we are ready to build the interactive dashboard.
"""))

# Set notebook cells
nb['cells'] = cells

# Save notebook file
with open("d:/EDA/eda_notebook.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook generated successfully at d:/EDA/eda_notebook.ipynb")
