import modal
import subprocess
import sys
import os

app = modal.App(name="llm-inference-agent")

image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path="/workspace")
)

@app.function(
    image=image,
    timeout=86400,            # 每次运行 24 小时
    max_containers=1,
    min_containers=1,
    retries=modal.Retries(
        max_retries=10000,    # 自动重启最多 10000 次
        backoff_coefficient=1.0  # 不延迟，失败后立即重试
    )
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

    for line in process.stdout:
        print(line.strip())

    process.wait()
    if process.returncode != 0:
        print(f"🔴 Process failed with code {process.returncode}")
        raise modal.exception.ExecutionError("Script execution failed")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--sandbox", action="store_true")
    args = parser.parse_args()

    if args.sandbox:
        print("🧪 Running in sandbox mode...")
        with app.run():
            run_app.local()
    elif args.run:
        print("🚀 Deploying and launching remotely...")
        app.deploy()
        run_app.spawn()
        print("✅ Launched on Modal Cloud.")
    else:
        print("📦 Deploying only...")
        app.deploy()
