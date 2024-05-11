import streamlit as st
import time
import datetime
from utils.db_operations import Connection

REFRESH_INTERVAL = 1.0
PG_CONN = "postgresql://postgres:postgres@localhost:5432/"

conn = Connection(pg_conn=PG_CONN)

header1 = st.empty()
chart1 = st.empty()

header2 = st.empty()
chart2 = st.empty()

header3 = st.empty()
dataframe3 = st.empty()

timestamp = st.empty()

time_diff = st.empty()

while True:
    start_time = time.time()

    latest_data = conn.get_latest_data()
    last_minute_data_cpu, last_minute_data_ram = conn.get_last_minute_data()

    last_minute_data_cpu["machine_id"] = last_minute_data_cpu["machine_id"].astype(str)
    last_minute_data_ram["machine_id"] = last_minute_data_ram["machine_id"].astype(str)

    header1.header("Last minute CPU usage:")
    chart1.line_chart(
        data=last_minute_data_cpu,
        x="window_start",
        y="avg_value",
        color="machine_id",
    )

    header2.header("Last minute RAM usage:")
    chart2.line_chart(
        data=last_minute_data_ram,
        x="window_start",
        y="avg_value",
        color="machine_id",
    )

    header3.header("Latest data:")
    dataframe3.dataframe(data=latest_data, hide_index=True)

    ts = datetime.datetime.now()
    timestamp.caption(f"Data last updated: {ts.strftime('%d.%m.%Y %H:%M:%S')}")

    time_diff.caption(f"Took {time.time()-start_time:.4f} sec to refresh.")

    time.sleep(max(0.0, start_time + REFRESH_INTERVAL - time.time()))
