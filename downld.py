#!/usr/bin/env python2
# coding=utf-8
import requests
from bs4 import BeautifulSoup as Bs4
import time

# Yaowen Xu
# 2021年2月1日 15点49分

head_url = "http://www.winkawaks.org/roms/full-rom-list.htm"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

print("roms-download: " + head_url)

# https://www.winkawaks.org/roms/full-rom-list.htm

zip_list = []
o_file = open('download.sh', 'w')

# construct download script
o_file.writelines("#!/bin/bash\n")
o_file.writelines("set -x\n")
o_file.writelines("# auto gen by yaowenxu\n")
o_file.writelines("\n")
o_file.writelines("PA=`pwd`\n")
o_file.writelines("cd $PA/roms\n")
o_file.writelines("\n")


def get_index_url():
    list_href = []
    reaponse = requests.get(head_url, headers=headers)
    baseurl = head_url[0:head_url.rindex('/')] + '/'
    # print(baseurl)
    soup = Bs4(reaponse.text, "lxml")
    urls = soup.find_all("a")
    # print(urls)
    if urls:
        for url in urls:
            url_href = url.get("href")
            if url_href:
                if url_href[0] == "/":
                    continue
                full_url_1 = baseurl + str(url_href)
                list_href.append(full_url_1)

    out_url = list(set(list_href))
    return out_url

# https://www.winkawaks.org/roms/neogeo/garoup.htm


def get_download_url(urllist):
    url_list = []
    for url in urllist:
        print("deal-with: " + url)
        baseurl_2 = url[0:url.rindex('/')] + '/'
        response = requests.get(url, headers=headers)
        soup = Bs4(response.text, "lxml")
        urls = soup.find_all("a")

        # deal with urls
        if urls:
            for url2 in urls:
                url2_1 = url2.get("href")
                if url2_1:

                    # check for index page
                    if url2_1[0] == "/":
                        continue
                    full_url_2 = baseurl_2 + str(url2_1)

                    # check for duplication
                    if full_url_2 in urllist:
                        continue

                    url_list.append(full_url_2)
                    print("get-download-link: " + full_url_2)

                    # Get the download link of the zip file and output it to the file;
                    get_zip_file_url(full_url_2)
        # break
    out_url = list(set(url_list))
    return out_url


def get_zip_file_url(url):
    baseurl_3 = url[0:url.rindex('/')] + '/'
    response = requests.get(url, headers=headers)
    soup = Bs4(response.text, "lxml")
    urls = soup.find_all("a")

    # deal with urls
    if urls:
        for url3 in urls:
            url3_1 = url3.get("href")
            if url3_1:
                linksuffix = url3_1[len(url3_1)-4:len(url3_1)]
                if linksuffix == ".zip":
                    ziplink_out = str(url3_1)
                    print(ziplink_out)
                    zip_list.append(ziplink_out)
                    print("get-zipfile-link: " + ziplink_out)
                    o_file.writelines("curl -OL " + ziplink_out + "\n")
    time.sleep(0.1)
    return


if __name__ == "__main__":
    urllist = get_index_url()
    print("index link numbers: "+str(len(urllist)))
    downlist = get_download_url(urllist)
    print("download link numbers: "+str(len(downlist)))
    zip_list = list(set(zip_list))
    print("zipfile numbers: "+str(len(zip_list)))

    o_file.writelines("\n")
    o_file.writelines("# Zip File Numbers: "+str(len(zip_list)))
    o_file.writelines("\n")
    o_file.close()
