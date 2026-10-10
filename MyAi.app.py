import json, random, time, datetime as dt
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LinguaQuest", page_icon="🦊", layout="centered")

L = ["en", "ru", "uz", "fr", "de", "zh"]
NAME = {"en": "English 🇬🇧", "ru": "Русский 🇷🇺", "uz": "O'zbek 🇺🇿",
        "fr": "Français 🇫🇷", "de": "Deutsch 🇩🇪", "zh": "中文 🇨🇳"}
VC = {"en": "en-US", "ru": "ru-RU", "uz": "uz-UZ", "fr": "fr-FR", "de": "de-DE", "zh": "zh-CN"}

def parse(txt):
    return [l.split("|") for l in txt.strip().split("\n")]

# Порядок колонок: en | ru | uz | fr | de | zh
LV = {
    1: parse("""hello|привет|salom|bonjour|hallo|你好
thank you|спасибо|rahmat|merci|danke|谢谢
yes|да|ha|oui|ja|是
no|нет|yo'q|non|nein|不
water|вода|suv|eau|Wasser|水
bread|хлеб|non|pain|Brot|面包
house|дом|uy|maison|Haus|房子
cat|кот|mushuk|chat|Katze|猫
dog|собака|it|chien|Hund|狗
mother|мама|ona|mère|Mutter|妈妈
father|папа|ota|père|Vater|爸爸
friend|друг|do'st|ami|Freund|朋友
one|один|bir|un|eins|一
two|два|ikki|deux|zwei|二
red|красный|qizil|rouge|rot|红色
blue|синий|ko'k|bleu|blau|蓝色"""),
    2: parse("""book|книга|kitob|livre|Buch|书
sun|солнце|quyosh|soleil|Sonne|太阳
city|город|shahar|ville|Stadt|城市
apple|яблоко|olma|pomme|Apfel|苹果
school|школа|maktab|école|Schule|学校
car|машина|mashina|voiture|Auto|汽车
tea|чай|choy|thé|Tee|茶
morning|утро|ertalab|matin|Morgen|早上
night|ночь|tun|nuit|Nacht|夜晚
love|любовь|sevgi|amour|Liebe|爱
milk|молоко|sut|lait|Milch|牛奶
fish|рыба|baliq|poisson|Fisch|鱼
table|стол|stol|table|Tisch|桌子
door|дверь|eshik|porte|Tür|门
money|деньги|pul|argent|Geld|钱
time|время|vaqt|temps|Zeit|时间"""),
    3: parse("""I love you|Я люблю тебя|Men seni sevaman|Je t'aime|Ich liebe dich|我爱你
How are you?|Как дела?|Ishlaringiz qalay?|Comment ça va ?|Wie geht's?|你好吗？
I am hungry|Я голоден|Men ochman|J'ai faim|Ich habe Hunger|我饿了
I want water|Я хочу воды|Men suv xohlayman|Je veux de l'eau|Ich will Wasser|我想喝水
What is your name?|Как тебя зовут?|Ismingiz nima?|Comment tu t'appelles ?|Wie heißt du ?|你叫什么名字？
Where is the station?|Где вокзал?|Vokzal qayerda?|Où est la gare ?|Wo ist der Bahnhof ?|车站在哪里？
See you tomorrow|До завтра|Ertagacha|À demain|Bis morgen|明天见
Thank you very much|Большое спасибо|Katta rahmat|Merci beaucoup|Vielen Dank|非常感谢
I don't understand|Я не понимаю|Men tushunmayapman|Je ne comprends pas|Ich verstehe nicht|我不明白
How much is this?|Сколько это стоит?|Bu qancha turadi?|Combien ça coûte ?|Wie viel kostet das ?|这个多少钱？
Can you help me?|Вы можете мне помочь?|Menga yordam bera olasizmi?|Pouvez-vous m'aider ?|Können Sie mir helfen ?|你能帮我吗？
Good night|Спокойной ночи|Xayrli tun|Bonne nuit|Gute Nacht|晚安"""),
}

LVN = {"ru": ["Лёгкий 🌱", "Средний 🔥", "Сложный 💎"],
       "uz": ["Oson 🌱", "O'rta 🔥", "Qiyin 💎"],
       "en": ["Easy 🌱", "Medium 🔥", "Hard 💎"]}

