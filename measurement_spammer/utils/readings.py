import psutil


def get_readings() -> dict[str, float]:
    res = {}
    res["memory_usage"] = psutil.virtual_memory().percent

    cpu_usage = psutil.cpu_times_percent()
    res["cpu_usage"] = 100.0 - cpu_usage.idle

    return res
