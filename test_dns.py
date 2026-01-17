import time, json, urllib3

class GoogleDNSChecker():
    def __init__(self) -> None:
        self.dnsServers = {
            "Google": {
                "url": "https://dns.google/resolve",
                "provider": "Google Public DNS",
                "location": "Mountain View CA, United States"
            },
            "Cloudflare": {
                "url": "https://cloudflare-dns.com/dns-query",
                "provider": "Cloudflare DNS",
                "location": "San Francisco CA, United States"
            },
            "Aliyun": {
                "url": "https://dns.alidns.com/resolve",
                "provider": "Aliyun Computing Co. Ltd",
                "location": "Hangzhou, China"
            }
        }
        self.currentServer = 'Google'
        self.PM = urllib3.PoolManager()
        self.headers = {
            'accept': 'application/dns-json'
        }

    def setServers(self, servers=''):
        # 兼容旧的服务器名称
        server_mapping = {
            'Google': 'Google',
            'OpenDNS': 'Google',
            'AT&T': 'Google',
            'Aliyun': 'Aliyun',
            'LG': 'Google',
            'IONICA': 'Google'
        }
        if servers in server_mapping:
            self.currentServer = server_mapping[servers]

    def getServers(self):
        return self.dnsServers[self.currentServer]

    def check(self, qname='', rdtype='A', max_retries=3):
        """查询域名的 IP 地址,支持重试"""
        for attempt in range(max_retries):
            try:
                server_info = self.dnsServers[self.currentServer]
                url = '{}?name={}&type={}'.format(server_info['url'], qname, rdtype)
                
                res = self.PM.request('GET', url, headers=self.headers, timeout=10.0)
                
                if res.status == 200:
                    data = json.loads(res.data.decode('utf-8'))
                    
                    if 'Answer' in data and len(data['Answer']) > 0:
                        ips = []
                        for answer in data['Answer']:
                            if 'data' in answer and answer.get('type') == 1:  # A记录
                                ips.append(answer['data'])
                        
                        if len(ips) > 0:
                            print('[成功] {} -> {}'.format(qname, ips[0]))
                            return True, ips
                
                # 如果没有获取到结果,等待后重试
                if attempt < max_retries - 1:
                    time.sleep(1)
                    
            except Exception as err:
                print('[错误] {} 查询失败 (尝试 {}/{}): {}'.format(qname, attempt + 1, max_retries, err))
                if attempt < max_retries - 1:
                    time.sleep(2)
        
        print('[失败] {} 无法解析'.format(qname))
        return False, []


if __name__ == '__main__':
    # 测试域名列表
    test_domains = [
        "github.com",
        "api.github.com",
        "raw.githubusercontent.com",
        "hub.docker.com",
        "themoviedb.org"
    ]
    
    print('=== 测试 DNS 解析功能 ===\n')
    
    # 测试 Google DNS
    print('--- 使用 Google DNS ---')
    dnsobj = GoogleDNSChecker()
    dnsobj.setServers('Google')
    
    success_count = 0
    for domain in test_domains:
        ret, ips = dnsobj.check(domain, 'A')
        if ret:
            success_count += 1
    
    print('\n成功: {}/{} 个域名\n'.format(success_count, len(test_domains)))
    
    # 测试阿里云 DNS
    print('--- 使用 Aliyun DNS ---')
    dnsobj.setServers('Aliyun')
    
    success_count = 0
    for domain in test_domains:
        ret, ips = dnsobj.check(domain, 'A')
        if ret:
            success_count += 1
    
    print('\n成功: {}/{} 个域名'.format(success_count, len(test_domains)))
