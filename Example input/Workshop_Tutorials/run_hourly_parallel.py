"""
Run hourly MAIZSIM simulations in parallel

*******************************NOTE**********************************
***This file must be with the folders that Excel Interface created***
*********************************************************************
"""

import sys
sys.dont_write_bytecode = True  # no __pycache__ from mp worker re-imports on Windows

import subprocess
import multiprocessing as mp
import os
from pathlib import Path
import time
import shutil

# Folder prefix to search for (change this for different folder prefix (As an example for workshop, it will be "Ex")
FOLDER_PREFIX = "Ex"

# Files needed to run simulation
required_files = [
    "2dmaizsim.exe",
    "maizsim.dll"
]

base_path = Path(__file__).resolve().parent


def find_source_folder(script_dir: Path) -> Path:

    def has_all(p: Path) -> bool:
        return all((p / f).exists() for f in required_files)

    env = os.environ.get("MAIZSIM_HOME")
    if env:
        p = Path(env)
        if has_all(p):
            return p

    def walk_up(name):
        cur = script_dir
        for _ in range(6):
            cur = cur.parent
            if cur == cur.parent:
                return None
            target = cur / name
            if has_all(target):
                return target
        return None

    for name in ("CLASSIM_Dev", "Models"):
        found = walk_up(name)
        if found:
            return found

    for cand in (script_dir, script_dir / "Models", script_dir / "bin"):
        if has_all(cand):
            return cand

    raise FileNotFoundError(
        f"Cannot find {required_files}. Set MAIZSIM_HOME env var."
    )


try:
    source_folder = find_source_folder(base_path)
except FileNotFoundError as e:
    print(f"ERROR: {e}")
    print(f"base_path = {base_path}")
    raise

def setup_folder(folder_path, folder_name):
    """Copy required exe and dll files to folder and create run.dat"""
    for filename in required_files:
        src = source_folder / filename
        dst = folder_path / filename
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    # Copy runXXX.dat to run.dat (MAIZSIM reads run.dat)
    run_src = folder_path / f"run{folder_name}.dat"                        
    run_dst = folder_path / "run.dat"
    if run_src.exists() and not run_dst.exists():
        shutil.copy2(run_src, run_dst)

def run_simulation(folder_name):
    """Run a single MAIZSIM simulation"""
    folder_path = base_path / folder_name

    # Setup folder with required files
    setup_folder(folder_path, folder_name)

    exe_path = folder_path / "2dmaizsim.exe"
    grid_bat = folder_path / "grid1.bat"

    if not exe_path.exists():
        return f"{folder_name}: ERROR - 2dmaizsim.exe not found"

    start_time = time.time()

    try:
        # Step 1: Run grid1.bat first
        if grid_bat.exists():
            subprocess.run(
                [str(grid_bat)],
                cwd=str(folder_path),
                capture_output=True,
                shell=True,
                timeout=60
            )

        # Step 2: Run simulation
        result = subprocess.run(
            [str(exe_path)],
            cwd=str(folder_path),
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes for hourly (longer than daily)
        )

        elapsed = time.time() - start_time

        # Check if output file exists
        g01_files = list(folder_path.glob("*.g01"))
        if g01_files:
            return f"{folder_name}: SUCCESS ({elapsed:.1f}s)"
        else:
            return f"{folder_name}: COMPLETED but no output ({elapsed:.1f}s)"

    except subprocess.TimeoutExpired:
        return f"{folder_name}: TIMEOUT (>30min)"
    except Exception as e:
        return f"{folder_name}: ERROR - {str(e)}"

def main():
    # Get all simulation folders matching the prefix
    sim_folders = [f.name for f in base_path.iterdir()
                   if f.is_dir() and f.name.startswith(FOLDER_PREFIX)]

    print(f"Found {len(sim_folders)} simulation folders:")
    for f in sorted(sim_folders):
        print(f"  {f}")

    if len(sim_folders) == 0:
        print("No simulation folders found!")
        return

    # Number of parallel processes
    num_workers = min(10, len(sim_folders))  # 8 workers (adjust based on CPU cores)
    print(f"\nRunning {len(sim_folders)} simulations with {num_workers} parallel workers...")
    print("=" * 60)

    start_total = time.time()

    # Run in parallel
    with mp.Pool(num_workers) as pool:
        results = pool.map(run_simulation, sorted(sim_folders))

    total_time = time.time() - start_total

    # Print results
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)

    success_count = 0
    for result in results:
        print(result)
        if "SUCCESS" in result:
            success_count += 1

    print("=" * 60)
    print(f"Total: {success_count}/{len(sim_folders)} successful")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f} min)")

if __name__ == "__main__":
    mp.freeze_support()  # Required for Windows
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"base_path     = {base_path}")
        print(f"source_folder = {source_folder}")
        import traceback
        traceback.print_exc()
    input("\nPress Enter to exit...")