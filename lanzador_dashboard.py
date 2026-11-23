import os
import sys
import webbrowser
import time
from pathlib import Path

def main():
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parent

    html_file = base_dir / "Dashboard_Portatil_UNCP_Daniel_Sulca.html"
    
    if html_file.exists():
        webbrowser.open(html_file.as_uri())
    else:
        webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    main()
