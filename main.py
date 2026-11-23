#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent
    src = repo_root / "assets" / "entry.png"
    
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")

if __name__ == "__main__":
    main()