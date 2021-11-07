import os
import re
import time
import urllib.parse

import requests
import json

BASE_URL = "https://music.163.com/"
METHOD_POST = "POST"
METHOD_GET = "GET"


def save_img(img_url: str, img_name: str):
    """
    保存图片

    :param img_url:
    :param img_name:
    """

    # 过滤非法字符
    img_name = re.sub('[\/:*?"<>|]', '', img_name)

    print(f"正在保存: {img_name}.jpg")

    if not os.path.exists("NetCloudCover"):
        os.mkdir("NetCloudCover")

    img_response = requests.get(img_url)

    file = open(f"NetCloudCover\\{img_name}.jpg", "wb")
    file.write(img_response.content)
    file.close()
    print(f"保存完成: {img_name}.jpg\n")


def request(method: str, url: str, data=None):
    """
    处理请求

    :param method: 请求方法
    :param url: 请求路径
    :param data:   post数据
    :return: json
    """
    response = requests.request(method=method, url=url, data=data)

    data = ""
    if response.status_code == 200:
        data = response.text

    return json.loads(data)


def parse_query(query: str):
    """
    对url参数进行解析
    :param query:
    :return:
    """

    params_dict = {}
    for entry in query.split("&"):
        items = entry.split("=")
        params_dict.update({items[0]: items[1]})

    return params_dict


# def process_url(self, url_str: str, path: str, param_names: list):
#     """
#     处理url
#
#     :param url_str:
#     :param param_names:
#     :param path:
#     :return:
#     """
#     if path.startswith("http"):
#         return path
#     else:
#         url = urllib.parse.urlparse(BASE_URL)
#         url.path = path
#
#         # 获取参数
#         param_dict = self.parse_query(url_str=url_str)
#
#         for name in param_names:
#             url.params = {name, param_dict[name]}
#
#         return url.__str__()

class NetCloudApi(object):
    song_ids = []
    song_list_ids = []

    def get_cover(self, url_list: list):
        """
        获取 歌单/歌曲 封面

        :param url_list: 歌单、歌曲链接
        """
        self.sort(url_list)
        self.song()
        self.song_list()

    def sort(self, url_list: list):
        """
        对链接进行分类

        :param url_list:
        """
        for url in url_list:
            temp = urllib.parse.urlparse(url)
            path = temp.path
            if path.__eq__("/song"):
                self.song_ids.append(parse_query(temp.query)["id"])
            elif path.__eq__("/playlist"):
                self.song_list_ids.append(parse_query(temp.query)["id"])
            else:
                pass

    def song(self):
        """
        获取歌单详细数据
        api: https://music.163.com/api/v3/song/detail

        请求方式: POST
        """
        url_str = BASE_URL + "api/v3/song/detail"

        # 拼接form数据
        form = "["
        for song_id in self.song_ids:
            form = form + f'{{"id": {song_id}}},'

        form = form[:-1] + "]"

        # 获取所有歌单封面img
        json_data = request(METHOD_POST, url=url_str, data={"c": form})

        # 获取playlist对象
        songs = json_data['songs']

        for song in songs:
            img_url = song["al"]["picUrl"]
            img_name = song["name"] + "_" + str(song["id"])

            # 保存图片
            save_img(img_url=img_url, img_name=img_name)

            # 防止封IP
            time.sleep(1.5)

        # 清除id
        self.song_ids.clear()

    def song_list(self):
        """
        获取歌单详细数据
        api: https://music.163.com/api/v6/playlist/detail

        请求方式: POST
        """
        url_str = BASE_URL + "api/v6/playlist/detail"

        # 获取所有歌单封面img
        for param_id in self.song_list_ids:
            json_data = request(METHOD_POST, url=url_str, data={"id": param_id})

            # 获取playlist对象
            play_list = json_data['playlist']
            img_url = play_list["coverImgUrl"]
            img_name = play_list["name"] + "_" + play_list["coverImgId_str"]

            # 保存图片
            save_img(img_url=img_url, img_name=img_name)

            # 防止封IP
            time.sleep(1.5)

        # 清除id
        self.song_list_ids.clear()
