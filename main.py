import streamlit as st
import os

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="云上红旗渠",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS 美化 (只给主页卡片加个阴影，不动侧边栏) ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Microsoft YaHei', sans-serif;
    }
    h1 {
        color: #D32F2F !important;
        font-weight: 900;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    [data-testid="stMetricValue"] {
        color: #D32F2F !important;
        font-size: 2rem !important;
    }
    /* 主页卡片样式 */
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        height: 180px;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #D32F2F;
        box-shadow: 0 5px 15px rgba(211, 47, 47, 0.1);
        transform: translateY(-2px);
    }
    .card-title {
        color: #D32F2F;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 8px;
        border-bottom: 1px solid #EEE;
        padding-bottom: 8px;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #555;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 侧边栏：制作团队 (纯原生 Markdown，绝对整齐) ---
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/2560px-Flag_of_the_People%27s_Republic_of_China.svg.png",
        width=40)
    st.markdown("### 🚩 云上红旗渠")

    # 把它顶到底部
    st.markdown("<br>" * 10, unsafe_allow_html=True)

    st.markdown("---")

    # 【这里是最关键的修改】
    # 使用原生 Markdown，不加任何花里胡哨的 HTML
    st.markdown("#### 👥 制作团队")

    st.markdown("**项目负责人**")
    st.markdown("马子恒")

    st.markdown("")  # 空一行，拉开间距

    st.markdown("**小组成员**")
    st.markdown("马苛豪")
    st.markdown("黄逸辉")

    st.markdown("---")
    st.caption("东南大学 · 机械工程学院")

# --- 4. 主页面内容 (保持不变) ---

st.markdown("<h1>☁️ 云上红旗渠</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>传承红色基因 · 赓续精神血脉 · AI 赋能历史</div>", unsafe_allow_html=True)

# 背景图
hero_img = "assets/background.jpg"
if not os.path.exists(hero_img):
    if os.path.exists("assets/photos/qianjunwanma.jpg"):
        hero_img = "assets/photos/qianjunwanma.jpg"
    else:
        hero_img = None

if hero_img:
    st.image(hero_img, use_container_width=True)

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("修筑历时", "10 年")
with c2: st.metric("干渠总长", "1500 km")
with c3: st.metric("削平山头", "1250 座")
with c4: st.metric("参与群众", "30 万人")

st.markdown("---")
st.subheader("🏛️ 探索数字展馆")

row1_1, row1_2 = st.columns(2)
row2_1, row2_2 = st.columns(2)

with row1_1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🗺️ 地图导览</div>
        <div class="card-desc">
            交互式重现红旗渠修筑路线，点击地标查看“青年洞”、“渠首”等关键节点的历史现场。
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("👉 点击左侧 [地图导览] 进入")

with row1_2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🎨 AI 影像修复</div>
        <div class="card-desc">
            利用深度学习技术为黑白老照片上色。让当年的修渠英雄从黑白变为彩色，让历史记忆鲜活如初。
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("👉 点击左侧 [AI修复体验] 进入")

with row2_1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🎖️ 英雄谱</div>
        <div class="card-desc">
            致敬平凡而伟大的人民。收录杨贵、任羊成及300名青年突击队的感人事迹。
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("👉 点击左侧 [英雄谱] 进入")

with row2_2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-title">🎞️ 历史影像馆</div>
        <div class="card-desc">
            珍贵的历史纪录片与口述历史档案。在这里静下心来，聆听太行山的回响。
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("👉 点击左侧 [历史影像馆] 进入")