"""
作家年表 · 第九批种子数据
来源：Modern Library 100 Best Novels 中尚未入库的作家
运行：python -m backend.seed_authors9
"""
import asyncio, os, re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Author, Work, AuthorEvent

AUTHORS = [
    dict(
        name="Arthur Koestler", name_zh="科斯特勒",
        birth=1905, death=1983, nationality="英国",
        bio_zh="匈牙利裔英国作家，《中午的黑暗》以苏联政治清洗为背景，深刻解剖极权主义对人的精神摧残，是20世纪政治小说的巅峰之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/ArthurKoestler.jpg/330px-ArthurKoestler.jpg",
        tags=["政治小说", "英国文学", "反极权"],
        works=[("Darkness at Noon", "《中午的黑暗》", 1941, "小说"),
               ("Scum of the Earth", "《地球的渣滓》", 1941, "回忆录"),
               ("The Act of Creation", "《创造的行为》", 1964, "非虚构")],
        events=[(1905, "生于布达佩斯", "birth"), (1983, "与妻子在伦敦共同自杀（帕金森病晚期）", "death"),
                (1941, "《中午的黑暗》出版，引发欧洲轰动", "life"),
                (1938, "脱离共产党，流亡西欧", "life")],
    ),
    dict(
        name="Malcolm Lowry", name_zh="马尔科姆·洛里",
        birth=1909, death=1957, nationality="英国",
        bio_zh="英国小说家，《在火山下》以1938年墨西哥亡灵节为背景，以酗酒英国领事的末日独白，呈现灵魂在政治与个人双重崩溃中的挣扎，被誉为英语文学中最伟大的意识流小说之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Malcolm_Lowry.jpg/330px-Malcolm_Lowry.jpg",
        tags=["现代主义", "英国文学", "意识流"],
        works=[("Under the Volcano", "《在火山下》", 1947, "小说"),
               ("Ultramarine", "《超海》", 1933, "小说"),
               ("Hear Us O Lord from Heaven Thy Dwelling Place", "《天父啊，俯听我们》", 1961, "短篇集")],
        events=[(1909, "生于英格兰柴郡", "birth"), (1957, "卒于英格兰苏塞克斯（酗酒引发意外）", "death"),
                (1947, "《在火山下》出版，耗时十年修改", "life"),
                (1940, "定居加拿大不列颠哥伦比亚", "life")],
    ),
    dict(
        name="Samuel Butler", name_zh="塞缪尔·巴特勒",
        birth=1835, death=1902, nationality="英国",
        bio_zh="英国维多利亚时代作家，《众生之路》死后出版，以半自传形式批判英国宗教、家庭与教育的虚伪，超前于其时代，深刻影响了萧伯纳等后继作家。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Samuel_Butler_by_Charles_Gogin.jpg/330px-Samuel_Butler_by_Charles_Gogin.jpg",
        tags=["维多利亚", "英国文学", "社会批判"],
        works=[("The Way of All Flesh", "《众生之路》", 1903, "小说"),
               ("Erewhon", "《埃瑞璜》", 1872, "小说"),
               ("The Authoress of the Odyssey", "《奥德赛的女作者》", 1897, "非虚构")],
        events=[(1835, "生于诺丁汉郡", "birth"), (1902, "卒于伦敦", "death"),
                (1859, "移居新西兰经营羊场，后返英从事写作", "life")],
    ),
    dict(
        name="Robert Graves", name_zh="罗伯特·格雷夫斯",
        birth=1895, death=1985, nationality="英国",
        bio_zh="英国诗人与小说家，以古罗马历史小说《我，克劳迪亚斯》闻名，以皇帝克劳迪亚斯第一人称叙述罗马宫廷阴谋，兼具史诗厚重与推理悬疑。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Robert_Graves_1.jpg/330px-Robert_Graves_1.jpg",
        tags=["历史小说", "英国文学", "古典世界"],
        works=[("I, Claudius", "《我，克劳迪亚斯》", 1934, "小说"),
               ("Claudius the God", "《神圣的克劳迪亚斯》", 1934, "小说"),
               ("Goodbye to All That", "《再见这一切》", 1929, "回忆录"),
               ("The White Goddess", "《白色女神》", 1948, "诗学")],
        events=[(1895, "生于伦敦温布利", "birth"), (1985, "卒于西班牙马略卡岛", "death"),
                (1929, "一战回忆录《再见这一切》出版", "life"),
                (1934, "《我，克劳迪亚斯》出版并获霍桑登奖", "life")],
    ),
    dict(
        name="Richard Wright", name_zh="理查德·赖特",
        birth=1908, death=1960, nationality="美国",
        bio_zh="美国非裔作家，《土生子》以黑人青年比格·托马斯的愤怒与死亡，震撼美国社会，是20世纪非裔美国文学的里程碑，与鲍德温、艾里森并称非裔美国文学三巨头。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Richard_Wright_profile.jpg/330px-Richard_Wright_profile.jpg",
        tags=["现实主义", "美国文学", "非裔文学", "社会批判"],
        works=[("Native Son", "《土生子》", 1940, "小说"),
               ("Black Boy", "《黑孩子》", 1945, "自传"),
               ("The Outsider", "《局外人》", 1953, "小说")],
        events=[(1908, "生于密西西比州纳齐兹", "birth"), (1960, "卒于巴黎（心脏病）", "death"),
                (1940, "《土生子》出版成为畅销书", "life"),
                (1947, "移居巴黎，成为黑人流亡文学代表", "life")],
    ),
    dict(
        name="John Dos Passos", name_zh="多斯·帕索斯",
        birth=1896, death=1970, nationality="美国",
        bio_zh="美国现代主义作家，《美国三部曲》融合新闻片段、传记、意识流与蒙太奇手法，构建20世纪初美国的全景史诗，被认为是形式最为激进的美国小说。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/John_Dos_Passos.jpg/330px-John_Dos_Passos.jpg",
        tags=["现代主义", "美国文学", "社会史诗"],
        works=[("U.S.A. Trilogy", "《美国三部曲》", 1938, "小说"),
               ("Three Soldiers", "《三个士兵》", 1921, "小说"),
               ("Manhattan Transfer", "《曼哈顿转运站》", 1925, "小说")],
        events=[(1896, "生于芝加哥", "birth"), (1970, "卒于巴尔的摩", "death"),
                (1925, "《曼哈顿转运站》出版，确立文学地位", "life"),
                (1938, "三部曲完成，成为美国左翼文学代表", "life")],
    ),
    dict(
        name="Sherwood Anderson", name_zh="舍伍德·安德森",
        birth=1876, death=1941, nationality="美国",
        bio_zh="美国短篇小说家，《温斯堡，俄亥俄》以中西部小镇为背景，以片段式短篇刻画孤独灵魂的压抑与渴望，深刻影响了海明威、福克纳等一代作家。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Sherwood_Anderson.jpg/330px-Sherwood_Anderson.jpg",
        tags=["现实主义", "美国文学", "短篇小说"],
        works=[("Winesburg, Ohio", "《温斯堡，俄亥俄》", 1919, "短篇集"),
               ("Poor White", "《穷白人》", 1920, "小说"),
               ("Death in the Woods", "《林中之死》", 1933, "短篇集")],
        events=[(1876, "生于俄亥俄州卡姆登", "birth"), (1941, "卒于巴拿马（腹膜炎）", "death"),
                (1919, "《温斯堡，俄亥俄》出版，影响美国现代文学", "life")],
    ),
    dict(
        name="Ford Madox Ford", name_zh="福特·马多克斯·福特",
        birth=1873, death=1939, nationality="英国",
        bio_zh="英国现代主义作家，《好兵》以不可靠叙述者讲述四段情感的纠缠与崩溃，是心理现实主义的先驱；《行进的终点》四部曲是一战文学的巅峰之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Ford_Madox_Ford_by_E.O._Hoppé%2C_1920.jpg/330px-Ford_Madox_Ford_by_E.O._Hoppé%2C_1920.jpg",
        tags=["现代主义", "英国文学", "一战文学"],
        works=[("The Good Soldier", "《好兵》", 1915, "小说"),
               ("Parade's End", "《行进的终点》", 1928, "小说"),
               ("Some Do Not...", "《有人不…》", 1924, "小说")],
        events=[(1873, "生于英格兰梅顿", "birth"), (1939, "卒于法国德诺（心脏病）", "death"),
                (1908, "创办《英国评论》，出版劳伦斯、托马斯·哈代等人作品", "life"),
                (1915, "《好兵》出版，奠定现代主义大师地位", "life")],
    ),
    dict(
        name="Evelyn Waugh", name_zh="伊夫林·沃",
        birth=1903, death=1966, nationality="英国",
        bio_zh="英国讽刺小说家，以锋利的笔触解剖英国上流社会的荒诞，《衰亡》《一抔土》《故园风雨后》是其代表作，晚期转向天主教信仰的严肃主题。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Evelyn_Waugh_-_retouched.jpg/330px-Evelyn_Waugh_-_retouched.jpg",
        tags=["讽刺", "英国文学", "社会批判"],
        works=[("A Handful of Dust", "《一抔土》", 1934, "小说"),
               ("Brideshead Revisited", "《故园风雨后》", 1945, "小说"),
               ("Scoop", "《独家新闻》", 1938, "小说"),
               ("Decline and Fall", "《衰亡》", 1928, "小说")],
        events=[(1903, "生于伦敦汉普斯特德", "birth"), (1966, "卒于萨默塞特（心脏病）", "death"),
                (1930, "皈依天主教，影响后期创作", "life"),
                (1945, "《故园风雨后》出版，成为最受欢迎的英国小说之一", "life")],
    ),
    dict(
        name="Thornton Wilder", name_zh="桑顿·怀尔德",
        birth=1897, death=1975, nationality="美国",
        bio_zh="美国小说家与剧作家，《圣路易斯雷大桥》以1714年秘鲁桥梁坍塌事件探讨命运与意义，《我们的小镇》是美国戏剧经典。曾获三届普利策奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Thornton_Wilder.jpg/330px-Thornton_Wilder.jpg",
        tags=["现代主义", "美国文学", "哲学小说"],
        works=[("The Bridge of San Luis Rey", "《圣路易斯雷大桥》", 1927, "小说"),
               ("Our Town", "《我们的小镇》", 1938, "戏剧"),
               ("The Ides of March", "《三月的思想》", 1948, "小说")],
        events=[(1897, "生于威斯康星州麦迪逊", "birth"), (1975, "卒于康涅狄格州（心脏病）", "death"),
                (1928, "《圣路易斯雷大桥》获普利策小说奖", "life"),
                (1938, "《我们的小镇》获普利策戏剧奖", "life")],
    ),
    dict(
        name="Anthony Burgess", name_zh="安东尼·伯吉斯",
        birth=1917, death=1993, nationality="英国",
        bio_zh="英国小说家，《发条橙》以未来黑帮少年亚历克斯的暴力与改造，质疑自由意志与国家权力的边界，斯坦利·库布里克改编的电影使其成为文化图腾。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Anthony_Burgess.jpg/330px-Anthony_Burgess.jpg",
        tags=["反乌托邦", "英国文学", "语言实验"],
        works=[("A Clockwork Orange", "《发条橙》", 1962, "小说"),
               ("Earthly Powers", "《尘世的权力》", 1980, "小说"),
               ("The Wanting Seed", "《渴望之种》", 1962, "小说")],
        events=[(1917, "生于曼彻斯特", "birth"), (1993, "卒于伦敦（肺癌）", "death"),
                (1962, "《发条橙》出版，因内容激烈引发广泛争议", "life"),
                (1971, "库布里克根据《发条橙》拍摄同名电影", "life")],
    ),
    dict(
        name="Sinclair Lewis", name_zh="辛克莱·刘易斯",
        birth=1885, death=1951, nationality="美国",
        bio_zh="美国现实主义作家，首位获诺贝尔文学奖的美国人，《大街》《巴比特》尖锐解剖美国中产阶级的精神空洞与小镇文化的压抑。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Sinclair_Lewis_1914.jpg/330px-Sinclair_Lewis_1914.jpg",
        tags=["现实主义", "美国文学", "社会批判"],
        works=[("Main Street", "《大街》", 1920, "小说"),
               ("Babbitt", "《巴比特》", 1922, "小说"),
               ("Elmer Gantry", "《爱尔默·甘特里》", 1927, "小说"),
               ("Arrowsmith", "《阿罗史密斯》", 1925, "小说")],
        events=[(1885, "生于明尼苏达州索克森特", "birth"), (1951, "卒于罗马（心脏病）", "death"),
                (1930, "获诺贝尔文学奖，是美国首位获此殊荣者", "life"),
                (1920, "《大街》出版，引发全美关于小镇生活的大讨论", "life")],
    ),
    dict(
        name="Willa Cather", name_zh="薇拉·凯瑟",
        birth=1873, death=1947, nationality="美国",
        bio_zh="美国作家，以描写美国内布拉斯加大草原移民生活著称，《啊，拓荒者！》《我的安东尼亚》是美国边疆文学的经典，以诗意笔触赞颂女性的坚韧与大地之美。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Willacather.jpg/330px-Willacather.jpg",
        tags=["现实主义", "美国文学", "移民文学", "女性文学"],
        works=[("Death Comes for the Archbishop", "《大主教之死》", 1927, "小说"),
               ("My Ántonia", "《我的安东尼亚》", 1918, "小说"),
               ("O Pioneers!", "《啊，拓荒者！》", 1913, "小说"),
               ("The Professor's House", "《教授之家》", 1925, "小说")],
        events=[(1873, "生于弗吉尼亚州温彻斯特", "birth"), (1947, "卒于纽约", "death"),
                (1923, "《一个失去的女士》获普利策奖", "life"),
                (1927, "《大主教之死》出版，被认为是其最成熟之作", "life")],
    ),
    dict(
        name="John Cheever", name_zh="约翰·契弗",
        birth=1912, death=1982, nationality="美国",
        bio_zh="美国短篇小说大师，被誉为「郊区的契诃夫」，以精致的短篇解剖美国中产阶级郊区生活中的虚伪、孤独与欲望，《游泳者》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/John_Cheever_1979.jpg/330px-John_Cheever_1979.jpg",
        tags=["现实主义", "美国文学", "短篇小说", "郊区文学"],
        works=[("The Wapshot Chronicle", "《瓦普肖特纪事》", 1957, "小说"),
               ("The Stories of John Cheever", "《约翰·契弗短篇小说集》", 1978, "短篇集"),
               ("Falconer", "《猎鹰者》", 1977, "小说")],
        events=[(1912, "生于马萨诸塞州昆西", "birth"), (1982, "卒于纽约奥西宁（癌症）", "death"),
                (1978, "短篇集出版，获普利策奖和国家书评奖", "life")],
    ),
    dict(
        name="Dashiell Hammett", name_zh="达希尔·哈米特",
        birth=1894, death=1961, nationality="美国",
        bio_zh="美国硬汉派犯罪小说鼻祖，《马耳他之鹰》《血腥的收获》开创美式侦探小说风格，以冷峻简洁的语言和道德含糊的人物影响了雷蒙德·钱德勒乃至后世无数作家。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Dashiell_Hammett.jpg/330px-Dashiell_Hammett.jpg",
        tags=["犯罪小说", "美国文学", "硬汉派"],
        works=[("The Maltese Falcon", "《马耳他之鹰》", 1930, "小说"),
               ("The Thin Man", "《瘦子》", 1934, "小说"),
               ("Red Harvest", "《血腥的收获》", 1929, "小说")],
        events=[(1894, "生于马里兰州圣玛丽县", "birth"), (1961, "卒于纽约（肺癌）", "death"),
                (1930, "《马耳他之鹰》出版，确立硬汉侦探小说风格", "life"),
                (1951, "麦卡锡时代以拒绝配合调查被投入监狱", "life")],
    ),
    dict(
        name="Muriel Spark", name_zh="缪丽尔·斯帕克",
        birth=1918, death=2006, nationality="英国",
        bio_zh="英国小说家，《布罗迪小姐的青春》以苏格兰女教师的狂热自恋与学生的背叛为核心，是战后英国文学中最精致、最具讽刺力量的作品之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Muriel_Spark.jpg/330px-Muriel_Spark.jpg",
        tags=["讽刺", "英国文学", "女性文学"],
        works=[("The Prime of Miss Jean Brodie", "《布罗迪小姐的青春》", 1961, "小说"),
               ("The Mandelbaum Gate", "《曼德尔鲍姆之门》", 1965, "小说"),
               ("Memento Mori", "《勿忘你终有一死》", 1959, "小说")],
        events=[(1918, "生于爱丁堡", "birth"), (2006, "卒于意大利佛罗伦萨", "death"),
                (1961, "《布罗迪小姐的青春》出版，奠定其文学地位", "life"),
                (1954, "皈依天主教，影响其后期创作方向", "life")],
    ),
    dict(
        name="Jean Rhys", name_zh="简·里斯",
        birth=1890, death=1979, nationality="英国",
        bio_zh="多米尼加裔英国作家，《藻海无边》是对《简·爱》的后殖民重写，以伯莎·梅森的视角颠覆了维多利亚文学的帝国叙事，是女性主义与后殖民文学的经典。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Jean_Rhys.jpg/330px-Jean_Rhys.jpg",
        tags=["现代主义", "英国文学", "后殖民文学", "女性文学"],
        works=[("Wide Sargasso Sea", "《藻海无边》", 1966, "小说"),
               ("Good Morning, Midnight", "《早安，午夜》", 1939, "小说"),
               ("Voyage in the Dark", "《黑暗中的航行》", 1934, "小说")],
        events=[(1890, "生于多米尼加罗索", "birth"), (1979, "卒于英格兰埃克塞特", "death"),
                (1966, "《藻海无边》出版，结束沉寂27年，震撼文坛", "life")],
    ),
    dict(
        name="William Styron", name_zh="威廉·斯泰伦",
        birth=1925, death=2006, nationality="美国",
        bio_zh="美国南方作家，《苏菲的选择》以奥斯维辛幸存者的故事探讨历史创伤与个人罪责，是美国战后文学中最具震撼力的作品之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/William_Styron.jpg/330px-William_Styron.jpg",
        tags=["现实主义", "美国文学", "南方文学", "二战文学"],
        works=[("Sophie's Choice", "《苏菲的选择》", 1979, "小说"),
               ("Lie Down in Darkness", "《躺在黑暗中》", 1951, "小说"),
               ("The Confessions of Nat Turner", "《纳特·特纳的自白》", 1967, "小说"),
               ("Darkness Visible", "《可见的黑暗》", 1990, "回忆录")],
        events=[(1925, "生于弗吉尼亚州纽波特纽斯", "birth"), (2006, "卒于马萨诸塞州（肺炎）", "death"),
                (1979, "《苏菲的选择》出版并获美国全国书评奖", "life"),
                (1967, "《纳特·特纳的自白》获普利策奖，引发关于种族书写权利的争论", "life")],
    ),
    dict(
        name="Paul Bowles", name_zh="保罗·鲍尔斯",
        birth=1910, death=1999, nationality="美国",
        bio_zh="美国作家与作曲家，长居摩洛哥丹吉尔，《遮蔽的天空》描写美国夫妇在撒哈拉沙漠的迷失与毁灭，是西方人在异域文化中自我消解的寓言。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Paul_Bowles_1993.jpg/330px-Paul_Bowles_1993.jpg",
        tags=["现代主义", "美国文学", "异域文学"],
        works=[("The Sheltering Sky", "《遮蔽的天空》", 1949, "小说"),
               ("Let It Come Down", "《随它去吧》", 1952, "小说"),
               ("The Delicate Prey", "《脆弱的猎物》", 1950, "短篇集")],
        events=[(1910, "生于纽约牙买加", "birth"), (1999, "卒于摩洛哥丹吉尔", "death"),
                (1947, "定居摩洛哥丹吉尔，此后终身居此", "life"),
                (1949, "《遮蔽的天空》出版，引发批评界轰动", "life")],
    ),
    dict(
        name="E. L. Doctorow", name_zh="多克托罗",
        birth=1931, death=2015, nationality="美国",
        bio_zh="美国历史小说家，《拉格泰姆时代》将虚构人物与历史名人（弗洛伊德、福特、杜·波依斯等）并置，以复调叙事重构20世纪初美国的阶级与种族矛盾。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Doctorow-2009.jpg/330px-Doctorow-2009.jpg",
        tags=["历史小说", "美国文学", "后现代"],
        works=[("Ragtime", "《拉格泰姆时代》", 1975, "小说"),
               ("Billy Bathgate", "《比利·巴斯盖特》", 1989, "小说"),
               ("The Book of Daniel", "《丹尼尔书》", 1971, "小说"),
               ("World's Fair", "《世博会》", 1985, "小说")],
        events=[(1931, "生于纽约布朗克斯", "birth"), (2015, "卒于纽约（肺癌）", "death"),
                (1975, "《拉格泰姆时代》出版，成为文学与流行文化的双重现象", "life")],
    ),
    dict(
        name="John Fowles", name_zh="约翰·福尔斯",
        birth=1926, death=2005, nationality="英国",
        bio_zh="英国后现代小说家，《大法师》《法国中尉的女人》是后现代文学的重要实验，以元小说手法打破叙事幻觉，《收藏家》则是心理惊悚的经典。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/John_Fowles.jpg/330px-John_Fowles.jpg",
        tags=["后现代", "英国文学", "元小说"],
        works=[("The Magus", "《大法师》", 1965, "小说"),
               ("The French Lieutenant's Woman", "《法国中尉的女人》", 1969, "小说"),
               ("The Collector", "《收藏家》", 1963, "小说")],
        events=[(1926, "生于英格兰埃塞克斯", "birth"), (2005, "卒于英格兰莱姆里吉斯", "death"),
                (1969, "《法国中尉的女人》出版，因元小说技巧震动文坛", "life")],
    ),
    dict(
        name="Robert Penn Warren", name_zh="罗伯特·潘·沃伦",
        birth=1905, death=1989, nationality="美国",
        bio_zh="美国南方作家、诗人，《国王的人马》以休伊·朗政治腐败为原型，探讨权力、理想与道德妥协，是美国政治小说的经典，并获普利策奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Robert_Penn_Warren_1980.jpg/330px-Robert_Penn_Warren_1980.jpg",
        tags=["现实主义", "美国文学", "南方文学", "政治小说"],
        works=[("All the King's Men", "《国王的人马》", 1946, "小说"),
               ("World Enough and Time", "《足够的世界和足够的时间》", 1950, "小说"),
               ("Band of Angels", "《天使群》", 1955, "小说")],
        events=[(1905, "生于肯塔基州格思里", "birth"), (1989, "卒于佛蒙特州（前列腺癌）", "death"),
                (1947, "《国王的人马》获普利策奖", "life"),
                (1986, "成为美国首位桂冠诗人", "life")],
    ),
    dict(
        name="Lawrence Durrell", name_zh="劳伦斯·达雷尔",
        birth=1912, death=1990, nationality="英国",
        bio_zh="英国作家，《亚历山大四部曲》以四部小说从不同视角讲述同一段故事，在地中海烈日下探讨爱欲与相对性，语言极富诗意，是英语文学中的感官盛宴。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Durrell_brothers.jpg/330px-Durrell_brothers.jpg",
        tags=["现代主义", "英国文学", "地中海文学"],
        works=[("Justine", "《贾斯汀》", 1957, "小说"),
               ("Balthazar", "《巴尔塔萨》", 1958, "小说"),
               ("The Alexandria Quartet", "《亚历山大四部曲》", 1960, "小说"),
               ("Bitter Lemons", "《苦柠檬》", 1957, "散文")],
        events=[(1912, "生于印度贾朗达尔", "birth"), (1990, "卒于法国（肺气肿）", "death"),
                (1957, "《贾斯汀》出版，亚历山大四部曲开篇", "life")],
    ),
    dict(
        name="Nathanael West", name_zh="纳撒尼尔·韦斯特",
        birth=1903, death=1940, nationality="美国",
        bio_zh="美国讽刺作家，《蝗虫之日》以好莱坞黄金时代的幻灭为背景，描绘梦想工厂下失落者的疯狂与暴力，是美国文学史上最黑暗的寓言之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Nathanael_West.jpg/330px-Nathanael_West.jpg",
        tags=["讽刺", "美国文学", "好莱坞"],
        works=[("The Day of the Locust", "《蝗虫之日》", 1939, "小说"),
               ("Miss Lonelyhearts", "《孤独芳心小姐》", 1933, "小说"),
               ("A Cool Million", "《一凉百万》", 1934, "小说")],
        events=[(1903, "生于纽约", "birth"), (1940, "卒于加利福尼亚（车祸）", "death"),
                (1939, "《蝗虫之日》出版，次年因车祸去世，年仅37岁", "life")],
    ),
    dict(
        name="Erskine Caldwell", name_zh="厄斯金·卡德威尔",
        birth=1903, death=1987, nationality="美国",
        bio_zh="美国南方作家，《烟草路》以乔治亚州贫困白人为主角，以粗粝写实的笔触描绘底层人的苦难与堕落，出版时引发巨大争议，也引发了关于南方贫困的社会讨论。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Erskine_Caldwell.jpg/330px-Erskine_Caldwell.jpg",
        tags=["现实主义", "美国文学", "南方文学"],
        works=[("Tobacco Road", "《烟草路》", 1932, "小说"),
               ("God's Little Acre", "《上帝的小小土地》", 1933, "小说")],
        events=[(1903, "生于佐治亚州怀特奥克斯", "birth"), (1987, "卒于亚利桑那州帕拉代斯谷", "death"),
                (1932, "《烟草路》出版，被指控淫秽，引发法律诉讼", "life")],
    ),
    dict(
        name="Walker Percy", name_zh="沃克·珀西",
        birth=1916, death=1990, nationality="美国",
        bio_zh="美国南方天主教作家，《影迷》以1960年代新奥尔良为背景，以一个迷失的股票经纪人探寻现代人的存在意义，是美国存在主义小说的代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Walker_Percy.jpg/330px-Walker_Percy.jpg",
        tags=["存在主义", "美国文学", "南方文学", "天主教文学"],
        works=[("The Moviegoer", "《影迷》", 1961, "小说"),
               ("The Last Gentleman", "《最后的绅士》", 1966, "小说"),
               ("Love in the Ruins", "《废墟中的爱情》", 1971, "小说")],
        events=[(1916, "生于亚拉巴马州伯明翰", "birth"), (1990, "卒于路易斯安那州科文顿（前列腺癌）", "death"),
                (1961, "《影迷》获全国书卷奖，奠定文学地位", "life"),
                (1954, "皈依天主教，影响其哲学与文学方向", "life")],
    ),
    dict(
        name="James T. Farrell", name_zh="詹姆斯·法雷尔",
        birth=1904, death=1979, nationality="美国",
        bio_zh="美国自然主义作家，《斯塔兹·朗尼根三部曲》以爱尔兰裔芝加哥工人阶级青年为主角，是美国城市底层生活的全景史诗，与德莱塞并列为美国自然主义顶峰。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/James_T._Farrell.jpg/330px-James_T._Farrell.jpg",
        tags=["自然主义", "美国文学", "工人阶级"],
        works=[("Studs Lonigan: A Trilogy", "《斯塔兹·朗尼根三部曲》", 1935, "小说"),
               ("Young Lonigan", "《年轻的朗尼根》", 1932, "小说"),
               ("Danny O'Neill series", "《丹尼·奥尼尔系列》", 1936, "小说")],
        events=[(1904, "生于芝加哥", "birth"), (1979, "卒于纽约（心脏病）", "death"),
                (1935, "三部曲完结出版，奠定其自然主义大师地位", "life")],
    ),
]


