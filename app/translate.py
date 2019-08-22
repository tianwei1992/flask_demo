import random
import json
from urllib.parse import quote
from hashlib import md5

import requests
from flask_babel import _

from app import app


def translate(q, from_lang, to_lang):
    """调用百度翻译接口"""
    if 'BAIDU_TRANSLATOR_APPID' not in app.config or \
            not app.config['BAIDU_TRANSLATOR_APPID'] or \
            'BAIDU_TRANSLATOR_SECRETKEY' not in app.config or \
            not app.config['BAIDU_TRANSLATOR_SECRETKEY']:
        return _('Error: the translation service is not configured.')

    appid = app.config['BAIDU_TRANSLATOR_APPID']
    secretKey = app.config['BAIDU_TRANSLATOR_SECRETKEY']

    salt = random.randint(32768, 65536)
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    
    covery_dic = {'es': 'spa',
                    }
    if to_lang in covery_dic:
        to_lang = covery_dic[to_lang]

    sign = appid+q+str(salt)+secretKey
    m1 = md5()
    m1.update(sign.encode('utf8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+quote(q)+'&from='+from_lang+'&to='+to_lang+'&salt='+str(salt)+'&sign='+sign
 
    try:
        r = requests.get(myurl)
        return json.loads(r.content.decode('utf-8-sig'))
    except Exception as e:
        return _('Error: the translation service failed.')


if __name__ == "__main__":
    result = tranlate('apple', 'en', 'zh') 
    print(result)
