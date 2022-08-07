import os
import sys
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    # frozen
    root_path = os.path.dirname(sys.executable)
else:
    # unfrozen
    bundle_path = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(bundle_path)

load_dotenv(dotenv_path=os.path.join(root_path, "config.env"))
