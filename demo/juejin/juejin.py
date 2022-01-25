"""
@Author : Zero
@Time   : 2021/9/22 18:58:24
"""
import re
from os import getenv
from time import strftime, localtime

from requests import get, post

from demo.juejin.config import getConfig

cookie = getenv('COOKIE')


def log(log_str, level="info"):
    time_str = strftime("%Y-%m-%d %H:%M:%S", localtime())
    print(f"{time_str} [{level.upper()}] {log_str}")


class JunJin:
    def __init__(self):
        is_check_in = get_today_status()
        if is_check_in is not True:
            check_in()
        else:
            log("今日已参与签到")
        show_hand()


def request(method, url):
    fetch = get if method == 'get' else post
    headers = {
        'Cookie': cookie
    }
    res = fetch(url=url, headers=headers)
    return res.json()


def get_today_status():
    (url, method) = getConfig('todayStatus')
    res = request(method, url)
    if res.get("err_no") != 0:
        raise Exception('查询今日签到状态：失败，{}'.format(res.get("err_msg")))

    return res.get("data")


def draw(is_free):
    action_type = '免费抽奖' if is_free else '有偿抽奖'
    count = 0
    (url, method) = getConfig('drawLottery')
    res = request(method, url)
    data = res.get("data")
    lottery_name = data.get("lottery_name")
    lottery_id = data.get("lottery_id")
    lottery_type = data.get("lottery_type")
    if lottery_type == 1:
        lottery_count = re.findall("\d+", lottery_name)[0]
        count = int(lottery_count)
    log("【{}】抽奖ID：{}, 获得: {}".format(action_type, lottery_id, lottery_name))
    return count


def check_in():
    (url, method) = getConfig('checkIn')
    res = request(method, url)
    if res.get("err_no") != 0:
        raise Exception('【签到】失败!，{}'.format(res.get("err_msg")))
    else:
        log("【签到】成功！当前矿石：{}".format(res.get("data").get("sum_point")))
        draw('free')


def get_ore_count():
    (url, method) = getConfig('oreCount')
    res = request(method, url)
    if res.get("err_no") != 0:
        raise Exception('【查询矿石数量】失败，{}'.format(res.get("err_msg")))

    return res.get("data")


def show_hand():
    count = get_ore_count()
    while count > 200:
        count = count - 200
        count = count + draw(False)
    else:
        log("矿石数量不够了，明天再试哦, 剩余矿石: {}".format(count))


if __name__ == "__main__":
    JunJin()
