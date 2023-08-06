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
                # url = f'https://api.wqwlkj.cn/wqwlapi/chatgpt.php?msg={question.strip()}&type=json'
                # url = f"http://www.emmapi.com/chatgpt?text={question.strip()}"
                url = f"https://v1.apigpt.cn/?q={question.strip()}"
                print('AI问题思考中=====')
                res = requests.get(url, timeout=25)
                res_json = dict()
                try:
                    res_json = json.loads(res.text)
                    print(f'AI问题回答:{res_json.get("ChatGPT_Answer")}')
                    if res_json.get('info'):
                        del res_json['info']
                except JSONDecodeError:
                    return {'code': 0, 'error': res_json.get('ChatGPT_Answer')}
                return {'code': 1, 'text': res_json.get('ChatGPT_Answer')}

            return ask_q()
        except ReadTimeout:
            return {'code': 0, 'error': 'ReadTimeout,please retry'}


if __name__ == '__main__':
    # r = FreeChatgpt.ask(question='帮我优化这段话:pandas快速替换所有字符中的特殊字符')
    # print(r)
    # t = FreeChatgpt.ask(question='中国文化的特点是什么？')
    # print(t)
    q = 'This thing is bright! I look for missing things as part of my job, and this thing is the brightest pocket flashlight that I have found. It has been a life saver. Well worth the money. The focus took a minute to figure out, but definitely a win!情感分析是正面还是负面?'
    s = FreeChatgpt.ask(question=q)
    print(s)

