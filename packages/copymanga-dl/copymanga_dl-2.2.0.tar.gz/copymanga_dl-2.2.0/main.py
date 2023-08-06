# -*- coding: UTF-8 -*-
import argparse
import datetime
import json
import os
import platform
import sys
import time

import requests
from retrying import retry
# 格式化输出
from rich import print as print
from rich.prompt import Prompt
from tqdm import tqdm

# 进行命令行参数设置
parser = argparse.ArgumentParser()

parser.add_argument(
    '--MangaPath',
    help='漫画的全拼，https://copymanga.site/comic/这部分')

parser.add_argument('--Url', help='copymanga的域名,如使用copymanga.site，那就输入site')

parser.add_argument('--Output', help='输出文件夹')

# todo 此功能暂时不在开发维护列表内，以后会随缘更新此功能
parser.add_argument(
    '--subscribe',
    help='是否切换到自动更新订阅模式(1/0，默认关闭(0))',
    default="0")

parser.add_argument(
    '--UseWebp',
    help='是否使用Webp(1/0，默认开启(1))',
    default="1")

parser.add_argument(
    '--UseOSCdn',
    help='是否使用海外cdn(1/0，默认关闭(0))',
    default="0")

parser.add_argument('--MangaStart', help='漫画开始下载话')

parser.add_argument('--MangaEnd', help='漫画结束下载话(如果只想下载一话请与MangaStart相同)')

parser.add_argument('--MangaList', help='漫画下载列表txt(每行一个漫画的全拼，具体请看Readme)')

parser.add_argument('--Proxy', help='设置代理')

args = parser.parse_args()

CmdMode = False
if args.MangaStart:
    CmdMode = True
else:
    print("[italic yellow]命令行重要参数丢失，默认启动用户输入模式[/italic yellow]")
now = datetime.datetime.now()

# 全局化headers，节省空间
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
api_headers = {
    'User-Agent': '"User-Agent" to "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44"',
    'version': now.strftime("%Y.%m.%d"),
    'region': '0',
    'webp': '0',
    "platform": "1",
    "referer": "https://www.copymanga.site/"

}
proxies = {}

def get_url():
    # *从GitHub(首先两个为CDN，方便中国大陆用户获取)中获取url的信息
    response = requests.get(
        'https://raw.fastgit.org/misaka10843/copymanga-downloader/master/url.json',
        headers=headers)
    if response.status_code != 200:
        print("您的网络似乎[italic red]不支持fastgit[/italic red]，我们正在切换新的请求地址")
        response = requests.get(
            'https://fastly.jsdelivr.net/gh/misaka10843/copymanga-downloader@master/url.json',
            headers=headers)
        if response.status_code != 200:
            print(
                "您的网络似乎也[italic red]不支持jsdelivr[/italic red]，我们只能请求GitHub原站了")
            response = requests.get(
                'https://raw.githubusercontent.com/misaka10843/copymanga-downloader/master/url.json',
                headers=headers)
            if response.status_code != 200:
                print("[italic red]我们无法获取到相关信息，请检查网络后重试[/italic red]")
                # *直接退出
                exit()
    url_list = response.json()
    print("[italic yellow]我们获取到copymanga有以下域名，请选择您希望使用的域名来确保连接通畅:[/italic yellow]")
    list_num = 0
    for i in url_list:
        # *循环输出url信息
        print(list_num, '->', i)
        list_num = list_num + 1
    get_url_list_num = input("您希望通过第几个域名来获取相关信息?(默认0)：")
    if len(get_url_list_num) == 0:
        get_url_list_num = 0
    # *从用户选择中获取到url信息并返回
    url = url_list[int(get_url_list_num)]
    return url


