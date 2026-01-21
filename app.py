import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語音樂課 - Romadiw", 
    page_icon="🎵", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺設計 (歡樂音樂風 🎵) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700;900&display=swap');

    /* 全局背景：清爽的淺藍色 */
    .stApp { 
        background-color: #E3F2FD; 
        font-family: 'Noto Sans TC', sans-serif;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* 標題樣式 */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 900 !important;
        text-align: center;
        padding-bottom: 10px;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0px;
    }
    
    /* 標題文字漸層 */
    .melody-text {
        background: linear-gradient(120deg, #1565C0, #7B1FA2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 一般文字顏色 */
    p, div, span, label, li {
        color: #37474F !important;
    }

    /* 按鈕：活力藍漸層 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        font-size: 18px;
        font-weight: 700;
        background: linear-gradient(90deg, #42A5F5 0%, #1E88E5 100%);
        color: #FFFFFF !important;
        border: none;
        padding: 12px 0px;
        box-shadow: 0px 4px 10px rgba(33, 150, 243, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(33, 150, 243, 0.5);
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
    }
    
    /* 單字卡片：白色背景 + 黃色邊框 */
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #FFF176; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #FDD835;
    }
    
    /* --- 完整歌詞歌譜樣式 --- */
    .song-sheet {
        background-color: #FFFFFF;
        padding: 40px 30px;
        border-radius: 20px;
        border: 4px solid #FFF59D; /* 亮黃色邊框 */
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        position: relative;
    }
    
    /* 裝飾用的音符 */
    .song-sheet::before {
        content: "🎵";
        position: absolute;
        top: 15px;
        left: 20px;
        font-size: 30px;
        opacity: 0.5;
    }
    .song-sheet::after {
        content: "🎶";
        position: absolute;
        bottom: 15px;
        right: 20px;
        font-size: 30px;
        opacity: 0.5;
    }

    .song-line-amis {
        font-size: 22px;
        font-weight: 800;
        color: #1565C0 !important;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    
    .song-line-zh {
        font-size: 15px;
        color: #90A4AE !important;
        margin-bottom: 25px; /* 句與句之間的距離 */
        font-weight: 500;
    }

    /* 單字大字體 */
    .big-font {
        font-size: 26px !important;
        font-weight: 800;
        color: #6A1B9A !important; 
        margin: 8px 0;
        letter-spacing: 0.5px;
    }
    .med-font {
        font-size: 16px !important;
        color: #546E7A !important;
        font-weight: 500;
        margin-bottom: 12px;
    }
    .emoji-icon {
        font-size: 48px;
        margin-bottom: 5px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    /* 動作標籤 */
    .action-tag {
        color: #0D47A1 !important;
        font-size: 13px;
        font-weight: 600;
        background: #BBDEFB;
        padding: 4px 12px;
        border-radius: 12px;
        display: inline-block;
    }

    /* Tab 樣式 */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.6);
        border-radius: 10px;
        padding: 8px 16px;
        font-weight: 600;
        color: #455A64 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #42A5F5 !important;
        color: #FFFFFF !important;
    }
    
    .stRadio label {
        font-size: 18px !important;
        padding: 10px;
        background: rgba(255,255,255,0.8);
        border-radius: 10px;
        margin-bottom: 5px;
        display: block;
        border: 1px solid #BBDEFB;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 ---

# 歌詞資料
LYRICS = [
    {"amis": "Kiso kiso kiso romadiw",      "zh": "你 你 你 唱歌",     "file": "song_line1"},
    {"amis": "Kako kako kako makero",       "zh": "我 我 我 跳舞",     "file": "song_line2"},
    {"amis": "Cingra cingra cingra mikongkong", "zh": "他 他 他 敲擊(打拍子)", "file": "song_line3"},
    {"amis": "Maemin kita maemin kita lipahak", "zh": "我們大家 我們大家 很快樂", "file": "song_line4"},
]

# 單字資料
VOCABULARY = [
    {"amis": "kiso",        "zh": "你",         "emoji": "👉", "action": "指著對方", "file": "v_kiso"},
    {"amis": "kako",        "zh": "我",         "emoji": "🙋‍♂️", "action": "拍拍胸口", "file": "v_kako"},
    {"amis": "cingra",      "zh": "他/她",      "emoji": "👈", "action": "指著旁邊", "file": "v_cingra"},
    {"amis": "romadiw",     "zh": "唱歌",       "emoji": "🎤", "action": "拿麥克風", "file": "v_romadiw"},
    {"amis": "makero",      "zh": "跳舞",       "emoji": "💃", "action": "轉圈圈",   "file": "v_makero"},
    {"amis": "mikongkong",  "zh": "敲擊/打拍子","emoji": "🥁", "action": "打鼓動作", "file": "v_mikongkong"},
    {"amis": "maemin kita", "zh": "我們大家",   "emoji": "👨‍👩‍👧‍👦", "action": "張開雙手", "file": "v_maeminkita"},
    {"amis": "lipahak",     "zh": "快樂",       "emoji": "😄", "action": "大笑",     "file": "v_lipahak"},
]

# 測驗題庫
QA_PAIRS = [
    {"subject": "Kiso",   "action": "romadiw",    "zh_subject": "你", "zh_action": "唱歌"},
    {"subject": "Kako",   "action": "makero",     "zh_subject": "我", "zh_action": "跳舞"},
    {"subject": "Cingra", "action": "mikongkong", "zh_subject": "他", "zh_action": "敲擊"},
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['m4a', 'mp3']:
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                st.audio(path, format=f'audio/{ext}')
                return
    
    try:
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇")

# --- 2. 隨機出題邏輯 ---

def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    
    # Q1: 聽力
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}

    # Q2: 歌詞填空
    q2_target = random.choice(QA_PAIRS)
    action_words = ["romadiw", "makero", "mikongkong"]
    q2_options = action_words.copy()
    random.shuffle(q2_options)
    st.session_state.q2_data = {"target": q2_target, "options": q2_options, "correct_ans": q2_target['action']}

    # Q3: 句子理解
    q3_target = random.choice(LYRICS)
    other_sentences = [s['zh'] for s in LYRICS if s['zh'] != q3_target['zh']]
    q3_options_pool = random.sample(other_sentences, min(2, len(other_sentences))) 
    q3_options = q3_options_pool + [q3_target['zh']]
    random.shuffle(q3_options)
    st.session_state.q3_data = {"target": q3_target, "options": q3_options}

if 'q1_data' not in st.session_state:
    init_quiz()

# --- 3. 介面邏輯 ---

def show_learning_mode():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: #1565C0 !important; font-size: 32px; margin: 0; font-weight:800;'>Romadiw Kita</h2>
            <div style='color: #546E7A !important; font-size: 18px; margin-top: 8px; font-weight:500;'>
                — 我們來唱歌 —
            </div>
            <div style='color: #546E7A !important; font-size: 15px; margin-top: 15px; font-weight: 500;'>
                講師：曾純美 &nbsp;&nbsp; 教材提供者：曾純美
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 點擊播放按鈕，跟著節奏一起唱！")
    
    # --- Part 1: 完整歌曲 (歌譜模式) ---
    st.markdown("### 🎵 歌詞")
    
    # 組合完整的 HTML 歌譜
    lyrics_html = '<div class="song-sheet">'
    for line in LYRICS:
        lyrics_html += f"""
            <div class="song-line-amis">{line['amis']}</div>
            <div class="song-line-zh">{line['zh']}</div>
        """
    lyrics_html += '</div>'
    st.markdown(lyrics_html, unsafe_allow_html=True)
    
    # 在歌譜下方提供分句播放功能
    with st.expander("🎧 播放歌詞錄音 (分句練習)", expanded=True):
        for i, line in enumerate(LYRICS):
            col_a, col_b = st.columns([0.2, 0.8])
            with col_a:
                st.markdown(f"**第 {i+1} 句**")
            with col_b:
                play_audio(line['amis'], filename_base=line['file'])

    st.markdown("---")

    # --- Part 2: 單字 ---
    st.markdown("### 📝 認識單字")
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(VOCABULARY):
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{item['emoji']}</div>
                <div class="big-font">{item['amis']}</div>
                <div class="med-font">{item['zh']}</div>
                <div class="action-tag">
                    {item['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #1565C0 !important; margin-bottom: 20px;'>🏆 音樂挑戰賽</h3>", unsafe_allow_html=True)
    
    st.progress(st.session_state.current_q / 3)
    st.write("") 

    # Q1
    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown("**第 1 關：聽聽看，這是什麼意思？**")
        play_audio(target['amis'], filename_base=target['file'])
        st.write("")
        cols = st.columns(3)
        for idx, opt in enumerate(data['options']):
            with cols[idx]:
                if st.button(f"{opt['emoji']} {opt['zh']}"):
                    if opt['amis'] == target['amis']:
                        st.balloons()
                        st.success(f"答對了！{target['amis']} 就是 {target['zh']}！")
                        time.sleep(1.5)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error(f"不對喔，{opt['zh']} 是 {opt['amis']}")

    # Q2
    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        target = data['target']
        st.markdown("**第 2 關：歌詞接龍**")
        st.markdown(f"歌詞唱到： **{target['subject']} {target['subject']} {target['subject']} ...**")
        st.markdown("接下要做什麼動作？")
        st.markdown(f"""
        <div style="background:#FFFFFF; padding:20px; border-radius:15px; border-left: 6px solid #1E88E5; margin: 15px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <span style="font-size:20px; color:#333 !important;">{target['subject']} {target['subject']} {target['subject']} <b>_______</b></span>
            <br><span style="color:#888; font-size:15px;">({target['zh_subject']} {target['zh_subject']} {target['zh_subject']} {target['zh_action']})</span>
        </div>
        """, unsafe_allow_html=True)
        ans = st.radio("請選擇正確的動作：", data['options'])
        if st.button("確定送出"):
            if ans == data['correct_ans']:
                st.balloons()
                st.success(f"太棒了！{target['subject']} 是搭配 {ans}！")
                time.sleep(1.5)
                st.session_state.score += 1
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再想一下，這首歌裡不是這樣唱的喔！")

    # Q3
    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown("**第 3 關：歌詞翻譯**")
        st.markdown("請聽這句歌詞，是什麼意思？")
        play_audio(target['amis'], filename_base=target['file'])
        for opt_text in data['options']:
            if st.button(opt_text):
                if opt_text == target['zh']:
                    st.balloons()
                    st.success("全對！你是阿美語歌王/歌后！🎤")
                    time.sleep(1.5)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("不對喔，再聽一次看看！")

    # 結算
    else:
        st.markdown(f"""
        <div style='text-align: center; padding: 40px; background-color: #FFFFFF; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);'>
            <h1 style='color: #1565C0 !important; margin-bottom:10px;'>🎉 挑戰成功！</h1>
            <p style='font-size: 20px; color: #455A64 !important;'>你已經學會這首歌了！</p>
            <div style='font-size: 80px; margin: 20px 0;'>💃</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 再玩一次 (題目會變喔)"):
            init_quiz()
            st.rerun()

# --- 4. 主程式 ---
def main():
    st.markdown("""
        <h1>
            <span class="melody-text">阿美語音樂課</span> 
            <span>🎵</span>
        </h1>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📖 學習歌曲", "🎮 練習挑戰"])
    
    with tab1:
        show_learning_mode()
    
    with tab2:
        show_quiz_mode()

if __name__ == "__main__":
    main()
