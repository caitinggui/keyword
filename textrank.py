#-*- encoding:utf-8 -*-

from __future__ import (absolute_import, division,
                        unicode_literals)
import logging

from . import util
from .segmentation import Segmentation

logger = logging.getLogger(__name__)


class TextRankforQuery(object):

    def __init__(self, keyword_num=10, min_word_len=2, if_long_text=True,
                 allow_word_num=10,
                 allow_speech_tags=util.allow_speech_tags,
                 delimiters=util.sentence_delimiters):
        """
        关键词提取
        Args:
            window     --  窗口大小，int，用来构造单词之间的边。默认值为2。
            lower      --  是否将文本转换为小写。默认为False。
            vertex_source   --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来构造pagerank对应的图中的节点。
                                默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。关键词也来自`vertex_source`。
            edge_source     --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来构造pagerank对应的图中的节点之间的边。
                                默认值为`'no_stop_words'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。边的构造要结合`window`参数。
            allow_word_num: 如果传入的句子词数小于某个值，就不进行关键字提取, 为1表示所有句子均提取
            keyword_num : 返回的关键词数
            sentence_delimiters       --  默认值是`?!;？！。；…\n`，用来将文本拆分为句子。
            allow_speech_tags: 允许保留的词性
        Return:
            如果经过处理，则返回关键词列表，否则原句返回
        """
        self.window = 10 if if_long_text else 2  # 如果是长文本就定为10，短文本在2-5之间
        self.lower = False
        self.vertex_source = "all_filters"
        self.edge_source = "no_stop_words"
        self.keyword_num = keyword_num  # 返回的关键词数
        self.allow_word_num = allow_word_num
        self.min_word_len = min_word_len  # 词的最小长度
        self.seg = Segmentation(allow_speech_tags=allow_speech_tags,
                                delimiters=delimiters)
        self.options = ['no_filter', 'no_stop_words', 'all_filters']

    def analyze(self, text):
        """分析文本
        Args:
            text: 文本内容，字符串。
        """

        self.word_index = {}
        self.index_word = {}
        self.keywords = []

        seg_result = self.seg.segment(text=text, lower=self.lower)
        # 不需要提取关键词就返回原句各种分词后的结果
        if len(seg_result.all_words) < self.allow_word_num:
            return seg_result

        # words_no_filter:对sentences中每个句子分词而得到的两级列表。
        # words_no_stop_words:去掉words_no_filter中的停止词而得到的两级列表。
        # words_all_filters:保留words_no_stop_words中指定词性的单词而得到的两级列表。
        # logger.debug('sentences in: %s', '||'.join(seg_result.sentences))
        # logger.debug('words_no_filter: %s', seg_result.words_no_filter)
        # logger.debug('words_no_stop_words: %s', seg_result.words_no_stop_words)
        # logger.debug('words_all_filters: %s', seg_result.words_all_filters)

        if self.vertex_source in self.options:
            _vertex_source = seg_result['words_' + self.vertex_source]
        else:
            _vertex_source = seg_result['words_all_filters']

        if self.edge_source in self.options:
            _edge_source = seg_result['words_' + self.edge_source]
        else:
            _edge_source = seg_result['words_no_stop_words']

        # 排序后的列表，元素为字典[{"word": str, "weight": float}]
        keywords = util.sort_words(
            _vertex_source, _edge_source, window=self.window)
        return keywords

    def topNKeywordsDict(self, keywords, keyword_num):
        """获取最重要的num个长度大于等于word_min_len的关键词。
        Args:
            keywords: 排序后的词，元素为字典[{"word": str, "weight": float}]
            keyword_num: 提取的关键词数
        Return:
            排名前N的词，格式为字典:{str: float}
        """
        keyword = {}
        count = 0
        for item in keywords:
            if count >= keyword_num:
                break
            if len(item.word) >= self.min_word_len:
                keyword[item.word] = item.weight
                count += 1
        return keyword

    def getKeywordsList(self, text, keyword_num=None):
        """
        返回的都是列表
        """
        if not text:
            return ''
        keyword_num = keyword_num if keyword_num else self.keyword_num
        keyword = self.getKeywordsDict(text, keyword_num)
        result = keyword.keys()
        logger.info("keyword in textrank: %s", result)
        return result

    def getKeywordsDict(self, text, keyword_num=None):
        """提取关键字后的结果为dict，未提取则是去除停用词的列表"""
        logger.debug("textrank text params: %s", text)
        if not text:
            return {}
        keyword_num = keyword_num if keyword_num else self.keyword_num
        keywords = self.analyze(text)
        # 提取关键字后是包含字典的列表
        if isinstance(keywords, dict):
            result = {}
            logger.info("text is too short to extract keyword")
            for k in keywords.words:
                result[k] = 0
            return result
        result = self.topNKeywordsDict(keywords, keyword_num)
        logger.info("keyword in textrank: %s", result)
        return result


if __name__ == '__main__':
    pass
