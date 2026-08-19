import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "work/on-premises/squid/src"))

c = get_config()  # noqa: F821

c.InteractiveShellApp.extensions.append("sparkmonitor.kernelextension")
c.InteractiveShellApp.extensions.append("squid.jupyter.extensions")
