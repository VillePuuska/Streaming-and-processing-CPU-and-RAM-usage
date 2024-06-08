import streamlit as st
import time
import datetime
import click
from utils.db_operations import Connection


@click.command()
@click.option(
    "--refresh-interval",
    type=float,
    default=1.0,
    help="""Interval for how often data on the page is refreshed.
    Default: 1.0""",
)
@click.option(
    "--pg-conn",
    type=str,
    default="postgresql://postgres:postgres@localhost:5432/",
    help="""Postgres connection string.
    Default: postgresql://postgres:postgres@localhost:5432/""",
)
def main(refresh_interval: float, pg_conn: str) -> None:
    conn = Connection(pg_conn=pg_conn)

    st.header("Last minute CPU usage:")
    chart1 = st.empty()

    st.header("Last minute RAM usage:")
    chart2 = st.empty()

    st.header("Latest data:")
    dataframe3 = st.empty()

    timestamp = st.empty()

    time_diff = st.empty()

    while True:
        start_time = time.time()

        latest_data = conn.get_latest_data()
        last_minute_data_cpu, last_minute_data_ram = conn.get_last_minute_data()

        chart1.line_chart(
            data=last_minute_data_cpu,
            x="window_start",
            y="avg_value",
            color="machine_id",
        )

        chart2.line_chart(
            data=last_minute_data_ram,
            x="window_start",
            y="avg_value",
            color="machine_id",
        )

        dataframe3.dataframe(data=latest_data, hide_index=True)

        ts = datetime.datetime.now()
        timestamp.caption(f"Data last updated: {ts.strftime('%d.%m.%Y %H:%M:%S')}")

        time_diff.caption(f"Took {time.time()-start_time:.4f} sec to refresh.")

        time.sleep(max(0.0, start_time + refresh_interval - time.time()))


if __name__ == "__main__":
    main()
