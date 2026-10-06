"""Run only a temporary API probe, never a Mari user project."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
output = root / "build/acceptance-20260928/host-mari7.1v1"
output.mkdir(parents=True, exist_ok=True)
profile = output / "profile"
for name in ("cache", "user", "scripts", "work", "profile"):
    (output / name).mkdir(exist_ok=True)
configuration = Path(os.environ["USERPROFILE"]) / ".mari/TheFoundry"
backup = output / "configuration-backup"
before = {}
if configuration.exists():
    for source in configuration.rglob("*"):
        if source.is_file():
            relative = source.relative_to(configuration)
            before[str(relative)] = hashlib.sha256(source.read_bytes()).hexdigest()
            destination = backup / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
environment = os.environ.copy()
environment.update({"USERPROFILE": str(profile), "HOME": str(profile),
                    "MARI_USER_PATH": str(output / "user"), "MARI_CACHE": str(output / "cache"),
                    "MARI_SCRIPT_PATH": str(output / "scripts"), "MARI_WORKING_DIR": str(output / "work"),
                    "MARI_LOG_FILE": str(output / "MariLog.txt"),
                    "MARI_ACCEPTANCE_DLL": str(root / "build/out/MariChineseHook.dll"),
                    "MARI_ACCEPTANCE_RESULT": str(output / "api-result.json")})
command = [r"C:\Program Files\Mari7.1v1\Bundle\bin\Mari7.1v1.exe", "-x", "-v",
           str(root / "scripts/acceptance_host_api.py")]
record = {"command": command, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "configuration_backup": str(backup), "configuration_before": before}
with (output / "process.log").open("wb") as stream:
    process = subprocess.Popen(command, env=environment, cwd=output / "work", stdout=stream,
                               stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
    record["pid"] = process.pid
    try:
        record["exit_code"] = process.wait(timeout=90)
    except subprocess.TimeoutExpired:
        record["timeout_seconds"] = 90
        process.terminate()
        record["exit_code"] = process.wait(timeout=10)
record["configuration_changed"] = []
for relative, digest in before.items():
    source = configuration / relative
    if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        record["configuration_changed"].append(relative)
        # Restore only the exact backed-up original file; no user data is deleted.
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup / relative, source)
record["api_result_present"] = (output / "api-result.json").exists()
(output / "process-result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in record.items() if key != "configuration_before"}, indent=2))
