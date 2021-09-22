"""
@Author : Zero
@Time   : 2021/9/22 19:01:06
"""

BASE_URL = "https://api.juejin.cn";
API_MAP = {
    "todayStatus": {
        'url': "/growth_api/v1/get_today_status",
        "method": "get"
    },
    "checkIn": {
        "url": "/growth_api/v1/check_in",
        "method": "post"
    },
    "lotteryConfig": {
        "url": "growth_api/v1/lottery_config/get",
        "method": "post"
    },
    "drawLottery": {
        "url": "/growth_api/v1/lottery/draw",
        "method": "post"
    },
    "oreCount": {
        "url": "/growth_api/v1/get_cur_point",
        "method": "get"
    }
}


def getConfig(key):
    temp = API_MAP.get(key);
    return ("{}{}".format(BASE_URL, temp.get("url")), temp.get('method'))
