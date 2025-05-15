
import os
import psutil

def report_cpu_cores() -> dict:
    """
    Return a dict containing:
      - logical_cores: total CPU threads
      - physical_cores: physical CPU packages/cores
    Falls back to os.cpu_count() if psutil cannot determine logical count.
    """
    logical = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False)

    if logical is None:
        # psutil sometimes returns None; fall back
        logical = os.cpu_count()

    return {
        "logical_cores": logical,
        "physical_cores": physical
    }
