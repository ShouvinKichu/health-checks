#!/usr/bin/env python3
import sys
import argparse
import psutil


# ── helpers ──────────────────────────────────────────────────────────────────

def bytes_to_human(n: int) -> str:
    """Convert raw bytes to a readable string (KB / MB / GB)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def bar(pct: float, width: int = 30) -> str:
    """Draw a simple ASCII progress bar for a percentage value."""
    filled = int(width * pct / 100)
    color  = "\033[92m" if pct < 70 else "\033[93m" if pct < 90 else "\033[91m"
    reset  = "\033[0m"
    return f"{color}{'█' * filled}{'░' * (width - filled)}{reset} {pct:5.1f}%"


def section(title: str) -> None:
    print(f"\n\033[1;34m{'─' * 50}\033[0m")
    print(f"\033[1;34m  {title}\033[0m")
    print(f"\033[1;34m{'─' * 50}\033[0m")


# ── memory sections ───

def show_ram() -> None:
    """Print a summary of physical RAM."""
    mem = psutil.virtual_memory()
    section("RAM")
    print(f"  {'Total':<12} {bytes_to_human(mem.total)}")
    print(f"  {'Used':<12} {bytes_to_human(mem.used)}")
    print(f"  {'Available':<12} {bytes_to_human(mem.available)}")
    # 'cached' and 'buffers' exist on Linux; on macOS psutil exposes 'cached' differently
    cached  = getattr(mem, "cached",  None)
    buffers = getattr(mem, "buffers", None)
    if cached  is not None: print(f"  {'Cached':<12} {bytes_to_human(cached)}")
    if buffers is not None: print(f"  {'Buffers':<12} {bytes_to_human(buffers)}")
    print(f"\n  Usage  {bar(mem.percent)}")


def show_swap() -> None:
    """Print swap/virtual memory summary."""
    swap = psutil.swap_memory()
    section("Swap")
    if swap.total == 0:
        print("  No swap configured.")
        return
    print(f"  {'Total':<12} {bytes_to_human(swap.total)}")
    print(f"  {'Used':<12} {bytes_to_human(swap.used)}")
    print(f"  {'Free':<12} {bytes_to_human(swap.free)}")
    print(f"\n  Usage  {bar(swap.percent)}")


def show_top_processes(n: int = 10) -> None:
    """List the top-N processes by RSS (resident set size — actual RAM held)."""
    section(f"Top {n} Processes by Memory (RSS)")

    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_info", "memory_percent"]):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass  # process died or we don't have permission — skip it

    # sort descending by RSS
    procs.sort(key=lambda x: x["memory_info"].rss if x["memory_info"] else 0, reverse=True)

    print(f"  {'PID':>7}  {'RSS':>9}  {'%MEM':>6}  Name")
    print(f"  {'─'*7}  {'─'*9}  {'─'*6}  {'─'*30}")
    for p in procs[:n]:
        rss  = bytes_to_human(p["memory_info"].rss) if p["memory_info"] else "n/a"
        pct  = f"{p['memory_percent']:.2f}" if p["memory_percent"] is not None else "n/a"
        name = (p["name"] or "?")[:40]
        print(f"  {p['pid']:>7}  {rss:>9}  {pct:>6}  {name}")


# ── entrypoint ────

def main() -> None:
    parser = argparse.ArgumentParser(description="System memory snapshot")
    parser.add_argument("--top", type=int, default=10,
                        help="Number of top processes to show (default: 10)")
    parser.add_argument("--no-procs", action="store_true",
                        help="Skip the process list")
    args = parser.parse_args()

    print("\n\033[1;37m  MEMORY SNAPSHOT\033[0m")

    show_ram()
    show_swap()
    if not args.no_procs:
        show_top_processes(args.top)

    print(f"\n{'─' * 50}\n")


if __name__ == "__main__":
    try:
        import psutil  # noqa: F811 — re-import just to give a clear error if missing
    except ImportError:
        print("psutil not found. Install it with:  pip install psutil")
        sys.exit(1)

    main()