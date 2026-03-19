"""
作家年表 · 第五批（~27 位）
西方古希腊罗马 + 中国古代（先秦→清）
运行：DATABASE_URL=postgresql+asyncpg://joker@localhost:5432/zuojia_nianbiao \
      /Users/joker/zuojia-nianbiao/.venv/bin/python -m backend.seed_authors5
"""
import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Author, Work, AuthorEvent

AUTHORS = [
    # ── 西方古希腊 ───────────────────────────────────────────────────────────
    dict(
        name="Homer", name_zh="荷马",
        birth=-800, death=-701, nationality="古希腊",
        bio_zh="古希腊盲诗人，西方文学史的起点，《伊利亚特》与《奥德赛》奠定了欧洲叙事文学、英雄形象与命运观念的基本原型，被誉为'西方文学之父'。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Homer_British_Museum.jpg/330px-Homer_British_Museum.jpg",
        tags=["古希腊文学", "史诗", "神话"],
        works=[("Iliad", "《伊利亚特》", -750, "史诗"),
               ("Odyssey", "《奥德赛》", -725, "史诗")],
        events=[(-800, "活跃于约公元前8世纪，生平不详", "birth"),
                (-750, "《伊利亚特》《奥德赛》口头流传成型", "life")],
    ),
    dict(
        name="Aeschylus", name_zh="埃斯库罗斯",
        birth=-525, death=-456, nationality="古希腊",
        bio_zh="古希腊悲剧之父，三大悲剧诗人中最年长者，以《俄瑞斯忒亚》三部曲确立了悲剧的基本形式，首创第二演员制，将希腊戏剧从祭祀仪式推向成熟艺术。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Aischylos_Glyptothek_Munich_261_-_new_background.jpg/330px-Aischylos_Glyptothek_Munich_261_-_new_background.jpg",
        tags=["古希腊文学", "悲剧"],
        works=[("Oresteia", "《俄瑞斯忒亚》三部曲", -458, "悲剧"),
               ("Prometheus Bound", "《被缚的普罗米修斯》", -460, "悲剧"),
               ("The Persians", "《波斯人》", -472, "悲剧")],
        events=[(-525, "生于埃琉西斯", "birth"),
                (-456, "卒于西西里", "death"),
                (-490, "参加马拉松战役", "life")],
    ),
    dict(
        name="Sophocles", name_zh="索福克勒斯",
        birth=-496, death=-406, nationality="古希腊",
        bio_zh="古希腊三大悲剧诗人之一，以《俄底浦斯王》《安提戈涅》展现命运与人类意志的对抗，其悲剧结构严谨、情节紧凑，被亚里士多德视为最完美的悲剧范本。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Sophocles_pushkin.jpg/330px-Sophocles_pushkin.jpg",
        tags=["古希腊文学", "悲剧", "命运"],
        works=[("Oedipus Rex", "《俄底浦斯王》", -429, "悲剧"),
               ("Antigone", "《安提戈涅》", -441, "悲剧"),
               ("Electra", "《厄勒克特拉》", -410, "悲剧")],
        events=[(-496, "生于雅典科罗诺斯", "birth"),
                (-406, "卒于雅典", "death")],
    ),
    dict(
        name="Euripides", name_zh="欧里庇得斯",
        birth=-480, death=-406, nationality="古希腊",
        bio_zh="古希腊三大悲剧诗人中最具现代感的一位，以《美狄亚》《特洛伊妇女》揭示战争残酷与女性困境，大量引入心理冲突，被誉为'哲学的悲剧诗人'。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Euripides_Pio-Clementino_Inv302.jpg/330px-Euripides_Pio-Clementino_Inv302.jpg",
        tags=["古希腊文学", "悲剧", "女性主义"],
        works=[("Medea", "《美狄亚》", -431, "悲剧"),
               ("The Trojan Women", "《特洛伊妇女》", -415, "悲剧"),
               ("Bacchae", "《酒神的伴侣》", -405, "悲剧")],
        events=[(-480, "生于萨拉米斯岛", "birth"),
                (-406, "卒于马其顿", "death")],
    ),
    dict(
        name="Virgil", name_zh="维吉尔",
        birth=-70, death=-19, nationality="古罗马",
        bio_zh="古罗马最伟大的诗人，以《埃涅阿斯记》为罗马建国神话树碑立传，其史诗继承荷马传统又融入罗马精神，深刻影响中世纪与文艺复兴文学。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Virgil_mosaic_-_Bardo_National_Museum.jpg/330px-Virgil_mosaic_-_Bardo_National_Museum.jpg",
        tags=["古罗马文学", "史诗"],
        works=[("Aeneid", "《埃涅阿斯记》", -19, "史诗"),
               ("Georgics", "《农事诗》", -29, "诗歌"),
               ("Eclogues", "《牧歌》", -37, "诗集")],
        events=[(-70, "生于曼图亚附近", "birth"),
                (-19, "卒于布林迪西", "death"),
                (-29, "获奥古斯都庇护，专注创作《埃涅阿斯记》", "life")],
    ),
    dict(
        name="Ovid", name_zh="奥维德",
        birth=-43, death=17, nationality="古罗马",
        bio_zh="古罗马诗人，以《变形记》将希腊罗马神话汇为一部宏大诗集，文笔优雅流畅，对文艺复兴及后世欧洲文学产生了深远影响。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Publius_Ovidius_Naso.jpg/330px-Publius_Ovidius_Naso.jpg",
        tags=["古罗马文学", "神话", "诗歌"],
        works=[("Metamorphoses", "《变形记》", 8, "长诗"),
               ("The Art of Love", "《爱的艺术》", -2, "教诲诗"),
               ("Tristia", "《哀怨诗集》", 9, "诗集")],
        events=[(-43, "生于苏尔莫纳", "birth"),
                (17, "卒于托米斯（今罗马尼亚）", "death"),
                (8, "被奥古斯都流放黑海沿岸，原因不明", "life")],
    ),
    # ── 中国先秦秦汉 ─────────────────────────────────────────────────────────
    dict(
        name="Sima Qian", name_zh="司马迁",
        birth=-145, death=-86, nationality="中国（西汉）",
        bio_zh="中国古代最伟大的史学家与文学家，《史记》首创纪传体通史，以'究天人之际，通古今之变，成一家之言'为志，忍受宫刑之辱完成旷世巨著。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Sima_Qian_%28painted_portrait%29.jpg/330px-Sima_Qian_%28painted_portrait%29.jpg",
        tags=["中国古代文学", "史传文学", "汉代"],
        works=[("Records of the Grand Historian", "《史记》", -91, "史传")],
        events=[(-145, "生于龙门（今陕西韩城）", "birth"),
                (-86, "卒于长安（约）", "death"),
                (-99, "因为李陵辩护触怒汉武帝，受宫刑", "life"),
                (-91, "忍辱完成《史记》130篇", "life")],
    ),
    # ── 中国魏晋 ─────────────────────────────────────────────────────────────
    dict(
        name="Cao Cao", name_zh="曹操",
        birth=155, death=220, nationality="中国（东汉末）",
        bio_zh="东汉末年政治家、军事家、文学家，建安文学领袖，以《短歌行》《观沧海》开创慷慨悲凉的'建安风骨'，奠定了中国古代文人诗的基调。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Cao_Cao.jpg/330px-Cao_Cao.jpg",
        tags=["中国古代文学", "建安文学", "诗歌"],
        works=[("Short Song", "《短歌行》", 208, "诗歌"),
               ("View of the Sea", "《观沧海》", 207, "诗歌")],
        events=[(155, "生于谯县（今安徽亳州）", "birth"),
                (220, "卒于洛阳", "death"),
                (208, "赤壁之战前夕赋《短歌行》", "life")],
    ),
    dict(
        name="Cao Zhi", name_zh="曹植",
        birth=192, death=232, nationality="中国（三国）",
        bio_zh="曹操之子，三国时期最重要的诗人，以《洛神赋》《白马篇》将建安文学推至顶峰，'七步成诗'的典故流传至今，钟嵘赞其为'骨气奇高，词采华茂'。",
        portrait_url=None,
        tags=["中国古代文学", "建安文学", "诗歌"],
        works=[("Ode to the Goddess of the Luo River", "《洛神赋》", 222, "辞赋"),
               ("White Horse", "《白马篇》", 215, "诗歌")],
        events=[(192, "生于谯县", "birth"),
                (232, "卒于陈郡（今河南淮阳）", "death"),
                (220, "曹丕称帝后备受猜忌，屡遭迁徙", "life")],
    ),
    # ── 中国唐代 ─────────────────────────────────────────────────────────────
    dict(
        name="Li Bai", name_zh="李白",
        birth=701, death=762, nationality="中国（唐朝）",
        bio_zh="中国最伟大的浪漫主义诗人，号'诗仙'，以豪放飘逸的诗风歌颂自然与自由，《将进酒》《静夜思》《蜀道难》流传千古，是唐诗盛唐气象的最高代表。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Li_Bai_1701.jpg/330px-Li_Bai_1701.jpg",
        tags=["中国古代文学", "唐诗", "浪漫主义"],
        works=[("Invitation to Wine", "《将进酒》", 752, "诗歌"),
               ("The Hard Road to Shu", "《蜀道难》", 742, "诗歌"),
               ("Quiet Night Thought", "《静夜思》", 726, "诗歌")],
        events=[(701, "生于碎叶城（今吉尔吉斯斯坦）", "birth"),
                (762, "卒于当涂", "death"),
                (742, "应诏入长安，供奉翰林", "life"),
                (744, "遭谗言被逐出长安，开始漫游", "life")],
    ),
    dict(
        name="Du Fu", name_zh="杜甫",
        birth=712, death=770, nationality="中国（唐朝）",
        bio_zh="中国最伟大的现实主义诗人，号'诗圣'，以'诗史'般的笔触记录安史之乱中黎民苍生的苦难，《春望》《三吏》《三别》是中国诗歌史的道德高峰。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Du_Fu.jpg/330px-Du_Fu.jpg",
        tags=["中国古代文学", "唐诗", "现实主义"],
        works=[("Spring View", "《春望》", 757, "诗歌"),
               ("Three Officials", "《三吏》", 759, "组诗"),
               ("Three Farewells", "《三别》", 759, "组诗"),
               ("Thatched Cottage", "《茅屋为秋风所破歌》", 761, "诗歌")],
        events=[(712, "生于河南巩县", "birth"),
                (770, "卒于衡州（今湖南衡阳）途中", "death"),
                (755, "安史之乱爆发，开始流亡", "life"),
                (759, "弃官入蜀，定居成都草堂", "life")],
    ),
    dict(
        name="Bai Juyi", name_zh="白居易",
        birth=772, death=846, nationality="中国（唐朝）",
        bio_zh="唐代中期最重要的诗人之一，倡导'新乐府运动'，以平易近人的语言写作讽喻诗，《长恨歌》《琵琶行》是中国叙事诗的典范，相传老妪能解其诗。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bai_Juyi_by_Chen_Hongshou.jpg/330px-Bai_Juyi_by_Chen_Hongshou.jpg",
        tags=["中国古代文学", "唐诗", "新乐府"],
        works=[("Song of Everlasting Regret", "《长恨歌》", 806, "叙事诗"),
               ("Pipa Song", "《琵琶行》", 816, "叙事诗")],
        events=[(772, "生于新郑（今河南）", "birth"),
                (846, "卒于洛阳", "death"),
                (806, "创作《长恨歌》，名震一时", "life"),
                (815, "因直言进谏贬谪江州，创作《琵琶行》", "life")],
    ),
    dict(
        name="Han Yu", name_zh="韩愈",
        birth=768, death=824, nationality="中国（唐朝）",
        bio_zh="唐代古文运动领袖，唐宋八大家之首，以'文以载道'为纲，反对骈文复兴先秦两汉散文传统，《师说》《马说》是中国古典散文的经典。",
        portrait_url=None,
        tags=["中国古代文学", "唐代散文", "古文运动"],
        works=[("On the Teacher", "《师说》", 802, "散文"),
               ("On Horses", "《马说》", 796, "散文")],
        events=[(768, "生于河阳（今河南孟州）", "birth"),
                (824, "卒于长安", "death"),
                (803, "因谏旱灾被贬阳山令", "life"),
                (819, "因《论佛骨表》触怒宪宗，贬潮州刺史", "life")],
    ),
    # ── 中国五代宋代 ─────────────────────────────────────────────────────────
    dict(
        name="Li Yu", name_zh="李煜",
        birth=937, death=978, nationality="中国（南唐）",
        bio_zh="南唐末代国主，词史上承前启后的关键人物，亡国后以词寄托家国之痛，《虞美人》《浪淘沙》等作以真情实感突破花间词的艳丽局限，开词之新境。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Li_Yu.jpg/330px-Li_Yu.jpg",
        tags=["中国古代文学", "宋词", "南唐"],
        works=[("Yu Meiren", "《虞美人》", 978, "词"),
               ("Lang Tao Sha", "《浪淘沙·帘外雨潺潺》", 975, "词")],
        events=[(937, "生于金陵（今南京）", "birth"),
                (978, "被宋太宗毒杀于汴京", "death"),
                (975, "南唐亡国，被俘至汴京", "life")],
    ),
    dict(
        name="Liu Yong", name_zh="柳永",
        birth=987, death=1053, nationality="中国（北宋）",
        bio_zh="北宋词人，婉约派代表，第一个大量创作慢词的词人，以市井俗语入词，开拓了词的题材与音乐形式，'凡有井水处，皆能歌柳词'。",
        portrait_url=None,
        tags=["中国古代文学", "宋词", "婉约派"],
        works=[("Rain Shower Bells", "《雨霖铃》", 1030, "词"),
               ("Wanghai Chao", "《望海潮》", 1015, "词")],
        events=[(987, "生于崇安（今福建武夷山）", "birth"),
                (1053, "卒（约）", "death"),
                (1034, "四度落第后终于中进士，已年近五十", "life")],
    ),
    dict(
        name="Su Shi", name_zh="苏轼",
        birth=1037, death=1101, nationality="中国（北宋）",
        bio_zh="北宋文学艺术的全才巨擘，唐宋八大家之一，词开豪放一派，散文、书法、绘画无一不精，《赤壁赋》《念奴娇·赤壁怀古》是宋代文学最高成就的标志。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Su_Dongpo.jpg/330px-Su_Dongpo.jpg",
        tags=["中国古代文学", "宋词", "豪放派", "散文"],
        works=[("Ode to Red Cliff", "《赤壁赋》", 1082, "赋"),
               ("Nian Nu Jiao: Red Cliff Nostalgia", "《念奴娇·赤壁怀古》", 1082, "词"),
               ("Shui Diao Ge Tou", "《水调歌头·明月几时有》", 1076, "词")],
        events=[(1037, "生于眉山（今四川）", "birth"),
                (1101, "卒于常州", "death"),
                (1079, "乌台诗案，被贬黄州", "life"),
                (1094, "再度被贬惠州、儋州", "life")],
    ),
    dict(
        name="Li Qingzhao", name_zh="李清照",
        birth=1084, death=1155, nationality="中国（两宋）",
        bio_zh="中国古代最杰出的女词人，婉约派集大成者，前期词明丽清新，后期词哀婉沉郁，《声声慢》《如梦令》以女性视角写出了词史上无人超越的细腻情感。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Li_Qingzhao.jpg/330px-Li_Qingzhao.jpg",
        tags=["中国古代文学", "宋词", "婉约派", "女性文学"],
        works=[("Sheng Sheng Man", "《声声慢》", 1130, "词"),
               ("Ru Meng Ling", "《如梦令》", 1100, "词"),
               ("Yi Jian Mei", "《一剪梅》", 1101, "词")],
        events=[(1084, "生于济南（今山东）", "birth"),
                (1155, "卒于临安（约）", "death"),
                (1127, "靖康之变，南渡，丈夫赵明诚去世", "life")],
    ),
    dict(
        name="Xin Qiji", name_zh="辛弃疾",
        birth=1140, death=1207, nationality="中国（南宋）",
        bio_zh="南宋最重要的词人，豪放派集大成者，一生以恢复中原为志，《破阵子》《青玉案·元夕》《永遇乐·京口北固亭怀古》将爱国情怀与豪壮词风融为一体。",
        portrait_url=None,
        tags=["中国古代文学", "宋词", "豪放派", "爱国"],
        works=[("Po Zhen Zi", "《破阵子·为陈同甫赋壮词以寄之》", 1188, "词"),
               ("Qing Yu An: Lantern Festival", "《青玉案·元夕》", 1174, "词"),
               ("Yong Yu Le", "《永遇乐·京口北固亭怀古》", 1205, "词")],
        events=[(1140, "生于历城（今济南）", "birth"),
                (1207, "卒于铅山（今江西）", "death"),
                (1162, "南渡归宋，此后长期遭投降派排挤", "life")],
    ),
    # ── 中国元代 ─────────────────────────────────────────────────────────────
    dict(
        name="Guan Hanqing", name_zh="关汉卿",
        birth=1234, death=1300, nationality="中国（元朝）",
        bio_zh="元代最伟大的杂剧作家，元曲四大家之首，一生创作杂剧六十余种，《窦娥冤》以感天动地的悲剧力量控诉黑暗司法，是中国古典戏曲的不朽之作。",
        portrait_url=None,
        tags=["中国古代文学", "元杂剧", "戏曲"],
        works=[("The Injustice to Dou E", "《窦娥冤》", 1280, "杂剧"),
               ("Rescued by a Coquette", "《救风尘》", 1280, "杂剧"),
               ("The Riverside Pavilion", "《望江亭》", 1280, "杂剧")],
        events=[(1234, "约生于大都（今北京）", "birth"),
                (1300, "约卒于元大都", "death")],
    ),
    # ── 中国明代 ─────────────────────────────────────────────────────────────
    dict(
        name="Luo Guanzhong", name_zh="罗贯中",
        birth=1330, death=1400, nationality="中国（元末明初）",
        bio_zh="中国章回小说的奠基人，《三国演义》将历史与虚构融合，塑造了曹操、诸葛亮等千古人物形象，是中国白话长篇小说的开山之作。",
        portrait_url=None,
        tags=["中国古代文学", "明代小说", "历史小说"],
        works=[("Romance of the Three Kingdoms", "《三国演义》", 1380, "小说")],
        events=[(1330, "约生于太原（今山西）", "birth"),
                (1400, "约卒", "death")],
    ),
    dict(
        name="Shi Nai'an", name_zh="施耐庵",
        birth=1296, death=1370, nationality="中国（元末明初）",
        bio_zh="《水浒传》的主要作者，以梁山一百零八将的传奇故事描绘官逼民反的社会主题，开创了中国英雄传奇小说的叙事传统。",
        portrait_url=None,
        tags=["中国古代文学", "明代小说", "英雄传奇"],
        works=[("Water Margin", "《水浒传》", 1370, "小说")],
        events=[(1296, "约生于兴化（今江苏）", "birth"),
                (1370, "约卒", "death")],
    ),
    dict(
        name="Wu Cheng'en", name_zh="吴承恩",
        birth=1500, death=1582, nationality="中国（明朝）",
        bio_zh="明代小说家，以《西游记》将唐僧西行取经的历史演化为浪漫主义神魔小说，孙悟空的形象成为中国文化中最重要的神话人物之一。",
        portrait_url=None,
        tags=["中国古代文学", "明代小说", "神魔小说"],
        works=[("Journey to the West", "《西游记》", 1570, "小说")],
        events=[(1500, "约生于淮安（今江苏）", "birth"),
                (1582, "约卒于淮安", "death")],
    ),
    dict(
        name="Tang Xianzu", name_zh="汤显祖",
        birth=1550, death=1616, nationality="中国（明朝）",
        bio_zh="中国戏曲史上与莎士比亚并称的伟大剧作家，'临川四梦'以至情反抗礼教，《牡丹亭》以杜丽娘死而复生的爱情故事成为中国古典戏曲的绝唱。",
        portrait_url=None,
        tags=["中国古代文学", "明代戏曲", "传奇"],
        works=[("The Peony Pavilion", "《牡丹亭》", 1598, "传奇"),
               ("The Purple Flute", "《紫箫记》", 1577, "传奇"),
               ("The Nanke Dream", "《南柯记》", 1600, "传奇")],
        events=[(1550, "生于临川（今江西抚州）", "birth"),
                (1616, "卒于临川", "death"),
                (1598, "《牡丹亭》问世，轰动一时", "life")],
    ),
    # ── 中国清代 ─────────────────────────────────────────────────────────────
    dict(
        name="Pu Songling", name_zh="蒲松龄",
        birth=1640, death=1715, nationality="中国（清朝）",
        bio_zh="清代文言短篇小说大家，《聊斋志异》以狐鬼花妖为主角，寄寓对科举制度的批判与对美好人性的向往，是中国古典小说的瑰宝。",
        portrait_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Pu_Songling.jpg/330px-Pu_Songling.jpg",
        tags=["中国古代文学", "清代小说", "志怪小说"],
        works=[("Strange Tales from a Chinese Studio", "《聊斋志异》", 1715, "短篇小说集")],
        events=[(1640, "生于淄川（今山东淄博）", "birth"),
                (1715, "卒于淄川", "death"),
                (1671, "开始收集素材创作《聊斋志异》", "life"),
                (1710, "71岁才补得岁贡生", "life")],
    ),
    dict(
        name="Wu Jingzi", name_zh="吴敬梓",
        birth=1701, death=1754, nationality="中国（清朝）",
        bio_zh="清代讽刺小说家，《儒林外史》以犀利的讽刺笔法揭露科举制度对知识分子精神的腐蚀，是中国古典讽刺小说的最高成就。",
        portrait_url=None,
        tags=["中国古代文学", "清代小说", "讽刺小说"],
        works=[("The Scholars", "《儒林外史》", 1750, "小说")],
        events=[(1701, "生于全椒（今安徽）", "birth"),
                (1754, "卒于扬州", "death"),
                (1736, "移居南京，开始创作《儒林外史》", "life")],
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

            b = a["birth"]
            b_str = f"公元前{abs(b)}" if b < 0 else str(b)
            d = a.get("death")
            d_str = ("今" if not d else (f"公元前{abs(d)}" if d < 0 else str(d)))
            print(f"  添加: {a['name_zh']} ({b_str}–{d_str})")
            added += 1

        await session.commit()
        print(f"\n完成：新增 {added} 位，跳过 {skipped} 位")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
