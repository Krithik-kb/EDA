import os
import sys
import logging
import pandas as pd
from src.eda_pipeline import (
    load_data,
    validate_data,
    clean_data,
    generate_visualizations,
    generate_summary_js,
    generate_markdown_report
)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("eda_run.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Paths Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "dataset.csv")

# Outputs Configuration (under outputs/)
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
OUTPUT_DATA_DIR = os.path.join(OUTPUT_DIR, "data")
OUTPUT_PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
OUTPUT_REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")

# Cleaned data in local data folder
CLEANED_DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_dataset.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SUMMARY_JS_PATH = os.path.join(BASE_DIR, "dashboard", "data_summary.js")

def ensure_directories():
    """
    Ensures all necessary output and standard directories exist.
    """
    dirs = [
        OUTPUT_DATA_DIR, 
        OUTPUT_PLOTS_DIR, 
        OUTPUT_REPORTS_DIR, 
        os.path.join(BASE_DIR, "data"),
        PLOTS_DIR,
        REPORTS_DIR,
        os.path.join(BASE_DIR, "dashboard")
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    logger.info("Directories initialized successfully.")

def log_dataset_overview(df):
    """
    Executes and logs dataset overview.
    """
    logger.info("=== Dataset Overview ===")
    logger.info(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    logger.info("Columns and Data Types:")
    for col, dtype in df.dtypes.items():
        logger.info(f" - {col}: {dtype}")
        
def log_missing_value_analysis(df):
    """
    Executes and logs missing value analysis.
    """
    logger.info("=== Missing Value Analysis ===")
    nulls = df.isnull().sum()
    total_nulls = nulls.sum()
    if total_nulls == 0:
        logger.info("No missing values detected.")
    else:
        for col, val in nulls.items():
            if val > 0:
                pct = (val / len(df)) * 100
                logger.info(f" - {col}: {val} missing values ({pct:.2f}%)")

def log_duplicate_detection(df):
    """
    Executes and logs duplicate record detection.
    """
    logger.info("=== Duplicate Detection ===")
    dupes = df.duplicated().sum()
    if dupes == 0:
        logger.info("No duplicate records detected.")
    else:
        logger.info(f"Detected {dupes} duplicate records.")

def log_summary_statistics(df):
    """
    Executes and logs summary statistics.
    """
    logger.info("=== Summary Statistics (Numerical Columns) ===")
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    desc = numeric_df.describe().T
    for col in desc.index:
        stats_str = ", ".join([f"{stat}={desc.loc[col, stat]:.2f}" for stat in ["mean", "std", "min", "50%", "max"]])
        logger.info(f" - {col}: {stats_str}")

def log_outlier_detection(df):
    """
    Executes and logs outlier detection.
    """
    logger.info("=== Outlier and Anomaly Detection ===")
    
    # Age outlier checks
    age_under_0 = (df["Age"] < 0).sum()
    age_over_100 = (df["Age"] > 100).sum()
    if age_under_0 > 0 or age_over_100 > 0:
        logger.warning(f" - Age: Found {age_under_0} records under 0 and {age_over_100} records over 100.")
    else:
        logger.info(" - Age: No obvious outliers detected.")
        
    # MonthlyCharges outlier checks
    charges_over_200 = (df["MonthlyCharges"] > 200).sum()
    if charges_over_200 > 0:
        logger.warning(f" - MonthlyCharges: Found {charges_over_200} records with charges > $200 (suggests data entry error).")
    else:
        logger.info(" - MonthlyCharges: No obvious outliers detected.")
        
    # SupportCalls outlier checks
    max_support = df["SupportCalls"].max()
    logger.info(f" - SupportCalls: Max value is {max_support}.")

def log_correlation_analysis(df):
    """
    Executes and logs correlation analysis.
    """
    logger.info("=== Correlation Analysis ===")
    numeric_cols = ["Age", "Tenure", "MonthlyCharges", "TotalCharges", "SupportCalls", "Churn"]
    # Ensure columns exist in df
    cols_to_corr = [c for c in numeric_cols if c in df.columns]
    if len(cols_to_corr) > 1:
        corr = df[cols_to_corr].corr()
        if "Churn" in corr.columns:
            churn_corr = corr["Churn"].drop("Churn").sort_values(ascending=False)
            logger.info("Correlation of numeric features with Churn target:")
            for col, val in churn_corr.items():
                logger.info(f" - {col}: {val:.4f}")
        return corr
    return None

def run_eda_pipeline():
    """
    Main pipeline orchestrator.
    """
    logger.info("Starting complete EDA execution...")
    
    # Step 1: Ensure directory structure
    ensure_directories()
    
    # Step 2: Load Raw Data
    if not os.path.exists(DATA_FILE):
        logger.error(f"Raw dataset not found at {DATA_FILE}!")
        raise FileNotFoundError(f"Missing required file: {DATA_FILE}")
        
    df_raw = load_data(DATA_FILE)
    
    # Step 3: Validation Check
    validate_data(df_raw)
    
    # Step 4: Run analysis checks on raw data
    log_dataset_overview(df_raw)
    log_missing_value_analysis(df_raw)
    log_duplicate_detection(df_raw)
    log_summary_statistics(df_raw)
    log_outlier_detection(df_raw)
    
    # Step 5: Clean Data
    df_clean, cleaning_stats = clean_data(df_raw)
    
    # Step 6: Save clean dataset in outputs/data and local data/
    logger.info("Saving cleaned datasets...")
    cleaned_output_path = os.path.join(OUTPUT_DATA_DIR, "cleaned_dataset.csv")
    df_clean.to_csv(cleaned_output_path, index=False)
    df_clean.to_csv(CLEANED_DATA_FILE, index=False)
    logger.info(f"Cleaned dataset saved to {cleaned_output_path} and {CLEANED_DATA_FILE}")
    
    # Step 7: Run analysis checks on cleaned data to verify cleanliness
    logger.info("Verifying data quality of cleaned dataset...")
    log_missing_value_analysis(df_clean)
    corr_matrix = log_correlation_analysis(df_clean)
    
    # Step 8: Generate visualizations
    logger.info("Generating and saving visualizations...")
    # Generate into outputs/plots
    generate_visualizations(df_clean, OUTPUT_PLOTS_DIR)
    # Mirror into local plots/ (for dashboard reference)
    generate_visualizations(df_clean, PLOTS_DIR)
    logger.info("Visualizations generated successfully.")
    
    # Step 9: Save JS data summary for the dashboard
    if corr_matrix is not None:
        generate_summary_js(
            df_clean, 
            corr_matrix, 
            cleaning_stats["raw_shape"], 
            cleaning_stats["raw_duplicates"], 
            cleaning_stats["raw_nulls"], 
            SUMMARY_JS_PATH
        )
        
    # Step 10: Generate structured Markdown report
    report_output_path = os.path.join(OUTPUT_REPORTS_DIR, "final_report.md")
    report_root_path = os.path.join(REPORTS_DIR, "final_report.md")
    generate_markdown_report(df_clean, cleaning_stats, report_output_path)
    generate_markdown_report(df_clean, cleaning_stats, report_root_path)
    logger.info(f"Reports saved to {report_output_path} and {report_root_path}")
    
    logger.info("EDA Pipeline executed successfully end-to-end!")

if __name__ == '__main__':
    try:
        run_eda_pipeline()
    except Exception as e:
        logger.exception("An error occurred during EDA execution:")
        sys.exit(1)
