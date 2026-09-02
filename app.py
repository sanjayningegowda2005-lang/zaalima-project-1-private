import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zaalima Data Pipeline Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Zaalima Data Engineering Pipeline")
st.markdown(
    "Real-time visibility into local staging data, transformation views, and pipeline analytics."
)

# Connect to SQLite staging database
DB_PATH = "pipeline_staging.db"


@st.cache_data
def load_data(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Sidebar Navigation
st.sidebar.header("Pipeline Controls")
view_option = st.sidebar.radio(
    "Select View Mode", ["Overview & KPIs", "Staging Views", "Execution Logs"]
)

if view_option == "Overview & KPIs":
    st.subheader("Key Performance Metrics")
    col1, col2, col3 = st.columns(3)

    try:
        df_summary = load_data(
            "SELECT COUNT(*) as total_records FROM product_revenue"
        )
        total_records = df_summary["total_records"].iloc[0]
        col1.metric("Processed Staging Records", total_records)
        col2.metric("Pipeline Status", "HEALTHY", delta="Active")
        col3.metric("Database Engine", "SQLite Serverless")
    except Exception as e:
        st.warning(
            f"Run your ETL scripts to populate staging database tables. ({e})"
        )

elif view_option == "Staging Views":
    st.subheader("Database Table Explorer")
    table_name = st.selectbox(
        "Select Staging Table / View",
        ["product_revenue", "vw_product_summary"],
    )
    try:
        df_table = load_data(f"SELECT * FROM {table_name}")
        st.dataframe(df_table, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load table '{table_name}': {e}")

elif view_option == "Execution Logs":
    st.subheader("Pipeline Execution Logs")
    try:
        with open("pipeline_execution.log", "r") as log_file:
            st.text_area(
                "System Logs", log_file.read(), height=300, disabled=True
            )
    except FileNotFoundError:
        st.info("No log file found. Run your ETL orchestrator to generate logs.")