from lxml import etree
import showlog
import json
import re
from lazysdk import lazyproxies
import requests


def get_html_with_proxies(
        url,
        proxies=None
):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }
    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxies,
        timeout=10,
        verify=False
    )
    return response.text


def clean_ytInitialPlayerResponse(ytInitialPlayerResponse_json):
    temp_res_dict = dict()

    responseContext = ytInitialPlayerResponse_json.get('responseContext')  # 非关键
    playabilityStatus = ytInitialPlayerResponse_json.get('playabilityStatus')  # 非关键
    streamingData = ytInitialPlayerResponse_json.get('streamingData')  # 视频流信息，可以供下载视频使用
    playerAds = ytInitialPlayerResponse_json.get('playerAds')  # 非关键
    playbackTracking = ytInitialPlayerResponse_json.get('playbackTracking')  # 非关键
    captions = ytInitialPlayerResponse_json.get('captions')  # 视频字幕信息，可下载字幕内容
    videoDetails = ytInitialPlayerResponse_json.get('videoDetails')  # 视频基本信息，重要，含有浏览次数
    playerConfig = ytInitialPlayerResponse_json.get('playerConfig')  # 非关键
    storyboards = ytInitialPlayerResponse_json.get('storyboards')  # 非关键
    microformat = ytInitialPlayerResponse_json.get('microformat')  # 含有分类信息和视频信息，有用
    trackingParams = ytInitialPlayerResponse_json.get('trackingParams')  # 非必要
    attestation = ytInitialPlayerResponse_json.get('attestation')  # 非必要
    videoQualityPromoSupportedRenderers = ytInitialPlayerResponse_json.get('videoQualityPromoSupportedRenderers')  # 非必要 支持/帮助信息
    adPlacements = ytInitialPlayerResponse_json.get('adPlacements')  # 非必要，广告内容

    temp_res_dict['author'] = videoDetails.get('author')  # 作者
    temp_res_dict['channelId'] = videoDetails.get('channelId')
    temp_res_dict['lengthSeconds'] = videoDetails.get('lengthSeconds')  # 时常：秒
    temp_res_dict['shortDescription'] = videoDetails.get('shortDescription')  # 简介
    temp_res_dict['title'] = videoDetails.get('title')  # 标题
    temp_res_dict['videoId'] = videoDetails.get('videoId')  # 视频id
    temp_res_dict['viewCount'] = videoDetails.get('viewCount')  # 观看人数

    temp_res_dict['publishDate'] = microformat.get('playerMicroformatRenderer').get('publishDate')  # 发布时间
    temp_res_dict['uploadDate'] = microformat.get('playerMicroformatRenderer').get('uploadDate')  # 上传时间
    temp_res_dict['category'] = microformat.get('playerMicroformatRenderer').get('category')  # 分类
    temp_res_dict['ownerProfileUrl'] = microformat.get('playerMicroformatRenderer').get('ownerProfileUrl')  # 作者主页

    temp_res_dict['streamingData'] = streamingData
    temp_res_dict['thumbnails'] = videoDetails.get('thumbnail').get('thumbnails')  # 封面图，默认下载"height": 188,"width": 336
    temp_res_dict['captions'] = captions  # 字幕信息captionTracks.baseUrl是基础，加上&fmt=json3&xorb=2&xobt=3&xovt=3&tlang=zh-Hans可以翻译为简体中文

    return temp_res_dict


def initial_player_response(
        url: str,
        proxies=None,
):
    showlog.info('正在获取页面源码...')
    page_source_code = get_html_with_proxies(
        url=url,
        proxies=proxies
    )  # 页面源码
    showlog.info(':) 获取成功')

    showlog.info('正在解析源码...')
    tree = etree.HTML(page_source_code, etree.HTMLParser())
    scripts = tree.xpath('/html/body/script/text()')
    for script in scripts:
        if 'var ytInitialPlayerResponse = ' in script:
            showlog.info('找到关键参数 ytInitialPlayerResponse 继续解析...')
            ytInitialPlayerResponse = re.findall('var ytInitialPlayerResponse = (.*?);var ', script, re.S)[0]
            ytInitialPlayerResponse_json = json.loads(ytInitialPlayerResponse)
            return ytInitialPlayerResponse_json