async def seed():
    raw_url = os.environ.get("DATABASE_URL", "")
    raw_url = re.sub(r"^postgresql(\+asyncpg)?://", "postgresql+asyncpg://", raw_url)
    raw_url = re.sub(r"[?&]sslmode=[^&]*", "", raw_url)
    raw_url = re.sub(r"[?&]channel_binding=[^&]*", "", raw_url)

    engine = create_async_engine(raw_url, echo=False, connect_args={"ssl": "require"})
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    added = skipped = 0
    async with Session() as session:
        for a in AUTHORS:
            exists = await session.scalar(select(Author).where(Author.name_zh == a["name_zh"]))
            if exists:
                print(f"  跳过: {a['name_zh']}")
                skipped += 1
                continue

            author = Author(
                name=a["name"], name_zh=a["name_zh"],
                birth=a["birth"], death=a.get("death"),
                nationality=a["nationality"],
                bio_zh=a.get("bio_zh", ""),
                portrait_url=a.get("portrait_url"),
                tags=a.get("tags", []),
            )
            session.add(author)
            await session.flush()

            for title, title_zh, year, genre in a.get("works", []):
                from .models import Work
                session.add(Work(author_id=author.id, title=title, title_zh=title_zh, year=year, genre=genre))
            for ev in a.get("events", []):
                from .models import AuthorEvent
                session.add(AuthorEvent(author_id=author.id, year=ev[0], event_zh=ev[1],
                                        event_type=ev[2] if len(ev) > 2 else "life"))

            print(f"  添加: {a['name_zh']} ({a['birth']}–{a.get('death') or '今'})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
