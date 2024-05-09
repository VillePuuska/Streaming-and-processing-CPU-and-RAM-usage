import psutil


def get_readings() -> dict[str, float]:
    res = {}
    res["memory_usage"] = psutil.virtual_memory().percent

    res["cpu_usage"] = psutil.cpu_percent()

    return res