T = {
 "play": ("Играть", "O'ynash", "Play"),
 "cards": ("Карточки", "Kartochkalar", "Cards"),
 "tutor": ("ИИ-тьютор", "AI ustoz", "AI Tutor"),
 "league": ("Лига", "Liga", "League"),
 "me": ("Профиль", "Profil", "Profile"),
 "level": ("Уровень сложности", "Qiyinlik darajasi", "Difficulty"),
 "start": ("Начать урок", "Darsni boshlash", "Start lesson"),
 "check": ("Проверить", "Tekshirish", "Check"),
 "next": ("Дальше", "Keyingi", "Next"),
 "ok": ("Верно!", "To'g'ri!", "Correct!"),
 "bad": ("Правильный ответ", "To'g'ri javob", "Correct answer"),
 "tn": ("Переведи", "Tarjima qil", "Translate"),
 "nt": ("Переведи", "Tarjima qil", "Translate"),
 "ls": ("Послушай и выбери перевод", "Eshit va tarjimasini tanla", "Listen and pick the translation"),
 "ty": ("Напиши перевод", "Tarjimani yoz", "Type the translation"),
 "bd": ("Составь перевод", "Tarjimani tuz", "Build the translation"),
 "clear": ("Очистить", "Tozalash", "Clear"),
 "done": ("Урок пройден!", "Dars tugadi!", "Lesson complete!"),
 "perf": ("Без ошибок! +20 XP", "Xatosiz! +20 XP", "Perfect! +20 XP"),
 "nohp": ("Сердца закончились 💔 Подожди (1 ❤ за 10 мин) или восстанови за 20 💎",
          "Yuraklar tugadi 💔 Kuting (10 daqiqada 1 ❤) yoki 20 💎 ga tiklang", "Out of hearts 💔 Wait (1 ❤ per 10 min) or refill for 20 💎"),
 "refill": ("Восстановить ❤", "❤ tiklash", "Refill ❤"),
 "nat": ("Я говорю на", "Men so'zlashaman", "I speak"),
 "lrn": ("Хочу выучить", "O'rganmoqchiman", "I want to learn"),
 "reset": ("Сбросить прогресс", "Jarayonni o'chirish", "Reset progress"),
 "flip": ("Показать перевод", "Tarjimani ko'rsat", "Show translation"),
 "ph": ("Спроси что угодно…", "Xohlagan narsani so'ra…", "Ask anything…"),
 "nokey": ("Введите API-ключ Anthropic в боковой панели.",
           "Anthropic API kalitini yon panelga kiriting.",
           "Enter your Anthropic API key in the sidebar."),
 "hello": ("Привет! Я твой ИИ-тьютор: объясню грамматику, проверю фразу, устрою диалог или викторину. С чего начнём?",
           "Salom! Men sening AI ustozingman: grammatikani tushuntiraman, iborani tekshiraman, dialog yoki viktorina o'tkazaman. Nimadan boshlaymiz?",
           "Hi! I'm your AI tutor: I explain grammar, check phrases, run dialogues and quizzes. Where shall we start?"),
 "lv": ("Уровень", "Daraja", "Level"),
 "you": ("Ты", "Sen", "You"),
 "back": ("К урокам", "Darslarga", "Back to lessons"),
}
CHIPS = {"ru": ["Объясни грамматику", "Мини-диалог", "Викторина"],
         "uz": ["Grammatikani tushuntir", "Mini-dialog", "Viktorina"],
         "en": ["Explain grammar", "Mini dialogue", "Quiz me"]}

# ---------------- состояние ----------------
S = st.session_state
for k, v in dict(ui="", tl="", xp=0, gems=30, streak=0, last="", hearts=5, hat=0.0, wk=0,
                 tot=0, perf=0, qs=None, qi=0, fb=None, lxp=0, mist=0, combo=0,
                 build=[], chat=[], card=0, res=None).items():
    S.setdefault(k, v)

def t(k):
    return T[k][["ru", "uz", "en"].index(S.ui or "ru")]

