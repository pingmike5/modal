import modal
import subprocess
import sys
import os

# 创建 Modal 应用（名字可自定义）
app = modal.App(name="gameai_app")

# 定义镜像并构建（支持 curl、pip 依赖、本地代码挂载）
image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

# Modal 远程函数（不立即运行，仅注册）
@app.function(
    image=image,
    concurrency_limit=1,  # sandbox 支持限制并发
    keep_warm=1,          # sandbox 支持保活
    timeout=86400,
    retries=-1,
)
def run_app():
    os.chdir("/workspace")
    print("🟢 Starting app.py...")

    process = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 实时打印日志（sandbox 中可在终端查看输出）
    for line in process.stdout:
        print(line.strip())

    # 检查退出码
    process.wait()
    if process.returncode != 0:
        print(f"🔴 Process failed with code {process.returncode}")
        raise modal.exception.ExecutionError("Script execution failed")


# 本地执行时使用 Modal sandbox 或 deploy 执行
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="运行远程函数")
    parser.add_argument("--sandbox", action="store_true", help="使用 sandbox 本地模拟")
    args = parser.parse_args()

    if args.sandbox:
        print("🧪 Running in sandbox mode...")
        with app.run():  # 使用 sandbox 启动环境
            run_app.local()  # 直接本地执行函数（类似 remote，但是 sandbox 环境中）
    elif args.run:
        print("🚀 Deploying and launching remotely...")
        app.deploy()
        run_app.spawn()  # 异步远程运行
        print("✅ Launched on Modal Cloud.")
    else:
        print("📦 Deploying only...")
        app.deploy()
