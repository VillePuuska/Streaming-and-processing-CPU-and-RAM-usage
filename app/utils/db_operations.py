import duckdb
import pandas as pd


def get_latest_data(pg_conn: str) -> pd.DataFrame:
    """
    Function returns a Pandas dataframe of the latest average measurements
    in Postgres/Timescale from the view latest_measurements_avg.
    """
    try:
        duckdb.sql(f"ATTACH '{pg_conn}' AS pg (TYPE POSTGRES)")
        res = duckdb.sql(
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
    finally:
        try:
            duckdb.sql("DETACH pg")
        except:
            pass
    return res


def get_last_minute_data(pg_conn: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function returns two Pandas dataframes as a tuple. First one contains the
    last minute of CPU usage measurements and the second one contains the
    last minute of RAM usage measurements.
    """
    try:
        duckdb.sql(f"ATTACH '{pg_conn}' AS pg (TYPE POSTGRES)")
        duckdb.sql(
            """
            CREATE OR REPLACE TABLE last_min AS
            FROM pg.public.measurements_last_minute
            """
        )
        res_cpu = duckdb.sql(
            """
            FROM last_min
            WHERE measurement_name = 'cpu_usage'
            """
        ).df()
        res_ram = duckdb.sql(
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
    finally:
        try:
            duckdb.sql("DETACH pg")
        except:
            pass
    return res_cpu, res_ram
