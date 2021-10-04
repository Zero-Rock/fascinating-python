"""
@Author : Zero
@Time   : 2021/9/22 18:58:24
"""
from demo.junjin.config import getConfig
from requests import get, post
from os import getenv

cookie = getenv('COOKIE')


class JunJin:
    def __init__(self):
        is_check_in = JunJin.getTodayStatus()
        if is_check_in is not True:
            JunJin.checkIn()
        else:
            print("今日已参与签到")
        JunJin.showHand()

    @staticmethod
    def request(method, url):
        fetch = get if method == 'get' else post
        headers = {
            'Cookie': cookie
        }
        res = fetch(url=url, headers=headers)
        return res.json()

    @staticmethod
    def getTodayStatus():
        (url, method) = getConfig('todayStatus')
        res = JunJin.request(method, url)
        if res.get("err_no") != 0:
            raise Exception('查询今日签到状态：失败，{}'.format(res.get("err_msg")))

        return res.get("data")

    @staticmethod
    def getOreCount():
        (url, method) = getConfig('oreCount')
        res = JunJin.request(method, url)
        if res.get("err_no") != 0:
            raise Exception('查询矿石数量：失败，{}'.format(res.get("err_msg")))

        return res.get("data")

    @staticmethod
    def checkIn():
        (url, method) = getConfig('checkIn')
        res = JunJin.request(method, url)
        if res.get("err_no") != 0:
            raise Exception('签到：失败，{}'.format(res.get("err_msg")))
        else:
            print("签到成功！当前积分：{}".format(res.get("data").get("sum_point")))
            JunJin.draw()

    @staticmethod
    def draw():
        count = 0
        (url, method) = getConfig('drawLottery')
        res = JunJin.request(method, url)
        data = res.get("data")
        lottery_name = data.get("lottery_name")
        lottery_id = data.get("lottery_id")
        lottery_type = data.get("lottery_type")
        if lottery_type == 1:
            count = 66
        print("抽奖ID：{}, 获得: {}".format(lottery_id, lottery_name))
        return count

    @staticmethod
    def showHand():
        count = JunJin.getOreCount()
        while count > 200:
            count = count - 200
            count = count + JunJin.draw()
        else:
            print("矿石数量不够了，明天再试哦, 剩余矿石: {}".format(count))


JunJin()
