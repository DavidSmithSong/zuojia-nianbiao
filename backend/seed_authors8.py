"""
作家年表 · 第八批种子数据
来源：Modern Library 100 Best Novels + portraits.json 中缺失作家
运行：python -m backend.seed_authors8
"""
import asyncio, os, re
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── Modern Library 100 核心作家 ──────────────────────────────────────────
    dict(
        name="W. Somerset Maugham", name_zh="毛姆",
        birth=1874, death=1965, nationality="英国",
        bio_zh="英国现代最受欢迎的小说家之一，以流畅洗练的笔触描绘人性，《人性的枷锁》《月亮与六便士》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/W._Somerset_Maugham_1934.jpg/330px-W._Somerset_Maugham_1934.jpg",
        tags=["现代主义", "英国文学", "心理小说"],
        works=[("Of Human Bondage", "《人性的枷锁》", 1915, "小说"),
               ("The Moon and Sixpence", "《月亮与六便士》", 1919, "小说"),
               ("The Razor's Edge", "《刀锋》", 1944, "小说"),
               ("Ashenden", "《阿申登》", 1928, "小说")],
        events=[(1874, "生于巴黎英国大使馆", "birth"), (1965, "卒于法国尼斯", "death"),
                (1915, "一战期间为英国情报部门工作，成为间谍", "life")],
    ),
    dict(
        name="D. H. Lawrence", name_zh="劳伦斯",
        birth=1885, death=1930, nationality="英国",
        bio_zh="英国现代主义作家，以描写工业文明对人性压抑著称，《儿子与情人》《恋爱中的女人》《查泰莱夫人的情人》引发巨大争议。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/DH_Lawrence_passport_photo.jpg/330px-DH_Lawrence_passport_photo.jpg",
        tags=["现代主义", "英国文学", "工业批判"],
        works=[("Sons and Lovers", "《儿子与情人》", 1913, "小说"),
               ("Women in Love", "《恋爱中的女人》", 1920, "小说"),
               ("Lady Chatterley's Lover", "《查泰莱夫人的情人》", 1928, "小说"),
               ("The Rainbow", "《虹》", 1915, "小说")],
        events=[(1885, "生于诺丁汉郡", "birth"), (1930, "卒于法国旺斯（肺结核）", "death"),
                (1928, "《查泰莱夫人的情人》在英国被禁30年", "life")],
    ),
    dict(
        name="John Steinbeck", name_zh="斯坦贝克",
        birth=1902, death=1968, nationality="美国",
        bio_zh="美国现实主义作家，诺贝尔文学奖得主，以底层劳动者为主角，《愤怒的葡萄》描写大萧条时代移民的苦难，震撼美国社会。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/JohnsteinbeckUSGOV.jpg/330px-JohnsteinbeckUSGOV.jpg",
        tags=["现实主义", "美国文学", "社会批判"],
        works=[("The Grapes of Wrath", "《愤怒的葡萄》", 1939, "小说"),
               ("Of Mice and Men", "《人鼠之间》", 1937, "小说"),
               ("East of Eden", "《伊甸园之东》", 1952, "小说")],
        events=[(1902, "生于加利福尼亚州萨利纳斯", "birth"), (1968, "卒于纽约", "death"),
                (1962, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Aldous Huxley", name_zh="赫胥黎",
        birth=1894, death=1963, nationality="英国",
        bio_zh="英国作家，《美丽新世界》是反乌托邦文学的经典，与奥威尔的《一九八四》并列，预言了科技极权对人性的消解。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Aldous_Huxley_smoking.jpg/330px-Aldous_Huxley_smoking.jpg",
        tags=["现代主义", "英国文学", "反乌托邦"],
        works=[("Brave New World", "《美丽新世界》", 1932, "小说"),
               ("Point Counter Point", "《针锋相对》", 1928, "小说"),
               ("The Doors of Perception", "《知觉之门》", 1954, "散文")],
        events=[(1894, "生于萨里郡戈达尔明", "birth"), (1963, "卒于洛杉矶（肺癌）", "death"),
                (1937, "移居美国，后长居加利福尼亚", "life")],
    ),
    dict(
        name="J. D. Salinger", name_zh="塞林格",
        birth=1919, death=2010, nationality="美国",
        bio_zh="美国作家，《麦田里的守望者》是20世纪青少年文学的经典，以霍尔顿的叛逆声音影响了整整一代美国青年，作者此后隐居。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Salinger_if_you_really_want_to_know.jpg/330px-Salinger_if_you_really_want_to_know.jpg",
        tags=["现代主义", "美国文学", "青春文学"],
        works=[("The Catcher in the Rye", "《麦田里的守望者》", 1951, "小说"),
               ("Franny and Zooey", "《弗兰尼与祖伊》", 1961, "小说"),
               ("Nine Stories", "《九故事》", 1953, "短篇集")],
        events=[(1919, "生于纽约", "birth"), (2010, "卒于新罕布什尔州", "death"),
                (1951, "《麦田里的守望者》出版后成名，随即隐居", "life")],
    ),
    dict(
        name="Joseph Conrad", name_zh="康拉德",
        birth=1857, death=1924, nationality="英国",
        bio_zh="波兰裔英国作家，以航海经历为素材，《黑暗的心》深刻揭示殖民主义的暴行，现代主义小说的先驱之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Joseph_Conrad.jpg/330px-Joseph_Conrad.jpg",
        tags=["现代主义", "英国文学", "殖民批判", "航海文学"],
        works=[("Heart of Darkness", "《黑暗的心》", 1902, "小说"),
               ("Lord Jim", "《吉姆爷》", 1900, "小说"),
               ("Nostromo", "《诺斯特罗莫》", 1904, "小说"),
               ("The Secret Agent", "《间谍》", 1907, "小说")],
        events=[(1857, "生于波兰别尔基切夫", "birth"), (1924, "卒于英国比辛顿", "death"),
                (1886, "加入英国国籍，以英语写作", "life")],
    ),
    dict(
        name="Henry James", name_zh="亨利·詹姆斯",
        birth=1843, death=1916, nationality="美国",
        bio_zh="美国裔英国小说家，心理现实主义的先驱，以精细的意识分析著称，《金碗》《鸽翼》《使节》构成其晚期三部曲。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Henry_James_by_John_Singer_Sargent_cleaned.jpg/330px-Henry_James_by_John_Singer_Sargent_cleaned.jpg",
        tags=["现实主义", "美国文学", "心理小说"],
        works=[("The Portrait of a Lady", "《贵妇画像》", 1881, "小说"),
               ("The Wings of the Dove", "《鸽翼》", 1902, "小说"),
               ("The Golden Bowl", "《金碗》", 1904, "小说"),
               ("The Ambassadors", "《使节》", 1903, "小说")],
        events=[(1843, "生于纽约", "birth"), (1916, "卒于伦敦", "death"),
                (1876, "定居欧洲，长居英国", "life")],
    ),
    dict(
        name="E. M. Forster", name_zh="福斯特",
        birth=1879, death=1970, nationality="英国",
        bio_zh="英国小说家，《印度之行》以英印关系隐喻帝国主义的困境，《霍华德庄园》探讨阶级融合的可能，以人文主义著称。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/E_M_Forster.jpg/330px-E_M_Forster.jpg",
        tags=["现代主义", "英国文学", "人文主义"],
        works=[("A Passage to India", "《印度之行》", 1924, "小说"),
               ("Howards End", "《霍华德庄园》", 1910, "小说"),
               ("A Room with a View", "《看得见风景的房间》", 1908, "小说")],
        events=[(1879, "生于伦敦", "birth"), (1970, "卒于考文垂", "death"),
                (1924, "《印度之行》出版后，沉默长达46年未再出长篇", "life")],
    ),
    dict(
        name="Graham Greene", name_zh="格林",
        birth=1904, death=1991, nationality="英国",
        bio_zh="英国小说家，以天主教信仰和政治题材著称，《事情的内核》《第三个人》《权力与荣耀》探索罪恶、救赎与人性的复杂。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Graham_Greene_%281956%29.jpg/330px-Graham_Greene_%281956%29.jpg",
        tags=["现代主义", "英国文学", "天主教文学", "政治小说"],
        works=[("The Power and the Glory", "《权力与荣耀》", 1940, "小说"),
               ("The Heart of the Matter", "《事情的内核》", 1948, "小说"),
               ("The Third Man", "《第三个人》", 1949, "小说"),
               ("The Quiet American", "《沉静的美国人》", 1955, "小说")],
        events=[(1904, "生于赫特福德郡", "birth"), (1991, "卒于瑞士韦维", "death")],
    ),
    dict(
        name="William Golding", name_zh="戈尔丁",
        birth=1911, death=1993, nationality="英国",
        bio_zh="英国小说家，诺贝尔文学奖得主，《蝇王》以荒岛上的孩子揭示人性的黑暗，是20世纪最有影响力的英语小说之一。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/William_Golding_1983.jpg/330px-William_Golding_1983.jpg",
        tags=["现代主义", "英国文学", "寓言小说"],
        works=[("Lord of the Flies", "《蝇王》", 1954, "小说"),
               ("The Inheritors", "《继承者》", 1955, "小说"),
               ("Rites of Passage", "《过关仪式》", 1980, "小说")],
        events=[(1911, "生于康沃尔郡", "birth"), (1993, "卒于康沃尔郡", "death"),
                (1983, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Salman Rushdie", name_zh="拉什迪",
        birth=1947, death=None, nationality="英国",
        bio_zh="印裔英国作家，《午夜之子》获布克奖，《撒旦诗篇》因被认为亵渎伊斯兰教遭伊朗宗教领袖发布追杀令，被迫隐居多年。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Salman_Rushdie_2015.jpg/330px-Salman_Rushdie_2015.jpg",
        tags=["魔幻现实主义", "英国文学", "后殖民文学"],
        works=[("Midnight's Children", "《午夜之子》", 1981, "小说"),
               ("The Satanic Verses", "《撒旦诗篇》", 1988, "小说"),
               ("The Moor's Last Sigh", "《摩尔人的最后叹息》", 1995, "小说")],
        events=[(1947, "生于印度孟买，印巴分治之日", "birth"),
                (1989, "《撒旦诗篇》遭伊朗追杀令，开始长达十年的隐居", "life"),
                (2022, "在美国演讲时遭刺，右眼失明", "life")],
    ),
    dict(
        name="Jack London", name_zh="杰克·伦敦",
        birth=1876, death=1916, nationality="美国",
        bio_zh="美国著名小说家，以冒险与自然为题材，《野性的呼唤》《白牙》是其代表作，同时是坚定的社会主义者。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/JackLondonphoto.jpg/330px-JackLondonphoto.jpg",
        tags=["现实主义", "美国文学", "冒险文学"],
        works=[("The Call of the Wild", "《野性的呼唤》", 1903, "小说"),
               ("White Fang", "《白牙》", 1906, "小说"),
               ("The Sea-Wolf", "《海狼》", 1904, "小说")],
        events=[(1876, "生于加利福尼亚州旧金山", "birth"), (1916, "卒于加利福尼亚州（自杀）", "death"),
                (1897, "参加克朗代克淘金潮，积累大量素材", "life")],
    ),
    dict(
        name="Kurt Vonnegut", name_zh="冯内古特",
        birth=1922, death=2007, nationality="美国",
        bio_zh="美国后现代主义作家，《第五号屠宰场》以黑色幽默描绘二战德累斯顿大轰炸，融合科幻与现实，是反战文学经典。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Kurt_Vonnegut_1972.jpg/330px-Kurt_Vonnegut_1972.jpg",
        tags=["后现代主义", "美国文学", "科幻", "反战"],
        works=[("Slaughterhouse-Five", "《第五号屠宰场》", 1969, "小说"),
               ("Cat's Cradle", "《猫的摇篮》", 1963, "小说"),
               ("Breakfast of Champions", "《冠军早餐》", 1973, "小说")],
        events=[(1922, "生于印第安纳波利斯", "birth"), (2007, "卒于纽约", "death"),
                (1945, "亲历德累斯顿大轰炸，被关押于地下屠宰场中幸存", "life")],
    ),
    dict(
        name="Jack Kerouac", name_zh="凯鲁亚克",
        birth=1922, death=1969, nationality="美国",
        bio_zh="美国垮掉的一代代表作家，《在路上》是20世纪美国反叛精神的圣经，以自由漫游对抗物质主义，影响了整个嬉皮士文化。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Kerouac_by_Palumbo.jpg/330px-Kerouac_by_Palumbo.jpg",
        tags=["垮掉的一代", "美国文学", "公路文学"],
        works=[("On the Road", "《在路上》", 1957, "小说"),
               ("The Dharma Bums", "《达摩流浪者》", 1958, "小说"),
               ("Big Sur", "《大瑟尔》", 1962, "小说")],
        events=[(1922, "生于马萨诸塞州洛厄尔", "birth"), (1969, "卒于佛罗里达州（酗酒）", "death"),
                (1947, "与尼尔·卡萨迪横穿美国，积累《在路上》素材", "life")],
    ),
    dict(
        name="Philip Roth", name_zh="菲利普·罗斯",
        birth=1933, death=2018, nationality="美国",
        bio_zh="美国当代最重要的小说家之一，普利策奖得主，以美国犹太人身份认同为核心，《美国牧歌》《人性的污点》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Philip_Roth_1_crop.jpg/330px-Philip_Roth_1_crop.jpg",
        tags=["当代文学", "美国文学", "犹太文学"],
        works=[("American Pastoral", "《美国牧歌》", 1997, "小说"),
               ("The Human Stain", "《人性的污点》", 2000, "小说"),
               ("Portnoy's Complaint", "《波特诺伊的怨诉》", 1969, "小说")],
        events=[(1933, "生于新泽西州纽瓦克", "birth"), (2018, "卒于纽约", "death"),
                (1998, "《美国牧歌》获普利策奖", "life")],
    ),
    dict(
        name="Saul Bellow", name_zh="索尔·贝娄",
        birth=1915, death=2005, nationality="美国",
        bio_zh="加拿大裔美国作家，诺贝尔文学奖得主，以知识分子在现代社会的困境为主题，《赫索格》《奥吉·马奇历险记》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Saul_Bellow_1976.jpg/330px-Saul_Bellow_1976.jpg",
        tags=["现代主义", "美国文学", "犹太文学"],
        works=[("The Adventures of Augie March", "《奥吉·马奇历险记》", 1953, "小说"),
               ("Herzog", "《赫索格》", 1964, "小说"),
               ("Humboldt's Gift", "《洪堡的礼物》", 1975, "小说")],
        events=[(1915, "生于加拿大魁北克", "birth"), (2005, "卒于马萨诸塞州", "death"),
                (1976, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Edith Wharton", name_zh="伊迪丝·华顿",
        birth=1862, death=1937, nationality="美国",
        bio_zh="美国女作家，普利策奖得主，以上流社会为背景揭示社会规范对个人的压抑，《纯真年代》《欢乐之家》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Edith_Wharton_%28portrait%29.jpg/330px-Edith_Wharton_%28portrait%29.jpg",
        tags=["现实主义", "美国文学", "女性文学"],
        works=[("The Age of Innocence", "《纯真年代》", 1920, "小说"),
               ("The House of Mirth", "《欢乐之家》", 1905, "小说"),
               ("Ethan Frome", "《伊坦·弗罗美》", 1911, "小说")],
        events=[(1862, "生于纽约", "birth"), (1937, "卒于法国圣布里斯苏福雷", "death"),
                (1921, "《纯真年代》获普利策奖，首位女性得主", "life")],
    ),
    dict(
        name="Ralph Ellison", name_zh="拉尔夫·艾里森",
        birth=1913, death=1994, nationality="美国",
        bio_zh="美国非裔作家，《隐形人》是20世纪最重要的美国小说之一，以黑人在白人社会中的隐形困境揭示种族主义的本质。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Ralph_Ellison_1963.jpg/330px-Ralph_Ellison_1963.jpg",
        tags=["美国文学", "非裔文学", "现代主义"],
        works=[("Invisible Man", "《隐形人》", 1952, "小说"),
               ("Shadow and Act", "《影子与行动》", 1964, "散文")],
        events=[(1913, "生于俄克拉荷马城", "birth"), (1994, "卒于纽约", "death"),
                (1953, "《隐形人》获美国国家图书奖", "life")],
    ),
    dict(
        name="Iris Murdoch", name_zh="艾丽斯·默多克",
        birth=1919, death=1999, nationality="英国",
        bio_zh="英裔爱尔兰小说家兼哲学家，布克奖得主，一生创作26部小说，以道德困境和存在主义哲学见长，晚年罹患阿尔茨海默症。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Iris_Murdoch.jpg/330px-Iris_Murdoch.jpg",
        tags=["现代主义", "英国文学", "哲学小说"],
        works=[("Under the Net", "《在网下》", 1954, "小说"),
               ("The Sea, The Sea", "《大海啊大海》", 1978, "小说"),
               ("The Bell", "《钟》", 1958, "小说")],
        events=[(1919, "生于都柏林", "birth"), (1999, "卒于牛津（阿尔茨海默症）", "death"),
                (1978, "《大海啊大海》获布克奖", "life")],
    ),
    dict(
        name="V. S. Naipaul", name_zh="奈保尔",
        birth=1932, death=2018, nationality="英国",
        bio_zh="特立尼达裔英国作家，诺贝尔文学奖得主，以后殖民视角审视第三世界，《毕司沃斯先生的房子》《河湾》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/V_S_Naipaul.jpg/330px-V_S_Naipaul.jpg",
        tags=["后殖民文学", "英国文学", "移民文学"],
        works=[("A House for Mr Biswas", "《毕司沃斯先生的房子》", 1961, "小说"),
               ("A Bend in the River", "《河湾》", 1979, "小说"),
               ("In a Free State", "《自由国度》", 1971, "小说")],
        events=[(1932, "生于特立尼达", "birth"), (2018, "卒于伦敦", "death"),
                (2001, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Rudyard Kipling", name_zh="吉卜林",
        birth=1865, death=1936, nationality="英国",
        bio_zh="英国作家，第一位获诺贝尔文学奖的英语作家，《丛林之书》《金姆》是其代表作，既颂扬大英帝国又揭示殖民主义的矛盾。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Rudyard_Kipling.jpg/330px-Rudyard_Kipling.jpg",
        tags=["帝国主义", "英国文学", "冒险文学"],
        works=[("The Jungle Book", "《丛林之书》", 1894, "小说"),
               ("Kim", "《金姆》", 1901, "小说"),
               ("Just So Stories", "《原来如此的故事》", 1902, "儿童文学")],
        events=[(1865, "生于印度孟买", "birth"), (1936, "卒于伦敦", "death"),
                (1907, "获诺贝尔文学奖，英语作家第一人", "life")],
    ),
    dict(
        name="Joseph Heller", name_zh="约瑟夫·海勒",
        birth=1923, death=1999, nationality="美国",
        bio_zh="美国小说家，《第22条军规》是20世纪最重要的反战小说，以荒诞逻辑揭示战争的荒谬，创造了英语中的新词Catch-22。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Joseph_Heller_1986.jpg/330px-Joseph_Heller_1986.jpg",
        tags=["后现代主义", "美国文学", "反战", "黑色幽默"],
        works=[("Catch-22", "《第22条军规》", 1961, "小说"),
               ("Something Happened", "《发生了什么》", 1974, "小说")],
        events=[(1923, "生于纽约布鲁克林", "birth"), (1999, "卒于纽约", "death"),
                (1944, "参加二战，飞行60次任务，积累素材", "life")],
    ),
    # ── portraits.json 中缺失的重要作家 ────────────────────────────────────────
    dict(
        name="Olga Tokarczuk", name_zh="托卡尔丘克",
        birth=1962, death=None, nationality="波兰",
        bio_zh="波兰当代最重要的作家，诺贝尔文学奖得主，《云游》《雅各书》以多声部叙事重构波兰历史，开创新的小说形式。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Olga_Tokarczuk_2019.jpg/330px-Olga_Tokarczuk_2019.jpg",
        tags=["当代文学", "波兰文学", "历史小说"],
        works=[("Flights", "《云游》", 2007, "小说"),
               ("The Books of Jacob", "《雅各书》", 2014, "小说"),
               ("Drive Your Plow Over the Bones of the Dead", "《糜骨之壤》", 2009, "小说")],
        events=[(1962, "生于波兰苏莱胡夫", "birth"),
                (2019, "获2018年诺贝尔文学奖（延迟颁发）", "life")],
    ),
    dict(
        name="Bing Xin", name_zh="冰心",
        birth=1900, death=1999, nationality="中国",
        bio_zh="中国现代著名女作家、诗人，以母爱、自然、儿童为主题，《繁星》《春水》受泰戈尔影响，《寄小读者》是儿童文学经典。",
        portrait_url=None,
        tags=["现代文学", "中国文学", "女性文学", "儿童文学"],
        works=[("Glittering Stars", "《繁星》", 1923, "诗集"),
               ("Spring Water", "《春水》", 1923, "诗集"),
               ("Letters to Young Readers", "《寄小读者》", 1926, "散文")],
        events=[(1900, "生于福建福州", "birth"), (1999, "卒于北京", "death"),
                (1923, "赴美国威尔斯利学院留学", "life")],
    ),
    dict(
        name="Ai Qing", name_zh="艾青",  # already exists - will be skipped
        birth=1910, death=1996, nationality="中国",
        bio_zh="", portrait_url=None, tags=[], works=[], events=[],
    ),
    dict(
        name="Henry Miller", name_zh="亨利·米勒",
        birth=1891, death=1980, nationality="美国",
        bio_zh="美国作家，《北回归线》《南回归线》因露骨描写在美国被禁30年，以自传体小说对抗清教徒道德，影响了垮掉的一代。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Henry_Miller_1939.jpg/330px-Henry_Miller_1939.jpg",
        tags=["现代主义", "美国文学", "自传小说"],
        works=[("Tropic of Cancer", "《北回归线》", 1934, "小说"),
               ("Tropic of Capricorn", "《南回归线》", 1939, "小说"),
               ("Big Sur and the Oranges of Hieronymus Bosch", "《大瑟尔》", 1957, "散文")],
        events=[(1891, "生于纽约曼哈顿", "birth"), (1980, "卒于加利福尼亚州太平洋丛林市", "death"),
                (1930, "移居巴黎，开始创作《北回归线》", "life")],
    ),
    dict(
        name="Carson McCullers", name_zh="卡森·麦卡勒斯",
        birth=1917, death=1967, nationality="美国",
        bio_zh="美国南方哥特文学女作家，以孤独和疏离为核心主题，《心是孤独的猎手》23岁出版即成名，探索现代人的精神荒漠。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Carson_McCullers_1940.jpg/330px-Carson_McCullers_1940.jpg",
        tags=["南方哥特", "美国文学", "女性文学"],
        works=[("The Heart Is a Lonely Hunter", "《心是孤独的猎手》", 1940, "小说"),
               ("The Member of the Wedding", "《婚礼的成员》", 1946, "小说"),
               ("Reflections in a Golden Eye", "《金色眼睛里的映象》", 1941, "小说")],
        events=[(1917, "生于佐治亚州哥伦布", "birth"), (1967, "卒于纽约（脑溢血）", "death"),
                (1940, "23岁出版《心是孤独的猎手》轰动文坛", "life")],
    ),
    dict(
        name="Theodore Dreiser", name_zh="德莱塞",
        birth=1871, death=1945, nationality="美国",
        bio_zh="美国自然主义文学代表作家，《嘉莉妹妹》《美国的悲剧》以冷峻笔触描绘资本主义社会的弱肉强食，开美国现代小说先河。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Theodore_Dreiser.jpg/330px-Theodore_Dreiser.jpg",
        tags=["自然主义", "美国文学", "社会批判"],
        works=[("Sister Carrie", "《嘉莉妹妹》", 1900, "小说"),
               ("An American Tragedy", "《美国的悲剧》", 1925, "小说"),
               ("Jennie Gerhardt", "《珍妮姑娘》", 1911, "小说")],
        events=[(1871, "生于印第安纳州特雷霍特", "birth"), (1945, "卒于洛杉矶", "death")],
    ),
    dict(
        name="Norman Mailer", name_zh="诺曼·梅勒",
        birth=1923, death=2007, nationality="美国",
        bio_zh="美国作家，普利策奖两度得主，《裸者与死者》是二战文学经典，一生以激进姿态介入美国政治文化，被称为20世纪美国良心。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Norman_Mailer_1988.jpg/330px-Norman_Mailer_1988.jpg",
        tags=["现代主义", "美国文学", "战争文学", "新新闻主义"],
        works=[("The Naked and the Dead", "《裸者与死者》", 1948, "小说"),
               ("The Executioner's Song", "《刽子手之歌》", 1979, "小说"),
               ("Armies of the Night", "《夜晚的军队》", 1968, "报告文学")],
        events=[(1923, "生于新泽西州朗布兰奇", "birth"), (2007, "卒于纽约", "death"),
                (1969, "参选纽约市长，以失败告终", "life")],
    ),
    # ── 其他重要缺失作家 ──────────────────────────────────────────────────────
    dict(
        name="Wole Soyinka", name_zh="索因卡",
        birth=1934, death=None, nationality="尼日利亚",
        bio_zh="尼日利亚剧作家、诗人，第一位获诺贝尔文学奖的非洲作家，将约鲁巴神话与西方戏剧传统融合，积极反对独裁政权。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Wole_Soyinka_2014.jpg/330px-Wole_Soyinka_2014.jpg",
        tags=["非洲文学", "戏剧", "后殖民文学"],
        works=[("Death and the King's Horseman", "《国王的马夫之死》", 1975, "戏剧"),
               ("The Lion and the Jewel", "《狮子与宝石》", 1963, "戏剧")],
        events=[(1934, "生于尼日利亚阿贝奥库塔", "birth"),
                (1986, "获诺贝尔文学奖，非洲第一人", "life"),
                (1967, "尼日利亚内战期间被囚禁两年", "life")],
    ),
    dict(
        name="Naguib Mahfouz", name_zh="马哈福兹",
        birth=1911, death=2006, nationality="埃及",
        bio_zh="埃及小说家，第一位获诺贝尔文学奖的阿拉伯作家，《开罗三部曲》以开罗街区为背景描绘埃及百年变迁，是阿拉伯现代文学的奠基之作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/NaguibMahfouz.jpg/330px-NaguibMahfouz.jpg",
        tags=["阿拉伯文学", "现实主义", "历史小说"],
        works=[("Cairo Trilogy", "《开罗三部曲》", 1957, "小说"),
               ("Midaq Alley", "《米达克胡同》", 1947, "小说"),
               ("Children of the Alley", "《街魂》", 1959, "小说")],
        events=[(1911, "生于开罗", "birth"), (2006, "卒于开罗", "death"),
                (1988, "获诺贝尔文学奖，阿拉伯作家第一人", "life"),
                (1994, "因《街魂》被指亵渎宗教，遭极端分子刺伤颈部", "life")],
    ),
    dict(
        name="Mo Yan", name_zh="莫言",  # already exists
        birth=1955, death=None, nationality="中国",
        bio_zh="", portrait_url=None, tags=[], works=[], events=[],
    ),
    dict(
        name="Patrick White", name_zh="帕特里克·怀特",
        birth=1912, death=1990, nationality="澳大利亚",
        bio_zh="澳大利亚小说家，诺贝尔文学奖得主，首位获此殊荣的澳大利亚作家，《风暴眼》以宏大叙事探索澳大利亚精神，语言繁复瑰丽。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Patrick_White.jpg/330px-Patrick_White.jpg",
        tags=["现代主义", "澳大利亚文学"],
        works=[("Voss", "《沃斯》", 1957, "小说"),
               ("The Eye of the Storm", "《风暴眼》", 1973, "小说"),
               ("Riders in the Chariot", "《战车骑士》", 1961, "小说")],
        events=[(1912, "生于英国伦敦", "birth"), (1990, "卒于澳大利亚悉尼", "death"),
                (1973, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Clarice Lispector", name_zh="克拉丽丝·李斯贝克托",
        birth=1920, death=1977, nationality="巴西",
        bio_zh="巴西最重要的女作家，以意识流和内心独白著称，被称为南美的弗吉尼亚·伍尔夫，《G.H.的激情》是拉美文学的里程碑。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Clarice_Lispector_foto_de_rosto.jpg/330px-Clarice_Lispector_foto_de_rosto.jpg",
        tags=["现代主义", "拉美文学", "女性文学", "意识流"],
        works=[("The Passion According to G.H.", "《G.H.的激情》", 1964, "小说"),
               ("The Hour of the Star", "《星辰时刻》", 1977, "小说"),
               ("Near to the Wild Heart", "《接近野性之心》", 1943, "小说")],
        events=[(1920, "生于乌克兰切切利尼克", "birth"), (1977, "卒于里约热内卢（癌症）", "death"),
                (1943, "21岁出版处女作引发轰动", "life")],
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
            if not a.get("bio_zh"):
                continue
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
                session.add(Work(author_id=author.id, title=title, title_zh=title_zh, year=year, genre=genre))
            for ev in a.get("events", []):
                session.add(AuthorEvent(author_id=author.id, year=ev[0], event_zh=ev[1],
                                        event_type=ev[2] if len(ev) > 2 else "life"))

            print(f"  添加: {a['name_zh']} ({a['birth']}–{a.get('death') or '今'})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
