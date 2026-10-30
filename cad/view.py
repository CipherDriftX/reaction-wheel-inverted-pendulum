"""Show assembly.step in the OCP CAD Viewer panel in VS Code.

Run:  .venv/bin/python cad/view.py
"""

from pathlib import Path

import cadquery as cq
from ocp_vscode import show

show(cq.importers.importStep(str(Path(__file__).resolve().parent / "step" / "assembly.step")))
