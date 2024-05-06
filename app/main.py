import streamlit as st
from utils.db_operations import get_latest_data, get_last_minute_data

PG_CONN = "postgresql://postgres:postgres@localhost:5432/"

latest_data = get_latest_data(pg_conn=PG_CONN)
last_minute_data_cpu, last_minute_data_ram = get_last_minute_data(pg_conn=PG_CONN)

last_minute_data_cpu["machine_id"] = last_minute_data_cpu["machine_id"].astype(str)
last_minute_data_ram["machine_id"] = last_minute_data_ram["machine_id"].astype(str)

st.header("Last minute CPU usage:")
st.line_chart(
    data=last_minute_data_cpu, x="window_start", y="avg_value", color="machine_id"
)

st.header("Last minute RAM usage:")
st.line_chart(
    data=last_minute_data_ram, x="window_start", y="avg_value", color="machine_id"
)

st.header("Latest data:")
st.dataframe(data=latest_data, hide_index=True)
