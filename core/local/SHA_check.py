# coding:utf-8
# coding: utf-8
"""
    更新和防篡改
"""
# TODO: 给! 老! 子! 重! 构! 这! 个!!!!!!!!!!!
import hashlib
import ssl
import urllib.parse
import urllib.request

# 计算好的SHA256的URL
sha_url = "https://raw.githubusercontent.com/AGJ-smart/MyTestRepo/main/verification.txt"
# 设立请求头
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
# 改铸币SSL规则
ssl._create_default_https_context = ssl._create_unverified_context
# 进行请求
req = urllib.request.Request(url=sha_url, headers=headers)
# 进行解码
response = urllib.request.urlopen(sha_url).read().decode("utf-8").rstrip()
print(response)

# 计算本地FMCL
sus = "FMCL(1).pyzw"  #
with open(sus, 'rb') as f:
    omg = hashlib.new("sha256", f.read()).hexdigest()

print(omg)
# 判断
if omg != response:
    print("您所运行的FMCL并非最新版或已被篡改，我们建议您从官网下载最新版")
else:
    print("您所使用的FMCL为最新版且未被篡改")