def get_settings():
    global download_path, proxies, Api_url
    # *初始化第一次初始化的开关（默认为关）
    first_initialization = 0
    if not os.path.isfile(os.curdir + 'settings.json') and not CmdMode:
        file = open(os.curdir + 'settings.json', 'w')
        file.close()
        # *打开
        first_initialization = 1
    elif not CmdMode and os.path.getsize(os.curdir + 'settings.json') == 0:
        # *打开
        first_initialization = 1
    # *如果为第一次初始化
    if first_initialization == 1:
        json_data = {}
        download_path = Prompt.ask(
            "您似乎是第一次启动此程序，请您先输入您需要下载的路径[italic yellow](请输入E:\\manga这种格式,不要最后一个斜杠哦qwq)[/italic yellow]")
        # *将反斜杠转成正斜杠
        json_data["download_path"] = download_path.replace('\\', '/')
        print(
            "\n接下来填写的是获取您的收藏漫画需要的参数，请认真填写哦qwq[italic yellow](如果不想获取的话也可以直接填写null)[/italic yellow]\n")
        cookies_get = Prompt.ask(
            "请输入您的authorization[italic yellow](如不会获取请看https://t.hk.uy/bdFu ("
            "此为获取用户收藏漫画,下载服务不受影响))[/italic yellow]")
        json_data["authorization"] = cookies_get
        if Prompt.ask("是否使用海外CDN？[italic green](y/n)[/italic green]").lower() == 'y':
            json_data["use_oversea_cdn"] = True
        else:
            json_data["use_oversea_cdn"] = False
        # *是否为了节省服务器带宽而使用webp
        if Prompt.ask("是否下载webp格式图片[italic yellow](可以节省服务器资源)？[/italic yellow][italic green](y/n)[/italic green]").lower() == 'y':
            json_data["use_webp"] = True
        else:
            json_data["use_webp"] = False
        # *获取proxies状态
        proxies_get = Prompt.ask(
            "您是否使用了代理？如果是，请填写代理地址[italic yellow](如http://127.0.0.1:8099或者socks5://127.0.0.1:8099，没有请直接回车)[/italic yellow]")
        json_data["proxies"] = proxies_get
        # *获取最新的域名状态
        json_data["api_url"] = get_url()
        # *写入文件
        with open(os.curdir + 'settings.json', 'w', encoding="utf-8") as fp:
            json.dump(json_data, fp, indent=2, ensure_ascii=False)

        print("[italic green]恭喜您已经完成初始化啦！[/italic green]\n我们将立即执行主要程序，\n[italic blue]如果您需要修改设置的话可以直接到程序根目录的settings.json更改qwq[/italic blue]")
    # *读取设置内容
    if not CmdMode:
        with open(os.curdir + 'settings.json', 'r', encoding="utf-8") as fp:
            json_data = json.load(fp)
            #! 只要下载路径/请求地址是空，那么就直接报错
            if not json_data["download_path"] or not json_data["api_url"]:
                print("[italic red]您的设置似乎出现了问题导致部分设置丢失，请您重新启动此程序后重新设置[/italic red]")
                fp.close()
                os.rename(
                    os.curdir +
                    'settings.json',
                    os.curdir +
                    'settings_old.json')
                exit()
            download_path = json_data["download_path"]
            if json_data["authorization"]:
                headers["authorization"] = json_data["authorization"]
            else:
                headers["authorization"] = "null"
            proxies_set = json_data["proxies"]
            Api_url = json_data["api_url"]
            if json_data["use_oversea_cdn"]:
                api_headers["region"] = '0'
            if json_data["use_webp"]:
                api_headers["webp"] = '1'
        if proxies_set:
            # 如果代理不存在协议前缀，则视为http代理
            if proxies_set.find('://') == -1:
                proxies_set = 'http://' + proxies_set
            proxies = {
                'http': proxies_set,
                'https': proxies_set
            }
        # *检测是否有此目录，没有就创建
        if not os.path.exists("%s/" % download_path):
            os.mkdir("%s/" % download_path)
    else:
        # *获取下载路径
        if not args.Output:
            print("[italic yellow]重要参数丢失，将默认为目录下的None文件夹[/italic yellow]")
            download_path = os.curdir + "None"
        download_path = args.Output
        # *检测是否有此目录，没有就创建
        if not os.path.exists("%s/" % download_path):
            os.mkdir("%s/" % download_path)
        # *获取API
        if not args.Url:
            print("[italic yellow]重要参数丢失，将默认为copymanga.org[/italic yellow]")
            Api_url = "copymanga.org"
        Api_url = args.Url

        if args.UseOSCdn != "0":
            api_headers["region"] = '0'
        if args.UseWebp != "0":
            api_headers["webp"] = '1'
        if args.Proxy:
            # 如果代理不存在协议前缀，则视为http代理
            proxies_set = args.Proxy
            if proxies_set.find('://') == -1:
                proxies_set = 'http://' + proxies_set
            proxies = {
                'http': proxies_set,
                'https': proxies_set
            }
        if not args.MangaPath or not args.MangaEnd or not args.MangaStart:
            print("[italic red]重要参数MangaPath/MangaStart/MangaEnd丢失，请确认填写[/italic red]")
            sys.exit(0)


