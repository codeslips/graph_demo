# -*- coding: utf-8 -*-
"""Media Crawl models package."""

from .bilibili import (
    BilibiliVideo,
    BilibiliVideoComment,
    BilibiliUpInfo,
    BilibiliContactInfo,
    BilibiliUpDynamic,
)
from .douyin import DouyinAweme, DouyinAwemeComment, DyCreator
from .kuaishou import KuaishouVideo, KuaishouVideoComment
from .weibo import WeiboNote, WeiboNoteComment, WeiboCreator
from .xhs import XhsCreator, XhsNote, XhsNoteComment
from .tieba import TiebaNote, TiebaComment, TiebaCreator
from .zhihu import ZhihuContent, ZhihuComment, ZhihuCreator
from .report import AnalysisReport

__all__ = [
    # Bilibili
    "BilibiliVideo",
    "BilibiliVideoComment",
    "BilibiliUpInfo",
    "BilibiliContactInfo",
    "BilibiliUpDynamic",
    # Douyin
    "DouyinAweme",
    "DouyinAwemeComment",
    "DyCreator",
    # Kuaishou
    "KuaishouVideo",
    "KuaishouVideoComment",
    # Weibo
    "WeiboNote",
    "WeiboNoteComment",
    "WeiboCreator",
    # Xiaohongshu
    "XhsCreator",
    "XhsNote",
    "XhsNoteComment",
    # Tieba
    "TiebaNote",
    "TiebaComment",
    "TiebaCreator",
    # Zhihu
    "ZhihuContent",
    "ZhihuComment",
    "ZhihuCreator",
    # Report
    "AnalysisReport",
]

