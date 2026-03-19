"""
作家年表 · 作家种子数据（第七批，45位）
覆盖：古典文学、中国古典、文艺复兴、启蒙时代、日本近现代、更多20世纪大师
运行：python -m backend.seed_authors7
"""
import asyncio, os, re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── 古希腊罗马 ────────────────────────────────────────────────────────────
    dict(
        name="Homer", name_zh="荷马",
        birth=-800, death=-701, nationality="古希腊",
        bio_zh="古希腊史诗诗人，相传为《伊利亚特》和《奥德赛》的作者，西方文学的源头，影响了整个西方文明的叙事传统。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Homer_British_Museum.jpg/330px-Homer_British_Museum.jpg",
        tags=["史诗", "古希腊文学", "口传文学"],
        works=[("Iliad", "《伊利亚特》", -750, "史诗"),
               ("Odyssey", "《奥德赛》", -725, "史诗")],
        events=[(-800, "约生于爱奥尼亚地区", "birth"), (-701, "约卒", "death")],
    ),
    dict(
        name="Sophocles", name_zh="索福克勒斯",
        birth=-496, death=-406, nationality="古希腊",
        bio_zh="古希腊三大悲剧诗人之一，将悲剧艺术推向顶峰，《俄狄浦斯王》被亚里士多德称为悲剧典范。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Sophocles_pushkin.jpg/330px-Sophocles_pushkin.jpg",
        tags=["悲剧", "古希腊文学", "戏剧"],
        works=[("Oedipus Rex", "《俄狄浦斯王》", -429, "悲剧"),
               ("Antigone", "《安提戈涅》", -441, "悲剧"),
               ("Electra", "《厄勒克特拉》", -410, "悲剧")],
        events=[(-496, "生于雅典附近科洛诺斯", "birth"), (-406, "卒于雅典", "death")],
    ),
    dict(
        name="Virgil", name_zh="维吉尔",
        birth=-70, death=-19, nationality="古罗马",
        bio_zh="古罗马最伟大的诗人，《埃涅阿斯纪》是拉丁文学的顶峰，但丁以其为向导游历地狱与炼狱。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Virgil_mosaic_-_Bardo_National_Museum.jpg/330px-Virgil_mosaic_-_Bardo_National_Museum.jpg",
        tags=["史诗", "古罗马文学", "诗歌"],
        works=[("Aeneid", "《埃涅阿斯纪》", -19, "史诗"),
               ("Georgics", "《农事诗》", -29, "诗歌"),
               ("Eclogues", "《牧歌》", -37, "诗歌")],
        events=[(-70, "生于曼图亚附近", "birth"), (-19, "卒于布林迪西", "death")],
    ),
    # ── 中世纪与文艺复兴 ──────────────────────────────────────────────────────
    dict(
        name="Dante Alighieri", name_zh="但丁",
        birth=1265, death=1321, nationality="意大利",
        bio_zh="意大利中世纪诗人，《神曲》是中世纪文学的顶峰，也是意大利语文学的奠基之作，被称为意大利语之父。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Dante_Alighieri_portrait_by_Giotto_di_Bondone_crop.jpg/330px-Dante_Alighieri_portrait_by_Giotto_di_Bondone_crop.jpg",
        tags=["中世纪文学", "意大利文学", "史诗"],
        works=[("Divine Comedy", "《神曲》", 1320, "史诗"),
               ("La Vita Nuova", "《新生》", 1295, "诗集")],
        events=[(1265, "生于佛罗伦萨", "birth"), (1321, "卒于拉文纳", "death"),
                (1302, "因政治原因被驱逐出佛罗伦萨，开始流亡", "life")],
    ),
    dict(
        name="Miguel de Cervantes", name_zh="塞万提斯",
        birth=1547, death=1616, nationality="西班牙",
        bio_zh="西班牙文艺复兴时期最重要的作家，《堂吉诃德》是西方文学史上第一部现代小说，影响了整个欧洲小说传统。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Cervantes_J%C3%A1uregui.jpg/330px-Cervantes_J%C3%A1uregui.jpg",
        tags=["文艺复兴", "西班牙文学", "小说"],
        works=[("Don Quixote", "《堂吉诃德》", 1605, "小说"),
               ("Exemplary Novels", "《模范小说》", 1613, "小说集")],
        events=[(1547, "生于阿尔卡拉-德-埃纳雷斯", "birth"), (1616, "卒于马德里", "death"),
                (1571, "参加勒班陀海战，左手致残", "life")],
    ),
    dict(
        name="William Shakespeare", name_zh="莎士比亚",
        birth=1564, death=1616, nationality="英国",
        bio_zh="英国文学史上最伟大的作家，人类历史上最杰出的戏剧家，37部戏剧、154首十四行诗影响了世界文学。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/330px-Shakespeare.jpg",
        tags=["文艺复兴", "英国文学", "戏剧", "诗歌"],
        works=[("Hamlet", "《哈姆雷特》", 1603, "悲剧"),
               ("King Lear", "《李尔王》", 1606, "悲剧"),
               ("Macbeth", "《麦克白》", 1606, "悲剧"),
               ("A Midsummer Night's Dream", "《仲夏夜之梦》", 1600, "喜剧")],
        events=[(1564, "生于英国斯特拉特福", "birth"), (1616, "卒于斯特拉特福", "death"),
                (1594, "成为环球剧院股东和主要剧作家", "life")],
    ),
    # ── 启蒙时代 ──────────────────────────────────────────────────────────────
    dict(
        name="Voltaire", name_zh="伏尔泰",
        birth=1694, death=1778, nationality="法国",
        bio_zh="法国启蒙运动领袖，以机智讽刺批判专制与宗教迷信，《老实人》是启蒙哲学小说的杰作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Atelier_de_Nicolas_de_Largilli%C3%A9re%2C_portrait_de_Voltaire_%28Institut_et_Mus%C3%A9e_Voltaire%29_-_002.jpg/330px-Atelier_de_Nicolas_de_Largilli%C3%A9re%2C_portrait_de_Voltaire_%28Institut_et_Mus%C3%A9e_Voltaire%29_-_002.jpg",
        tags=["启蒙运动", "法国文学", "哲学小说"],
        works=[("Candide", "《老实人》", 1759, "小说"),
               ("Zadig", "《扎第格》", 1748, "小说"),
               ("Letters Concerning the English Nation", "《英国书简》", 1733, "散文")],
        events=[(1694, "生于巴黎", "birth"), (1778, "卒于巴黎", "death"),
                (1726, "因冒犯贵族被流亡英国，受洛克思想影响", "life")],
    ),
    dict(
        name="Jean-Jacques Rousseau", name_zh="卢梭",
        birth=1712, death=1778, nationality="法国",
        bio_zh="法国启蒙思想家、文学家，《社会契约论》奠定民主政治理论，《忏悔录》开创现代自传文学，对浪漫主义影响深远。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Jean-Jacques_Rousseau_%28painted_portrait%29.jpg/330px-Jean-Jacques_Rousseau_%28painted_portrait%29.jpg",
        tags=["启蒙运动", "法国文学", "哲学"],
        works=[("The Social Contract", "《社会契约论》", 1762, "哲学"),
               ("Confessions", "《忏悔录》", 1782, "自传"),
               ("Emile", "《爱弥儿》", 1762, "教育哲学")],
        events=[(1712, "生于日内瓦", "birth"), (1778, "卒于埃尔莫农维尔", "death")],
    ),
    dict(
        name="Johann Wolfgang von Goethe", name_zh="歌德",
        birth=1749, death=1832, nationality="德国",
        bio_zh="德国文学最伟大的代表，《浮士德》是德语文学的顶峰，也是世界文学的巨著，《少年维特的烦恼》开创浪漫主义先河。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Goethe_%28Stieler_1828%29.jpg/330px-Goethe_%28Stieler_1828%29.jpg",
        tags=["德语文学", "古典主义", "浪漫主义"],
        works=[("Faust", "《浮士德》", 1832, "诗剧"),
               ("The Sorrows of Young Werther", "《少年维特的烦恼》", 1774, "小说"),
               ("Wilhelm Meister's Apprenticeship", "《威廉·迈斯特的学习年代》", 1796, "小说")],
        events=[(1749, "生于法兰克福", "birth"), (1832, "卒于魏玛", "death"),
                (1775, "应邀前往魏玛宫廷，此后定居魏玛", "life")],
    ),
    # ── 中国古典文学 ──────────────────────────────────────────────────────────
    dict(
        name="Cao Xueqin", name_zh="曹雪芹",
        birth=1715, death=1763, nationality="中国",
        bio_zh="中国古典小说巅峰《红楼梦》的作者，以贾府兴衰映照人生百态，被誉为中国文化的百科全书。",
        portrait_url=None,
        tags=["古典文学", "中国文学", "小说"],
        works=[("Dream of the Red Chamber", "《红楼梦》", 1791, "小说")],
        events=[(1715, "约生于南京", "birth"), (1763, "约卒于北京西山", "death"),
                (1744, "开始创作《红楼梦》，历时十年", "life")],
    ),
    dict(
        name="Wu Cheng'en", name_zh="吴承恩",
        birth=1500, death=1582, nationality="中国",
        bio_zh="中国明代小说家，《西游记》是中国古典四大名著之一，以唐僧取经为主线构建了瑰丽的神话世界。",
        portrait_url=None,
        tags=["古典文学", "中国文学", "神话小说"],
        works=[("Journey to the West", "《西游记》", 1592, "小说")],
        events=[(1500, "约生于淮安", "birth"), (1582, "约卒于淮安", "death")],
    ),
    dict(
        name="Luo Guanzhong", name_zh="罗贯中",
        birth=1330, death=1400, nationality="中国",
        bio_zh="中国元末明初小说家，《三国演义》是中国第一部长篇历史小说，也是古典四大名著之一。",
        portrait_url=None,
        tags=["古典文学", "中国文学", "历史小说"],
        works=[("Romance of the Three Kingdoms", "《三国演义》", 1522, "小说")],
        events=[(1330, "约生于山西太原", "birth"), (1400, "约卒", "death")],
    ),
    dict(
        name="Shi Nai'an", name_zh="施耐庵",
        birth=1296, death=1371, nationality="中国",
        bio_zh="中国元末明初小说家，《水浒传》是中国第一部以农民起义为题材的长篇小说，也是古典四大名著之一。",
        portrait_url=None,
        tags=["古典文学", "中国文学", "英雄小说"],
        works=[("Water Margin", "《水浒传》", 1589, "小说")],
        events=[(1296, "约生于江苏兴化", "birth"), (1371, "约卒", "death")],
    ),
    dict(
        name="Li Bai", name_zh="李白",
        birth=701, death=762, nationality="中国",
        bio_zh="唐代最伟大的浪漫主义诗人，被称为诗仙，一生创作诗歌千余首，以豪放飘逸著称，《静夜思》《将进酒》传诵千古。",
        portrait_url=None,
        tags=["诗歌", "中国文学", "唐诗", "浪漫主义"],
        works=[("Complete Works of Li Bai", "《李太白全集》", 762, "诗集"),
               ("Quiet Night Thoughts", "《静夜思》", 726, "诗"),
               ("Invitation to Wine", "《将进酒》", 752, "诗")],
        events=[(701, "生于碎叶城（今吉尔吉斯斯坦）", "birth"), (762, "卒于安徽当涂", "death"),
                (742, "受唐玄宗召见，供奉翰林", "life"),
                (744, "因得罪权贵被赐金放还", "life")],
    ),
    dict(
        name="Du Fu", name_zh="杜甫",
        birth=712, death=770, nationality="中国",
        bio_zh="唐代最伟大的现实主义诗人，被称为诗圣，以沉郁顿挫的风格记录安史之乱等历史，被誉为诗史。",
        portrait_url=None,
        tags=["诗歌", "中国文学", "唐诗", "现实主义"],
        works=[("Spring View", "《春望》", 757, "诗"),
               ("Three Officials and Three Farewells", "《三吏三别》", 759, "诗组"),
               ("Ballad of the Army Carts", "《兵车行》", 750, "诗")],
        events=[(712, "生于河南巩县", "birth"), (770, "卒于湖南耒阳", "death"),
                (755, "安史之乱爆发，开始颠沛流离的生涯", "life")],
    ),
    dict(
        name="Su Shi", name_zh="苏轼",
        birth=1037, death=1101, nationality="中国",
        bio_zh="北宋文学家、书法家，苏东坡，唐宋八大家之一，词、诗、文、书、画无所不精，《赤壁赋》《水调歌头》传世。",
        portrait_url=None,
        tags=["诗歌", "中国文学", "宋词", "散文"],
        works=[("Ode to the Red Cliff", "《赤壁赋》", 1082, "散文"),
               ("Shui Diao Ge Tou", "《水调歌头》", 1076, "词"),
               ("Complete Works of Su Dongpo", "《东坡全集》", 1101, "诗文集")],
        events=[(1037, "生于四川眉山", "birth"), (1101, "卒于常州", "death"),
                (1079, "因乌台诗案被贬黄州，《赤壁赋》作于此时", "life")],
    ),
    dict(
        name="Pu Songling", name_zh="蒲松龄",
        birth=1640, death=1715, nationality="中国",
        bio_zh="清代短篇小说家，《聊斋志异》收录近500篇文言短篇，以狐鬼花妖寄托对黑暗现实的批判，是中国文言短篇小说的顶峰。",
        portrait_url=None,
        tags=["古典文学", "中国文学", "短篇小说", "志怪"],
        works=[("Strange Stories from a Chinese Studio", "《聊斋志异》", 1740, "短篇集")],
        events=[(1640, "生于山东淄川", "birth"), (1715, "卒于山东淄川", "death"),
                (1679, "开始创作《聊斋志异》", "life")],
    ),
    # ── 19世纪英美文学 ────────────────────────────────────────────────────────
    dict(
        name="Jane Austen", name_zh="简·奥斯汀",
        birth=1775, death=1817, nationality="英国",
        bio_zh="英国19世纪最重要的女作家，以精妙的讽刺笔触描绘乡绅阶级的婚姻与社交，《傲慢与偏见》是英国文学经典。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/CassandraAusten-JaneAusten%28c.1810%29_hires.jpg/330px-CassandraAusten-JaneAusten%28c.1810%29_hires.jpg",
        tags=["现实主义", "英国文学", "女性文学"],
        works=[("Pride and Prejudice", "《傲慢与偏见》", 1813, "小说"),
               ("Sense and Sensibility", "《理智与情感》", 1811, "小说"),
               ("Emma", "《爱玛》", 1815, "小说")],
        events=[(1775, "生于英国汉普郡斯蒂文顿", "birth"), (1817, "卒于温切斯特", "death")],
    ),
    dict(
        name="Mark Twain", name_zh="马克·吐温",
        birth=1835, death=1910, nationality="美国",
        bio_zh="美国19世纪最重要的作家，以幽默讽刺著称，《哈克贝利·费恩历险记》被称为美国文学的源头，海明威如是说。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Mark_Twain_by_AF_Bradley.jpg/330px-Mark_Twain_by_AF_Bradley.jpg",
        tags=["现实主义", "美国文学", "幽默讽刺"],
        works=[("Adventures of Huckleberry Finn", "《哈克贝利·费恩历险记》", 1884, "小说"),
               ("The Adventures of Tom Sawyer", "《汤姆·索亚历险记》", 1876, "小说"),
               ("The Prince and the Pauper", "《王子与贫儿》", 1881, "小说")],
        events=[(1835, "生于密苏里州佛罗里达", "birth"), (1910, "卒于康涅狄格州", "death")],
    ),
    dict(
        name="Emily Dickinson", name_zh="艾米莉·狄金森",
        birth=1830, death=1886, nationality="美国",
        bio_zh="美国19世纪最重要的诗人之一，一生隐居，死后诗歌才被发表，以独特的破折号和斜韵开创现代诗歌先河。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Emily_Dickinson_daguerreotype_%28cropped%29.jpg/330px-Emily_Dickinson_daguerreotype_%28cropped%29.jpg",
        tags=["诗歌", "美国文学", "现代主义先驱"],
        works=[("Poems by Emily Dickinson", "《艾米莉·狄金森诗集》", 1890, "诗集")],
        events=[(1830, "生于马萨诸塞州阿默斯特", "birth"), (1886, "卒于阿默斯特", "death"),
                (1862, "写信给文学评论家希金森，开始文学往来", "life")],
    ),
    dict(
        name="Leo Tolstoy", name_zh="列夫·托尔斯泰",  # already exists as 托尔斯泰
        birth=1828, death=1910, nationality="俄国",
        bio_zh="",
        portrait_url=None, tags=[], works=[], events=[],
    ),
    dict(
        name="George Eliot", name_zh="乔治·艾略特",
        birth=1819, death=1880, nationality="英国",
        bio_zh="英国维多利亚时代最重要的女作家，以男性笔名发表作品，《米德尔马契》被弗吉尼亚·伍尔夫称为成人写的少数小说之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/George_Eliot%2C_by_François_D%27Albert_Durade.jpg/330px-George_Eliot%2C_by_François_D%27Albert_Durade.jpg",
        tags=["现实主义", "英国文学", "女性文学"],
        works=[("Middlemarch", "《米德尔马契》", 1872, "小说"),
               ("The Mill on the Floss", "《弗洛斯河上的磨坊》", 1860, "小说"),
               ("Silas Marner", "《织工马南》", 1861, "小说")],
        events=[(1819, "生于沃里克郡", "birth"), (1880, "卒于伦敦", "death")],
    ),
    # ── 日本文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Natsume Soseki", name_zh="夏目漱石",
        birth=1867, death=1916, nationality="日本",
        bio_zh="日本近代文学奠基人，《我是猫》《心》以知识分子的孤独与彷徨折射明治时代的社会变迁，头像曾印于日元纸币。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Natsume_Soseki_photo.jpg/330px-Natsume_Soseki_photo.jpg",
        tags=["日本文学", "近代文学", "知识分子文学"],
        works=[("I Am a Cat", "《我是猫》", 1905, "小说"),
               ("Kokoro", "《心》", 1914, "小说"),
               ("Botchan", "《少爷》", 1906, "小说"),
               ("Sanshiro", "《三四郎》", 1908, "小说")],
        events=[(1867, "生于江户（东京）", "birth"), (1916, "卒于东京", "death"),
                (1900, "赴英国伦敦留学，研究英国文学", "life")],
    ),
    dict(
        name="Ryunosuke Akutagawa", name_zh="芥川龙之介",
        birth=1892, death=1927, nationality="日本",
        bio_zh="日本短篇小说巨匠，《罗生门》《地狱变》以精炼笔触探讨人性的善恶，35岁服安眠药自尽，日本设有以其命名的文学奖。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Akutagawa_Ryunosuke.jpg/330px-Akutagawa_Ryunosuke.jpg",
        tags=["日本文学", "短篇小说", "新思潮派"],
        works=[("Rashomon", "《罗生门》", 1915, "小说"),
               ("In a Grove", "《竹林中》", 1922, "小说"),
               ("Hell Screen", "《地狱变》", 1918, "小说")],
        events=[(1892, "生于东京", "birth"), (1927, "服安眠药自尽，卒于东京", "death")],
    ),
    dict(
        name="Osamu Dazai", name_zh="太宰治",
        birth=1909, death=1948, nationality="日本",
        bio_zh="日本无赖派代表作家，《人间失格》是日本文学史上最畅销的小说之一，以自传式笔触书写生命的颓败与绝望，五次自杀未遂后投河。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Dazai_Osamu.jpg/330px-Dazai_Osamu.jpg",
        tags=["日本文学", "无赖派", "私小说"],
        works=[("No Longer Human", "《人间失格》", 1948, "小说"),
               ("The Setting Sun", "《斜阳》", 1947, "小说"),
               ("Run, Melos!", "《奔跑吧，梅勒斯》", 1940, "小说")],
        events=[(1909, "生于青森县金木", "birth"), (1948, "与情人投玉川上水，卒于东京", "death")],
    ),
    # ── 更多20世纪大师 ────────────────────────────────────────────────────────
    dict(
        name="Vladimir Nabokov", name_zh="纳博科夫",
        birth=1899, death=1977, nationality="俄国",
        bio_zh="俄裔美国小说家，以俄语和英语双语写作著称，《洛丽塔》是20世纪最有争议也最精美的小说之一，语言艺术登峰造极。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Vladimir_Nabokov_1973.jpg/330px-Vladimir_Nabokov_1973.jpg",
        tags=["现代主义", "俄国文学", "美国文学", "后现代"],
        works=[("Lolita", "《洛丽塔》", 1955, "小说"),
               ("Pale Fire", "《微暗的火》", 1962, "小说"),
               ("The Gift", "《天赋》", 1938, "小说")],
        events=[(1899, "生于圣彼得堡", "birth"), (1977, "卒于瑞士蒙特勒", "death"),
                (1940, "流亡美国，开始用英语写作", "life")],
    ),
    dict(
        name="George Orwell", name_zh="奥威尔",
        birth=1903, death=1950, nationality="英国",
        bio_zh="英国作家，《动物农场》和《一九八四》是20世纪反极权主义的最重要文学作品，影响了整个冷战时代的政治思想。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/George_Orwell_press_photo.jpg/330px-George_Orwell_press_photo.jpg",
        tags=["现代主义", "英国文学", "政治小说", "反乌托邦"],
        works=[("Animal Farm", "《动物农场》", 1945, "小说"),
               ("Nineteen Eighty-Four", "《一九八四》", 1949, "小说"),
               ("Homage to Catalonia", "《向加泰罗尼亚致敬》", 1938, "散文")],
        events=[(1903, "生于英属印度孟加拉邦", "birth"), (1950, "卒于伦敦（肺结核）", "death"),
                (1936, "赴西班牙参加内战，后写成《向加泰罗尼亚致敬》", "life")],
    ),
    dict(
        name="James Baldwin", name_zh="詹姆斯·鲍德温",
        birth=1924, death=1987, nationality="美国",
        bio_zh="美国非裔作家，以种族、性别和身份认同为核心主题，《向苍天呼吁》《土生子》是美国黑人文学的里程碑。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/James_Baldwin_37_Allan_Warren.jpg/330px-James_Baldwin_37_Allan_Warren.jpg",
        tags=["美国文学", "非裔文学", "社会批判"],
        works=[("Go Tell It on the Mountain", "《向苍天呼吁》", 1953, "小说"),
               ("Giovanni's Room", "《乔万尼的房间》", 1956, "小说"),
               ("The Fire Next Time", "《下次将是烈火》", 1963, "散文")],
        events=[(1924, "生于纽约哈莱姆", "birth"), (1987, "卒于法国圣保罗德旺斯", "death"),
                (1948, "移居法国巴黎，逃离美国种族歧视", "life")],
    ),
    dict(
        name="Toni Morrison", name_zh="托尼·莫里森",
        birth=1931, death=2019, nationality="美国",
        bio_zh="美国非裔女作家，诺贝尔文学奖得主，《宠儿》以奴隶制的创伤为主题，是美国文学中最重要的作品之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Toni_Morrison_2008-2.jpg/330px-Toni_Morrison_2008-2.jpg",
        tags=["美国文学", "非裔文学", "女性文学"],
        works=[("Beloved", "《宠儿》", 1987, "小说"),
               ("Song of Solomon", "《所罗门之歌》", 1977, "小说"),
               ("The Bluest Eye", "《最蓝的眼睛》", 1970, "小说")],
        events=[(1931, "生于俄亥俄州洛雷恩", "birth"), (2019, "卒于纽约", "death"),
                (1993, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Gabriel Garcia Marquez", name_zh="加西亚·马尔克斯",  # already exists
        birth=1927, death=2014, nationality="哥伦比亚",
        bio_zh="", portrait_url=None, tags=[], works=[], events=[],
    ),
    dict(
        name="Doris Lessing", name_zh="多丽丝·莱辛",
        birth=1919, death=2013, nationality="英国",
        bio_zh="英国女作家，诺贝尔文学奖得主，《金色笔记》是20世纪女性主义文学的里程碑，以多声部叙事探讨女性意识。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Doris_Lessing_c1980.jpg/330px-Doris_Lessing_c1980.jpg",
        tags=["现代主义", "英国文学", "女性文学"],
        works=[("The Golden Notebook", "《金色笔记》", 1962, "小说"),
               ("The Grass Is Singing", "《野草在歌唱》", 1950, "小说")],
        events=[(1919, "生于伊朗克尔曼沙赫", "birth"), (2013, "卒于伦敦", "death"),
                (2007, "获诺贝尔文学奖，时年88岁", "life")],
    ),
    dict(
        name="Milan Kundera", name_zh="米兰·昆德拉",
        birth=1929, death=2023, nationality="捷克",
        bio_zh="捷克裔法国作家，《不能承受的生命之轻》是20世纪最重要的小说之一，以哲学笔触探讨历史、爱情与存在。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Milan_Kundera_-_fotografija.jpg/330px-Milan_Kundera_-_fotografija.jpg",
        tags=["现代主义", "捷克文学", "哲学小说"],
        works=[("The Unbearable Lightness of Being", "《不能承受的生命之轻》", 1984, "小说"),
               ("The Book of Laughter and Forgetting", "《笑忘书》", 1979, "小说"),
               ("Immortality", "《不朽》", 1990, "小说")],
        events=[(1929, "生于捷克布尔诺", "birth"), (2023, "卒于巴黎", "death"),
                (1968, "布拉格之春后遭到迫害，作品被禁", "life"),
                (1975, "流亡法国", "life")],
    ),
    dict(
        name="Günter Grass", name_zh="君特·格拉斯",
        birth=1927, death=2015, nationality="德国",
        bio_zh="德国作家，诺贝尔文学奖得主，《铁皮鼓》是20世纪最重要的德语小说，以荒诞手法描绘纳粹德国的历史。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Bundesarchiv_B_145_Bild-F078072-0004%2C_Günter_Grass.jpg/330px-Bundesarchiv_B_145_Bild-F078072-0004%2C_Günter_Grass.jpg",
        tags=["现代主义", "德语文学", "魔幻现实主义"],
        works=[("The Tin Drum", "《铁皮鼓》", 1959, "小说"),
               ("Cat and Mouse", "《猫与鼠》", 1961, "小说")],
        events=[(1927, "生于但泽（今格但斯克）", "birth"), (2015, "卒于吕贝克", "death"),
                (1999, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Patrick Modiano", name_zh="莫迪亚诺",
        birth=1945, death=None, nationality="法国",
        bio_zh="法国作家，诺贝尔文学奖得主，以记忆、身份和二战占领时期的巴黎为核心主题，被称为当代普鲁斯特。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Patrick_Modiano_par_Helene_Bamberger_%28cropped%29.jpg/330px-Patrick_Modiano_par_Helene_Bamberger_%28cropped%29.jpg",
        tags=["当代文学", "法国文学", "记忆文学"],
        works=[("Missing Person", "《暗店街》", 1978, "小说"),
               ("In the Cafe of Lost Youth", "《青春咖啡馆》", 2007, "小说")],
        events=[(1945, "生于巴黎布洛涅-比扬古", "birth"),
                (2014, "获诺贝尔文学奖", "life")],
    ),
    # ── 中国当代 ──────────────────────────────────────────────────────────────
    dict(
        name="Ba Jin", name_zh="巴金",
        birth=1904, death=2005, nationality="中国",
        bio_zh="中国现代著名作家，激流三部曲《家》《春》《秋》是中国现代文学经典，晚年以《随想录》对文革进行深刻反思。",
        portrait_url=None,
        tags=["现代文学", "中国文学", "激流三部曲"],
        works=[("Family", "《家》", 1933, "小说"),
               ("Spring", "《春》", 1938, "小说"),
               ("Autumn", "《秋》", 1940, "小说"),
               ("Random Thoughts", "《随想录》", 1986, "散文")],
        events=[(1904, "生于四川成都", "birth"), (2005, "卒于上海", "death"),
                (1927, "赴法国留学，创作《灭亡》", "life"),
                (1978, "开始写《随想录》，呼吁建立文革博物馆", "life")],
    ),
    dict(
        name="Ding Ling", name_zh="丁玲",
        birth=1904, death=1986, nationality="中国",
        bio_zh="中国现代著名女作家，《莎菲女士的日记》开创女性意识写作先河，获斯大林文学奖，后遭右派打击，晚年平反。",
        portrait_url=None,
        tags=["现代文学", "中国文学", "女性文学"],
        works=[("Miss Sophie's Diary", "《莎菲女士的日记》", 1928, "小说"),
               ("The Sun Shines over the Sanggan River", "《太阳照在桑干河上》", 1948, "小说")],
        events=[(1904, "生于湖南临澧", "birth"), (1986, "卒于北京", "death"),
                (1957, "被划为右派，开始长达22年的迫害", "life")],
    ),
    dict(
        name="Tie Ning", name_zh="铁凝",
        birth=1957, death=None, nationality="中国",
        bio_zh="中国当代著名女作家，现任中国作协主席，《玫瑰门》《大浴女》以细腻笔触书写女性命运，获多项国家文学奖项。",
        portrait_url=None,
        tags=["当代文学", "中国文学", "女性文学"],
        works=[("Rose Gate", "《玫瑰门》", 1988, "小说"),
               ("The Bathing Women", "《大浴女》", 2000, "小说")],
        events=[(1957, "生于北京", "birth"),
                (2006, "当选中国作家协会主席", "life")],
    ),
    dict(
        name="Chi Zijian", name_zh="迟子建",
        birth=1964, death=None, nationality="中国",
        bio_zh="中国当代著名女作家，以东北黑土地为创作背景，《额尔古纳河右岸》获茅盾文学奖，以史诗笔触书写鄂温克族的百年命运。",
        portrait_url=None,
        tags=["当代文学", "中国文学", "地域文学"],
        works=[("The Right Bank of the Ergun River", "《额尔古纳河右岸》", 2005, "小说"),
               ("Puppet Manchukuo", "《伪满洲国》", 2000, "小说")],
        events=[(1964, "生于黑龙江漠河", "birth"),
                (2008, "《额尔古纳河右岸》获茅盾文学奖", "life")],
    ),
    dict(
        name="Can Xue", name_zh="残雪",
        birth=1953, death=None, nationality="中国",
        bio_zh="中国先锋派代表女作家，以卡夫卡式的梦幻笔法书写内心世界，多次被提名诺贝尔文学奖，在西方享有极高声誉。",
        portrait_url=None,
        tags=["先锋文学", "中国文学", "女性文学"],
        works=[("Dialogues in Paradise", "《天堂里的对话》", 1988, "小说"),
               ("Yellow Mud Street", "《黄泥街》", 1987, "小说")],
        events=[(1953, "生于湖南长沙", "birth"),
                (1985, "发表《污水上的肥皂泡》，先锋风格引发关注", "life")],
    ),
    dict(
        name="Zhang Wei", name_zh="张炜",
        birth=1956, death=None, nationality="中国",
        bio_zh="中国当代著名作家，《古船》《你在高原》是其代表作，后者以450万字成为中国最长的长篇小说，获茅盾文学奖。",
        portrait_url=None,
        tags=["当代文学", "中国文学", "史诗小说"],
        works=[("The Ancient Ship", "《古船》", 1987, "小说"),
               ("You Are on the Plateau", "《你在高原》", 2010, "小说")],
        events=[(1956, "生于山东龙口", "birth"),
                (2011, "《你在高原》获茅盾文学奖", "life")],
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
            # 跳过占位条目（bio为空说明是重复）
            if not a.get("bio_zh"):
                continue
            exists = await session.scalar(
                select(Author).where(Author.name_zh == a["name_zh"])
            )
            if exists:
                print(f"  跳过: {a['name_zh']} (已存在)")
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
                session.add(Work(author_id=author.id, title=title, title_zh=title_zh, year=year, genre=genre))

            for ev in a.get("events", []):
                year, event_zh = ev[0], ev[1]
                event_type = ev[2] if len(ev) > 2 else "life"
                session.add(AuthorEvent(author_id=author.id, year=year, event_zh=event_zh, event_type=event_type))

            print(f"  添加: {a['name_zh']} ({a['birth']}–{a.get('death') or '今'})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
