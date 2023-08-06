import os
import re
import subprocess
import tempfile
from functools import partial


def get_tmpfile(suffix=".txt"):
    tfp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    filename = tfp.name
    filename = os.path.normpath(filename)
    tfp.close()
    return filename, partial(os.remove, tfp.name)


def get_default_gateway():
    t1, r1 = get_tmpfile(suffix=".txt")
    t2, r2 = get_tmpfile(suffix=".txt")
    t3, r3 = get_tmpfile(suffix=".txt")
    t4, r4 = get_tmpfile(suffix=".txt")
    t5, r5 = get_tmpfile(suffix=".txt")

    v = rf"""
    
@echo off
type nul >{t1}
type nul >{t2}
for /f "tokens=2,3 delims={{,}}" %%a in ('"wmic nicconfig where IPEnabled="True" get DefaultIPGateway /value | findstr "I" "') do (
  for /f "tokens=1-3 delims=^." %%i in ("%%~a") do (
    for /l %%l in (1,1,1) do (
      ping -n 1 %%i.%%j.%%k.%%l | findstr "bytes=32"
     if errorlevel 1 (echo %%i.%%j.%%k.%%l DOWN >> {t3}) else (echo %%i.%%j.%%k.%%l ACTIVE >> {t4})
  )
 )
)
    
    """

    execute, rexe = get_tmpfile(suffix=".bat")
    with open(execute, mode="w", encoding="utf-8") as f:
        f.write(v)

    ou = subprocess.run(execute, capture_output=True, shell=True).stdout.decode(
        "utf-8", "ignore"
    )
    try:
        r1()
        r2()
        r3()
        r4()
        r5()
        rexe()
    except Exception:
        pass
    return re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ou)[0]
