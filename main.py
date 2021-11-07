import api


def test():
    url_list = [
        "http://music.163.com/playlist?id=5193023281",
        "http://music.163.com/song?id=1433957694",
        "http://music.163.com/playlist?id=2792595434",
        "http://music.163.com/song?id=1890025868",
        "http://music.163.com/playlist?id=2965734634",
        "http://music.163.com/song?id=1493816591",
        "http://music.163.com/playlist?id=2047012641",
        "http://music.163.com/song?id=1498778223",
        "http://music.163.com/playlist?id=5333919927",
        "http://music.163.com/song?id=1399694841"
    ]
    nca = api.NetCloudApi()
    nca.get_cover(url_list=url_list)


if __name__ == '__main__':
    test()
