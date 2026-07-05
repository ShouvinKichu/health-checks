import shutil


def check_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)

    total_gb = total / (1024 ** 3)
    used_gb = used / (1024 ** 3)
    free_gb = free / (1024 ** 3)

    usage_percent = (used / total) * 100

    print(f"Disk Usage for: {path}")
    print("-" * 35)
    print(f"Total Space : {total_gb:.2f} GB")
    print(f"Used Space  : {used_gb:.2f} GB")
    print(f"Free Space  : {free_gb:.2f} GB")
    print(f"Usage       : {usage_percent:.2f}%")

    if usage_percent > 80:
        print("\n⚠️ Warning: Disk usage is above 80%!")
    else:
        print("\n✅ Disk usage is healthy.")


check_disk_usage()