def sync():
    if S.hearts < 5:
        n = int((time.time() - S.hat) // 600)
        if n > 0:
            S.hearts = min(5, S.hearts + n)
            S.hat = time.time() if S.hearts < 5 else 0.0

st.markdown("""<style>
button[kind="primary"]{background:#58cc02!important;border:0!important;border-bottom:4px solid #3f9a00!important;
border-radius:14px!important;font-weight:800!important;color:#fff!important}
.title{font-size:34px;font-weight:900;background:linear-gradient(90deg,#58cc02,#1cb0f6,#a560ff);
-webkit-background-clip:text;color:transparent}
.big{font-size:34px;font-weight:900;text-align:center;padding:14px;border:2px solid #2c3160;border-radius:18px}
</style>""", unsafe_allow_html=True)

# ---------------- первый запуск ----------------
if not (S.ui and S.tl):
    st.markdown('<div class="title">🦊 LinguaQuest</div>', unsafe_allow_html=True)
    ui = st.radio("Я говорю на / Men so'zlashaman / I speak", ["ru", "uz", "en"],
                  format_func=lambda x: NAME[x], horizontal=True)
    tl = st.radio("Хочу выучить / O'rganmoqchiman / I want to learn",
                  [l for l in ["en", "ru", "fr", "de", "zh"] if l != ui],
                  format_func=lambda x: NAME[x], horizontal=True)
    if st.button("▶ Start", type="primary", use_container_width=True):
        S.ui, S.tl = ui, tl
        st.rerun()
    st.stop()

sync()
NI, CI = L.index(S.ui), L.index(S.tl)

# ---------------- звук (речь браузера) ----------------
def speak(text, lang):
    components.html(
        f"""<button style="font-size:22px;padding:8px 18px;border-radius:12px;border:0;background:#1cb0f6;color:#fff;cursor:pointer"
        onclick="s()">🔊</button><script>function s(){{var u=new SpeechSynthesisUtterance({json.dumps(text)});
        u.lang='{VC[lang]}';speechSynthesis.cancel();speechSynthesis.speak(u)}}</script>""", height=56)

# ---------------- генерация урока ----------------
def tok(s):
    return list(s) if S.tl == "zh" else s.split()

def make(level):
    pool = LV[level]
    qs = []
    for w in random.sample(pool, min(8, len(pool))):
        k = random.choice({1: ["tn", "nt"], 2: ["tn", "nt", "ls", "ty"], 3: ["bd", "tn"]}[level])
        if k == "ty" and S.tl == "zh":
            k = "nt"
        def opts(col):
            d = random.sample([x[col] for x in pool if x[col] != w[col]], 3) return random.sample([w[col]] + d, 4)
        if k == "tn":
            qs.append(dict(k=k, p=w[CI], a=w[NI], o=opts(NI)))
        elif k == "nt":
            qs.append(dict(k=k, p=w[NI], a=w[CI], o=opts(CI)))
        elif k == "ls":
            qs.append(dict(k=k, say=w[CI], a=w[NI], o=opts(NI)))
        elif k == "ty":
            qs.append(dict(k=k, p=w[NI], a=w[CI], say=w[CI]))
        else:
            a = tok(w[CI])
            extra = [x for o in pool if o is not w for x in tok(o[CI]) if x not in a]
            qs.append(dict(k=k, p=w[NI], a=a, say=w[CI],
                           pool=random.sample(a + random.sample(extra, min(3, len(extra))),
                                              len(a) + min(3, len(extra)))))
    return qs

def grade(ok, cor):
    S.fb = (ok, cor)
    if ok:
        S.combo += 1
        S.lxp += 10 + (5 if S.combo >= 3 else 0)
    else:
        S.combo = 0
        S.mist += 1
        if S.hearts == 5:
            S.hat = time.time()
        S.hearts -= 1
    st.rerun()

def award():
    x = S.lxp + (0 if S.mist else 20)
    g = 5 + (0 if S.mist else 5)
    today = str(dt.date.today())
    if S.last != today:
        yest = str(dt.date.today() - dt.timedelta(days=1))
        S.streak = S.streak + 1 if S.last == yest else 1
        S.last = today
    S.xp += x; S.wk += x; S.gems += g; S.tot += 1; S.perf += int(S.mist == 0)
    S.res = (x, g, S.mist == 0)

# ---------------- вкладка: урок ----------------
def lesson():
    if S.hearts <= 0 and S.fb is None:
        st.error(t("nohp"))
        if S.gems >= 20 and st.button(t("refill")):
            S.gems -= 20; S.hearts = 5; S.qs = None
            st.rerun()
        return
    if S.qs is None:
        lvl = st.radio(t("level"), [1, 2, 3], format_func=lambda i: LVN[S.ui][i - 1], horizontal=True)
        if st.button(t("start"), type="primary", use_container_width=True):
            S.qs, S.qi, S.fb, S.lxp, S.mist, S.combo, S.build = make(lvl), 0, None, 0, 0, 0, []
            st.rerun()
        return
    if S.qi >= len(S.qs):
        x, g, perfect = S.res
        st.balloons()
        st.success(f"🎉 {t('done')}")
        if perfect:
            st.info(t("perf"))
        c = st.columns(3)
        c[0].metric("XP", f"+{x}"); c[1].metric("💎", f"+{g}"); c[2].metric("🔥", S.streak)
        if st.button(t("back"), type="primary", use_container_width=True):
            S.qs = None
            st.rerun()
        return

    q = S.qs[S.qi]
    st.progress(S.qi / len(S.qs))
    if S.combo >= 2:
        st.caption(f"🔥 Combo x{S.combo}")
    st.subheader(t(q["k"]))
    if q["k"] == "ls":
        speak(q["say"], S.tl)
    elif q["k"] != "bd":
        st.markdown(f"<div class='big'>{q['p']}</div>", unsafe_allow_html=True)

    if S.fb is None:
        if q["k"] in ("tn", "nt", "ls"):
            ch = st.radio("answer", q["o"], index=None, key=f"r{S.qi}", label_visibility="collapsed")
            if st.button(t("check"), disabled=ch is None, type="primary", use_container_width=True):
                grade(ch == q["a"], q["a"])
        elif q["k"] == "ty":
            txt = st.text_input("answer", key=f"t{S.qi}", label_visibility="collapsed")
            norm = lambda s: "".join(c for c in s.lower() if c not in ".,!?¿¡'’").strip()
            if st.button(t("check"), disabled=not txt.strip(), type="primary", use_container_width=True):
                grade(norm(txt) == norm(q["a"]), q["a"])
        else:
            sep = "" if S.tl == "zh" else " "
            st.markdown(f"<div class='big'>{q['p']}</div>", unsafe_allow_html=True)
            st.info(sep.join(q["pool"][i] for i in S.build) or "…")
            cols = st.columns(3)
            for i, tk in enumerate(q["pool"]):
                if i not in S.build and cols[i % 3].button(tk, key=f"b{S.qi}_{i}"):
                    S.build.append(i)
                    st.rerun()
            c1, c2 = st.columns(2)
            if c1.button(t("clear")):
                S.build = []
                st.rerun()
            if c2.button(t("check"), disabled=not S.build, type="primary"): grade([q["pool"][i] for i in S.build] == q["a"], sep.join(q["a"]))
    else:
        ok, cor = S.fb
        if q.get("say"):
            speak(q["say"], S.tl)
        (st.success if ok else st.error)(f"{'✅ ' + t('ok') if ok else '❌ ' + t('bad') + ': ' + cor}")
        if st.button(t("next"), type="primary", use_container_width=True):
            S.qi += 1; S.fb = None; S.build = []
            if S.qi >= len(S.qs):
                award()
            st.rerun()

# ---------------- вкладка: карточки ----------------
def cards():
    lvl = st.radio(t("level"), [1, 2, 3], format_func=lambda i: LVN[S.ui][i - 1],
                   horizontal=True, key="cl")
    pool = LV[lvl]
    S.card %= len(pool)
    w = pool[S.card]
    st.markdown(f"<div class='big'>{w[CI]}</div>", unsafe_allow_html=True)
    speak(w[CI], S.tl)
    if st.toggle(t("flip"), key=f"f{lvl}{S.card}"):
        st.markdown(f"<div class='big' style='color:#1cb0f6'>{w[NI]}</div>", unsafe_allow_html=True)
    c = st.columns(3)
    if c[0].button("⬅️"): S.card -= 1; st.rerun()
    if c[1].button("🔀"): S.card = random.randrange(len(pool)); st.rerun()
    if c[2].button("➡️"): S.card += 1; st.rerun()

# ---------------- вкладка: ИИ-тьютор ----------------
def claude(msgs, key):
    sysm = (f"You are a friendly, concise language tutor inside a learning game. The learner speaks "
            f"{NAME[S.ui]} and is learning {NAME[S.tl]}. Always reply in {NAME[S.ui]}, using "
            f"{NAME[S.tl]} only for examples (with translations). Max ~120 words, a few emojis, "
            f"end with a tiny question or mini-exercise.")
    r = requests.post("https://api.anthropic.com/v1/messages",
                      headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                               "content-type": "application/json"},
                      json={"model": "claude-haiku-5-5", "max_tokens": 600,
                            "system": sysm, "messages": msgs}, timeout=60)
    r.raise_for_status()
    return r.json()["content"][0]["text"]

