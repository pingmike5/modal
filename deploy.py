import modal

APP_NAME = "llm-inference-agent-sandbox"  # 新的应用名称
WORKSPACE_DIR = "/workspace"

# 初始化 Modal 应用
app = modal.App.lookup(APP_NAME, create_if_missing=True)

# 构建镜像
image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install_from_requirements("requirements.txt")
    .add_local_dir(".", remote_path=WORKSPACE_DIR)
)

def run_in_sandbox():
    print("🧪 Launching sandbox...")

    # 创建沙盒（sandbox 实例）
    sandbox = modal.Sandbox.create(app=app, image=image)

    # 直接在 sandbox 中运行带路径的 app.py（无需 cd）
    print("🚀 Running app.py in sandbox...")
    p = sandbox.exec("python3", f"{WORKSPACE_DIR}/app.py")

    # 输出日志
    print("📤 STDOUT:")
    print(p.stdout.read())

    print("📛 STDERR:")
    print(p.stderr.read())

    # 可选：运行结束后关闭沙盒
    sandbox.terminate()
    print("✅ Sandbox execution complete.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sandbox", action="store_true", help="Run app.py in Modal Sandbox")
    args = parser.parse_args()

    if args.sandbox:
        run_in_sandbox()
    else:
        print("ℹ️ Use --sandbox to run in Modal Sandbox")
