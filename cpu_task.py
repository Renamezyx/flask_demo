def cpu_heavy_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total
