import duckdb
import pandas as pd


class Connection:
    """
    Object to hold the connection to the database.

    `pg_conn` is the connection string to the database.

    Methods for getting data:
    - get_latest_data: -> pd.DataFrame
    - get_last_minute_data: -> tuple[pd.DataFrame, pd.DataFrame]
    """

    def __init__(self, pg_conn: str) -> None:
        self.conn = duckdb.connect()
        self.conn.sql(
            f"""
            INSTALL postgres;
            LOAD postgres;
            ATTACH '{pg_conn}' AS pg (TYPE POSTGRES);
            """
        )

    def get_latest_data(self) -> pd.DataFrame:
        """
        Method returns a Pandas dataframe of the latest average measurements
        in Postgres/Timescale from the view latest_measurements_avg.
        """
        try:
            res = self.conn.sql(
                """
                FROM pg.public.latest_measurements_avg
                ORDER BY machine_id, measurement_name
                """
            ).df()
        except:
            return pd.DataFrame(
                {
                    "machine_id": [],
                    "measurement_name": [],
                    "window_start": [],
                    "avg_value": [],
                }
            )
        return res

    def get_last_minute_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Method returns two Pandas dataframes as a tuple. First one contains the
        last minute of CPU usage measurements and the second one contains the
        last minute of RAM usage measurements.
        """
        try:
            self.conn.sql(
                """
                CREATE OR REPLACE TABLE last_min AS
                FROM pg.public.measurements_last_minute
                """
            )
            res_cpu = self.conn.sql(
                """
                FROM last_min
                WHERE measurement_name = 'cpu_usage'
                """
            ).df()
            res_ram = self.conn.sql(
                """
                FROM last_min
                WHERE measurement_name = 'memory_usage'
                """
            ).df()
        except:
            res = pd.DataFrame(
                {
                    "machine_id": [],
                    "measurement_name": [],
                    "window_start": [],
                    "avg_value": [],
                }
            )
            return res, res
        return res_cpu, res_ram