def tutor():
    key = st.sidebar.text_input("Anthropic API key", type="password")
    if not key:
        try:
            key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            key = ""
    with st.chat_message("assistant"):
        st.write(t("hello"))
    for m in S.chat:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    cols = st.columns(3)
    prompt = None
    for i, c in enumerate(CHIPS[S.ui]):
        if cols[i].button(c, key=f"chip{i}"):
            prompt = c
    prompt = st.chat_input(t("ph")) or prompt
    if prompt:
        if not key:
            st.warning(t("nokey"))
            return
        S.chat.append({"role": "user", "content": prompt})
        try:
            ans = claude(S.chat, key)
        except Exception as e:
            ans = f"⚠️ {e}"
        S.chat.append({"role": "assistant", "content": ans})
        st.rerun()

# ---------------- вкладка: лига ----------------
def league():
    bots = [("Alisher", 380), ("Anna", 320), ("Li Wei", 270), ("Pierre", 220), ("Mia", 170),
            ("Timur", 130), ("Jack", 90), ("Sofia", 60), ("Dilnoza", 30)]
    rows = sorted(bots + [(t("you"), S.wk)], key=lambda r: -r[1])
    for i, (n, x) in enumerate(rows):
        m = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i + 1}."
        line = f"{m} **{n}** — {x} XP"
        st.success(line) if n == t("you") else st.markdown(line)

