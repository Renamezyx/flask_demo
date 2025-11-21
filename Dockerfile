# 使用官方 Python 镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下所有文件拷贝到容器工作目录
COPY . /app

# 设置环境变量，防止 Python 输出缓冲，便于日志打印
ENV PYTHONUNBUFFERED=1

# 安装依赖
# 假设你有 requirements.txt
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认端口
EXPOSE 5004

# 默认启动命令
CMD ["python", "app.py"]