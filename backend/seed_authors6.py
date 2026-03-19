"""
作家年表 · 作家种子数据（第六批，30位重要作家）
包含：中国现代文学经典 + 西方20世纪大师 + 日本文学 + 拉美文学
运行：python -m backend.seed_authors6
"""
import asyncio
import os
import sys

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── 中国现代文学 ──────────────────────────────────────────────────────────
    dict(
        name="Lu Xun", name_zh="鲁迅",
        birth=1881, death=1936, nationality="中国",
        bio_zh="中国现代文学奠基人，以《狂人日记》开创白话小说，《阿Q正传》深刻剖析国民性，被誉为民族魂。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Lu_Xun_circa_1930.jpg/330px-Lu_Xun_circa_1930.jpg",
        tags=["现代文学", "中国文学", "短篇小说", "杂文"],
        works=[("A Madman's Diary", "《狂人日记》", 1918, "小说"),
               ("The True Story of Ah Q", "《阿Q正传》", 1921, "小说"),
               ("Call to Arms", "《呐喊》", 1923, "小说集"),
               ("Wandering", "《彷徨》", 1926, "小说集")],
        events=[(1881, "生于浙江绍兴", "birth"), (1936, "卒于上海", "death"),
                (1902, "赴日本留学，后弃医从文", "life"),
                (1918, "发表《狂人日记》，中国现代文学诞生", "life"),
                (1930, "参与发起中国左翼作家联盟", "life")],
    ),
    dict(
        name="Lao She", name_zh="老舍",
        birth=1899, death=1966, nationality="中国",
        bio_zh="中国现代著名小说家、剧作家，以北京市民生活为题材，《骆驼祥子》《茶馆》是其代表作，文革中投湖自尽。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Lao_She.jpg/330px-Lao_She.jpg",
        tags=["现代文学", "中国文学", "北京文化", "戏剧"],
        works=[("Rickshaw Boy", "《骆驼祥子》", 1937, "小说"),
               ("Teahouse", "《茶馆》", 1957, "戏剧"),
               ("Four Generations Under One Roof", "《四世同堂》", 1946, "小说"),
               ("Cat Country", "《猫城记》", 1932, "小说")],
        events=[(1899, "生于北京", "birth"), (1966, "卒于北京（文革中投湖）", "death"),
                (1924, "赴英国伦敦大学任教", "life"),
                (1950, "回国后创作《龙须沟》", "life")],
    ),
    dict(
        name="Shen Congwen", name_zh="沈从文",
        birth=1902, death=1988, nationality="中国",
        bio_zh="中国现代著名小说家，以湘西为背景构建文学世界，《边城》是其代表作，以诗意笔触描绘乡土中国。1949年后转向文物研究。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Shen_Congwen.jpg/330px-Shen_Congwen.jpg",
        tags=["现代文学", "中国文学", "乡土文学", "湘西"],
        works=[("Border Town", "《边城》", 1934, "小说"),
               ("The Long River", "《长河》", 1945, "小说"),
               ("Xiao Xiao", "《萧萧》", 1925, "小说")],
        events=[(1902, "生于湖南凤凰", "birth"), (1988, "卒于北京", "death"),
                (1923, "只身闯北京开始文学生涯", "life"),
                (1949, "停止文学创作，转向文物研究", "life")],
    ),
    dict(
        name="Zhang Ailing", name_zh="张爱玲",
        birth=1920, death=1995, nationality="中国",
        bio_zh="20世纪中国最重要的女作家之一，以精妙的市民心理描写著称，《倾城之恋》《金锁记》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Eileen_Chang.jpg/330px-Eileen_Chang.jpg",
        tags=["现代文学", "中国文学", "女性文学", "上海"],
        works=[("Love in a Fallen City", "《倾城之恋》", 1943, "小说"),
               ("The Golden Cangue", "《金锁记》", 1943, "小说"),
               ("Lust, Caution", "《色，戒》", 1979, "小说"),
               ("Red Rose White Rose", "《红玫瑰与白玫瑰》", 1944, "小说")],
        events=[(1920, "生于上海", "birth"), (1995, "卒于洛杉矶", "death"),
                (1943, "《倾城之恋》等成名作相继发表", "life"),
                (1952, "离开中国大陆，移居香港", "life"),
                (1955, "移居美国", "life")],
    ),
    dict(
        name="Yu Hua", name_zh="余华",
        birth=1960, death=None, nationality="中国",
        bio_zh="中国当代最重要的小说家之一，以先锋实验起步，后转向现实主义，《活着》《许三观卖血记》震撼人心。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Yu_Hua_in_2012.jpg/330px-Yu_Hua_in_2012.jpg",
        tags=["当代文学", "中国文学", "先锋文学"],
        works=[("To Live", "《活着》", 1992, "小说"),
               ("Chronicle of a Blood Merchant", "《许三观卖血记》", 1995, "小说"),
               ("Brothers", "《兄弟》", 2005, "小说"),
               ("The Seventh Day", "《第七天》", 2013, "小说")],
        events=[(1960, "生于浙江海盐", "birth"),
                (1983, "开始发表先锋小说", "life"),
                (1992, "《活着》发表，转向现实主义", "life")],
    ),
    dict(
        name="Wang Anyi", name_zh="王安忆",
        birth=1954, death=None, nationality="中国",
        bio_zh="中国当代著名女作家，以上海为叙事背景，《长恨歌》获茅盾文学奖，被誉为《海派文学《代表人物。",
        portrait_url=None,
        tags=["当代文学", "中国文学", "女性文学", "上海"],
        works=[("The Song of Everlasting Sorrow", "《长恨歌》", 1995, "小说"),
               ("Brocade Valley", "《锦绣谷之恋》", 1987, "小说"),
               ("Love on a Barren Mountain", "《荒山之恋》", 1986, "小说")],
        events=[(1954, "生于南京，长于上海", "birth"),
                (1995, "《长恨歌》发表", "life"),
                (2004, "《长恨歌》获茅盾文学奖", "life")],
    ),
    # ── 俄国文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Fyodor Dostoevsky", name_zh="陀思妥耶夫斯基",
        birth=1821, death=1881, nationality="俄国",
        bio_zh="俄国伟大的心理小说家，深刻探索人性的善恶与上帝的存在，《罪与罚》《卡拉马佐夫兄弟》是西方文学的高峰。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Dostoevsky_1872.jpg/330px-Dostoevsky_1872.jpg",
        tags=["现实主义", "俄国文学", "心理小说", "存在主义"],
        works=[("Crime and Punishment", "《罪与罚》", 1866, "小说"),
               ("The Idiot", "《白痴》", 1869, "小说"),
               ("The Brothers Karamazov", "《卡拉马佐夫兄弟》", 1880, "小说"),
               ("Notes from Underground", "《地下室手记》", 1864, "小说")],
        events=[(1821, "生于莫斯科", "birth"), (1881, "卒于圣彼得堡", "death"),
                (1849, "因参与革命活动被捕，临刑前获赦，流放西伯利亚", "life"),
                (1866, "《罪与罚》出版", "life")],
    ),
    dict(
        name="Ivan Turgenev", name_zh="屠格涅夫",
        birth=1818, death=1883, nationality="俄国",
        bio_zh="俄国现实主义小说家，以抒情笔触描绘俄国乡村生活，《父与子》引发时代论战，《猎人笔记》呼唤废除农奴制。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Ivan_Turgenev_by_Repin.jpg/330px-Ivan_Turgenev_by_Repin.jpg",
        tags=["现实主义", "俄国文学", "乡村文学"],
        works=[("Fathers and Sons", "《父与子》", 1862, "小说"),
               ("A Sportsman's Sketches", "《猎人笔记》", 1852, "小说集"),
               ("On the Eve", "《前夜》", 1860, "小说")],
        events=[(1818, "生于奥廖尔", "birth"), (1883, "卒于法国布日瓦勒", "death"),
                (1852, "《猎人笔记》出版，呼吁废除农奴制", "life")],
    ),
    dict(
        name="Maxim Gorky", name_zh="高尔基",
        birth=1868, death=1936, nationality="俄国",
        bio_zh="苏联文学奠基人，社会主义现实主义文学的开创者，《母亲》是革命文学的经典，自传三部曲展现底层生活。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Maxim_Gorky_1906.jpg/330px-Maxim_Gorky_1906.jpg",
        tags=["现实主义", "俄国文学", "无产阶级文学"],
        works=[("Mother", "《母亲》", 1906, "小说"),
               ("My Childhood", "《童年》", 1913, "自传"),
               ("The Lower Depths", "《底层》", 1902, "戏剧")],
        events=[(1868, "生于下诺夫哥罗德", "birth"), (1936, "卒于莫斯科", "death"),
                (1917, "俄国革命后积极参与文化建设", "life")],
    ),
    dict(
        name="Mikhail Bulgakov", name_zh="布尔加科夫",
        birth=1891, death=1940, nationality="俄国",
        bio_zh="苏联时期最重要的作家之一，《大师与玛格丽特》是20世纪最伟大的小说之一，生前被禁，死后出版震撼世界。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Bulgakov_nCarl_Bulla.jpg/330px-Bulgakov_nCarl_Bulla.jpg",
        tags=["魔幻现实主义", "俄国文学", "讽刺文学"],
        works=[("The Master and Margarita", "《大师与玛格丽特》", 1967, "小说"),
               ("The White Guard", "《白卫军》", 1925, "小说"),
               ("Heart of a Dog", "《狗心》", 1925, "小说")],
        events=[(1891, "生于基辅", "birth"), (1940, "卒于莫斯科", "death"),
                (1930, "作品遭禁，向斯大林写信请求出境或继续工作", "life"),
                (1967, "《大师与玛格丽特》在其死后27年出版", "life")],
    ),
    # ── 中欧文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Franz Kafka", name_zh="卡夫卡",
        birth=1883, death=1924, nationality="奥地利",
        bio_zh="捷克裔德语作家，20世纪文学最重要的先驱之一，以荒诞笔法揭示现代人的异化处境，生前默默无闻，死后震惊世界。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kafka_portrait.jpg/330px-Kafka_portrait.jpg",
        tags=["现代主义", "存在主义", "荒诞文学"],
        works=[("The Metamorphosis", "《变形记》", 1915, "小说"),
               ("The Trial", "《审判》", 1925, "小说"),
               ("The Castle", "《城堡》", 1926, "小说"),
               ("In the Penal Colony", "《在流放地》", 1919, "小说")],
        events=[(1883, "生于布拉格", "birth"), (1924, "卒于维也纳（肺结核）", "death"),
                (1915, "《变形记》出版", "life"),
                (1924, "临终嘱托友人布罗德销毁手稿，布罗德未执行", "life")],
    ),
    dict(
        name="Stefan Zweig", name_zh="茨威格",
        birth=1881, death=1942, nationality="奥地利",
        bio_zh="奥地利著名作家，以心理传记和中短篇小说著称，《昨日的世界》记录了欧洲文明的兴衰，流亡中与妻子双双自尽。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Stefan_Zweig_1912.jpg/330px-Stefan_Zweig_1912.jpg",
        tags=["现代主义", "奥地利文学", "心理小说"],
        works=[("The World of Yesterday", "《昨日的世界》", 1942, "自传"),
               ("Letter from an Unknown Woman", "《一个陌生女人的来信》", 1922, "小说"),
               ("Chess Story", "《象棋的故事》", 1942, "小说")],
        events=[(1881, "生于维也纳", "birth"), (1942, "卒于巴西彼得罗波利斯（自尽）", "death"),
                (1934, "因纳粹迫害流亡英国", "life"),
                (1941, "移居巴西，对欧洲文明的消逝感到绝望", "life")],
    ),
    dict(
        name="Hermann Hesse", name_zh="黑塞",
        birth=1877, death=1962, nationality="德国",
        bio_zh="德裔瑞士作家，诺贝尔文学奖得主，融合东西方哲学，《悉达多》《荒原狼》《玻璃球游戏》探索人的精神旅程。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Hesse_Portrait.jpg/330px-Hesse_Portrait.jpg",
        tags=["现代主义", "德语文学", "东方哲学"],
        works=[("Siddhartha", "《悉达多》", 1922, "小说"),
               ("Steppenwolf", "《荒原狼》", 1927, "小说"),
               ("The Glass Bead Game", "《玻璃球游戏》", 1943, "小说"),
               ("Demian", "《德米安》", 1919, "小说")],
        events=[(1877, "生于卡尔夫", "birth"), (1962, "卒于蒙塔尼奥拉", "death"),
                (1946, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Thomas Mann", name_zh="托马斯·曼",
        birth=1875, death=1955, nationality="德国",
        bio_zh="德国20世纪最重要的小说家，诺贝尔文学奖得主，《魔山》《布登勃洛克家族》以宏大叙事探讨欧洲文明的衰落。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Thomas_Mann_1929.jpg/330px-Thomas_Mann_1929.jpg",
        tags=["现代主义", "德语文学", "史诗小说"],
        works=[("Buddenbrooks", "《布登勃洛克家族》", 1901, "小说"),
               ("The Magic Mountain", "《魔山》", 1924, "小说"),
               ("Death in Venice", "《威尼斯之死》", 1912, "小说")],
        events=[(1875, "生于吕贝克", "birth"), (1955, "卒于苏黎世", "death"),
                (1929, "获诺贝尔文学奖", "life"),
                (1933, "因反对纳粹流亡海外", "life")],
    ),
    # ── 英美文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Virginia Woolf", name_zh="伍尔夫",
        birth=1882, death=1941, nationality="英国",
        bio_zh="英国现代主义文学大师，意识流小说的开创者之一，《到灯塔去》《达洛维夫人》以诗意散文探索意识与时间，投河自尽。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/George_Charles_Beresford_-_Virginia_Woolf_in_1902_-_restoration.jpg/330px-George_Charles_Beresford_-_Virginia_Woolf_in_1902_-_restoration.jpg",
        tags=["现代主义", "英国文学", "意识流", "女性文学"],
        works=[("Mrs Dalloway", "《达洛维夫人》", 1925, "小说"),
               ("To the Lighthouse", "《到灯塔去》", 1927, "小说"),
               ("The Waves", "《海浪》", 1931, "小说"),
               ("A Room of One's Own", "《一间自己的房间》", 1929, "散文")],
        events=[(1882, "生于伦敦", "birth"), (1941, "投河自尽，卒于塞克斯郡", "death"),
                (1917, "与丈夫创办霍加斯出版社", "life"),
                (1925, "《达洛维夫人》出版", "life")],
    ),
    dict(
        name="Ernest Hemingway", name_zh="海明威",
        birth=1899, death=1961, nationality="美国",
        bio_zh="美国现代文学大师，诺贝尔文学奖得主，以简洁《冰山理论《写作风格著称，《老人与海》是其代表作，晚年自杀。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/ErnestHemingway.jpg/330px-ErnestHemingway.jpg",
        tags=["现代主义", "美国文学", "简洁主义", "迷惘的一代"],
        works=[("The Old Man and the Sea", "《老人与海》", 1952, "小说"),
               ("A Farewell to Arms", "《永别了，武器》", 1929, "小说"),
               ("The Sun Also Rises", "《太阳照常升起》", 1926, "小说"),
               ("For Whom the Bell Tolls", "《丧钟为谁而鸣》", 1940, "小说")],
        events=[(1899, "生于伊利诺伊州奥克帕克", "birth"), (1961, "卒于爱达荷州（自杀）", "death"),
                (1918, "一战期间赴意大利战场，身负重伤", "life"),
                (1954, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="William Faulkner", name_zh="福克纳",
        birth=1897, death=1962, nationality="美国",
        bio_zh="美国南方文学大师，诺贝尔文学奖得主，以约克纳帕塌法县构建南方神话，意识流技法登峰造极，《喧哗与骚动》是其代表作。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/William_Faulkner_1954.jpg/330px-William_Faulkner_1954.jpg",
        tags=["现代主义", "美国文学", "意识流", "南方文学"],
        works=[("The Sound and the Fury", "《喧哗与骚动》", 1929, "小说"),
               ("As I Lay Dying", "《我弥留之际》", 1930, "小说"),
               ("Absalom, Absalom!", "《押沙龙，押沙龙！》", 1936, "小说")],
        events=[(1897, "生于密西西比州", "birth"), (1962, "卒于密西西比州", "death"),
                (1950, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="F. Scott Fitzgerald", name_zh="菲茨杰拉德",
        birth=1896, death=1940, nationality="美国",
        bio_zh="美国《爵士时代《代言人，《了不起的盖茨比》是美国文学史上最完美的小说之一，以绚烂与幻灭诠释美国梦。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/F_Scott_Fitzgerald_1921.jpg/330px-F_Scott_Fitzgerald_1921.jpg",
        tags=["现代主义", "美国文学", "迷惘的一代", "美国梦"],
        works=[("The Great Gatsby", "《了不起的盖茨比》", 1925, "小说"),
               ("Tender Is the Night", "《夜色温柔》", 1934, "小说"),
               ("This Side of Paradise", "《人间天堂》", 1920, "小说")],
        events=[(1896, "生于明尼苏达州圣保罗", "birth"), (1940, "卒于好莱坞（心脏病）", "death"),
                (1925, "《了不起的盖茨比》出版", "life")],
    ),
    # ── 法国文学（继续）──────────────────────────────────────────────────────
    dict(
        name="Albert Camus", name_zh="加缪",
        birth=1913, death=1960, nationality="法国",
        bio_zh="法国存在主义/荒诞主义作家，诺贝尔文学奖得主，《局外人》《鼠疫》以冷峻笔触探讨荒诞与反抗，42岁死于车祸。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Albert_Camus%2C_gagnant_de_prix_Nobel%2C_portrait_en_buste%2C_pos%C3%A9_au_bureau%2C_faisant_face_%C3%A0_gauche%2C_cigarette_de_tabagisme.jpg/330px-Albert_Camus%2C_gagnant_de_prix_Nobel%2C_portrait_en_buste%2C_pos%C3%A9_au_bureau%2C_faisant_face_%C3%A0_gauche%2C_cigarette_de_tabagisme.jpg",
        tags=["存在主义", "荒诞主义", "法国文学"],
        works=[("The Stranger", "《局外人》", 1942, "小说"),
               ("The Plague", "《鼠疫》", 1947, "小说"),
               ("The Myth of Sisyphus", "《西西弗神话》", 1942, "哲学"),
               ("The Fall", "《堕落》", 1956, "小说")],
        events=[(1913, "生于阿尔及利亚蒙多维", "birth"), (1960, "卒于桑斯附近（车祸）", "death"),
                (1942, "《局外人》与《西西弗神话》同年出版", "life"),
                (1957, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Simone de Beauvoir", name_zh="波伏娃",
        birth=1908, death=1986, nationality="法国",
        bio_zh="法国存在主义哲学家、女性主义先驱，《第二性》是女性主义奠基之作，与萨特终身伴侣，共同引领20世纪思想解放。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Simone_de_Beauvoir2.png/330px-Simone_de_Beauvoir2.png",
        tags=["存在主义", "女性主义", "法国文学", "哲学"],
        works=[("The Second Sex", "《第二性》", 1949, "哲学"),
               ("The Mandarins", "《名士风流》", 1954, "小说"),
               ("Memoirs of a Dutiful Daughter", "《端方淑女回忆录》", 1958, "自传")],
        events=[(1908, "生于巴黎", "birth"), (1986, "卒于巴黎", "death"),
                (1949, "《第二性》出版，掀起女性主义思潮", "life")],
    ),
    # ── 拉美文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Gabriel García Márquez", name_zh="加西亚·马尔克斯",
        birth=1927, death=2014, nationality="哥伦比亚",
        bio_zh="哥伦比亚小说家，诺贝尔文学奖得主，魔幻现实主义文学的代表人物，《百年孤独》是20世纪西班牙语最伟大的作品。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Gabriel_Garcia_Marquez.jpg/330px-Gabriel_Garcia_Marquez.jpg",
        tags=["魔幻现实主义", "拉美文学", "西班牙语文学"],
        works=[("One Hundred Years of Solitude", "《百年孤独》", 1967, "小说"),
               ("Love in the Time of Cholera", "《霍乱时期的爱情》", 1985, "小说"),
               ("No One Writes to the Colonel", "《没有人给他写信的上校》", 1961, "小说")],
        events=[(1927, "生于哥伦比亚阿拉卡塔卡", "birth"), (2014, "卒于墨西哥城", "death"),
                (1967, "《百年孤独》出版，引发全球文学震动", "life"),
                (1982, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Jorge Luis Borges", name_zh="博尔赫斯",
        birth=1899, death=1986, nationality="阿根廷",
        bio_zh="阿根廷作家，20世纪文学的魔术师，以迷宫、镜子、图书馆等意象构建无限宇宙，影响了无数后世作家。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Jorge_Luis_Borges_1951%2C_by_Grete_Stern.jpg/330px-Jorge_Luis_Borges_1951%2C_by_Grete_Stern.jpg",
        tags=["魔幻现实主义", "拉美文学", "后现代文学"],
        works=[("Ficciones", "《虚构集》", 1944, "短篇集"),
               ("The Aleph", "《阿莱夫》", 1949, "短篇集"),
               ("Labyrinths", "《迷宫》", 1962, "短篇集")],
        events=[(1899, "生于布宜诺斯艾利斯", "birth"), (1986, "卒于日内瓦", "death"),
                (1955, "双目失明，仍坚持创作", "life"),
                (1961, "获福门托尔国际文学奖", "life")],
    ),
    dict(
        name="Pablo Neruda", name_zh="聂鲁达",
        birth=1904, death=1973, nationality="智利",
        bio_zh="智利诗人，诺贝尔文学奖得主，以激情澎湃的诗歌著称，《二十首情诗和一首绝望的歌》是拉丁美洲最广泛阅读的诗集。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Pablo_Neruda_1963.jpg/330px-Pablo_Neruda_1963.jpg",
        tags=["诗歌", "拉美文学", "政治文学"],
        works=[("Twenty Love Poems", "《二十首情诗和一首绝望的歌》", 1924, "诗集"),
               ("Canto General", "《诗歌总集》", 1950, "诗集"),
               ("Odes to Common Things", "《元素颂》", 1954, "诗集")],
        events=[(1904, "生于智利帕拉尔", "birth"), (1973, "卒于圣地亚哥（皮诺切特政变后12天）", "death"),
                (1971, "获诺贝尔文学奖", "life")],
    ),
    # ── 日本文学 ──────────────────────────────────────────────────────────────
    dict(
        name="Yasunari Kawabata", name_zh="川端康成",
        birth=1899, death=1972, nationality="日本",
        bio_zh="日本第一位诺贝尔文学奖得主，以纤细感伤的美学著称，《雪国》《古都》展现了日本传统美的凄婉哀愁。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Yasunari_Kawabata_1938.jpg/330px-Yasunari_Kawabata_1938.jpg",
        tags=["日本文学", "唯美主义", "新感觉派"],
        works=[("Snow Country", "《雪国》", 1956, "小说"),
               ("The Sound of the Mountain", "《山音》", 1954, "小说"),
               ("The Old Capital", "《古都》", 1962, "小说"),
               ("The Dancing Girl of Izu", "《伊豆的舞女》", 1926, "小说")],
        events=[(1899, "生于大阪", "birth"), (1972, "卒于神奈川（自杀）", "death"),
                (1968, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Yukio Mishima", name_zh="三岛由纪夫",
        birth=1925, death=1970, nationality="日本",
        bio_zh="日本战后最重要的作家之一，以极端美学和右翼政治著称，《金阁寺》是其代表作，1970年率众兵变失败后切腹自尽。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Yukio_Mishima.jpg/330px-Yukio_Mishima.jpg",
        tags=["日本文学", "唯美主义", "战后文学"],
        works=[("The Temple of the Golden Pavilion", "《金阁寺》", 1956, "小说"),
               ("Confessions of a Mask", "《假面的告白》", 1949, "小说"),
               ("The Sea of Fertility", "《丰饶之海》", 1970, "小说")],
        events=[(1925, "生于东京", "birth"), (1970, "发动兵变失败，切腹自尽", "death"),
                (1970, "《丰饶之海》四部曲完结当天自杀", "life")],
    ),
    dict(
        name="Kenzaburo Oe", name_zh="大江健三郎",
        birth=1935, death=2023, nationality="日本",
        bio_zh="日本第二位诺贝尔文学奖得主，以战后日本的精神创伤和残障儿子为素材，创作了深刻的个人神话体系。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Kenzaburo_Oe-press_conference_Dec_07_2006-3.jpg/330px-Kenzaburo_Oe-press_conference_Dec_07_2006-3.jpg",
        tags=["日本文学", "战后文学", "个人神话"],
        works=[("A Personal Matter", "《个人的体验》", 1964, "小说"),
               ("The Silent Cry", "《万延元年的足球队》", 1967, "小说"),
               ("Rouse Up O Young Men of the New Age!", "《新人呵，醒来吧》", 1983, "小说")],
        events=[(1935, "生于爱媛县", "birth"), (2023, "卒于东京", "death"),
                (1963, "长子光出生时脑疝，成为创作核心主题", "life"),
                (1994, "获诺贝尔文学奖", "life")],
    ),
    dict(
        name="Haruki Murakami", name_zh="村上春树",
        birth=1949, death=None, nationality="日本",
        bio_zh="当代日本最具国际影响力的作家，融合西方流行文化与日本传统，《挪威的森林》《1Q84》在全球拥有大量读者。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Murakami_Haruki_%282009%29.jpg/330px-Murakami_Haruki_%282009%29.jpg",
        tags=["当代文学", "日本文学", "魔幻现实主义"],
        works=[("Norwegian Wood", "《挪威的森林》", 1987, "小说"),
               ("Kafka on the Shore", "《海边的卡夫卡》", 2002, "小说"),
               ("1Q84", "《1Q84》", 2009, "小说"),
               ("The Wind-Up Bird Chronicle", "《奇鸟行状录》", 1994, "小说")],
        events=[(1949, "生于京都", "birth"),
                (1987, "《挪威的森林》畅销，奠定国际声誉", "life")],
    ),
    # ── 其他重要作家 ──────────────────────────────────────────────────────────
    dict(
        name="Rabindranath Tagore", name_zh="泰戈尔",
        birth=1861, death=1941, nationality="印度",
        bio_zh="印度伟大诗人、作家、哲学家，亚洲第一位诺贝尔文学奖得主，《吉檀迦利》以神秘主义与人道主义感动世界。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Rabindranath_Tagore_in_1909.jpg/330px-Rabindranath_Tagore_in_1909.jpg",
        tags=["诗歌", "印度文学", "神秘主义"],
        works=[("Gitanjali", "《吉檀迦利》", 1910, "诗集"),
               ("The Home and the World", "《家与世界》", 1916, "小说"),
               ("Gora", "《戈拉》", 1910, "小说")],
        events=[(1861, "生于加尔各答", "birth"), (1941, "卒于加尔各答", "death"),
                (1913, "获诺贝尔文学奖，亚洲第一人", "life"),
                (1924, "访问中国，受到热烈欢迎", "life")],
    ),
    dict(
        name="Italo Calvino", name_zh="卡尔维诺",
        birth=1923, death=1985, nationality="意大利",
        bio_zh="意大利后现代文学大师，以充满想象力的叙事结构著称，《看不见的城市》《如果在冬夜，一个旅人》是元小说经典。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/ItaloCalvino.jpg/330px-ItaloCalvino.jpg",
        tags=["后现代文学", "意大利文学", "元小说"],
        works=[("Invisible Cities", "《看不见的城市》", 1972, "小说"),
               ("If on a winter's night a traveler", "《如果在冬夜，一个旅人》", 1979, "小说"),
               ("Our Ancestors", "《我们的祖先》", 1960, "小说")],
        events=[(1923, "生于古巴圣地亚哥", "birth"), (1985, "卒于锡耶纳（脑溢血）", "death"),
                (1972, "《看不见的城市》出版", "life")],
    ),
    dict(
        name="Samuel Beckett", name_zh="贝克特",
        birth=1906, death=1989, nationality="爱尔兰",
        bio_zh="爱尔兰剧作家、小说家，诺贝尔文学奖得主，荒诞派戏剧的代表人物，《等待戈多》以极简方式揭示存在的荒诞。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Samuel_Beckett%2C_Pic%2C_1.jpg/330px-Samuel_Beckett%2C_Pic%2C_1.jpg",
        tags=["荒诞派", "爱尔兰文学", "戏剧", "现代主义"],
        works=[("Waiting for Godot", "《等待戈多》", 1953, "戏剧"),
               ("Endgame", "《终局》", 1957, "戏剧"),
               ("Molloy", "《莫洛伊》", 1951, "小说")],
        events=[(1906, "生于都柏林", "birth"), (1989, "卒于巴黎", "death"),
                (1953, "《等待戈多》在巴黎首演，震惊戏剧界", "life"),
                (1969, "获诺贝尔文学奖", "life")],
    ),
]


async def seed():
    raw_url = os.environ.get("DATABASE_URL", "")
    import re
    raw_url = re.sub(r"^postgresql(\+asyncpg)?://", "postgresql+asyncpg://", raw_url)
    raw_url = re.sub(r"[?&]sslmode=[^&]*", "", raw_url)
    raw_url = re.sub(r"[?&]channel_binding=[^&]*", "", raw_url)

    engine = create_async_engine(raw_url, echo=False, connect_args={"ssl": "require"})
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    added = skipped = 0
    async with Session() as session:
        for a in AUTHORS:
            exists = await session.scalar(
                select(Author).where(Author.name_zh == a["name_zh"])
            )
            if exists:
                print(f"  跳过: {a['name_zh']} (已存在)")
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
