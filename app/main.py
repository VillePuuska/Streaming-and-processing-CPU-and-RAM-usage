import streamlit as st
from utils.db_operations import get_latest_data, get_last_minute_data

PG_CONN = "postgresql://postgres:postgres@localhost:5432/"

latest_data = get_latest_data(pg_conn=PG_CONN)
last_minute_data = get_last_minute_data(pg_conn=PG_CONN)

st.header("Last minute data:")
st.line_chart(
    data=last_minute_data, x="window_start", y="avg_value", color="measurement_name"
)