def manga_search(manga_name):
    global get_list_name, get_list_manga
    print("[italic blue]正在搜索中...[/italic blue]\r", end="")
    # *获取搜索结果
    response = requests.get(
        'https://api.%s/api/v3/search/comic?format=json&limit=20&offset=0&platform=3&q=%s' %
        (Api_url, manga_name), headers=api_headers, proxies=proxies)
    print("[italic green]搜索完毕啦！  [/italic green]\n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        list_num = 0

        print("已搜索出以下漫画[italic yellow](如果没有您要找的漫画，请更换关键词即可)[/italic yellow]：")
        # *循环输出搜索列表
        for i in manga_search_list["results"]["list"]:
            print(list_num, '->', i["name"])
            list_num = list_num + 1
        get_list_num = Prompt.ask(
            "您需要下载的漫画是序号几？[italic green](默认0)[/italic green]")
        if len(get_list_num) == 0:
            get_list_num = 0
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["path_word"]
        get_list_manga = manga_search_list["results"]["list"][int(
            get_list_num)]["name"]
    else:
        # *报告远程服务器无法连接的状态码
        print("[italic yellow]服务器似乎[/italic yellow][italic red]无法连接[/italic red][italic yellow]了qwq[/italic yellow]\n")
        print("[italic yellow]如需使用代理，可使用命令，如：set https_proxy=http://127.0.0.1:7890，或者在settings.json中设置代理[/italic yellow]")
        print("[italic yellow]返回的状态码是：%d[/italic yellow]" %
              response.status_code)
        sys.exit(0)


def manga_chapter_group(manga_pathWord):
    if CmdMode:
        global get_list_manga
    chapter_group = requests.get(
        'https://api.%s/api/v3/comic2/%s'
        % (Api_url, manga_pathWord), headers=api_headers, proxies=proxies)
    chapter_group_list = chapter_group.json()

    if chapter_group.status_code == 200:
        # * 获取group值并强转list
        group_list = list(chapter_group_list["results"]["groups"].keys())
        if CmdMode:
            get_list_manga = chapter_group_list["results"]["comic"]["name"]
            return "default"
        if len(group_list) == 1:
            return "default"
        else:
            list_num = 0
            # *循环输出
            while list_num < len(group_list):
                print(list_num, '->',
                      chapter_group_list["results"]["groups"][group_list[list_num]]["name"])
                list_num = list_num + 1
            # *获取选项
            Get_group = Prompt.ask(
                "我们获取到了一些不同的分组，请输入需要下载的分组序号[italic green](默认为0)[/italic green]:", default="0")
            # *添加默认选项
            if len(Get_group) == 0:
                Get_group = 0
            else:
                Get_group = int(Get_group)
            # *将path_word传给manga_chapter_list
            return chapter_group_list["results"]["groups"][group_list[Get_group]]["path_word"]


def manga_chapter_list():
    global all_chapter, start_chapter, end_chapter, manga_chapter
    group_name = manga_chapter_group(get_list_name)
    # *获取章节列表
    manga_chapter = requests.get(
        'https://api.%s/api/v3/comic/%s/group/%s/chapters?limit=500&offset=0&platform=3' %
        (Api_url, get_list_name, group_name), headers=api_headers, proxies=proxies)
    # !简要判断是否服务器无法连接
    if manga_chapter.status_code == 200:
        # *将api解析成json
        chapter_list = manga_chapter.json()
        if not CmdMode:
            print("我们获取了[italic yellow]%s[/italic yellow]话的内容，请问是如何下载呢？" %
                  chapter_list["results"]["total"])
            # *判断用户需要怎么下载
            how_download = Prompt.ask(
                "[bold yellow]1->全本下载\n2->范围下载\n3->单话下载[bold yellow]\n您的选择是[italic green](默认全本下载)[/italic green]", choices=["1", "2", "3"], default="1")
            all_chapter = 0  # !防止误触发

            if len(how_download) == 0:
                how_download = 1
            if int(how_download) == 1:
                all_chapter = 1
            elif int(how_download) == 2:
                start_chapter = Prompt.ask("[bold yellow]从第几话？[/bold yellow]")
                end_chapter = Prompt.ask("[bold yellow]到第几话？[/bold yellow]")
            elif int(how_download) == 3:
                start_chapter = end_chapter = Prompt.ask(
                    "[bold yellow]下载第几话？[/bold yellow]")
        else:
            start_chapter = args.MangaStart
            end_chapter = args.MangaEnd
            all_chapter = 0
    else:
        # *报告远程服务器无法连接的状态码
        print("[italic yellow]服务器似乎[/italic yellow][italic red]无法连接[/italic red][italic yellow]了qwq[/italic yellow]\n")
        print("[italic yellow]返回的状态码是：%d[/italic yellow]" %
              manga_chapter.status_code)
        sys.exit(0)


@retry(wait_fixed=30, stop_max_attempt_number=3)
def download(url: str, fname: str, img_num: str):

    # 用流stream的方式获取url的数据
    resp = requests.get(url, stream=True, verify=False,
                        headers=api_headers, proxies=proxies)
    # 拿到文件的长度，并把total初始化为0
    total = int(resp.headers.get('content-length', 0))
    # 打开当前目录的fname文件(名字你来传入)
    # 初始化tqdm，传入总数，文件名等数据，接着就是写入，更新等操作了
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
            bar.set_description("\r正在下载[%s]第%s张: %s" % (fname, img_num, size))


def manga_download():
    print("[italic yellow]开始安排下载ing[/italic yellow]")
    # *解析全局传输的json
    manga_chapter_list = manga_chapter.json()
    # *判断是否为全本下载
    if all_chapter == 1:
        # *开始循环
        for i in manga_chapter_list["results"]["list"]:
            # *获取每章的图片url以及顺序
            response = requests.get(
                'https://api.%s/api/v3/comic/%s/chapter2/%s?platform=3' % (
                    Api_url, get_list_name, i["uuid"]),
                headers=api_headers, proxies=proxies)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while i["size"] > j:
                # 直接传给chapter_analysis做调用download
                chapter_analysis(response, j)
                j = j + 1
        # *试图跳出循环
        if (platform.system() == 'Windows'):
            os.system("cls")
        else:
            os.system("clear")
        print(
            "[bold green]这个漫画已经全部下载完了qwq[bold green]")
        time.sleep(10)
        sys.exit(0)
    elif all_chapter == 0:
        # *通过输入的数量来循环
        startchapter = start_chapter
        while int(end_chapter) >= int(startchapter):
            # ?因为数组为0开始，所以必须减去1
            startchapter_id = int(startchapter) - 1
            # *获取每章的图片url以及顺序
            response = requests.get(
                'https://api.%s/api/v3/comic/%s/chapter2/%s?platform=3' %
                (Api_url,
                 get_list_name,
                 manga_chapter_list["results"]["list"][startchapter_id]["uuid"]),
                headers=api_headers,
                proxies=proxies)
            response = response.json()
            j = 0
            # *通过获取的数量来循环
            while manga_chapter_list["results"]["list"][startchapter_id]["size"] > j:
                # 直接传给chapter_analysis做调用download
                chapter_analysis(response, j)
                j = j + 1
            startchapter = int(startchapter) + 1
        # *试图跳出循环
        if (platform.system() == 'Windows'):
            os.system("cls")
        else:
            os.system("clear")
        print(
            "[bold green]这个漫画已经全部下载完了qwq[bold green]")
        # *返回到初始界面
        welcome()


def chapter_analysis(response, j):
    img_url = response["results"]["chapter"]["contents"][j]["url"]
    img_num = response["results"]["chapter"]["words"][j]
    chapter_index = response["results"]["chapter"]["index"] + 1
    chapter_name = response["results"]["chapter"]["name"]
    # *检测是否有此目录，没有就创建
    if not os.path.exists("%s/%s/" % (download_path, get_list_manga)):
        os.mkdir("%s/%s/" % (download_path, get_list_manga))
    if not os.path.exists(
        "%s/%s/%.3d - %s/" %
        (download_path,
         get_list_manga,
         chapter_index,
         chapter_name)):
        os.mkdir("%s/%s/%.3d - %s/" %
                 (download_path, get_list_manga, chapter_index, chapter_name))
    # 分析图片位置以及名称
    img_ext = 'webp' if img_url.endswith('webp') else 'jpg'
    img_path = "%s/%s/%.3d - %s/%s.%s" % (download_path,
                                          get_list_manga,
                                          chapter_index,
                                          chapter_name,
                                          img_num,
                                          img_ext)
    download(img_url, img_path, img_num)


def manga_collection(offset):
    global get_list_name, get_list_manga
    if headers["authorization"] == "null":
        print(
            "[italic yellow]您并未填写Authorization，请按照https://shorturl.at/bevHW 填写并添加到settings.json中的authorization字段[/italic yellow]")
        return
    manga_search_list = ""
    print("[italic blue]正在查询中...[italic blue]\r", end="")
    response = requests.get(
        'https://%s/api/v3/member/collect/comics?limit=12&offset={'
        '%s}&free_type=1&ordering=-datetime_modifier' % (Api_url, offset),
        headers=headers, proxies=proxies)
    print("[italic green]查询完毕啦！  [/italic green]\n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        list_num = 0

        # print("已查询出以下漫画(输入pn为下一页，pu为上一页)：")
        print("已查询出以下漫画[italic yellow](暂且只能查询前50个)[/italic yellow]：")
        # *循环输出搜索列表
        for i in manga_search_list["results"]["list"]:
            print(list_num, '->', i["comic"]["name"])
            list_num = list_num + 1
        get_list_num = Prompt.ask(
            "您需要下载的漫画是序号几？[italic green](默认0)[/italic green]")
        if len(get_list_num) == 0:
            get_list_num = 0
        # Todo：查询漫画时翻页功能
        # 因为一些原因，无法使用下列方法查询其他页数漫画
        # if get_list_num == "pn":
        #    offsetnum = offset + 12
        #    print(offsetnum)
        #    manga_collection(offsetnum)
        # elif get_list_num == "pu":
        #    if offset == "0":
        #        print("没有上一页了qwq")
        #        manga_collection()
        #    else:
        #        offsetnum = offset - 12
        #        manga_collection(offsetnum)
        # offsetnum = offset - 12
        # manga_collection(offsetnum)
        get_list_name = manga_search_list["results"]["list"][int(
            get_list_num)]["comic"]["name"]
        manga_search(get_list_name)
    else:
        # *报告远程服务器无法连接的状态码
        print("[italic yellow]服务器似乎[/italic yellow][italic red]无法连接[/italic red][italic yellow]了qwq[/italic yellow]\n")
        print("[italic yellow]返回的状态码是：%d[/italic yellow]" %
              response.status_code)
        sys.exit(0)


def manga_collection_backup():
    global get_list_name, get_list_manga
    if headers["authorization"] == "null":
        print(
            "[italic yellow]您并未填写Authorization，请按照https://shorturl.at/bevHW 填写并添加到settings.json中的authorization字段[/italic yellow]")
        return
    manga_search_list = ""
    print("[italic blue]正在查询中...[italic blue]\r", end="")
    response = requests.get(
        'https://%s/api/v3/member/collect/comics?limit=500&offset=0&free_type=1&ordering=-datetime_modifier' %
        Api_url, headers=headers, proxies=proxies)
    print("[italic green]查询完毕啦！  [/italic green]\n")
    # !简要判断是否服务器无法连接
    if response.status_code == 200:
        # *将api解析成json
        manga_search_list = response.json()
        # *初始化列表的序号
        manga_list = manga_search_list["results"]["list"]
        # 输出txt
        print("正在输出到程序目录下的backup.csv....")
        f = open("./backup.csv", "w", encoding='GBK')
        f.write('漫画名,最后更新时间\n')
        for line in manga_list:
            f.write('%s,%s\n' % (line["comic"]["name"],
                    line["comic"]["datetime_updated"]))
        f.close()
        f = open("./backup.txt", "w", encoding='utf-8')
        # 输出txt
        print("正在输出到程序目录下的backup.txt....")
        for line in manga_list:
            f.write('%s\n' % line["comic"]["name"])
        f.close()
        print(
            "[italic green]写入完成！[/italic green][italic yellow](SCV请用Excel打开，编码为GBK)[/italic yellow]")
        welcome()
    else:
        # *报告远程服务器无法连接的状态码
        print("[italic yellow]服务器似乎[/italic yellow][italic red]无法连接[/italic red][italic yellow]了qwq[/italic yellow]\n")
        print("[italic yellow]返回的状态码是：%d[/italic yellow]" %
              response.status_code)
        sys.exit(0)


def welcome():
    if not CmdMode:
        is_search = Prompt.ask(
            "您是想搜索还是查看您的收藏？[italic yellow](0:导出收藏,1:搜索,2:收藏  默认1)[/italic yellow]", choices=["0", "1", "2"], default="1")
        if is_search == "2":
            manga_collection(0)
        elif is_search == "0":
            manga_collection_backup()
        manga_name = input("请输入漫画名称:")
        manga_search(manga_name)
    else:
        global get_list_name
        get_list_name = args.MangaPath


def main():
    requests.packages.urllib3.disable_warnings()
    get_settings()
    welcome()
    manga_chapter_list()
    manga_download()


if __name__ == "__main__":
    main()
