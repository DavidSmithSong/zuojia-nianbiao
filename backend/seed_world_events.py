"""
作家年表 · 世界历史大事种子数据（1800-2026，约 200 条）
运行：python -m backend.seed_world_events
需要环境变量 DATABASE_URL
"""
import asyncio
import os
import sys

# ── 数据定义 ────────────────────────────────────────────────────────────────────
# (year, event_zh, event_en, category, region, significance)
WORLD_EVENTS = [
    # 1800s
    (1804, "拿破仑加冕法国皇帝", "Napoleon crowned Emperor of France", "politics", "欧洲", 5),
    (1807, "废除奴隶贸易法案（英国）", "Slave Trade Act abolishes slave trade in Britain", "politics", "欧洲", 4),
    (1812, "拿破仑远征俄罗斯失败", "Napoleon's failed invasion of Russia", "war", "欧洲", 5),
    (1815, "拿破仑战争结束，维也纳会议", "Napoleonic Wars end; Congress of Vienna", "politics", "欧洲", 5),
    (1819, "新加坡由英国建立", "Singapore founded by British", "politics", "亚洲", 3),
    (1821, "希腊独立战争爆发", "Greek War of Independence begins", "war", "欧洲", 4),
    (1825, "第一条公共铁路（英国斯托克顿-达林顿）开通", "First public railway opens in England", "science", "欧洲", 4),
    (1830, "法国七月革命", "French July Revolution", "politics", "欧洲", 4),
    (1833, "英国废除奴隶制", "Slavery Abolition Act in British Empire", "politics", "欧洲", 4),
    (1839, "第一次鸦片战争爆发", "First Opium War begins", "war", "亚洲", 5),
    (1842, "《南京条约》签订，香港割让英国", "Treaty of Nanking; Hong Kong ceded to Britain", "politics", "亚洲", 5),
    (1848, "欧洲革命年·《共产党宣言》发表", "Year of Revolutions; Communist Manifesto published", "politics", "欧洲", 5),
    (1851, "太平天国运动爆发（中国）", "Taiping Rebellion begins in China", "war", "中国", 5),
    (1853, "克里米亚战争爆发", "Crimean War begins", "war", "欧洲", 4),
    (1856, "第二次鸦片战争爆发", "Second Opium War begins", "war", "亚洲", 4),
    (1859, "达尔文发表《物种起源》", "Darwin publishes On the Origin of Species", "science", "全球", 5),
    (1861, "美国南北战争爆发", "American Civil War begins", "war", "美洲", 5),
    (1861, "俄国农奴制废除", "Emancipation of serfs in Russia", "politics", "欧洲", 4),
    (1864, "第一国际成立", "First International founded", "politics", "欧洲", 3),
    (1865, "美国南北战争结束，林肯遇刺", "American Civil War ends; Lincoln assassinated", "war", "美洲", 5),
    (1868, "明治维新开始（日本）", "Meiji Restoration begins in Japan", "politics", "亚洲", 5),
    (1870, "普法战争爆发", "Franco-Prussian War begins", "war", "欧洲", 4),
    (1871, "德意志帝国统一", "Unification of Germany", "politics", "欧洲", 5),
    (1871, "巴黎公社成立与覆灭", "Paris Commune rises and falls", "politics", "欧洲", 4),
    (1876, "贝尔发明电话", "Alexander Graham Bell invents the telephone", "science", "美洲", 4),
    (1878, "爱迪生发明电灯", "Edison invents the light bulb", "science", "美洲", 4),
    (1882, "三国同盟（德意奥）成立", "Triple Alliance formed", "politics", "欧洲", 4),
    (1884, "柏林会议瓜分非洲", "Berlin Conference divides Africa", "politics", "全球", 4),
    (1894, "中日甲午战争爆发", "First Sino-Japanese War begins", "war", "亚洲", 5),
    (1895, "《马关条约》签订，台湾割让日本", "Treaty of Shimonoseki; Taiwan ceded to Japan", "politics", "亚洲", 5),
    (1895, "卢米埃尔兄弟发明电影放映机", "Lumière brothers invent the cinematograph", "culture", "欧洲", 4),
    (1898, "美西战争·美国帝国主义崛起", "Spanish-American War; US imperialism rises", "war", "美洲", 4),
    (1898, "戊戌变法（百日维新）", "Hundred Days' Reform in China", "politics", "中国", 4),
    (1899, "义和团运动爆发", "Boxer Rebellion begins in China", "war", "中国", 4),
    # 1900s
    (1900, "八国联军入侵北京，《辛丑条约》", "Eight-Nation Alliance invades Beijing", "war", "中国", 5),
    (1903, "莱特兄弟首次飞行", "Wright brothers' first powered flight", "science", "美洲", 5),
    (1904, "日俄战争爆发", "Russo-Japanese War begins", "war", "亚洲", 4),
    (1905, "俄国第一次革命·爱因斯坦发表狭义相对论", "Russian Revolution of 1905; Einstein's special relativity", "science", "全球", 5),
    (1906, "旧金山大地震", "San Francisco earthquake", "disaster", "美洲", 3),
    (1907, "三国协约（英法俄）形成", "Triple Entente formed", "politics", "欧洲", 4),
    (1910, "日本吞并朝鲜", "Japan annexes Korea", "politics", "亚洲", 4),
    (1911, "辛亥革命推翻清朝", "Xinhai Revolution overthrows Qing dynasty", "politics", "中国", 5),
    (1912, "中华民国成立，清朝灭亡", "Republic of China established; Qing dynasty ends", "politics", "中国", 5),
    (1912, "泰坦尼克号沉没", "Titanic sinks", "disaster", "全球", 3),
    (1914, "第一次世界大战爆发", "World War I begins", "war", "欧洲", 5),
    (1915, "亚美尼亚种族灭绝", "Armenian Genocide", "war", "亚洲", 5),
    (1916, "凡尔登战役，索姆河战役", "Battle of Verdun; Battle of the Somme", "war", "欧洲", 4),
    (1917, "俄国十月革命", "Russian October Revolution", "politics", "欧洲", 5),
    (1917, "美国参加一战", "United States enters World War I", "war", "美洲", 4),
    (1918, "第一次世界大战结束", "World War I ends", "war", "全球", 5),
    (1918, "西班牙大流感全球蔓延", "Spanish flu pandemic", "disaster", "全球", 5),
    (1919, "五四运动（中国）", "May Fourth Movement, China", "politics", "中国", 5),
    (1919, "《凡尔赛条约》签订", "Treaty of Versailles signed", "politics", "欧洲", 5),
    (1920, "国际联盟成立", "League of Nations founded", "politics", "全球", 4),
    (1921, "中国共产党成立", "Chinese Communist Party founded", "politics", "中国", 5),
    (1922, "苏联成立", "Soviet Union founded", "politics", "欧洲", 5),
    (1922, "意大利法西斯墨索里尼上台", "Mussolini's March on Rome", "politics", "欧洲", 4),
    (1923, "土耳其共和国成立，奥斯曼帝国灭亡", "Turkey becomes a republic; Ottoman Empire ends", "politics", "亚洲", 4),
    (1924, "列宁逝世，斯大林掌权", "Lenin dies; Stalin rises to power", "politics", "欧洲", 5),
    (1927, "国共分裂，中国内战开始", "Chinese Nationalist-Communist split", "war", "中国", 5),
    (1929, "全球经济大萧条开始", "Great Depression begins", "economy", "全球", 5),
    (1931, "日本侵占中国东北（九一八事变）", "Mukden Incident; Japan occupies Manchuria", "war", "亚洲", 5),
    (1933, "希特勒就任德国总理", "Hitler becomes Chancellor of Germany", "politics", "欧洲", 5),
    (1933, "罗斯福新政", "Roosevelt's New Deal in the US", "economy", "美洲", 4),
    (1934, "中国共产党长征", "Chinese Communist Long March", "war", "中国", 5),
    (1936, "西班牙内战爆发", "Spanish Civil War begins", "war", "欧洲", 4),
    (1937, "中国全面抗战爆发（七七事变）", "Second Sino-Japanese War begins", "war", "中国", 5),
    (1937, "南京大屠杀", "Nanjing Massacre", "war", "中国", 5),
    (1939, "第二次世界大战爆发", "World War II begins", "war", "全球", 5),
    (1941, "珍珠港事件，美国参加二战", "Pearl Harbor attack; US enters WWII", "war", "全球", 5),
    (1942, "斯大林格勒战役", "Battle of Stalingrad", "war", "欧洲", 5),
    (1944, "诺曼底登陆", "D-Day Normandy landings", "war", "欧洲", 5),
    (1945, "第二次世界大战结束，联合国成立", "World War II ends; United Nations founded", "war", "全球", 5),
    (1945, "广岛、长崎原子弹爆炸", "Atomic bombs dropped on Hiroshima and Nagasaki", "war", "亚洲", 5),
    (1947, "印巴分治，印度独立", "India-Pakistan partition; Indian independence", "politics", "亚洲", 5),
    (1947, "美国马歇尔计划，冷战开始", "Marshall Plan; Cold War begins", "politics", "全球", 5),
    (1948, "以色列建国，第一次中东战争", "Israel founded; First Arab-Israeli War", "war", "亚洲", 5),
    (1948, "《世界人权宣言》通过", "Universal Declaration of Human Rights adopted", "politics", "全球", 4),
    (1949, "中华人民共和国成立", "People's Republic of China founded", "politics", "中国", 5),
    (1949, "北约成立", "NATO founded", "politics", "全球", 4),
    # 1950s
    (1950, "朝鲜战争爆发", "Korean War begins", "war", "亚洲", 4),
    (1953, "朝鲜战争停战", "Korean War armistice", "war", "亚洲", 4),
    (1953, "DNA双螺旋结构发现", "Discovery of DNA double helix", "science", "全球", 5),
    (1954, "麦卡锡主义盛行，法国在奠边府败仗", "McCarthyism peaks; France defeated at Dien Bien Phu", "politics", "全球", 4),
    (1955, "万隆会议召开", "Bandung Conference", "politics", "全球", 4),
    (1955, "华沙条约组织成立", "Warsaw Pact signed", "politics", "欧洲", 4),
    (1956, "匈牙利革命遭苏联镇压", "Hungarian Revolution crushed by Soviet Union", "war", "欧洲", 4),
    (1956, "苏伊士运河危机", "Suez Crisis", "politics", "亚洲", 4),
    (1957, "苏联发射人类首颗人造卫星斯普特尼克", "Sputnik launched by Soviet Union", "science", "全球", 5),
    (1958, "中国大跃进", "China's Great Leap Forward", "politics", "中国", 5),
    (1959, "古巴革命胜利，卡斯特罗上台", "Cuban Revolution; Castro takes power", "politics", "美洲", 4),
    # 1960s
    (1960, "非洲年，17国独立", "Year of Africa, 17 nations gain independence", "politics", "非洲", 4),
    (1961, "柏林墙建造", "Berlin Wall constructed", "politics", "欧洲", 5),
    (1961, "苏联宇航员加加林进入太空", "Gagarin becomes first human in space", "science", "全球", 5),
    (1962, "古巴导弹危机", "Cuban Missile Crisis", "politics", "全球", 5),
    (1963, "肯尼迪遇刺", "Kennedy assassinated", "politics", "美洲", 5),
    (1964, "美国《民权法案》通过", "US Civil Rights Act passed", "politics", "美洲", 4),
    (1965, "美国大规模介入越战", "US escalates Vietnam War", "war", "亚洲", 5),
    (1966, "中国文化大革命开始", "Cultural Revolution begins in China", "politics", "中国", 5),
    (1967, "第三次中东战争（六日战争）", "Six-Day War in the Middle East", "war", "亚洲", 4),
    (1968, "全球学生运动·布拉格之春", "Global student protests; Prague Spring", "politics", "全球", 5),
    (1968, "马丁·路德·金遇刺", "Martin Luther King Jr. assassinated", "politics", "美洲", 5),
    (1969, "人类首次登月（阿波罗11号）", "Moon landing (Apollo 11)", "science", "全球", 5),
    # 1970s
    (1971, "孟加拉国独立战争", "Bangladesh Liberation War", "war", "亚洲", 4),
    (1971, "中华人民共和国恢复联合国安理会席位", "PRC restores UN Security Council seat", "politics", "全球", 4),
    (1972, "尼克松访华，中美关系解冻", "Nixon visits China; Sino-US relations normalize", "politics", "全球", 5),
    (1973, "第四次中东战争·石油危机", "Yom Kippur War; Oil Crisis", "economy", "全球", 5),
    (1973, "智利皮诺切特政变", "Pinochet coup in Chile", "politics", "美洲", 4),
    (1975, "越战结束，西贡陷落", "Vietnam War ends; Fall of Saigon", "war", "亚洲", 5),
    (1975, "柬埔寨红色高棉上台", "Khmer Rouge takes power in Cambodia", "war", "亚洲", 5),
    (1976, "文化大革命结束，四人帮被捕", "Cultural Revolution ends; Gang of Four arrested", "politics", "中国", 5),
    (1977, "中国恢复高考", "China restores college entrance exams", "politics", "中国", 4),
    (1978, "中国改革开放开始", "China launches Reform and Opening-up", "economy", "中国", 5),
    (1979, "伊朗伊斯兰革命", "Iranian Islamic Revolution", "politics", "亚洲", 5),
    (1979, "苏联入侵阿富汗", "Soviet invasion of Afghanistan", "war", "亚洲", 5),
    (1979, "撒切尔夫人就任英国首相", "Thatcher becomes UK Prime Minister", "politics", "欧洲", 4),
    # 1980s
    (1980, "两伊战争爆发", "Iran-Iraq War begins", "war", "亚洲", 4),
    (1980, "波兰团结工会运动", "Solidarity movement in Poland", "politics", "欧洲", 4),
    (1981, "里根就任美国总统，新自由主义兴起", "Reagan takes office; neoliberalism rises", "politics", "美洲", 4),
    (1984, "印度英迪拉·甘地遇刺", "Indira Gandhi assassinated", "politics", "亚洲", 4),
    (1985, "戈尔巴乔夫上台，苏联改革开始", "Gorbachev takes power; Soviet reforms begin", "politics", "欧洲", 5),
    (1986, "切尔诺贝利核事故", "Chernobyl nuclear disaster", "disaster", "欧洲", 5),
    (1987, "股市黑色星期一", "Black Monday stock market crash", "economy", "全球", 4),
    (1988, "两伊战争结束", "Iran-Iraq War ends", "war", "亚洲", 4),
    (1989, "柏林墙倒塌", "Fall of the Berlin Wall", "politics", "欧洲", 5),
    (1989, "天安门广场事件", "Tiananmen Square incident", "politics", "中国", 5),
    # 1990s
    (1990, "德国统一", "German reunification", "politics", "欧洲", 5),
    (1990, "纳尔逊·曼德拉获释，南非种族隔离结束", "Mandela freed; end of apartheid", "politics", "非洲", 5),
    (1991, "苏联解体", "Dissolution of the Soviet Union", "politics", "欧洲", 5),
    (1991, "海湾战争", "Gulf War", "war", "亚洲", 5),
    (1992, "南斯拉夫内战·波斯尼亚战争", "Bosnian War begins", "war", "欧洲", 4),
    (1993, "互联网向公众开放（万维网诞生）", "World Wide Web opens to the public", "science", "全球", 5),
    (1994, "卢旺达种族灭绝", "Rwandan Genocide", "war", "非洲", 5),
    (1994, "南非首次多种族选举", "South Africa's first multiracial elections", "politics", "非洲", 5),
    (1994, "中国全面接入国际互联网", "China connects to global Internet", "science", "中国", 4),
    (1997, "香港回归中国", "Hong Kong returned to China", "politics", "中国", 5),
    (1997, "亚洲金融危机", "Asian Financial Crisis", "economy", "亚洲", 5),
    (1998, "克林顿弹劾案", "Clinton impeachment", "politics", "美洲", 3),
    (1999, "北约轰炸南联盟·科索沃战争", "NATO bombing of Yugoslavia; Kosovo War", "war", "欧洲", 4),
    (1999, "澳门回归中国", "Macau returned to China", "politics", "中国", 4),
    # 2000s
    (2001, "9·11恐怖袭击", "September 11 attacks", "war", "美洲", 5),
    (2001, "美国入侵阿富汗", "US invades Afghanistan", "war", "亚洲", 5),
    (2003, "美国入侵伊拉克", "US invades Iraq", "war", "亚洲", 5),
    (2003, "非典（SARS）疫情", "SARS outbreak", "disaster", "亚洲", 4),
    (2004, "印度洋大海啸", "Indian Ocean tsunami", "disaster", "亚洲", 5),
    (2005, "卡特里娜飓风袭击美国", "Hurricane Katrina hits the US", "disaster", "美洲", 4),
    (2007, "苹果发布第一代iPhone", "Apple releases the first iPhone", "science", "全球", 4),
    (2008, "全球金融危机", "Global Financial Crisis", "economy", "全球", 5),
    (2008, "北京奥运会", "Beijing Olympics", "culture", "中国", 4),
    (2009, "奥巴马就任美国总统", "Obama inaugurated as US President", "politics", "美洲", 4),
    # 2010s
    (2010, "海地地震·智利地震", "Haiti and Chile earthquakes", "disaster", "美洲", 4),
    (2010, "阿拉伯之春开始", "Arab Spring begins", "politics", "亚洲", 5),
    (2011, "东日本大地震·福岛核事故", "Japan earthquake and Fukushima nuclear disaster", "disaster", "亚洲", 5),
    (2011, "本·拉登被击毙", "Osama bin Laden killed", "war", "亚洲", 4),
    (2012, "习近平就任中共中央总书记", "Xi Jinping becomes CCP General Secretary", "politics", "中国", 5),
    (2013, "斯诺登泄露美国监控项目", "Snowden reveals NSA surveillance programs", "politics", "全球", 4),
    (2014, "俄罗斯吞并克里米亚", "Russia annexes Crimea", "war", "欧洲", 5),
    (2015, "欧洲难民危机高峰", "European refugee crisis peaks", "politics", "欧洲", 4),
    (2015, "《巴黎气候协定》签署", "Paris Climate Agreement signed", "science", "全球", 4),
    (2016, "英国脱欧公投", "Brexit referendum in the UK", "politics", "欧洲", 4),
    (2016, "特朗普当选美国总统", "Trump elected US President", "politics", "美洲", 5),
    (2017, "人工智能热潮兴起（AlphaGo击败人类棋手）", "AI boom; AlphaGo defeats human Go champion", "science", "全球", 4),
    (2018, "中美贸易战爆发", "US-China trade war begins", "economy", "全球", 5),
    (2019, "香港抗议运动", "Hong Kong protests", "politics", "中国", 4),
    # 2020s
    (2020, "新冠疫情全球大流行", "COVID-19 global pandemic", "disaster", "全球", 5),
    (2020, "乔治·弗洛伊德事件·全球反种族歧视运动", "George Floyd killing; global anti-racism protests", "politics", "全球", 4),
    (2021, "美国国会山事件", "US Capitol stormed", "politics", "美洲", 4),
    (2021, "阿富汗塔利班重新掌权", "Taliban retakes Afghanistan", "war", "亚洲", 5),
    (2022, "俄罗斯全面入侵乌克兰", "Russia invades Ukraine", "war", "欧洲", 5),
    (2022, "ChatGPT发布，生成式AI革命", "ChatGPT released; generative AI revolution", "science", "全球", 5),
    (2023, "以色列-哈马斯战争爆发", "Israel-Hamas War begins", "war", "亚洲", 5),
    (2024, "全球AI竞赛加剧", "Global AI competition intensifies", "science", "全球", 4),
    (2025, "美国特朗普第二任期就职", "Trump begins second presidential term", "politics", "美洲", 4),
]


async def seed():
    import asyncpg

    url = os.environ["DATABASE_URL"]
    conn = await asyncpg.connect(url)

    inserted = 0
    skipped  = 0
    for row in WORLD_EVENTS:
        year, event_zh, event_en, category, region, significance = row
        existing = await conn.fetchval(
            "SELECT id FROM world_events WHERE year=$1 AND event_zh=$2", year, event_zh
        )
        if existing:
            skipped += 1
            continue
        await conn.execute(
            """INSERT INTO world_events
               (year, event_zh, event_en, category, region, significance)
               VALUES ($1, $2, $3, $4, $5, $6)""",
            year, event_zh, event_en, category, region, significance,
        )
        inserted += 1

    await conn.close()
    print(f"完成：插入 {inserted} 条，跳过 {skipped} 条（已存在）")


if __name__ == "__main__":
    if "DATABASE_URL" not in os.environ:
        print("请设置 DATABASE_URL 环境变量", file=sys.stderr)
        sys.exit(1)
    asyncio.run(seed())
