#!/usr/bin/env python3
"""
Benchmark script to compare execution speed of:
  - tsunami       (serial)
  - tsunami-parallel (coarray, run with cafrun -n 8)

Runs each version multiple times and reports timing statistics and speedup.
"""

import subprocess
import time
import sys
import os
from statistics import mean, stdev

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERIAL_BIN = os.path.join(SCRIPT_DIR, "tsunami")
PARALLEL_BIN = os.path.join(SCRIPT_DIR, "tsunami-parallel")
CAFRUN = "cafrun"
NUM_IMAGES = 8          # number of parallel images for cafrun
NUM_RUNS = 3            # number of runs per version for averaging
TIMEOUT = 600           # timeout per run in seconds

# --- Helper: run a command and measure wall-clock time ---
def run_and_time(cmd: list[str], label: str) -> float | None:
    """Run a command, return elapsed wall-clock time in seconds, or None on failure."""
    print(f"  Running ({label}): {' '.join(cmd)} ...", flush=True)
    t_start = time.perf_counter()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            cwd=SCRIPT_DIR,
        )
        t_end = time.perf_counter()
        elapsed = t_end - t_start
        if result.returncode != 0:
            print(f"    ERROR: exit code {result.returncode}")
            stderr_tail = result.stderr.strip().splitlines()[-5:]
            for line in stderr_tail:
                print(f"    stderr: {line}")
            return None
        print(f"    Done in {elapsed:.3f}s")
        return elapsed
    except subprocess.TimeoutExpired:
        print(f"    TIMEOUT after {TIMEOUT}s")
        return None
    except FileNotFoundError:
        print(f"    ERROR: executable not found")
        return None


# --- Main ---
def main():
    # Check binaries
    for bin_path, name in [(SERIAL_BIN, "tsunami"), (PARALLEL_BIN, "tsunami-parallel")]:
        if not os.path.isfile(bin_path):
            print(f"ERROR: {name} not found at {bin_path}")
            sys.exit(1)
        if not os.access(bin_path, os.X_OK):
            print(f"ERROR: {name} is not executable: {bin_path}")
            sys.exit(1)

    print("=" * 60)
    print("  Tsunami Benchmark")
    print(f"  Runs per version: {NUM_RUNS}")
    print(f"  Parallel images:  {NUM_IMAGES}")
    print("=" * 60)

    # --- Serial benchmark ---
    print("\n--- Serial (tsunami) ---")
    serial_times = []
    for i in range(1, NUM_RUNS + 1):
        t = run_and_time([SERIAL_BIN], f"run {i}/{NUM_RUNS}")
        if t is not None:
            serial_times.append(t)

    # --- Parallel benchmark ---
    print(f"\n--- Parallel (tsunami-parallel, cafrun -n {NUM_IMAGES}) ---")
    parallel_times = []
    for i in range(1, NUM_RUNS + 1):
        t = run_and_time(
            [CAFRUN, "-n", str(NUM_IMAGES), PARALLEL_BIN],
            f"run {i}/{NUM_RUNS}",
        )
        if t is not None:
            parallel_times.append(t)

    # --- Report ---
    print("\n" + "=" * 60)
    print("  RESULTS")
    print("=" * 60)

    if serial_times:
        print(f"\n  Serial (tsunami):")
        print(f"    Times : {[f'{t:.3f}s' for t in serial_times]}")
        print(f"    Min   : {min(serial_times):.3f}s")
        print(f"    Max   : {max(serial_times):.3f}s")
        print(f"    Mean  : {mean(serial_times):.3f}s")
        if len(serial_times) > 1:
            print(f"    Stdev : {stdev(serial_times):.3f}s")
        serial_avg = mean(serial_times)
    else:
        print("\n  Serial: all runs FAILED")
        serial_avg = None

    if parallel_times:
        print(f"\n  Parallel (tsunami-parallel, {NUM_IMAGES} images):")
        print(f"    Times : {[f'{t:.3f}s' for t in parallel_times]}")
        print(f"    Min   : {min(parallel_times):.3f}s")
        print(f"    Max   : {max(parallel_times):.3f}s")
        print(f"    Mean  : {mean(parallel_times):.3f}s")
        if len(parallel_times) > 1:
            print(f"    Stdev : {stdev(parallel_times):.3f}s")
        parallel_avg = mean(parallel_times)
    else:
        print("\n  Parallel: all runs FAILED")
        parallel_avg = None

    if serial_avg is not None and parallel_avg is not None:
        speedup = serial_avg / parallel_avg
        print(f"\n  Speedup: {speedup:.2f}x")
        print(f"  (serial {serial_avg:.3f}s / parallel {parallel_avg:.3f}s)")
    else:
        print("\n  Speedup: N/A (incomplete data)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
