#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
import os
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(funcName)s[line:%(lineno)d]%(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)


path = os.path.dirname(os.path.abspath(__file__))
print(path)
try:
    reload(sys)
    sys.path.append(path)
    sys.setdefaultencoding('utf-8')
except:
    pass

from textrank import TextRankforQuery

texts = ['算法基于textrank，有一些调整，目前使用效果还好，后续有改动的话再说，目前就这样了。主要用法就是下面这么用的，更进一步的请阅读源码，同时也可以自己修改源码来调整使用效果.加油!', '我长度小于10', '我是一串乱七八糟的词，没有, 的地的的的的的东东的的的的', '']

print('--------------------')
print("默认只处理词长大于等于10的句子, 小于该长度的，分数会被置为0")
tr4w = TextRankforQuery()

for text in texts:
    # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    # tr4w.analyze(text=text, lower=False, window=10,
                 # vertex_source='all_filters',
                 # edge_source='no_stop_words',
                 # allow_word_num=10)
    # 长查询window暂定为10，短查询范围为2-5之间
    print('关键词：')
    txt = tr4w.getKeywordsDict(text)
    for item in txt:
        print(item, txt[item])

print('--------------------')
print("对任何长度的句子都做处理")
tr4w = TextRankforQuery(allow_word_num=1)
for text in texts:
    print('关键词：')
    txt = tr4w.getKeywordsDict(text)
    for item in txt:
        print(item, txt[item])
