#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests


def search(
        keyword: str,
        page: int = 1,
        page_size: int = 10
):
    """

    :param keyword:
    :param page:
    :param page_size:
    :return:
    """
    offset = (page - 1) * page_size
    url = f'https://www.ixigua.com/api/searchv2/complex/{keyword}/{offset}'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Host": "www.ixigua.com",
        "Referer": "https://www.ixigua.com/search",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )
