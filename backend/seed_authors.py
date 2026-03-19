"""
作家年表 · 作家种子数据（第二批，约 35 位）
运行：python -m backend.seed_authors
"""
import asyncio
import os
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Author, Work, AuthorEvent

# ── 作家数据 ─────────────────────────────────────────────────────────────────
# (name, name_zh, birth, death, nationality, bio_zh, portrait_url, tags, works, events)
# works: list of (title, title_zh, year, genre)
# events: list of (year, event_zh, event_type)

AUTHORS = [
    # ── 西方现实主义 ──────────────────────────────────────────────────────────
    dict(
        name="Stendhal", name_zh="司汤达",
        birth=1783, death=1842, nationality="法国",
        bio_zh="法国现实主义小说奠基人，以精细的心理描写著称，代表作《红与黑》深刻揭示了复辟王朝时期的社会矛盾。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Stendhal.jpg/330px-Stendhal.jpg",
        tags=["现实主义", "法国文学", "心理小说"],
        works=[("The Red and the Black", "《红与黑》", 1830, "小说"),
               ("The Charterhouse of Parma", "《帕尔马修道院》", 1839, "小说")],
        events=[(1783, "生于格勒诺布尔", "birth"), (1842, "卒于巴黎", "death"),
                (1814, "拿破仑战败后开始文学创作", "life")],
    ),
    dict(
        name="Honoré de Balzac", name_zh="巴尔扎克",
        birth=1799, death=1850, nationality="法国",
        bio_zh="法国现实主义文学巨匠，以《人间喜剧》构建了波旁王朝时期法国社会的全景图，共创作近百部小说。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/%E5%A5%A5%C2%B7%E5%B7%B4%E5%B0%94%E6%89%8E%E5%85%8B.png/330px-%E5%A5%A5%C2%B7%E5%B7%B4%E5%B0%94%E6%89%8E%E5%85%8B.png",
        tags=["现实主义", "法国文学", "人间喜剧"],
        works=[("Père Goriot", "《高老头》", 1835, "小说"),
               ("Eugénie Grandet", "《欧也妮·葛朗台》", 1833, "小说"),
               ("Lost Illusions", "《幻灭》", 1843, "小说")],
        events=[(1799, "生于图尔", "birth"), (1850, "卒于巴黎", "death"),
                (1829, "开始构建《人间喜剧》体系", "life")],
    ),
    dict(
        name="Victor Hugo", name_zh="雨果",
        birth=1802, death=1885, nationality="法国",
        bio_zh="法国浪漫主义文学领袖，剧作家、诗人、小说家，以《巴黎圣母院》和《悲惨世界》名垂文学史。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Victor_Hugo_by_%C3%89tienne_Carjat_1876_-_full.jpg/330px-Victor_Hugo_by_%C3%89tienne_Carjat_1876_-_full.jpg",
        tags=["浪漫主义", "法国文学", "戏剧"],
        works=[("The Hunchback of Notre-Dame", "《巴黎圣母院》", 1831, "小说"),
               ("Les Misérables", "《悲惨世界》", 1862, "小说"),
               ("Hernani", "《欧那尼》", 1830, "戏剧")],
        events=[(1802, "生于贝桑松", "birth"), (1885, "卒于巴黎", "death"),
                (1851, "因反对拿破仑三世流亡海外", "life")],
    ),
    dict(
        name="Alexander Pushkin", name_zh="普希金",
        birth=1799, death=1837, nationality="俄国",
        bio_zh="俄国文学之父，现代俄语文学语言的奠基者，诗歌、小说、戏剧均有卓越成就，决斗中死亡。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Orest_Kiprensky_-_%D0%9F%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_%D0%BF%D0%BE%D1%8D%D1%82%D0%B0_%D0%90.%D0%A1.%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D0%B0_-_Google_Art_Project.jpg/330px-Orest_Kiprensky_-_%D0%9F%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_%D0%BF%D0%BE%D1%8D%D1%82%D0%B0_%D0%90.%D0%A1.%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D0%B0_-_Google_Art_Project.jpg",
        tags=["浪漫主义", "俄国文学", "诗歌"],
        works=[("Eugene Onegin", "《叶甫盖尼·奥涅金》", 1833, "诗体小说"),
               ("The Captain's Daughter", "《上尉的女儿》", 1836, "小说"),
               ("Boris Godunov", "《鲍里斯·戈都诺夫》", 1831, "戏剧")],
        events=[(1799, "生于莫斯科", "birth"), (1837, "决斗中中弹身亡", "death")],
    ),
    dict(
        name="Charles Dickens", name_zh="狄更斯",
        birth=1812, death=1870, nationality="英国",
        bio_zh="英国维多利亚时代最伟大的小说家，以幽默与批判精神描绘工业化时代的社会不公，深刻影响英语文学传统。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Dickens_Gurney_head.jpg/330px-Dickens_Gurney_head.jpg",
        tags=["现实主义", "英国文学", "批判现实主义"],
        works=[("Oliver Twist", "《雾都孤儿》", 1839, "小说"),
               ("A Tale of Two Cities", "《双城记》", 1859, "小说"),
               ("Great Expectations", "《远大前程》", 1861, "小说"),
               ("David Copperfield", "《大卫·科波菲尔》", 1850, "小说")],
        events=[(1812, "生于朴茨茅斯", "birth"), (1870, "卒于盖德山庄", "death"),
                (1824, "童年在皮鞋作坊做工，经历贫困", "life")],
    ),
    dict(
        name="Gustave Flaubert", name_zh="福楼拜",
        birth=1821, death=1880, nationality="法国",
        bio_zh="法国现实主义大师，以极致的艺术追求和客观叙事风格著称，《包法利夫人》是西方文学史上的里程碑。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Gustave_Flaubert.jpg/330px-Gustave_Flaubert.jpg",
        tags=["现实主义", "法国文学", "自然主义"],
        works=[("Madame Bovary", "《包法利夫人》", 1857, "小说"),
               ("Sentimental Education", "《情感教育》", 1869, "小说"),
               ("Salammbo", "《萨朗波》", 1862, "小说")],
        events=[(1821, "生于鲁昂", "birth"), (1880, "卒于克鲁瓦塞", "death"),
                (1857, "《包法利夫人》出版，遭受猥亵罪起诉但最终无罪", "life")],
    ),
    dict(
        name="Leo Tolstoy", name_zh="托尔斯泰",
        birth=1828, death=1910, nationality="俄国",
        bio_zh="俄国文学巨匠，以史诗规模描绘人类命运与历史，《战争与和平》《安娜·卡列尼娜》被列为世界文学巅峰之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Leo_Tolstoy_1908_Portrait_%283x4_cropped%29.jpg/330px-Leo_Tolstoy_1908_Portrait_%283x4_cropped%29.jpg",
        tags=["现实主义", "俄国文学", "道德哲学"],
        works=[("War and Peace", "《战争与和平》", 1869, "小说"),
               ("Anna Karenina", "《安娜·卡列尼娜》", 1878, "小说"),
               ("The Death of Ivan Ilyich", "《伊万·伊里奇之死》", 1886, "中篇小说"),
               ("Resurrection", "《复活》", 1899, "小说")],
        events=[(1828, "生于雅斯纳亚·波利亚纳庄园", "birth"),
                (1910, "离家出走后卒于阿斯塔波沃火车站", "death"),
                (1882, "精神危机，皈依基督教道德观", "life")],
    ),
    dict(
        name="Henrik Ibsen", name_zh="易卜生",
        birth=1828, death=1906, nationality="挪威",
        bio_zh="挪威剧作家，现代戏剧之父，以问题剧探讨个人自由、女性解放与社会虚伪，深刻影响20世纪戏剧传统。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Henrik_Ibsen_av_Eilif_Peterssen_1895.jpg/330px-Henrik_Ibsen_av_Eilif_Peterssen_1895.jpg",
        tags=["现实主义", "挪威文学", "现代戏剧"],
        works=[("A Doll's House", "《玩偶之家》", 1879, "戏剧"),
               ("Hedda Gabler", "《海达·高布乐》", 1890, "戏剧"),
               ("Ghosts", "《群鬼》", 1881, "戏剧"),
               ("The Wild Duck", "《野鸭》", 1884, "戏剧")],
        events=[(1828, "生于希恩", "birth"), (1906, "卒于克里斯蒂安尼亚（奥斯陆）", "death"),
                (1864, "离开挪威流亡欧洲长达27年", "life")],
    ),
    dict(
        name="Anton Chekhov", name_zh="契诃夫",
        birth=1860, death=1904, nationality="俄国",
        bio_zh="俄国短篇小说大师与剧作家，以简洁精准的笔墨揭示日常生活中的荒诞与悲凉，深刻影响现代短篇小说和戏剧创作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Anton_Chekhov_1889.jpg/330px-Anton_Chekhov_1889.jpg",
        tags=["现实主义", "俄国文学", "短篇小说"],
        works=[("The Cherry Orchard", "《樱桃园》", 1904, "戏剧"),
               ("The Seagull", "《海鸥》", 1896, "戏剧"),
               ("The Lady with the Dog", "《带狗的女人》", 1899, "短篇小说"),
               ("Ward No.6", "《第六病室》", 1892, "中篇小说")],
        events=[(1860, "生于塔甘罗格", "birth"), (1904, "卒于巴登韦勒", "death"),
                (1884, "医学院毕业，行医同时写作", "life")],
    ),
    dict(
        name="Nikolai Gogol", name_zh="果戈里",
        birth=1809, death=1852, nationality="俄国",
        bio_zh="俄国批判现实主义奠基人，以荒诞讽刺手法揭露沙俄官僚社会的腐败，《死魂灵》是俄国文学的奠基之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/3/31/NV_Gogol.png",
        tags=["现实主义", "俄国文学", "讽刺文学"],
        works=[("Dead Souls", "《死魂灵》", 1842, "小说"),
               ("The Overcoat", "《外套》", 1842, "短篇小说"),
               ("The Inspector General", "《钦差大臣》", 1836, "戏剧")],
        events=[(1809, "生于索罗钦齐", "birth"), (1852, "卒于莫斯科", "death"),
                (1836, "《钦差大臣》上演，引发轰动", "life")],
    ),
    dict(
        name="Marcel Proust", name_zh="普鲁斯特",
        birth=1871, death=1922, nationality="法国",
        bio_zh="法国意识流小说先驱，以七卷本《追忆似水年华》重新定义了时间、记忆与意识在文学中的表达方式。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Otto_Wegener_Proust_vers_1895_bis.jpg/330px-Otto_Wegener_Proust_vers_1895_bis.jpg",
        tags=["现代主义", "法国文学", "意识流"],
        works=[("In Search of Lost Time", "《追忆似水年华》", 1913, "小说")],
        events=[(1871, "生于巴黎", "birth"), (1922, "卒于巴黎", "death"),
                (1909, "开始创作《追忆似水年华》", "life")],
    ),
    dict(
        name="James Joyce", name_zh="乔伊斯",
        birth=1882, death=1941, nationality="爱尔兰",
        bio_zh="爱尔兰现代主义文学旗手，以《尤利西斯》将意识流技法推向极致，深刻改变了20世纪英语文学的面貌。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Revolutionary_Joyce_Better_Contrast.jpg/330px-Revolutionary_Joyce_Better_Contrast.jpg",
        tags=["现代主义", "爱尔兰文学", "意识流"],
        works=[("Dubliners", "《都柏林人》", 1914, "短篇小说集"),
               ("A Portrait of the Artist as a Young Man", "《一个青年艺术家的肖像》", 1916, "小说"),
               ("Ulysses", "《尤利西斯》", 1922, "小说"),
               ("Finnegans Wake", "《芬尼根守灵夜》", 1939, "小说")],
        events=[(1882, "生于都柏林", "birth"), (1941, "卒于苏黎世", "death"),
                (1904, "离开爱尔兰，开始流亡欧洲", "life")],
    ),
    dict(
        name="Jean-Paul Sartre", name_zh="萨特",
        birth=1905, death=1980, nationality="法国",
        bio_zh="法国存在主义哲学家与作家，以'存在先于本质'的哲学命题影响了整个20世纪的思想与文学，1964年拒绝诺贝尔奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jean_Paul_Sartre_1965.jpg/330px-Jean_Paul_Sartre_1965.jpg",
        tags=["存在主义", "法国文学", "哲学"],
        works=[("Nausea", "《恶心》", 1938, "小说"),
               ("No Exit", "《禁闭》", 1944, "戏剧"),
               ("Being and Nothingness", "《存在与虚无》", 1943, "哲学"),
               ("The Words", "《文字》", 1964, "自传")],
        events=[(1905, "生于巴黎", "birth"), (1980, "卒于巴黎", "death"),
                (1964, "拒绝诺贝尔文学奖", "life"),
                (1945, "创办《现代》杂志，推动存在主义思潮", "life")],
    ),
    # ── 中国现代文学 ──────────────────────────────────────────────────────────
    dict(
        name="Guo Moruo", name_zh="郭沫若",
        birth=1892, death=1978, nationality="中国",
        bio_zh="中国现代文学奠基人之一，诗人、剧作家、历史学家，以浪漫主义诗集《女神》开创中国新诗时代。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/2/26/Guo_Moruo.jpg",
        tags=["中国现代文学", "浪漫主义", "诗歌"],
        works=[("Goddess", "《女神》", 1921, "诗集"),
               ("Qu Yuan", "《屈原》", 1942, "话剧"),
               ("Cai Wenji", "《蔡文姬》", 1959, "话剧")],
        events=[(1892, "生于四川乐山", "birth"), (1978, "卒于北京", "death"),
                (1921, "出版《女神》，宣告中国新诗诞生", "life"),
                (1924, "翻译歌德《少年维特之烦恼》", "life")],
    ),
    dict(
        name="Mao Dun", name_zh="茅盾",
        birth=1896, death=1981, nationality="中国",
        bio_zh="中国现实主义文学巨匠，以《子夜》深刻揭示30年代中国民族工业的困境，是中国社会分析小说的代表人物。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/4/46/Mao_Dun.jpg",
        tags=["中国现代文学", "现实主义", "社会分析"],
        works=[("Midnight", "《子夜》", 1933, "小说"),
               ("Spring Silkworms", "《春蚕》", 1932, "短篇小说"),
               ("Disillusion", "《幻灭》", 1927, "小说")],
        events=[(1896, "生于浙江桐乡", "birth"), (1981, "卒于北京", "death"),
                (1921, "参与发起文学研究会", "life"),
                (1927, "大革命失败，开始创作《蚀》三部曲", "life")],
    ),
    dict(
        name="Xu Zhimo", name_zh="徐志摩",
        birth=1897, death=1931, nationality="中国",
        bio_zh="中国浪漫主义诗人，新月派代表人物，以优美流丽的诗歌语言著称，《再别康桥》是中国新诗的经典之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/%E5%BE%90%E5%BF%97%E6%91%A9%E8%82%96%E5%83%8F%E7%85%A7.jpg/330px-%E5%BE%90%E5%BF%97%E6%91%A9%E8%82%96%E5%83%8F%E7%85%A7.jpg",
        tags=["中国现代文学", "新月派", "诗歌"],
        works=[("Second Farewell to Cambridge", "《再别康桥》", 1928, "诗歌"),
               ("Zhimo's Poems", "《志摩的诗》", 1925, "诗集")],
        events=[(1897, "生于浙江海宁", "birth"), (1931, "因飞机失事卒于济南", "death"),
                (1921, "留学英国剑桥，结识英国文学界", "life")],
    ),
    dict(
        name="Cao Yu", name_zh="曹禺",
        birth=1910, death=1996, nationality="中国",
        bio_zh="中国现代戏剧奠基人，以《雷雨》《日出》《北京人》构建了中国现代话剧的高峰，被誉为中国的莎士比亚。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Young_Cao_Yu.jpg/330px-Young_Cao_Yu.jpg",
        tags=["中国现代文学", "话剧", "戏剧"],
        works=[("Thunderstorm", "《雷雨》", 1934, "话剧"),
               ("Sunrise", "《日出》", 1936, "话剧"),
               ("Peking Man", "《北京人》", 1940, "话剧"),
               ("The Wilderness", "《原野》", 1937, "话剧")],
        events=[(1910, "生于天津", "birth"), (1996, "卒于北京", "death"),
                (1934, "《雷雨》在南京首演，轰动剧坛", "life")],
    ),
    dict(
        name="Ai Qing", name_zh="艾青",
        birth=1910, death=1996, nationality="中国",
        bio_zh="中国现代诗歌旗手，以《大堰河——我的保姆》奠定诗名，其诗歌将现实主义与浪漫主义融为一体，影响深远。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/4/43/Ai_Qing_1929.jpg",
        tags=["中国现代文学", "诗歌", "现实主义"],
        works=[("Dayan He — My Wet Nurse", "《大堰河——我的保姆》", 1933, "诗歌"),
               ("I Love This Land", "《我爱这土地》", 1938, "诗歌"),
               ("Toward the Sun", "《向太阳》", 1938, "诗集")],
        events=[(1910, "生于浙江金华", "birth"), (1996, "卒于北京", "death"),
                (1932, "旅法期间因参加革命活动被捕入狱，狱中开始创作", "life"),
                (1957, "被错划为右派，下放劳改", "life")],
    ),
    dict(
        name="Su Tong", name_zh="苏童",
        birth=1963, death=None, nationality="中国",
        bio_zh="中国先锋文学代表作家，以细腻感性的笔触描绘江南历史与女性命运，《妻妾成群》改编为电影《大红灯笼高高挂》。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/%E8%8B%8F%E7%AB%A5_20230827.jpg/330px-%E8%8B%8F%E7%AB%A5_20230827.jpg",
        tags=["中国当代文学", "先锋文学", "新历史主义"],
        works=[("Wives and Concubines", "《妻妾成群》", 1990, "中篇小说"),
               ("Rice", "《米》", 1991, "小说"),
               ("My Life as Emperor", "《我的帝王生涯》", 1992, "小说"),
               ("Binu and the Great Wall", "《碧奴》", 2006, "小说")],
        events=[(1963, "生于苏州", "birth"),
                (1987, "加入先锋文学运动", "life"),
                (1991, "《妻妾成群》改编为电影《大红灯笼高高挂》", "life")],
    ),
    dict(
        name="Mo Yan", name_zh="莫言",
        birth=1955, death=None, nationality="中国",
        bio_zh="中国当代文学旗帜，以魔幻现实主义手法书写高密东北乡的历史，2012年获诺贝尔文学奖，是首位获此殊荣的中国籍作家。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/MoYan_Hamburg_2008.jpg/330px-MoYan_Hamburg_2008.jpg",
        tags=["中国当代文学", "魔幻现实主义", "诺贝尔奖"],
        works=[("Red Sorghum", "《红高粱家族》", 1986, "小说"),
               ("The Garlic Ballads", "《天堂蒜薹之歌》", 1988, "小说"),
               ("Big Breasts and Wide Hips", "《丰乳肥臀》", 1996, "小说"),
               ("Life and Death Are Wearing Me Out", "《生死疲劳》", 2006, "小说"),
               ("Frog", "《蛙》", 2009, "小说")],
        events=[(1955, "生于山东高密", "birth"),
                (1986, "《红高粱家族》出版，引起轰动", "life"),
                (1988, "张艺谋将《红高粱》搬上银幕，获柏林金熊奖", "life"),
                (2012, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Han Shaogong", name_zh="韩少功",
        birth=1953, death=None, nationality="中国",
        bio_zh="中国寻根文学代表作家，以《爸爸爸》开创寻根文学运动，探索中华文化的深层心理结构与历史积淀。",
        portrait_url=None,
        tags=["中国当代文学", "寻根文学"],
        works=[("Pa Pa Pa", "《爸爸爸》", 1985, "中篇小说"),
               ("A Dictionary of Maqiao", "《马桥词典》", 1996, "小说")],
        events=[(1953, "生于湖南长沙", "birth"),
                (1985, "发表《文学的根》，宣告寻根文学运动", "life")],
    ),
    dict(
        name="Ge Fei", name_zh="格非",
        birth=1964, death=None, nationality="中国",
        bio_zh="中国先锋文学重要作家，以叙事迷宫和时间错位著称，《迷舟》确立其先锋地位，后期转向长篇历史叙事。",
        portrait_url=None,
        tags=["中国当代文学", "先锋文学"],
        works=[("Lost Boat", "《迷舟》", 1987, "短篇小说"),
               ("Peach Blossom Beauty", "《人面桃花》", 2004, "小说"),
               ("Spring Flowers, Autumn Moon", "《山河入梦》", 2007, "小说")],
        events=[(1964, "生于江苏丹徒", "birth"),
                (1987, "《迷舟》发表，跻身先锋文学核心", "life")],
    ),
    dict(
        name="Liu Zhenyun", name_zh="刘震云",
        birth=1958, death=None, nationality="中国",
        bio_zh="中国当代著名小说家，以幽默犀利的笔法描绘中国基层官场与市井生活，代表作被多次改编为电影。",
        portrait_url=None,
        tags=["中国当代文学", "新写实主义"],
        works=[("I Am Not Madame Bovary", "《我不是潘金莲》", 2012, "小说"),
               ("A Word Is Worth Ten Thousand Words", "《一句顶一万句》", 2009, "小说"),
               ("Cell Phone", "《手机》", 2003, "小说")],
        events=[(1958, "生于河南延津", "birth"),
                (1991, "《单位》《一地鸡毛》发表，确立新写实主义风格", "life")],
    ),
]

# ── 种子脚本 ──────────────────────────────────────────────────────────────────

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
            # 检查是否已存在
            result = await session.execute(
                select(Author).where(Author.name_zh == a["name_zh"])
            )
            existing = result.scalar_one_or_none()
            if existing:
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
            await session.flush()  # 获取 author.id

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
