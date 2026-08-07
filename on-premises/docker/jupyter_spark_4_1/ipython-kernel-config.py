import sys


c = get_config()  # noqa: F821

sys.path.insert(0, "/home/jovyan/work/notebooks/jupyter/spark")

c.InteractiveShellApp.extensions.append("sparkmonitor.kernelextension")
c.InteractiveShellApp.extensions.append("lib")
