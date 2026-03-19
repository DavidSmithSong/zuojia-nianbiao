"""
作家年表 · 作家种子数据（第三批，~25 位）
运行：DATABASE_URL=postgresql+asyncpg://joker@localhost:5432/zuojia_nianbiao \
      /Users/joker/zuojia-nianbiao/.venv/bin/python -m backend.seed_authors3
"""
import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── 西方文艺复兴 / 古典 ───────────────────────────────────────────────────
    dict(
        name="Miguel de Cervantes", name_zh="塞万提斯",
        birth=1547, death=1616, nationality="西班牙",
        bio_zh="西班牙文艺复兴时期最伟大的作家，以《堂吉诃德》开创近代欧洲小说传统，被誉为现代小说之父。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Cervantes_J%C3%A1uregui.jpg/330px-Cervantes_J%C3%A1uregui.jpg",
        tags=["文艺复兴", "西班牙文学", "骑士小说"],
        works=[("Don Quixote", "《堂吉诃德》", 1605, "小说"),
               ("Exemplary Novels", "《惩戒小说集》", 1613, "短篇小说集")],
        events=[(1547, "生于阿尔卡拉·德·埃纳雷斯", "birth"),
                (1616, "卒于马德里", "death"),
                (1571, "参加勒班陀海战，右手致残", "life"),
                (1605, "《堂吉诃德》第一部出版，立即风靡全欧", "life")],
    ),
    dict(
        name="William Shakespeare", name_zh="莎士比亚",
        birth=1564, death=1616, nationality="英国",
        bio_zh="英国文学史上最伟大的剧作家与诗人，37部戏剧横跨悲剧、喜剧与历史剧，深刻塑造了英语文学传统与西方文化。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/330px-Shakespeare.jpg",
        tags=["文艺复兴", "英国文学", "戏剧", "诗歌"],
        works=[("Hamlet", "《哈姆雷特》", 1600, "悲剧"),
               ("Romeo and Juliet", "《罗密欧与朱丽叶》", 1597, "悲剧"),
               ("Macbeth", "《麦克白》", 1606, "悲剧"),
               ("King Lear", "《李尔王》", 1606, "悲剧"),
               ("A Midsummer Night's Dream", "《仲夏夜之梦》", 1600, "喜剧"),
               ("The Merchant of Venice", "《威尼斯商人》", 1600, "喜剧")],
        events=[(1564, "生于斯特拉特福德", "birth"),
                (1616, "卒于斯特拉特福德", "death"),
                (1594, "成为环球剧院股东演员", "life"),
                (1609, "出版十四行诗集", "life")],
    ),
    dict(
        name="Johann Wolfgang von Goethe", name_zh="歌德",
        birth=1749, death=1832, nationality="德国",
        bio_zh="德国文学最高成就代表，诗人、剧作家、科学家，《浮士德》是德语文学的顶峰，《少年维特之烦恼》开创欧洲浪漫主义。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Goethe_%28Stieler_1828%29.jpg/330px-Goethe_%28Stieler_1828%29.jpg",
        tags=["古典主义", "浪漫主义", "德国文学", "狂飙突进"],
        works=[("The Sorrows of Young Werther", "《少年维特之烦恼》", 1774, "书信体小说"),
               ("Faust", "《浮士德》", 1808, "诗剧"),
               ("Wilhelm Meister's Apprenticeship", "《威廉·迈斯特的学习年代》", 1796, "小说")],
        events=[(1749, "生于法兰克福", "birth"),
                (1832, "卒于魏玛", "death"),
                (1774, "《少年维特之烦恼》出版，引发欧洲'维特热'", "life"),
                (1805, "席勒逝世，开始专注完成《浮士德》", "life")],
    ),
    # ── 西方 19 世纪 ──────────────────────────────────────────────────────────
    dict(
        name="Jane Austen", name_zh="奥斯丁",
        birth=1775, death=1817, nationality="英国",
        bio_zh="英国小说家，以精细入微的心理刻画和社会批判著称，在简·奥斯丁时代之前，女性小说家鲜少获得如此高的文学地位。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/CassandraAusten-JaneAusten%28c.1810%29_hires.jpg/330px-CassandraAusten-JaneAusten%28c.1810%29_hires.jpg",
        tags=["现实主义", "英国文学", "婚恋小说"],
        works=[("Pride and Prejudice", "《傲慢与偏见》", 1813, "小说"),
               ("Sense and Sensibility", "《理智与情感》", 1811, "小说"),
               ("Emma", "《爱玛》", 1815, "小说"),
               ("Persuasion", "《劝导》", 1818, "小说")],
        events=[(1775, "生于史蒂文顿", "birth"),
                (1817, "卒于温切斯特", "death"),
                (1813, "《傲慢与偏见》出版，奠定其文学声誉", "life")],
    ),
    dict(
        name="Ivan Turgenev", name_zh="屠格涅夫",
        birth=1818, death=1883, nationality="俄国",
        bio_zh="俄国现实主义小说家，以简洁优美的散文风格著称，《父与子》精准捕捉了19世纪俄国两代知识分子的思想冲突。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Turgenev_by_Repin.jpg/330px-Turgenev_by_Repin.jpg",
        tags=["现实主义", "俄国文学", "贵族文学"],
        works=[("Fathers and Sons", "《父与子》", 1862, "小说"),
               ("A Hunter's Sketches", "《猎人笔记》", 1852, "短篇小说集"),
               ("On the Eve", "《前夜》", 1860, "小说"),
               ("Rudin", "《罗亭》", 1856, "小说")],
        events=[(1818, "生于奥廖尔", "birth"),
                (1883, "卒于布日瓦尔", "death"),
                (1852, "《猎人笔记》出版，引起沙皇当局注意", "life"),
                (1862, "《父与子》出版，引发俄国知识界大辩论", "life")],
    ),
    dict(
        name="Émile Zola", name_zh="左拉",
        birth=1840, death=1902, nationality="法国",
        bio_zh="法国自然主义文学领袖，以《卢贡-马卡尔家族》系列二十卷描绘第二帝国时期的法国社会，'我控诉'一信成为现代公共知识分子的典范。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/%C3%89mile_Zola_by_Nadar_1902.jpg/330px-%C3%89mile_Zola_by_Nadar_1902.jpg",
        tags=["自然主义", "法国文学", "社会小说"],
        works=[("Germinal", "《萌芽》", 1885, "小说"),
               ("Nana", "《娜娜》", 1880, "小说"),
               ("The Belly of Paris", "《巴黎之胃》", 1873, "小说")],
        events=[(1840, "生于巴黎", "birth"),
                (1902, "卒于巴黎（煤气中毒）", "death"),
                (1898, "发表《我控诉》公开信，为德雷福斯辩护", "life")],
    ),
    dict(
        name="Guy de Maupassant", name_zh="莫泊桑",
        birth=1850, death=1893, nationality="法国",
        bio_zh="法国短篇小说之王，师承福楼拜，以十年时间创作逾三百篇短篇小说，构建了西方短篇小说的基本范式。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Guy_de_Maupassant_%281888%29.jpg/330px-Guy_de_Maupassant_%281888%29.jpg",
        tags=["现实主义", "法国文学", "短篇小说"],
        works=[("The Necklace", "《项链》", 1884, "短篇小说"),
               ("Boule de Suif", "《羊脂球》", 1880, "短篇小说"),
               ("Bel-Ami", "《漂亮朋友》", 1885, "小说"),
               ("Une Vie", "《一生》", 1883, "小说")],
        events=[(1850, "生于迪耶普附近", "birth"),
                (1893, "卒于巴黎（精神错乱）", "death"),
                (1880, "《羊脂球》发表，一举成名", "life")],
    ),
    dict(
        name="Maxim Gorky", name_zh="高尔基",
        birth=1868, death=1936, nationality="俄国/苏联",
        bio_zh="苏联文学奠基人，无产阶级文学最重要代表，自学成才的流浪者以笔书写底层人民的苦难与尊严，《母亲》是社会主义现实主义文学的标志之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Maxim_Gorky_LOC_25382u.jpg/330px-Maxim_Gorky_LOC_25382u.jpg",
        tags=["现实主义", "俄国文学", "无产阶级文学"],
        works=[("The Lower Depths", "《底层》", 1902, "戏剧"),
               ("Mother", "《母亲》", 1906, "小说"),
               ("My Childhood", "《童年》", 1913, "自传体小说"),
               ("My Universities", "《我的大学》", 1923, "自传体小说")],
        events=[(1868, "生于下诺夫哥罗德", "birth"),
                (1936, "卒于莫斯科", "death"),
                (1906, "《母亲》在美国出版，引发国际关注", "life"),
                (1934, "主持第一次苏联作家代表大会，确立社会主义现实主义", "life")],
    ),
    dict(
        name="Samuel Beckett", name_zh="贝克特",
        birth=1906, death=1989, nationality="爱尔兰",
        bio_zh="爱尔兰荒诞派戏剧大师，《等待戈多》以极简的戏剧形式触及存在的荒诞与虚无，1969年获诺贝尔文学奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Samuel_Beckett%2C_Pic%2C_1_.jpg/330px-Samuel_Beckett%2C_Pic%2C_1_.jpg",
        tags=["荒诞派", "爱尔兰文学", "现代主义"],
        works=[("Waiting for Godot", "《等待戈多》", 1953, "戏剧"),
               ("Endgame", "《终局》", 1957, "戏剧"),
               ("Molloy", "《莫洛伊》", 1951, "小说"),
               ("Murphy", "《墨菲》", 1938, "小说")],
        events=[(1906, "生于都柏林附近", "birth"),
                (1989, "卒于巴黎", "death"),
                (1953, "《等待戈多》巴黎首演，引发轰动", "life"),
                (1969, "获诺贝尔文学奖，拒绝亲赴典礼", "life")],
    ),
    dict(
        name="Vladimir Nabokov", name_zh="纳博科夫",
        birth=1899, death=1977, nationality="俄裔美国",
        bio_zh="俄裔美国作家，以英俄双语写作，《洛丽塔》在震惊世界的同时展示了其登峰造极的文学技巧，被视为20世纪最重要的英语小说之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Vladimir_Nabokov_1973.jpg/330px-Vladimir_Nabokov_1973.jpg",
        tags=["现代主义", "美国文学", "俄国文学"],
        works=[("Lolita", "《洛丽塔》", 1955, "小说"),
               ("Pale Fire", "《微暗的火》", 1962, "小说"),
               ("Speak, Memory", "《说吧，记忆》", 1951, "回忆录"),
               ("The Gift", "《天赋》", 1938, "小说")],
        events=[(1899, "生于圣彼得堡", "birth"),
                (1977, "卒于蒙特勒", "death"),
                (1919, "俄国革命后流亡欧洲", "life"),
                (1940, "移居美国，转用英语写作", "life"),
                (1955, "《洛丽塔》在巴黎出版后引发全球争议", "life")],
    ),
    # ── 中国现代文学（五四—1949）──────────────────────────────────────────────
    dict(
        name="Ding Ling", name_zh="丁玲",
        birth=1904, death=1986, nationality="中国",
        bio_zh="中国现代女性文学先驱，早期以《莎菲女士的日记》展现五四女性的精神困境，后转向革命文学，以《太阳照在桑干河上》获斯大林文学奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Ding_Ling.jpg/330px-Ding_Ling.jpg",
        tags=["中国现代文学", "女性文学", "革命文学"],
        works=[("Miss Sophie's Diary", "《莎菲女士的日记》", 1928, "中篇小说"),
               ("The Sun Shines over the Sanggan River", "《太阳照在桑干河上》", 1948, "小说")],
        events=[(1904, "生于湖南临澧", "birth"),
                (1986, "卒于北京", "death"),
                (1928, "《莎菲女士的日记》发表，轰动文坛", "life"),
                (1951, "《太阳照在桑干河上》获斯大林文学奖", "life"),
                (1957, "被错划为右派", "life")],
    ),
    dict(
        name="Zhao Shuli", name_zh="赵树理",
        birth=1906, death=1970, nationality="中国",
        bio_zh="中国解放区文学代表作家，以农民熟悉的语言和故事形式创作，《小二黑结婚》《李有才板话》开创'山药蛋派'文学风格。",
        portrait_url=None,
        tags=["中国现代文学", "解放区文学", "农村题材"],
        works=[("Xiao Erhei's Marriage", "《小二黑结婚》", 1943, "中篇小说"),
               ("The Rhymes of Li Youcai", "《李有才板话》", 1943, "小说"),
               ("Changes in Li Village", "《李家庄的变迁》", 1945, "小说")],
        events=[(1906, "生于山西沁水", "birth"),
                (1970, "文化大革命中被迫害致死", "death"),
                (1943, "《小二黑结婚》出版，毛泽东称赞其为文艺方向", "life")],
    ),
    # ── 中国当代文学（新时期 1978— ）──────────────────────────────────────────
    dict(
        name="Lu Yao", name_zh="路遥",
        birth=1949, death=1992, nationality="中国",
        bio_zh="中国当代著名作家，以《平凡的世界》描绘1975—1985年陕北农村青年的奋斗历程，激励数代中国读者，获茅盾文学奖。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/9f510fb30f2442a7d9330ad2de43ad4bd11373f0?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "现实主义", "茅盾文学奖"],
        works=[("Life", "《人生》", 1982, "中篇小说"),
               ("An Ordinary World", "《平凡的世界》", 1988, "小说")],
        events=[(1949, "生于陕西清涧", "birth"),
                (1992, "因肝病卒于西安，年仅42岁", "death"),
                (1988, "《平凡的世界》出版，获第三届茅盾文学奖", "life")],
    ),
    dict(
        name="Chen Zhongshi", name_zh="陈忠实",
        birth=1942, death=2016, nationality="中国",
        bio_zh="中国当代著名作家，历时六年创作《白鹿原》，以渭河平原半个世纪的沧桑变迁展现中华民族的文化心理，获茅盾文学奖。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/8601a18b87d6277f9e2f9c5e28381f30e924fc1?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "现实主义", "茅盾文学奖"],
        works=[("White Deer Plain", "《白鹿原》", 1993, "小说")],
        events=[(1942, "生于陕西西安灞桥区", "birth"),
                (2016, "卒于西安", "death"),
                (1993, "《白鹿原》出版，获第四届茅盾文学奖", "life")],
    ),
    dict(
        name="Jia Pingwa", name_zh="贾平凹",
        birth=1952, death=None, nationality="中国",
        bio_zh="中国当代文学重要作家，以商州系列和《废都》《秦腔》《古炉》等长篇深刻描绘中国西北的历史与现实，多次获茅盾文学奖提名。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Jia_Pingwa_at_the_2019_Guadalajara_International_Book_Fair.jpg/330px-Jia_Pingwa_at_the_2019_Guadalajara_International_Book_Fair.jpg",
        tags=["中国当代文学", "秦派文学"],
        works=[("Ruined Capital", "《废都》", 1993, "小说"),
               ("Shaanxi Opera", "《秦腔》", 2005, "小说"),
               ("Ancient Stove", "《古炉》", 2011, "小说"),
               ("Happy Dreams", "《高兴》", 2007, "小说")],
        events=[(1952, "生于陕西商洛", "birth"),
                (1993, "《废都》出版，引发广泛争议", "life"),
                (2008, "《秦腔》获第七届茅盾文学奖", "life")],
    ),
    dict(
        name="Wang Anyi", name_zh="王安忆",
        birth=1954, death=None, nationality="中国",
        bio_zh="中国当代著名女作家，以《长恨歌》将上海弄堂生活与历史变迁融为一体，是新时期中国女性文学的重要代言人。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Wang_Anyi_%28%E7%8E%8B%E5%AE%89%E5%BF%86%29.jpg/330px-Wang_Anyi_%28%E7%8E%8B%E5%AE%89%E5%BF%86%29.jpg",
        tags=["中国当代文学", "女性文学", "上海书写"],
        works=[("Song of Everlasting Sorrow", "《长恨歌》", 1995, "小说"),
               ("Brocade Valley", "《富萍》", 2000, "小说"),
               ("The Age of Enlightenment", "《启蒙时代》", 2007, "小说")],
        events=[(1954, "生于南京，成长于上海", "birth"),
                (1995, "《长恨歌》出版，获茅盾文学奖", "life"),
                (2004, "当选中国作家协会副主席", "life")],
    ),
    dict(
        name="Shi Tiesheng", name_zh="史铁生",
        birth=1951, death=2010, nationality="中国",
        bio_zh="中国当代著名作家，21岁因病致残，在轮椅上完成了对生命意义的深刻追问，《我与地坛》是中国散文的传世之作。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/63d0f703918fa0ec08fad71a2e9759ee3d6ddb80?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "散文", "生命哲学"],
        works=[("My Altar of the Earth", "《我与地坛》", 1991, "散文"),
               ("Notes on Illness", "《病隙碎笔》", 2002, "随笔"),
               ("The Destiny of Storytelling", "《务虚笔记》", 1996, "小说")],
        events=[(1951, "生于北京", "birth"),
                (2010, "卒于北京", "death"),
                (1972, "因脊椎病致双腿瘫痪", "life"),
                (1991, "《我与地坛》发表，引起强烈反响", "life")],
    ),
    dict(
        name="Tie Ning", name_zh="铁凝",
        birth=1957, death=None, nationality="中国",
        bio_zh="中国当代重要女作家，现任中国作家协会主席，以《哦，香雪》《玫瑰门》《大浴女》深刻描绘中国女性的生命体验。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/8ad4b31c8701a18b87d6520c1b9fe9cdd4110c74?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "女性文学"],
        works=[("Oh, Xiangxue", "《哦，香雪》", 1982, "短篇小说"),
               ("Rose Gate", "《玫瑰门》", 1988, "小说"),
               ("The Great Bathing Woman", "《大浴女》", 2000, "小说")],
        events=[(1957, "生于北京", "birth"),
                (1982, "《哦，香雪》获全国优秀短篇小说奖", "life"),
                (2006, "当选中国作家协会主席", "life")],
    ),
    dict(
        name="Ah Cheng", name_zh="阿城",
        birth=1949, death=None, nationality="中国",
        bio_zh="中国寻根文学代表作家，以《棋王》将中国传统文化精髓融入当代叙事，语言简洁凝练，标志着新时期文学的重要转折。",
        portrait_url=None,
        tags=["中国当代文学", "寻根文学"],
        works=[("Chess King", "《棋王》", 1984, "中篇小说"),
               ("Tree King", "《树王》", 1985, "中篇小说"),
               ("Child King", "《孩子王》", 1985, "中篇小说")],
        events=[(1949, "生于北京", "birth"),
                (1984, "《棋王》发表，引发寻根文学思潮", "life")],
    ),
    dict(
        name="Chi Zijian", name_zh="迟子建",
        birth=1964, death=None, nationality="中国",
        bio_zh="中国当代著名女作家，以东北边地的自然景观与民间传说为底色，《额尔古纳河右岸》荣获茅盾文学奖，展现鄂温克族百年历史。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/1ad5ad6eddc451da857dfaa8b0fd5266d0163233?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "东北文学", "茅盾文学奖"],
        works=[("The Right Bank of the Argun River", "《额尔古纳河右岸》", 2005, "小说"),
               ("Puppet on a String", "《白雪乌鸦》", 2010, "小说")],
        events=[(1964, "生于黑龙江漠河", "birth"),
                (2005, "《额尔古纳河右岸》出版", "life"),
                (2008, "《额尔古纳河右岸》获第七届茅盾文学奖", "life")],
    ),
    dict(
        name="Bi Feiyu", name_zh="毕飞宇",
        birth=1964, death=None, nationality="中国",
        bio_zh="中国当代著名作家，以《推拿》深入盲人群体内部生活，荣获茅盾文学奖，被译介至多国，是中国当代文学走向世界的代表作家之一。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/f9dcd100baa1cd11728b1571b812c8fcc3ce2d78?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "茅盾文学奖"],
        works=[("Massage", "《推拿》", 2008, "小说"),
               ("The Moon Opera", "《青衣》", 2000, "中篇小说"),
               ("Jade Peony", "《玉米》", 2001, "中篇小说")],
        events=[(1964, "生于江苏兴化", "birth"),
                (2011, "《推拿》获第八届茅盾文学奖", "life")],
    ),
    dict(
        name="Yan Lianke", name_zh="阎连科",
        birth=1958, death=None, nationality="中国",
        bio_zh="中国当代重要作家，以神实主义手法揭示中国社会的荒诞与苦难，《受活》《丁庄梦》《日熄》在国际文学界引起广泛反响。",
        portrait_url="https://bkimg.cdn.bcebos.com/pic/a044ad345982b2b7ffd4e7a936adcbef76099b9f?x-bce-process=image/format,f_auto",
        tags=["中国当代文学", "神实主义"],
        works=[("Dream of Ding Village", "《丁庄梦》", 2006, "小说"),
               ("Lenin's Kisses", "《受活》", 2004, "小说"),
               ("The Day the Sun Died", "《日熄》", 2015, "小说")],
        events=[(1958, "生于河南嵩县", "birth"),
                (2014, "获卡夫卡文学奖", "life")],
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

            print(f"  添加: {a['name_zh']} ({a['birth']}–{a.get('death') or '今'})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
