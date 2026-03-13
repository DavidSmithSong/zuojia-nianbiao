#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作家年表 - 数据初始化脚本
Author: 宋化富
Project: 交互式作家时间线网站
Created: 2026-03-03
"""

import json
import os
import sys

AUTHORS = [

    # ---- 中国作家 ----

    {
        "name": "Lu Xun",
        "name_zh": "鲁迅",
        "birth": 1881,
        "death": 1936,
        "nationality": "中国",
        "bio_zh": (
            "原名周树人，浙江绍兴人，中国现代文学奠基人。"
            "弃医从文，以《狂人日记》开创白话小说先河。"
            "其杂文犀利深刻，揭露封建礼教'吃人'本质，"
            "被誉为'民族魂'，深刻影响了整个二十世纪中国文学走向。"
        ),
        "major_works": [
            {"title": "A Madman's Diary",             "title_zh": "狂人日记",  "year": 1918},
            {"title": "The True Story of Ah Q",       "title_zh": "阿Q正传",   "year": 1921},
            {"title": "Call to Arms",                  "title_zh": "呐喊",      "year": 1923},
            {"title": "Wandering",                     "title_zh": "彷徨",      "year": 1926},
            {"title": "Dawn Blossoms Plucked at Dusk", "title_zh": "朝花夕拾",  "year": 1928},
        ],
        "key_events": [
            {"year": 1898, "event_zh": "赴南京求学，接触西方自然科学"},
            {"year": 1902, "event_zh": "赴日本留学，先学医后转向文学"},
            {"year": 1918, "event_zh": "以'鲁迅'为笔名发表《狂人日记》，开创白话文小说"},
            {"year": 1930, "event_zh": "参与发起中国左翼作家联盟"},
            {"year": 1936, "event_zh": "因肺结核病逝于上海，举国哀悼"},
        ],
    },

    {
        "name": "Zhang Ailing",
        "name_zh": "张爱玲",
        "birth": 1920,
        "death": 1995,
        "nationality": "中国",
        "bio_zh": (
            "上海名门之后，以精准冷峻的笔触描绘乱世中的男女情欲与人性幽微。"
            "《倾城之恋》《金锁记》奠定其'祖师奶奶'地位。"
            "晚年旅居美国，深居简出，其作品在二十世纪末重新引发研究热潮。"
        ),
        "major_works": [
            {"title": "Love in a Fallen City", "title_zh": "倾城之恋",  "year": 1943},
            {"title": "The Golden Cangue",     "title_zh": "金锁记",    "year": 1943},
            {"title": "Romances",              "title_zh": "传奇",      "year": 1944},
            {"title": "The Rice-Sprout Song",  "title_zh": "秧歌",      "year": 1954},
            {"title": "Lust, Caution",         "title_zh": "色，戒",    "year": 1979},
        ],
        "key_events": [
            {"year": 1920, "event_zh": "生于上海，祖父为晚清名臣李鸿章外孙"},
            {"year": 1939, "event_zh": "考入香港大学文学院"},
            {"year": 1943, "event_zh": "《倾城之恋》《金锁记》相继在上海《杂志》发表，声名大噪"},
            {"year": 1952, "event_zh": "移居香港，开始为美国新闻处撰写反共小说"},
            {"year": 1955, "event_zh": "移居美国，后与剧作家赖雅结婚"},
            {"year": 1995, "event_zh": "孤独辞世于洛杉矶公寓，享年74岁"},
        ],
    },

    {
        "name": "Shen Congwen",
        "name_zh": "沈从文",
        "birth": 1902,
        "death": 1988,
        "nationality": "中国",
        "bio_zh": (
            "湖南凤凰人，以湘西世界为素材构建独特的文学乌托邦。"
            "《边城》以清丽文笔呈现湘西人性之美，被誉为'田园牧歌'。"
            "1949年后转型为文物研究者，在中国古代服饰研究领域同样成就卓著。"
        ),
        "major_works": [
            {"title": "Border Town",     "title_zh": "边城",   "year": 1934},
            {"title": "The Long River",  "title_zh": "长河",   "year": 1945},
            {"title": "Autobiography of Shen Congwen", "title_zh": "从文自传", "year": 1934},
            {"title": "A Study of Ancient Chinese Costumes", "title_zh": "中国古代服饰研究", "year": 1981},
        ],
        "key_events": [
            {"year": 1902, "event_zh": "生于湖南凤凰，苗汉土家族混血"},
            {"year": 1922, "event_zh": "只身闯北京，开始自学写作"},
            {"year": 1930, "event_zh": "执教武汉大学、青岛大学"},
            {"year": 1934, "event_zh": "《边城》发表，奠定文学史地位"},
            {"year": 1949, "event_zh": "政治压力下停止文学创作，转入历史博物馆研究文物"},
            {"year": 1988, "event_zh": "逝于北京；诺贝尔文学奖委员会曾将其列为候选人"},
        ],
    },

    {
        "name": "Yu Hua",
        "name_zh": "余华",
        "birth": 1960,
        "death": None,
        "nationality": "中国",
        "bio_zh": (
            "浙江海盐人，先锋文学代表人物，后转向写实主义叙事。"
            "《活着》以平静克制的语言讲述极端苦难，被译为数十种语言。"
            "其作品以黑色幽默解构历史暴力，在国际文坛享有高度声誉。"
        ),
        "major_works": [
            {"title": "To Live",    "title_zh": "活着",       "year": 1992},
            {"title": "Chronicle of a Blood Merchant", "title_zh": "许三观卖血记", "year": 1995},
            {"title": "Brothers",  "title_zh": "兄弟",        "year": 2005},
            {"title": "The Seventh Day", "title_zh": "第七天", "year": 2013},
            {"title": "Wencheng",  "title_zh": "文城",        "year": 2021},
        ],
        "key_events": [
            {"year": 1960, "event_zh": "生于浙江杭州，父亲是外科医生"},
            {"year": 1983, "event_zh": "发表处女作，开始先锋文学创作"},
            {"year": 1992, "event_zh": "《活着》出版，标志风格转向写实"},
            {"year": 1994, "event_zh": "张艺谋改编《活着》获戛纳评审团大奖"},
            {"year": 2008, "event_zh": "《兄弟》英译本在西方引发广泛关注"},
        ],
    },

    {
        "name": "Mo Yan",
        "name_zh": "莫言",
        "birth": 1955,
        "death": None,
        "nationality": "中国",
        "bio_zh": (
            "原名管谟业，山东高密人，以魔幻现实主义手法重构中国乡土历史。"
            "《红高粱家族》将家族史诗与民间传奇融为一体。"
            "2012年获诺贝尔文学奖，是首位获此殊荣的中国籍作家。"
        ),
        "major_works": [
            {"title": "Red Sorghum Clan",         "title_zh": "红高粱家族",  "year": 1987},
            {"title": "The Garlic Ballads",       "title_zh": "天堂蒜薹之歌","year": 1988},
            {"title": "Big Breasts and Wide Hips","title_zh": "丰乳肥臀",    "year": 1995},
            {"title": "Life and Death are Wearing Me Out", "title_zh": "生死疲劳", "year": 2006},
            {"title": "Frog",                     "title_zh": "蛙",          "year": 2009},
        ],
        "key_events": [
            {"year": 1955, "event_zh": "生于山东高密县，文革期间辍学务农"},
            {"year": 1976, "event_zh": "参军入伍，开始系统阅读与写作"},
            {"year": 1987, "event_zh": "张艺谋将《红高粱》搬上银幕，获柏林金熊奖"},
            {"year": 2012, "event_zh": "获诺贝尔文学奖，成为首位中国籍得主"},
        ],
    },

    {
        "name": "Ba Jin",
        "name_zh": "巴金",
        "birth": 1904,
        "death": 2005,
        "nationality": "中国",
        "bio_zh": (
            "原名李尧棠，四川成都人，中国现代文学巨匠。"
            "《家》《春》《秋》激流三部曲深刻批判封建大家族制度，"
            "晚年以《随想录》进行彻底的自我反省，"
            "成为中国知识分子良知的象征。"
        ),
        "major_works": [
            {"title": "Family",         "title_zh": "家",    "year": 1931},
            {"title": "Spring",         "title_zh": "春",    "year": 1938},
            {"title": "Autumn",         "title_zh": "秋",    "year": 1940},
            {"title": "Random Thoughts","title_zh": "随想录","year": 1979},
        ],
        "key_events": [
            {"year": 1904, "event_zh": "生于四川成都官宦世家"},
            {"year": 1923, "event_zh": "离家出走，赴上海追求个人解放"},
            {"year": 1927, "event_zh": "旅法期间完成《灭亡》，正式走上文学道路"},
            {"year": 1931, "event_zh": "《家》出版，轰动文坛"},
            {"year": 1966, "event_zh": "文革中遭受批斗，被迫停止创作"},
            {"year": 2003, "event_zh": "获国家最高荣誉勋章；2005年辞世，享年101岁"},
        ],
    },

    {
        "name": "Lao She",
        "name_zh": "老舍",
        "birth": 1899,
        "death": 1966,
        "nationality": "中国",
        "bio_zh": (
            "原名舒庆春，满族，北京人。以京味语言描绘市民生活，"
            "《骆驼祥子》《茶馆》是中国现代文学经典。"
            "文革初期遭迫害，投太平湖自尽，1978年获平反昭雪。"
        ),
        "major_works": [
            {"title": "Rickshaw Boy", "title_zh": "骆驼祥子", "year": 1937},
            {"title": "Teahouse",     "title_zh": "茶馆",     "year": 1957},
            {"title": "Four Generations Under One Roof", "title_zh": "四世同堂", "year": 1944},
        ],
        "key_events": [
            {"year": 1899, "event_zh": "生于北京，父亲为旗兵，八国联军入京时阵亡"},
            {"year": 1924, "event_zh": "赴英国伦敦大学东方学院任教，开始小说创作"},
            {"year": 1937, "event_zh": "《骆驼祥子》出版，奠定国际声誉"},
            {"year": 1957, "event_zh": "话剧《茶馆》首演，被誉为'东方舞台艺术珍品'"},
            {"year": 1966, "event_zh": "文革中遭红卫兵批斗后投湖自尽"},
        ],
    },

    {
        "name": "Bing Xin",
        "name_zh": "冰心",
        "birth": 1900,
        "death": 1999,
        "nationality": "中国",
        "bio_zh": (
            "原名谢婉莹，福建长乐人，中国现代文学史上杰出的女作家。"
            "以爱的哲学为核心，《繁星》《春水》以清丽小诗表达对母爱、自然、童心的礼赞，"
            "影响了几代中国读者，被誉为'文坛祖母'。"
        ),
        "major_works": [
            {"title": "Myriad Stars",              "title_zh": "繁星",   "year": 1923},
            {"title": "Spring Waters",             "title_zh": "春水",   "year": 1923},
            {"title": "Letters to Young Readers",  "title_zh": "寄小读者","year": 1926},
            {"title": "Ode to the Cherry Blossoms","title_zh": "樱花赞", "year": 1962},
        ],
        "key_events": [
            {"year": 1900, "event_zh": "生于福州，父亲为海军将领"},
            {"year": 1919, "event_zh": "五四运动期间参与学生运动，开始文学创作"},
            {"year": 1923, "event_zh": "赴美国威尔斯利学院留学，攻读文学"},
            {"year": 1926, "event_zh": "《寄小读者》出版，开创中国儿童文学新风"},
            {"year": 1999, "event_zh": "辞世，享年99岁"},
        ],
    },

    {
        "name": "Wang Zengqi",
        "name_zh": "汪曾祺",
        "birth": 1920,
        "death": 1997,
        "nationality": "中国",
        "bio_zh": (
            "江苏高邮人，师从沈从文，中国当代短篇小说大师。"
            "以平淡冲和的文风写市井日常，《受戒》《大淖记事》被誉为'散文化小说'典范。"
            "晚年转型为美食随笔作家，深受读者喜爱。"
        ),
        "major_works": [
            {"title": "Ordination",       "title_zh": "受戒",   "year": 1980},
            {"title": "Daner Bay",        "title_zh": "大淖记事","year": 1981},
            {"title": "Puqiao Collection","title_zh": "蒲桥集", "year": 1989},
        ],
        "key_events": [
            {"year": 1920, "event_zh": "生于江苏高邮，祖父是清末举人"},
            {"year": 1939, "event_zh": "考入西南联大中文系，师从沈从文"},
            {"year": 1980, "event_zh": "《受戒》发表，沉寂三十年后重焕文学生命"},
            {"year": 1997, "event_zh": "辞世，享年77岁"},
        ],
    },

    {
        "name": "Can Xue",
        "name_zh": "残雪",
        "birth": 1953,
        "death": None,
        "nationality": "中国",
        "bio_zh": (
            "原名邓小华，湖南道县人，中国最重要的先锋文学作家之一。"
            "以梦魇般的意象和意识流叙事构建独特的内心宇宙，"
            "多次被提名诺贝尔文学奖，在卡夫卡与博尔赫斯研究方面亦有深厚造诣。"
        ),
        "major_works": [
            {"title": "Yellow Mud Street",     "title_zh": "黄泥街",    "year": 1985},
            {"title": "Dialogues in Paradise", "title_zh": "天堂里的对话","year": 1988},
            {"title": "The Last Lover",        "title_zh": "最后的情人", "year": 2005},
            {"title": "Frontier",             "title_zh": "边疆",       "year": 2008},
        ],
        "key_events": [
            {"year": 1953, "event_zh": "生于湖南长沙，父母均为党政干部后遭打压"},
            {"year": 1966, "event_zh": "文化大革命中随家人下放农村"},
            {"year": 1985, "event_zh": "《黄泥街》引发文坛震动，先锋写作正式登场"},
            {"year": 2019, "event_zh": "入围诺贝尔文学奖赔率榜前列，国际声誉持续攀升"},
        ],
    },

    # ---- 西方作家 ----

    {
        "name": "Franz Kafka",
        "name_zh": "卡夫卡",
        "birth": 1883,
        "death": 1924,
        "nationality": "奥匈帝国（捷克）",
        "bio_zh": (
            "生于布拉格的德语犹太作家，以荒诞而精确的笔触描绘现代人的异化与官僚体制的压迫。"
            "《变形记》《审判》《城堡》建构了独特的'卡夫卡式'世界，"
            "深刻影响了二十世纪存在主义文学与后现代主义思潮。"
        ),
        "major_works": [
            {"title": "The Metamorphosis", "title_zh": "变形记",  "year": 1915},
            {"title": "In the Penal Colony","title_zh": "在流放地","year": 1919},
            {"title": "The Trial",         "title_zh": "审判",    "year": 1925},
            {"title": "The Castle",        "title_zh": "城堡",    "year": 1926},
            {"title": "Amerika",           "title_zh": "美国",    "year": 1927},
        ],
        "key_events": [
            {"year": 1883, "event_zh": "生于布拉格，父亲为强势的犹太商人"},
            {"year": 1906, "event_zh": "获布拉格大学法学博士，入职保险公司"},
            {"year": 1912, "event_zh": "一夜之间写成《判决》，文学觉醒之夜"},
            {"year": 1915, "event_zh": "《变形记》出版，奠定文学史地位"},
            {"year": 1924, "event_zh": "因喉结核病逝，临终嘱托好友布罗德销毁手稿，布罗德违命保存"},
        ],
    },

    {
        "name": "Jorge Luis Borges",
        "name_zh": "博尔赫斯",
        "birth": 1899,
        "death": 1986,
        "nationality": "阿根廷",
        "bio_zh": (
            "阿根廷作家、诗人，拉丁美洲文学先驱，以迷宫、镜子、无限图书馆等意象"
            "构建令人眩晕的元小说宇宙。《虚构集》《阿莱夫》是后现代文学圣经，"
            "深刻影响了马尔克斯、卡尔维诺等一代作家。"
        ),
        "major_works": [
            {"title": "Ficciones",    "title_zh": "虚构集", "year": 1944},
            {"title": "The Aleph",    "title_zh": "阿莱夫", "year": 1949},
            {"title": "Labyrinths",   "title_zh": "迷宫",   "year": 1962},
            {"title": "The Book of Sand", "title_zh": "沙之书", "year": 1975},
        ],
        "key_events": [
            {"year": 1899, "event_zh": "生于布宜诺斯艾利斯，祖父为阿根廷独立战争英雄"},
            {"year": 1914, "event_zh": "随家人旅居欧洲，接触超现实主义与表现主义"},
            {"year": 1938, "event_zh": "头部重伤后险些丧命，转型写作短篇奇幻小说"},
            {"year": 1944, "event_zh": "《虚构集》出版，改变世界文学走向"},
            {"year": 1955, "event_zh": "双目近乎失明，出任阿根廷国立图书馆馆长"},
            {"year": 1986, "event_zh": "病逝于日内瓦，享年86岁"},
        ],
    },

    {
        "name": "Albert Camus",
        "name_zh": "加缪",
        "birth": 1913,
        "death": 1960,
        "nationality": "法国（阿尔及利亚裔）",
        "bio_zh": (
            "法国作家、哲学家，存在主义与荒诞主义代表人物。"
            "《局外人》以冷峻的第一人称呈现现代人的疏离，"
            "《西西弗斯神话》将荒诞升华为哲学体系。"
            "1957年获诺贝尔文学奖，1960年死于车祸，享年46岁。"
        ),
        "major_works": [
            {"title": "The Stranger",          "title_zh": "局外人",     "year": 1942},
            {"title": "The Myth of Sisyphus",  "title_zh": "西西弗斯神话","year": 1942},
            {"title": "The Plague",            "title_zh": "鼠疫",       "year": 1947},
            {"title": "The Rebel",             "title_zh": "反抗者",     "year": 1951},
            {"title": "The Fall",              "title_zh": "堕落",       "year": 1956},
        ],
        "key_events": [
            {"year": 1913, "event_zh": "生于阿尔及利亚蒙多维，父亲在一战中阵亡"},
            {"year": 1930, "event_zh": "确诊肺结核，被迫中断学业"},
            {"year": 1942, "event_zh": "《局外人》与《西西弗斯神话》同年出版，一举成名"},
            {"year": 1944, "event_zh": "二战期间主编地下抵抗运动刊物《战斗报》"},
            {"year": 1957, "event_zh": "获诺贝尔文学奖，演讲中论述艺术家的责任"},
            {"year": 1960, "event_zh": "死于汽车事故，口袋里有一张未使用的火车票"},
        ],
    },

    {
        "name": "Fyodor Dostoevsky",
        "name_zh": "陀思妥耶夫斯基",
        "birth": 1821,
        "death": 1881,
        "nationality": "俄国",
        "bio_zh": (
            "俄国小说家，以对人类心理深渊的穿透性探索著称。"
            "《罪与罚》《白痴》《卡拉马佐夫兄弟》深入剖析罪恶、苦难与救赎，"
            "被尼采、弗洛伊德、萨特等思想家奉为精神导师。"
        ),
        "major_works": [
            {"title": "Poor Folk",              "title_zh": "穷人",      "year": 1846},
            {"title": "Crime and Punishment",   "title_zh": "罪与罚",    "year": 1866},
            {"title": "The Idiot",              "title_zh": "白痴",      "year": 1869},
            {"title": "Demons",                 "title_zh": "群魔",      "year": 1872},
            {"title": "The Brothers Karamazov", "title_zh": "卡拉马佐夫兄弟","year": 1880},
        ],
        "key_events": [
            {"year": 1821, "event_zh": "生于莫斯科，父亲为军医"},
            {"year": 1849, "event_zh": "因参与革命活动被捕，在行刑前一刻获赦，流放西伯利亚"},
            {"year": 1866, "event_zh": "《罪与罚》发表，举世震惊"},
            {"year": 1867, "event_zh": "为还赌债出走欧洲，穷困潦倒中完成《赌徒》"},
            {"year": 1880, "event_zh": "《卡拉马佐夫兄弟》完成，翌年病逝"},
        ],
    },

    {
        "name": "William Faulkner",
        "name_zh": "福克纳",
        "birth": 1897,
        "death": 1962,
        "nationality": "美国",
        "bio_zh": (
            "美国南方文学代表人物，以意识流与多重叙事视角呈现美国南方的衰落与罪孽。"
            "虚构的约克纳帕塔法郡构成其文学王国。"
            "1949年获诺贝尔文学奖，被誉为'美国最伟大的小说家之一'。"
        ),
        "major_works": [
            {"title": "The Sound and the Fury", "title_zh": "喧哗与骚动",   "year": 1929},
            {"title": "As I Lay Dying",         "title_zh": "我弥留之际",   "year": 1930},
            {"title": "Light in August",        "title_zh": "八月之光",     "year": 1932},
            {"title": "Absalom, Absalom!",      "title_zh": "押沙龙，押沙龙！","year": 1936},
        ],
        "key_events": [
            {"year": 1897, "event_zh": "生于密西西比州，南方没落贵族家庭"},
            {"year": 1918, "event_zh": "一战期间以加拿大人身份入皇家空军，未曾参战"},
            {"year": 1929, "event_zh": "《喧哗与骚动》出版，意识流技法震惊文坛"},
            {"year": 1949, "event_zh": "获诺贝尔文学奖，发表著名的'人类不朽'演讲"},
            {"year": 1962, "event_zh": "因酗酒引发并发症病逝"},
        ],
    },

    {
        "name": "Ernest Hemingway",
        "name_zh": "海明威",
        "birth": 1899,
        "death": 1961,
        "nationality": "美国",
        "bio_zh": (
            "美国作家，'迷失的一代'代言人，以冰山理论开创简洁硬汉风格。"
            "《太阳照常升起》《永别了，武器》《老人与海》奠定其文学巨匠地位。"
            "1954年获诺贝尔文学奖，1961年以猎枪自尽。"
        ),
        "major_works": [
            {"title": "The Sun Also Rises",     "title_zh": "太阳照常升起","year": 1926},
            {"title": "A Farewell to Arms",     "title_zh": "永别了，武器","year": 1929},
            {"title": "For Whom the Bell Tolls","title_zh": "丧钟为谁而鸣","year": 1940},
            {"title": "The Old Man and the Sea","title_zh": "老人与海",   "year": 1952},
        ],
        "key_events": [
            {"year": 1899, "event_zh": "生于伊利诺伊州奥克帕克"},
            {"year": 1918, "event_zh": "一战期间赴意大利前线担任救护车驾驶员，负重伤"},
            {"year": 1921, "event_zh": "旅居巴黎，与菲茨杰拉德、庞德等'迷失的一代'相交"},
            {"year": 1952, "event_zh": "《老人与海》发表，次年获普利策奖"},
            {"year": 1954, "event_zh": "获诺贝尔文学奖"},
            {"year": 1961, "event_zh": "在爱达荷州凯彻姆家中以猎枪自尽"},
        ],
    },

    {
        "name": "Virginia Woolf",
        "name_zh": "伍尔夫",
        "birth": 1882,
        "death": 1941,
        "nationality": "英国",
        "bio_zh": (
            "英国现代主义文学核心人物，布卢姆斯伯里文化圈灵魂。"
            "以意识流笔法探索女性内心世界，《达洛维夫人》《到灯塔去》是现代小说里程碑。"
            "《一间自己的房间》是女性主义文学批评的奠基之作。"
        ),
        "major_works": [
            {"title": "Mrs Dalloway",        "title_zh": "达洛维夫人",   "year": 1925},
            {"title": "To the Lighthouse",   "title_zh": "到灯塔去",     "year": 1927},
            {"title": "Orlando",             "title_zh": "奥兰多",       "year": 1928},
            {"title": "A Room of One's Own", "title_zh": "一间自己的房间","year": 1929},
            {"title": "The Waves",           "title_zh": "海浪",         "year": 1931},
        ],
        "key_events": [
            {"year": 1882, "event_zh": "生于伦敦，父亲为著名文学评论家莱斯利·斯蒂芬"},
            {"year": 1895, "event_zh": "母亲去世，首次精神崩溃"},
            {"year": 1917, "event_zh": "与丈夫伦纳德创立霍加斯出版社"},
            {"year": 1925, "event_zh": "《达洛维夫人》出版，意识流技法臻于成熟"},
            {"year": 1929, "event_zh": "《一间自己的房间》出版，女性主义批评先声"},
            {"year": 1941, "event_zh": "精神病复发，投塞姆河自溺"},
        ],
    },

    {
        "name": "Gabriel Garcia Marquez",
        "name_zh": "加西亚·马尔克斯",
        "birth": 1927,
        "death": 2014,
        "nationality": "哥伦比亚",
        "bio_zh": (
            "哥伦比亚作家，魔幻现实主义宗师。"
            "《百年孤独》以马孔多小镇为舞台，将拉丁美洲历史幻化为神话史诗，"
            "被誉为二十世纪最伟大的西班牙语小说。1982年获诺贝尔文学奖。"
        ),
        "major_works": [
            {"title": "One Hundred Years of Solitude","title_zh": "百年孤独",      "year": 1967},
            {"title": "The Autumn of the Patriarch",  "title_zh": "族长的秋天",    "year": 1975},
            {"title": "Love in the Time of Cholera",  "title_zh": "霍乱时期的爱情","year": 1985},
            {"title": "The General in His Labyrinth", "title_zh": "迷宫中的将军",  "year": 1989},
        ],
        "key_events": [
            {"year": 1927, "event_zh": "生于哥伦比亚阿拉卡塔卡，由外祖父母抚养长大"},
            {"year": 1948, "event_zh": "哥伦比亚内战期间开始新闻写作生涯"},
            {"year": 1965, "event_zh": "驾车途中突然顿悟《百年孤独》开篇，折返家中写作"},
            {"year": 1967, "event_zh": "《百年孤独》出版，首版8000册一周售罄"},
            {"year": 1982, "event_zh": "获诺贝尔文学奖，身着哥伦比亚传统白色礼服出席典礼"},
            {"year": 2014, "event_zh": "病逝于墨西哥城，享年87岁"},
        ],
    },

    {
        "name": "Italo Calvino",
        "name_zh": "卡尔维诺",
        "birth": 1923,
        "death": 1985,
        "nationality": "意大利",
        "bio_zh": (
            "意大利作家，以轻盈的想象力和严谨的结构意识著称。"
            "从新写实主义起步，经由寓言、元小说，最终抵达后现代文学巅峰。"
            "《如果在冬夜，一个旅人》以元小说形式重写阅读行为本身，影响深远。"
        ),
        "major_works": [
            {"title": "The Path to the Spiders' Nests","title_zh": "蛛巢小径",      "year": 1947},
            {"title": "Our Ancestors",                 "title_zh": "我们的祖先",    "year": 1960},
            {"title": "Invisible Cities",              "title_zh": "看不见的城市",  "year": 1972},
            {"title": "If on a Winter's Night a Traveler","title_zh": "如果在冬夜，一个旅人","year": 1979},
            {"title": "Six Memos for the Next Millennium","title_zh": "新千年文学备忘录","year": 1988},
        ],
        "key_events": [
            {"year": 1923, "event_zh": "生于古巴圣地亚哥，父母均为植物学家"},
            {"year": 1943, "event_zh": "加入意大利抵抗运动，对抗德国占领"},
            {"year": 1947, "event_zh": "处女作《蛛巢小径》出版，获新写实主义大师卡尔洛·莱维赏识"},
            {"year": 1972, "event_zh": "《看不见的城市》出版，与博尔赫斯并列后现代文学先驱"},
            {"year": 1985, "event_zh": "脑溢血病逝，去世前正准备哈佛大学诺顿讲座讲稿"},
        ],
    },

    {
        "name": "Olga Tokarczuk",
        "name_zh": "奥尔加·托卡尔丘克",
        "birth": 1962,
        "death": None,
        "nationality": "波兰",
        "bio_zh": (
            "波兰作家，心理学背景赋予其作品深厚的人文关怀。"
            "以星座式叙事打破线性时间，《航班》《云游》融合旅行、历史与哲思。"
            "2018年获诺贝尔文学奖，是波兰第五位、也是首位在世时获奖的波兰女作家。"
        ),
        "major_works": [
            {"title": "Primeval and Other Times",    "title_zh": "太古和其他的时间",     "year": 1996},
            {"title": "House of Day, House of Night","title_zh": "日间的房子，夜间的房子","year": 1998},
            {"title": "Flights",                     "title_zh": "航班",                 "year": 2007},
            {"title": "The Books of Jacob",          "title_zh": "雅各书",               "year": 2014},
        ],
        "key_events": [
            {"year": 1962, "event_zh": "生于波兰苏莱胡夫，父亲为图书馆员"},
            {"year": 1985, "event_zh": "毕业于华沙大学心理学系，后从事心理咨询"},
            {"year": 1993, "event_zh": "出版处女作，正式开启文学生涯"},
            {"year": 2008, "event_zh": "《航班》获波兰最高文学奖——尼刻奖"},
            {"year": 2018, "event_zh": "获2018年度诺贝尔文学奖（延迟至2019年颁发）"},
        ],
    },
]


# --------------------------------------------------------------------------- #
# 辅助函数
# --------------------------------------------------------------------------- #

def print_summary() -> None:
    """打印数据摘要，用于快速核查。"""
    print(f"\n{'='*60}")
    print(f"  作家年表 · 数据摘要")
    print(f"{'='*60}")
    print(f"  总作家数：{len(AUTHORS)}")
    chinese = [a for a in AUTHORS if "中国" in a["nationality"]]
    western = [a for a in AUTHORS if "中国" not in a["nationality"]]
    print(f"  中国作家：{len(chinese)} 位")
    print(f"  西方作家：{len(western)} 位")
    print()
    print(f"  {'序号':<4} {'中文名':<14} {'生年':<6} {'卒年':<6} {'国籍'}")
    print(f"  {'-'*58}")
    for i, a in enumerate(AUTHORS, 1):
        death = str(a["death"]) if a["death"] else "在世"
        print(f"  {i:<4} {a['name_zh']:<14} {a['birth']:<6} {death:<6} {a['nationality']}")
    print(f"{'='*60}\n")


def export_json(filepath: str = "authors_seed.json") -> None:
    """将数据导出为 JSON 文件，供前端或调试使用。"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(AUTHORS, f, ensure_ascii=False, indent=2)
    print(f"[OK] JSON 已导出至：{filepath}")