# ---------------- вкладка: профиль ----------------
def me():
    st.progress((S.xp % 100) / 100, text=f"{t('lv')} {S.xp // 100 + 1} · {S.xp} XP")
    badges = [(S.streak >= 3, "🔥 3 days"), (S.xp >= 100, "⭐ 100 XP"),
              (S.perf > 0, "💯 Perfect"), (S.tot >= 5, "📚 5 lessons")]
    st.write(" ".join(f"`{b}`" if ok else f"~~{b}~~" for ok, b in badges))
    ui = st.radio(t("nat"), ["ru", "uz", "en"], index=["ru", "uz", "en"].index(S.ui),
                  format_func=lambda x: NAME[x], horizontal=True)
    opts = [l for l in ["en", "ru", "fr", "de", "zh"] if l != ui]
    tl = st. radio(t("lrn"), opts, index=opts.index(S.tl) if S.tl in opts else 0,
                  format_func=lambda x: NAME[x], horizontal=True)
    if (ui, tl) != (S.ui, S.tl):
        S.ui, S.tl, S.qs = ui, tl, None
        st.rerun()
    if S.gems >= 20 and S.hearts < 5 and st.button(t("refill") + " (20 💎)"):
        S.gems -= 20; S.hearts = 5
        st.rerun()
    if st.button(t("reset")):
        for k in list(S.keys()):
            del S[k]
        st.rerun()

# ---------------- каркас ----------------
st.markdown('<div class="title">🦊 LinguaQuest</div>', unsafe_allow_html=True)
c = st.columns(4)
c[0].metric("🔥", S.streak); c[1].metric("💎", S.gems)
c[2].metric("❤️", S.hearts); c[3].metric("⭐ XP", S.xp)

tabs = st.tabs([f"🎮 {t('play')}", f"🃏 {t('cards')}", f"🤖 {t('tutor')}",
                f"🏆 {t('league')}", f"👤 {t('me')}"])
for tab, fn in zip(tabs, [lesson, cards, tutor, league, me]):
    with tab:
        fn()
