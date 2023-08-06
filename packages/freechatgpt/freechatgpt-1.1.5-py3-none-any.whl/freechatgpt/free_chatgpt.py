# -*- coding: utf-8 -*-
# @Time    : 2023/3/2 10:42
# @Author  : abo123456789
# @Desc    : free_chatgpt.py
import json
from json import JSONDecodeError

import requests
import retrying
from requests import ReadTimeout


def retry_if_timeout_error(excep):
    return isinstance(excep, ReadTimeout)


class FreeChatgpt(object):

    @staticmethod
    def ask(question: str):
        try:
            @retrying.retry(stop_max_attempt_number=4, stop_max_delay=100000,
                            wait_fixed=1500, retry_on_exception=retry_if_timeout_error)
            def ask_q():
                if not question or not question.strip():
                    return {'code': 0, 'error': 'question is null!'}
                url = f'https://api.wqwlkj.cn/wqwlapi/chatgpt.php?msg={question.strip()}&type=json'
                print('AI问题思考中=====')
                res = requests.get(url, timeout=25)
                print(f'AI问题回答:{res.text}')
                try:
                    res_json = json.loads(res.text)
                    del res_json['info']
                except JSONDecodeError:
                    return {'code': 0, 'error': res.text}
                return res_json

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


if __name__ == '__main__':
    # r = FreeChatgpt.ask(question='帮我创作一个广告视频宣传跨境选品SAAS？')
    # print(r)
    # t = FreeChatgpt.ask(question='帮我创作一个广告视频宣传华为mate手机卖点？')
    # print(t)
    q = 'This thing is bright! I look for missing things as part of my job, and this thing is the brightest pocket flashlight that I have found. It has been a life saver. Well worth the money. The focus took a minute to figure out, but definitely a win!情感分析是正面还是负面?'
    s = FreeChatgpt.ask(question=q)
    print(s)