def seed_database(database_url=None) -> None:
    """
    将作家数据写入 PostgreSQL 数据库。
    依赖：psycopg2-binary  （pip install psycopg2-binary）

    参数：
      database_url: 格式 postgresql://user:password@host:port/dbname
                    若为 None，则读取环境变量 DATABASE_URL
    """
    try:
        import psycopg2
    except ImportError:
        print("[ERROR] 请先安装 psycopg2：pip install psycopg2-binary")
        sys.exit(1)

    url = database_url or os.getenv("DATABASE_URL")
    if not url:
        print("[ERROR] 请设置环境变量 DATABASE_URL 或传入 database_url 参数")
        sys.exit(1)

    conn = psycopg2.connect(url)
    cur  = conn.cursor()

    INSERT_AUTHOR = """
        INSERT INTO authors (name, name_zh, birth, death, nationality, bio_zh)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (name_zh) DO UPDATE
            SET name        = EXCLUDED.name,
                birth       = EXCLUDED.birth,
                death       = EXCLUDED.death,
                nationality = EXCLUDED.nationality,
                bio_zh      = EXCLUDED.bio_zh
        RETURNING id;
    """

    INSERT_WORK = """
        INSERT INTO works (author_id, title, title_zh, year)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (author_id, title_zh) DO NOTHING;
    """

    INSERT_AUTHOR_EVENT = """
        INSERT INTO author_events (author_id, year, event_zh)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """

    for author in AUTHORS:
        cur.execute(INSERT_AUTHOR, (
            author["name"],
            author["name_zh"],
            author["birth"],
            author.get("death"),
            author["nationality"],
            author["bio_zh"],
        ))
        author_id = cur.fetchone()[0]

        for work in author.get("major_works", []):
            cur.execute(INSERT_WORK, (
                author_id,
                work["title"],
                work["title_zh"],
                work["year"],
            ))

        for event in author.get("key_events", []):
            cur.execute(INSERT_AUTHOR_EVENT, (
                author_id,
                event["year"],
                event["event_zh"],
            ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"[OK] 已成功将 {len(AUTHORS)} 位作家的数据写入数据库。")


# --------------------------------------------------------------------------- #
# 入口
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="作家年表数据初始化脚本")
    parser.add_argument(
        "--action",
        choices=["summary", "json", "seed"],
        default="summary",
        help="summary=打印摘要 | json=导出JSON | seed=写入数据库",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="PostgreSQL 连接串，默认读取环境变量 DATABASE_URL",
    )
    parser.add_argument(
        "--output",
        default="authors_seed.json",
        help="JSON 导出路径（仅 --action json 时有效）",
    )
    args = parser.parse_args()

    if args.action == "summary":
        print_summary()
    elif args.action == "json":
        export_json(args.output)
    elif args.action == "seed":
        seed_database(args.db_url)
