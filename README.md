# hosts  

## Note  
每日自动更新 github, docker 和 tinyMediaManager 的 IP 地址。  

**最近更新**: 已修复 DNS 查询失败问题,从 dnschecker.org 切换到 Google DNS-over-HTTPS API,确保稳定可靠的域名解析。

hosts Url:   
Raw Url: ``` https://raw.githubusercontent.com/shidahuilang/hosts/main/hosts ```  
CDN Url: ``` https://gcore.jsdelivr.net/gh/shidahuilang/hosts@main/hosts ```  
CDN Url: ``` https://cdn.staticaly.com/gh/shidahuilang/hosts/main/hosts ```    ```(推荐)```  

## Used  
Windows/MacOS:  
```
推荐使用 SwitchHosts
https://switchhosts.vercel.app
```
![image](https://github.com/shidahuilang/hosts/raw/main/1.png)

Linux:
```
# 删除旧的 hosts 记录
sudo sed -i '/# ING Hosts Start/,/# ING Hosts End/d' /etc/hosts
# 添加最新的 hosts
curl -s -L https://raw.githubusercontent.com/shidahuilang/hosts/main/hosts | sudo tee -a /etc/hosts
```

## 技术说明

- **DNS 查询**: 使用 Google DNS-over-HTTPS API 和阿里云 DNS API
- **自动更新**: 每3天自动运行一次 (可手动触发)
- **质量保证**: 内置验证机制,至少解析成功 60% 的域名才会提交更新
- **错误处理**: 支持自动重试,失败时保留原有 hosts 文件

## 包含的域名

- **GitHub**: 33 个域名 (github.com, api.github.com, raw.githubusercontent.com 等)
- **Docker**: 5 个域名 (hub.docker.com, ghcr.io, gcr.io 等)
- **TMM**: 6 个域名 (themoviedb.org, api.themoviedb.org 等)
