import os
import time


def io_heavy_task(size_mb):
    filename = f"/tmp/io_test_{int(time.time() * 1000)}.dat"
    data = b"0" * 1024 * 1024  # 1 MB

    with open(filename, "wb") as f:
        for _ in range(size_mb):
            f.write(data)

    # 删掉文件，避免占用磁盘
    os.remove(filename)
