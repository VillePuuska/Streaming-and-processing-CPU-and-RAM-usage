import duckdb
import numpy as np
from numpy.typing import NDArray


def get_latest_data(pg_conn: str) -> tuple[dict[str, NDArray], dict[str, NDArray]]:
    duckdb.sql(
        f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{pg_conn}' AS pg (TYPE POSTGRES);
        """
    )
    res_cpu = duckdb.sql(
        """
        FROM pg.public.latest_measurements
        WHERE measurement_name = 'cpu_usage'
        """
    ).fetchnumpy()
    res_ram = duckdb.sql(
        """
        FROM pg.public.latest_measurements
        WHERE measurement_name = 'memory_usage'
        """
    ).fetchnumpy()
    duckdb.sql("DETACH pg")
    return res_cpu, res_ram


def get_last_minute_data(
    pg_conn: str,
) -> tuple[dict[str, NDArray], dict[str, NDArray]]:
    duckdb.sql(
        f"""
        INSTALL postgres;
        LOAD postgres;
        ATTACH '{pg_conn}' AS pg (TYPE POSTGRES);
        """
    )
    res_cpu = duckdb.sql(
        """
        FROM pg.public.measurements_last_minute
        WHERE measurement_name = 'cpu_usage'
        """
    ).fetchnumpy()
    res_ram = duckdb.sql(
        """
        FROM pg.public.measurements_last_minute
        WHERE measurement_name = 'memory_usage'
        """
    ).fetchnumpy()
    duckdb.sql("DETACH pg")
    return res_cpu, res_ram
