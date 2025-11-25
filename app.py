from flask import Flask, jsonify, request
import time
from cpu_task import cpu_heavy_task
from io_task import io_heavy_task
from common.logger_base import logger
app = Flask(__name__)


# 1. 普通快速接口（用来压 QPS）
@app.route("/api/fast")
def fast():
    logger.info("/api/fast 被访问")
    return jsonify({"msg": "fast ok", "timestamp": time.time()})


# 2. CPU 密集接口（压 CPU）
@app.route("/api/cpu")
def cpu():
    logger.info("/api/cpu 被访问")
    n = int(request.args.get("n", 5000000))
    result = cpu_heavy_task(n)
    return jsonify({"msg": "cpu ok", "result": result})


# 3. I/O 密集接口（模拟磁盘写入）
@app.route("/api/io")
def io():
    logger.info("/api/io 被访问")
    size = int(request.args.get("size", 5))  # MB
    io_heavy_task(size)
    return jsonify({"msg": "io ok", "size_mb": size})


# 4. 延迟接口（模拟网络慢）
@app.route("/api/slow")
def slow():
    logger.info("/api/slow 被访问")
    delay = float(request.args.get("delay", 1))
    time.sleep(delay)
    return jsonify({"msg": "slow ok", "delay": delay})


# 5. 健康检查
@app.route("/api/health")
def health():
    logger.info("/api/health 被访问")
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    # 仅开发环境使用，生产建议用 gunicorn + Nginx
    app.run(host="0.0.0.0", port=5004, debug=False)
