"""
作家年表 · 作家种子数据（第四批，~25 位）
运行：DATABASE_URL=postgresql+asyncpg://joker@localhost:5432/zuojia_nianbiao \
      /Users/joker/zuojia-nianbiao/.venv/bin/python -m backend.seed_authors4
"""
import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── 中世纪 ────────────────────────────────────────────────────────────────
    dict(
        name="Dante Alighieri", name_zh="但丁",
        birth=1265, death=1321, nationality="意大利",
        bio_zh="意大利中世纪最伟大的诗人，《神曲》以三界游历构建了中世纪基督教宇宙观的文学总结，被誉为'中世纪的最后一位诗人，新时代的第一位诗人'。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Dante_Alighieri_portrait_by_Giotto_di_Bondone_crop.jpg/330px-Dante_Alighieri_portrait_by_Giotto_di_Bondone_crop.jpg",
        tags=["中世纪", "意大利文学", "神曲"],
        works=[("The Divine Comedy", "《神曲》", 1321, "长诗"),
               ("La Vita Nuova", "《新生》", 1295, "诗文集")],
        events=[(1265, "生于佛罗伦萨", "birth"),
                (1321, "卒于拉文纳", "death"),
                (1302, "因政治纷争被驱逐出佛罗伦萨，开始流亡", "life"),
                (1307, "开始创作《神曲》", "life")],
    ),
    # ── 文艺复兴 ──────────────────────────────────────────────────────────────
    dict(
        name="Giovanni Boccaccio", name_zh="薄伽丘",
        birth=1313, death=1375, nationality="意大利",
        bio_zh="意大利文艺复兴时期作家，《十日谈》以黑死病为背景，借百篇故事赞颂人性、讽刺教会，是欧洲近代短篇小说的奠基之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Andrea_del_Castagno_Giovanni_Boccaccio_c_1450.jpg/330px-Andrea_del_Castagno_Giovanni_Boccaccio_c_1450.jpg",
        tags=["文艺复兴", "意大利文学", "人文主义"],
        works=[("The Decameron", "《十日谈》", 1353, "小说集")],
        events=[(1313, "生于佛罗伦萨附近", "birth"),
                (1375, "卒于切尔塔尔多", "death"),
                (1348, "佛罗伦萨黑死病，《十日谈》素材来源", "life")],
    ),
    dict(
        name="François Rabelais", name_zh="拉伯雷",
        birth=1494, death=1553, nationality="法国",
        bio_zh="法国文艺复兴时期作家，以《巨人传》系列将人文主义精神、民间狂欢文化与讽刺批判融为一体，巴赫金以其为'狂欢化'理论的核心案例。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Rabelais_Portrait_-_Mus%C3%A9e_des_Beaux-Arts_de_Blois_-_crop.jpg/330px-Rabelais_Portrait_-_Mus%C3%A9e_des_Beaux-Arts_de_Blois_-_crop.jpg",
        tags=["文艺复兴", "法国文学", "人文主义"],
        works=[("Gargantua and Pantagruel", "《巨人传》", 1532, "小说")],
        events=[(1494, "生于希农附近", "birth"),
                (1553, "卒于巴黎", "death")],
    ),
    # ── 17 世纪古典主义 ───────────────────────────────────────────────────────
    dict(
        name="John Milton", name_zh="弥尔顿",
        birth=1608, death=1674, nationality="英国",
        bio_zh="英国17世纪最重要的诗人，清教徒诗人，以史诗《失乐园》重述《圣经》堕落故事，被誉为莎士比亚之后英语文学最伟大的诗人。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/John_Milton_by_Pieter_van_der_Plaes.jpg/330px-John_Milton_by_Pieter_van_der_Plaes.jpg",
        tags=["古典主义", "英国文学", "清教徒文学", "史诗"],
        works=[("Paradise Lost", "《失乐园》", 1667, "史诗"),
               ("Paradise Regained", "《复乐园》", 1671, "史诗"),
               ("Areopagitica", "《论出版自由》", 1644, "政论")],
        events=[(1608, "生于伦敦", "birth"),
                (1674, "卒于伦敦", "death"),
                (1651, "因过度用眼完全失明，口述完成《失乐园》", "life")],
    ),
    dict(
        name="Molière", name_zh="莫里哀",
        birth=1622, death=1673, nationality="法国",
        bio_zh="法国古典主义喜剧大师，以《吝啬鬼》《伪君子》《唐璜》等作品对法国社会的虚伪与贪婪进行深刻讽刺，是西方喜剧传统的奠基人之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/MoliereWikipedia.jpg/330px-MoliereWikipedia.jpg",
        tags=["古典主义", "法国文学", "喜剧"],
        works=[("The Miser", "《吝啬鬼》", 1668, "喜剧"),
               ("Tartuffe", "《伪君子》", 1664, "喜剧"),
               ("Don Juan", "《唐璜》", 1665, "喜剧"),
               ("The Misanthrope", "《恨世者》", 1666, "喜剧")],
        events=[(1622, "生于巴黎", "birth"),
                (1673, "在第四次《无病呻吟》演出中晕倒，当晚去世", "death"),
                (1644, "创建伊吕斯特剧团，开始巡回演出", "life")],
    ),
    # ── 18 世纪启蒙 ───────────────────────────────────────────────────────────
    dict(
        name="Daniel Defoe", name_zh="笛福",
        birth=1660, death=1731, nationality="英国",
        bio_zh="英国启蒙时期作家，被誉为英国小说之父，《鲁滨逊漂流记》以写实笔法描写个人在自然中的奋斗，奠定了英国现实主义小说的基础。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Daniel_Defoe.jpg/330px-Daniel_Defoe.jpg",
        tags=["启蒙主义", "英国文学", "现实主义"],
        works=[("Robinson Crusoe", "《鲁滨逊漂流记》", 1719, "小说"),
               ("Moll Flanders", "《摩尔·弗兰德斯》", 1722, "小说")],
        events=[(1660, "生于伦敦", "birth"),
                (1731, "卒于伦敦", "death"),
                (1719, "59岁出版《鲁滨逊漂流记》，开启新的文学类型", "life")],
    ),
    dict(
        name="Friedrich Schiller", name_zh="席勒",
        birth=1759, death=1805, nationality="德国",
        bio_zh="德国古典主义与浪漫主义之间的重要作家，剧作家与诗人，以《强盗》《阴谋与爱情》揭露封建专制，与歌德共同构成'魏玛古典主义'高峰。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Friedrich_Schiller_by_Ludovike_Simanowiz_%281794%29.jpg/330px-Friedrich_Schiller_by_Ludovike_Simanowiz_%281794%29.jpg",
        tags=["古典主义", "德国文学", "狂飙突进"],
        works=[("The Robbers", "《强盗》", 1781, "戏剧"),
               ("Intrigue and Love", "《阴谋与爱情》", 1784, "戏剧"),
               ("Wallenstein", "《华伦斯坦》", 1799, "戏剧"),
               ("Ode to Joy", "《欢乐颂》", 1785, "诗歌")],
        events=[(1759, "生于马尔巴赫", "birth"),
                (1805, "卒于魏玛", "death"),
                (1799, "与歌德在魏玛合作，共同推动古典主义文学", "life")],
    ),
    # ── 19 世纪浪漫主义 ───────────────────────────────────────────────────────
    dict(
        name="George Gordon Byron", name_zh="拜伦",
        birth=1788, death=1824, nationality="英国",
        bio_zh="英国浪漫主义诗人，以《恰尔德·哈罗尔德游记》《唐璜》闻名，其叛逆精神与传奇人生催生了'拜伦式英雄'这一文学原型，深刻影响欧洲浪漫主义运动。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Thomas_Phillips_-_George_Gordon_Byron%2C_6th_Baron_Byron_-_Google_Art_Project.jpg/330px-Thomas_Phillips_-_George_Gordon_Byron%2C_6th_Baron_Byron_-_Google_Art_Project.jpg",
        tags=["浪漫主义", "英国文学", "诗歌"],
        works=[("Childe Harold's Pilgrimage", "《恰尔德·哈罗尔德游记》", 1812, "长诗"),
               ("Don Juan", "《唐璜》", 1819, "长诗"),
               ("Manfred", "《曼弗雷德》", 1817, "诗剧")],
        events=[(1788, "生于伦敦", "birth"),
                (1824, "卒于希腊迈索隆吉翁（参加希腊独立战争）", "death"),
                (1812, "《恰尔德·哈罗尔德游记》出版，一夜成名", "life")],
    ),
    dict(
        name="Percy Bysshe Shelley", name_zh="雪莱",
        birth=1792, death=1822, nationality="英国",
        bio_zh="英国浪漫主义诗人，激进的政治理想主义者，以《解放了的普罗米修斯》《西风颂》《云雀颂》展现对自由与美的极致追求，溺水身亡年仅29岁。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Percy_Bysshe_Shelley_by_Alfred_Clint.jpg/330px-Percy_Bysshe_Shelley_by_Alfred_Clint.jpg",
        tags=["浪漫主义", "英国文学", "诗歌"],
        works=[("Prometheus Unbound", "《解放了的普罗米修斯》", 1820, "诗剧"),
               ("Ode to the West Wind", "《西风颂》", 1820, "诗歌"),
               ("To a Skylark", "《云雀颂》", 1820, "诗歌")],
        events=[(1792, "生于菲尔德普莱斯", "birth"),
                (1822, "在意大利溺水身亡，年仅29岁", "death"),
                (1818, "移居意大利，创作高峰期", "life")],
    ),
    dict(
        name="Walt Whitman", name_zh="惠特曼",
        birth=1819, death=1892, nationality="美国",
        bio_zh="美国浪漫主义诗人，以《草叶集》创立自由诗体，以豪放的长诗赞颂美国民主精神与人的身体，奠定了美国现代诗歌的基础。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Walt_Whitman_-_George_Collins_Cox.jpg/330px-Walt_Whitman_-_George_Collins_Cox.jpg",
        tags=["浪漫主义", "美国文学", "自由诗"],
        works=[("Leaves of Grass", "《草叶集》", 1855, "诗集"),
               ("Song of Myself", "《自我之歌》", 1855, "长诗"),
               ("O Captain! My Captain!", "《啊，船长！我的船长！》", 1865, "诗歌")],
        events=[(1819, "生于西山丘", "birth"),
                (1892, "卒于卡姆登", "death"),
                (1855, "自费出版《草叶集》第一版，爱默生高度赞扬", "life"),
                (1865, "南北战争期间在华盛顿医院担任义务护理员", "life")],
    ),
    dict(
        name="Thomas Hardy", name_zh="哈代",
        birth=1840, death=1928, nationality="英国",
        bio_zh="英国维多利亚时代末期小说家与诗人，以《德伯家的苔丝》《无名的裘德》揭露维多利亚时代道德伪善与宗教压迫，开创英国批判现实主义的悲剧高峰。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Thomas_Hardy_by_William_Strang%2C_1893.jpg/330px-Thomas_Hardy_by_William_Strang%2C_1893.jpg",
        tags=["现实主义", "英国文学", "悲剧"],
        works=[("Tess of the d'Urbervilles", "《德伯家的苔丝》", 1891, "小说"),
               ("Jude the Obscure", "《无名的裘德》", 1895, "小说"),
               ("Far from the Madding Crowd", "《远离尘嚣》", 1874, "小说")],
        events=[(1840, "生于多塞特郡", "birth"),
                (1928, "卒于多尔切斯特", "death"),
                (1896, "《无名的裘德》因内容引发强烈批评，哈代此后转为专写诗歌", "life")],
    ),
    dict(
        name="Charles Baudelaire", name_zh="波德莱尔",
        birth=1821, death=1867, nationality="法国",
        bio_zh="法国象征主义诗歌先驱，以《恶之花》将美与丑、罪与救赎融为一体，开创了现代诗歌的感官体验与城市书写，深刻影响20世纪欧洲文学。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/tienne_Carjat%2C_Atelier_Carjat_%26_Cie%2C_Charles_Baudelaire%2C_vers_1863.jpg/330px-tienne_Carjat%2C_Atelier_Carjat_%26_Cie%2C_Charles_Baudelaire%2C_vers_1863.jpg",
        tags=["象征主义", "法国文学", "诗歌"],
        works=[("Les Fleurs du mal", "《恶之花》", 1857, "诗集"),
               ("Le Spleen de Paris", "《巴黎的忧郁》", 1869, "散文诗集")],
        events=[(1821, "生于巴黎", "birth"),
                (1867, "卒于巴黎", "death"),
                (1857, "《恶之花》出版，因伤风化罪被起诉并删改", "life")],
    ),
    dict(
        name="D. H. Lawrence", name_zh="劳伦斯",
        birth=1885, death=1930, nationality="英国",
        bio_zh="英国现代主义小说家，以《儿子与情人》《虹》《查泰莱夫人的情人》探索工业文明对人类本能与自然生命的压抑，其作品长期面临审查。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/DH_Lawrence_passport_photo.jpg/330px-DH_Lawrence_passport_photo.jpg",
        tags=["现代主义", "英国文学", "心理小说"],
        works=[("Sons and Lovers", "《儿子与情人》", 1913, "小说"),
               ("The Rainbow", "《虹》", 1915, "小说"),
               ("Women in Love", "《恋爱中的女人》", 1920, "小说"),
               ("Lady Chatterley's Lover", "《查泰莱夫人的情人》", 1928, "小说")],
        events=[(1885, "生于诺丁汉郡", "birth"),
                (1930, "卒于旺斯，年仅44岁", "death"),
                (1915, '《虹》出版后因"淫秽"内容被查禁', "life")],
    ),
    dict(
        name="T. S. Eliot", name_zh="艾略特",
        birth=1888, death=1965, nationality="美国/英国",
        bio_zh="美国裔英国诗人，现代主义诗歌最重要的代表，《荒原》以碎片化的叙事和文化引用描绘了一战后西方文明的精神危机，1948年获诺贝尔文学奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/The_Love_Song_of_J._Alfred_Prufrock.djvu/page1-330px-The_Love_Song_of_J._Alfred_Prufrock.djvu.jpg",
        tags=["现代主义", "英美文学", "诗歌", "意象派"],
        works=[("The Waste Land", "《荒原》", 1922, "长诗"),
               ("The Love Song of J. Alfred Prufrock", "《J·阿尔弗雷德·普鲁弗洛克的情歌》", 1915, "诗歌"),
               ("Four Quartets", "《四个四重奏》", 1943, "诗集"),
               ("Murder in the Cathedral", "《大教堂谋杀案》", 1935, "戏剧")],
        events=[(1888, "生于圣路易斯", "birth"),
                (1965, "卒于伦敦", "death"),
                (1914, "定居英国，结识庞德，开始现代主义创作", "life"),
                (1948, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Bertolt Brecht", name_zh="布莱希特",
        birth=1898, death=1956, nationality="德国",
        bio_zh="德国剧作家与诗人，史诗剧场（间离效果）的创立者，以《三分钱歌剧》《勇气妈妈》《伽利略传》打破观众的情感幻觉，推动观众理性思考社会问题。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Bertolt-Brecht.jpg/330px-Bertolt-Brecht.jpg",
        tags=["现代主义", "德国文学", "史诗剧场"],
        works=[("The Threepenny Opera", "《三分钱歌剧》", 1928, "戏剧"),
               ("Mother Courage and Her Children", "《勇气妈妈和她的孩子们》", 1941, "戏剧"),
               ("Life of Galileo", "《伽利略传》", 1943, "戏剧"),
               ("The Good Person of Szechwan", "《四川好人》", 1943, "戏剧")],
        events=[(1898, "生于奥格斯堡", "birth"),
                (1956, "卒于东柏林", "death"),
                (1933, "纳粹上台，流亡欧洲和美国", "life"),
                (1949, "回到东柏林，创立柏林剧团", "life")],
    ),
    # ── 中国现代文学 ──────────────────────────────────────────────────────────
    dict(
        name="Hu Shi", name_zh="胡适",
        birth=1891, death=1962, nationality="中国",
        bio_zh="中国现代文学运动的先驱，五四新文化运动主将，以《文学改良刍议》率先提出白话文学主张，推动了中国文学语言的现代转型。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Hu_Shih.jpg/330px-Hu_Shih.jpg",
        tags=["中国现代文学", "新文化运动", "白话文"],
        works=[("A Preliminary Discussion of Literary Reform", "《文学改良刍议》", 1917, "论文"),
               ("Experiments", "《尝试集》", 1920, "诗集")],
        events=[(1891, "生于安徽绩溪", "birth"),
                (1962, "卒于台北", "death"),
                (1917, "《文学改良刍议》发表于《新青年》，掀起白话文运动", "life"),
                (1938, "出任中国驻美大使", "life")],
    ),
    dict(
        name="Wen Yiduo", name_zh="闻一多",
        birth=1899, death=1946, nationality="中国",
        bio_zh="中国现代诗人、学者，新月派代表人物，提出新诗'三美'主张（音乐美、绘画美、建筑美），以《死水》《红烛》奠定新格律诗的里程碑，后因民主运动遭暗杀。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Wen_Yiduo.jpg/330px-Wen_Yiduo.jpg",
        tags=["中国现代文学", "新月派", "诗歌"],
        works=[("Red Candle", "《红烛》", 1923, "诗集"),
               ("Dead Water", "《死水》", 1928, "诗集")],
        events=[(1899, "生于湖北浠水", "birth"),
                (1946, "在昆明遭国民党特务暗杀", "death"),
                (1922, "留学美国，研习美术与文学", "life"),
                (1928, "《死水》出版，确立新格律诗地位", "life")],
    ),
    dict(
        name="Dai Wangshu", name_zh="戴望舒",
        birth=1905, death=1950, nationality="中国",
        bio_zh="中国现代派诗歌代表人物，以《雨巷》确立象征主义诗风，被称为'雨巷诗人'，其诗歌将法国象征主义与中国古典意境融为一体。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/d1a20cf431adcbef76094d36aaaf2edda3cc9ff9?x-bce-process=image/format,f_auto",
        tags=["中国现代文学", "现代派诗歌", "象征主义"],
        works=[("Rain Alley", "《雨巷》", 1927, "诗歌"),
               ("My Memory", "《我的记忆》", 1929, "诗集"),
               ("Disaster Years", "《灾难的岁月》", 1948, "诗集")],
        events=[(1905, "生于杭州", "birth"),
                (1950, "卒于北京", "death"),
                (1927, "《雨巷》发表，叶圣陶称其为'雨巷诗人'", "life"),
                (1932, "旅居法国，深受法国象征主义影响", "life")],
    ),
    dict(
        name="Xia Yan", name_zh="夏衍",
        birth=1900, death=1995, nationality="中国",
        bio_zh="中国现代著名剧作家，以《上海屋檐下》《法西斯细菌》描绘沦陷前夕的上海市民生活，是中国左翼电影和话剧运动的重要推动者。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/1c950a7b02087bf47bec2b76f9d3572c11dfcf4a?x-bce-process=image/format,f_auto",
        tags=["中国现代文学", "话剧", "左翼文学"],
        works=[("Under Shanghai Eaves", "《上海屋檐下》", 1937, "话剧"),
               ("Fascist Germs", "《法西斯细菌》", 1942, "话剧")],
        events=[(1900, "生于浙江杭州", "birth"),
                (1995, "卒于北京", "death"),
                (1930, "参加左翼作家联盟，推动左翼电影运动", "life")],
    ),
    # ── 中国古代 ──────────────────────────────────────────────────────────────
    dict(
        name="Qu Yuan", name_zh="屈原",
        birth=-340, death=-278, nationality="中国（楚国）",
        bio_zh="中国第一位伟大的爱国主义诗人，楚辞的奠基人，以《离骚》《九歌》开创中国浪漫主义文学传统，投汨罗江以死明志，端午节由此而来。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Qu_Yuan.jpg/330px-Qu_Yuan.jpg",
        tags=["中国古代文学", "楚辞", "爱国主义"],
        works=[("Li Sao", "《离骚》", -278, "长诗"),
               ("Nine Songs", "《九歌》", -300, "组诗"),
               ("Heavenly Questions", "《天问》", -300, "长诗")],
        events=[(-340, "生于楚国秭归", "birth"),
                (-278, "楚国郢都沦陷，投汨罗江殉国", "death"),
                (-304, "因政敌谗言被楚怀王疏远，流放汉北", "life")],
    ),
    dict(
        name="Tao Yuanming", name_zh="陶渊明",
        birth=365, death=427, nationality="中国（东晋）",
        bio_zh="中国田园诗的开山鼻祖，东晋诗人，以辞官归隐、躬耕田园的生活实践了儒道思想的融合，《桃花源记》构建了中国文人的精神乌托邦。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Tao_Yuanming_by_Guo_Xu.jpg/330px-Tao_Yuanming_by_Guo_Xu.jpg",
        tags=["中国古代文学", "田园诗", "东晋"],
        works=[("Peach Blossom Spring", "《桃花源记》", 421, "散文"),
               ("Return", "《归去来兮辞》", 405, "辞赋"),
               ("Drinking Alone", "《饮酒》", 410, "诗集")],
        events=[(365, "生于浔阳柴桑（今江西九江）", "birth"),
                (427, "卒于浔阳", "death"),
                (405, "辞去彭泽县令，归隐田园，始写田园诗", "life")],
    ),
    dict(
        name="Cao Xueqin", name_zh="曹雪芹",
        birth=1715, death=1763, nationality="中国（清朝）",
        bio_zh="中国古典小说最高成就《红楼梦》的作者，以贾家衰败为线索，构建了一个包容百科的艺术世界，被誉为中国文化的百科全书。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Cao_Xueqin.jpg/330px-Cao_Xueqin.jpg",
        tags=["中国古代文学", "清代小说", "红楼梦"],
        works=[("Dream of the Red Chamber", "《红楼梦》", 1754, "小说")],
        events=[(1715, "生于南京（约）", "birth"),
                (1763, "卒于北京（约）", "death"),
                (1728, "家道中落，随家迁至北京", "life"),
                (1754, "在贫病交加中创作《红楼梦》前80回", "life")],
    ),
]

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/zuojia_nianbiao"
)


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        added = 0
        skipped = 0
        for a in AUTHORS:
            result = await session.execute(
                select(Author).where(Author.name_zh == a["name_zh"])
            )
            if result.scalar_one_or_none():
                print(f"  跳过（已存在）: {a['name_zh']}")
                skipped += 1
                continue

            author = Author(
                name=a["name"],
                name_zh=a["name_zh"],
                birth=a["birth"],
                death=a.get("death"),
                nationality=a["nationality"],
                bio_zh=a.get("bio_zh", ""),
                portrait_url=a.get("portrait_url"),
                tags=a.get("tags", []),
            )
            session.add(author)
            await session.flush()

            for title, title_zh, year, genre in a.get("works", []):
                session.add(Work(
                    author_id=author.id,
                    title=title, title_zh=title_zh,
                    year=year, genre=genre,
                ))

            for ev in a.get("events", []):
                year, event_zh = ev[0], ev[1]
                event_type = ev[2] if len(ev) > 2 else "life"
                session.add(AuthorEvent(
                    author_id=author.id,
                    year=year, event_zh=event_zh, event_type=event_type,
                ))

            birth_str = str(a["birth"]) if a["birth"] > 0 else f"公元前{abs(a['birth'])}"
            print(f"  添加: {a['name_zh']} ({birth_str}–{a.get('death') or '今'})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
