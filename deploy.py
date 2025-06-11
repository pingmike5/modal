import modal
import time

APP_NAME = "llm-inference-agent-sandbox"
WORKSPACE_DIR = "/workspace"
SANDBOX_NAME = "main-sandbox"  # 给沙盒起名方便查找

# 初始化应用
app = modal.App.lookup(APP_NAME, create_if_missing=True)

# 构建镜像
image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path=WORKSPACE_DIR)
)

def run_in_fresh_sandbox():
    print("🔍 Checking existing sandbox...")

    # 查看是否已有沙盒，存在就终止
    existing = modal.Sandbox.lookup(SANDBOX_NAME, app=app, raise_if_not_found=False)
    if existing:
        print("🛑 Terminating existing sandbox...")
        existing.terminate()
        existing.wait(raise_on_termination=False)
        print("✅ Terminated.")

    print("🚀 Launching new sandbox...")
    sandbox = modal.Sandbox.create(
        name=SANDBOX_NAME,
        app=app,
        image=image,
        timeout=86400,  # 如果你需要共享 volume，可在此配置
    )

    print("📁 Launching app.py (background)...")
    sandbox.exec("python3", f"{WORKSPACE_DIR}/app.py")

    print("✅ New sandbox launched.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", action="store_true", help="Run app.py in Modal Sandbox")
    args = parser.parse_args()

    if args.sandbox:
        run_in_fresh_sandbox()
    else:
        print("ℹ️ Use --sandbox to run in Modal Sandbox")
