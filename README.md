# Modal 部署指南,会封号，勿用

1. 注册网站：[https://modal.com](https://modal.com)

2. 在个人资料页获取 API Token，例如：modal token set –token-id ak-XVbmGM9PF3TLwiu52 –token-secret as-Wo9a4CUsfGHkFu8q

3. 在 GitHub 仓库的 Settings → Secrets and variables → Actions 中，设置以下两个变量：

- `MODAL_TOKEN_ID`  
  这是你的 Modal Token ID，通常是以 `ak-` 开头的一串字符，比如 `ak-XVbmGM9PF3TLwiu52`。

- `MODAL_TOKEN_SECRET`  
  这是你的 Modal Token Secret，通常是以 `as-` 开头的一串字符，比如 `as-Wo9a4CUsfGHkFu8q7`。

4. 修改app.py里面的变量参数，deploy.py里面的app名字最好还是修改一下，最好让AI再修改一下。启动github action即可。
5.  节点获取说明：  
根据 UUID 和固定隧道域名手动配置，支持 vmess、vless、trojan 三种协议。

---

## 感谢


特别感谢上游项目作者 eooce 的 py-argo 项目。
