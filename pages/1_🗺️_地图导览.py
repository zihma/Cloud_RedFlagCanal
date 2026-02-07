import streamlit as st
import folium
from streamlit_folium import st_folium
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="红旗渠·地理叙事", page_icon="🗺️", layout="wide")

# --- 2. 红色主题 CSS (不改配置文件，直接注入) ---
st.markdown("""
    <style>
    /* 1. 标题样式：红旗渠红 + 底部红线 */
    h1 {
        color: #D32F2F !important;
        font-family: 'Microsoft YaHei', sans-serif;
        font-weight: 800;
        border-bottom: 3px solid #D32F2F;
        padding-bottom: 15px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* 2. 二级标题样式 */
    h3 {
        color: #B71C1C !important; /* 深红色 */
        border-left: 5px solid #D32F2F;
        padding-left: 10px;
    }

    /* 3. 右侧信息卡片样式 */
    .info-box {
        background-color: #f9f9f9; /* 浅灰背景 */
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 4. 图片圆角 */
    img {
        border-radius: 8px;
    }

    /* 5. 去掉一些默认边距 */
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 路径设置 ---
PHOTO_DIR = "assets/photos"

# --- 4. 数据列表 ---
locations = [
    # --- 第一阶段：源头与誓师 (最北/最西) ---
    # 誓师地，起点
    {"name": "千军万马上太行", "desc": "誓师大会壮阔场景。队伍蜿蜒上山，红旗招展，誓把河山重安排。",
     "img": "qianjunwanma.jpg", "lat": 36.38, "lon": 113.62, "color": "red", "icon": "flag"},
    # 渠首，引水入林
    {"name": "分水枢纽 (渠首)", "desc": "引漳入林的源头。在这里，漳河水被拦腰截断，引入红旗渠。",
     "img": "hongyinghuiliu.jpg", "lat": 36.35, "lon": 113.60, "color": "blue", "icon": "tint"},

    # --- 第二阶段：干渠险段 (向东南流) ---
    # 空心坝其实在青年洞上游一点点，按水流应该先经空心坝
    {"name": "空心坝", "desc": "渠水穿腹而过，河水溢流而下。解决渠水与河水交叉冲突的典范。",
     "img": "kongxinba.jpg", "lat": 36.29, "lon": 113.73, "color": "green", "icon": "random"},
    {"name": "青年洞", "desc": "红旗渠精神的象征。300名青年突击队历时1年5个月凿穿悬崖。",
     "img": "qingniandong.jpg", "lat": 36.27, "lon": 113.76, "color": "red", "icon": "star"},

    # --- 第三阶段：向东延伸的分支 (曙光洞在东北方向) ---
    # 这一段是三干渠，在地图偏右上方，我们先画它，避免线最后折回来
    {"name": "曙光洞", "desc": "全长3898米的最长隧洞，穿过卢寨岭，见证了艰难的开凿历史。",
     "img": "shuguangdong.jpg", "lat": 36.20, "lon": 113.92, "color": "purple", "icon": "adjust"},
    {"name": "曙光渡桥", "desc": "连接曙光洞的宏伟石桥，宛如长虹卧波。",
     "img": "shuguangduqiao.jpg", "lat": 36.21, "lon": 113.93, "color": "gray", "icon": "road"},

    # --- 第四阶段：向南延伸的分支 (一干渠，一直流到合涧) ---
    # 这一段是一干渠，一路向南
    {"name": "桃园渡桥", "desc": "神奇的三用桥：上面通车，中间通水，下面排洪。",
     "img": "taoyuanqiao.jpg", "lat": 36.06, "lon": 113.81, "color": "darkblue", "icon": "bridge"},
    {"name": "南谷洞渡槽", "desc": "早期的石砌渡槽代表作，横跨露水河，气势如虹。",
     "img": "nangudong.jpg", "lat": 36.02, "lon": 113.80, "color": "orange", "icon": "road"},
    # 终点，汇流
    {"name": "红英汇流", "desc": "一干渠与英雄渠汇合处，两股清流激动相拥，庆祝胜利。",
     "img": "hongyinghuiliu.jpg", "lat": 35.98, "lon": 113.77, "color": "cadetblue", "icon": "link"}
]

# --- 5. 页面布局 ---

st.title("🗺️ 红旗渠 · 红色地图导览")

# 检查文件夹
if not os.path.exists(PHOTO_DIR):
    st.error(f"❌ 路径检查失败：请确保你的项目中有 `{PHOTO_DIR}` 文件夹。")
    st.stop()

col1, col2 = st.columns([1.8, 1.2])

# --- 左侧：地图 ---
with col1:
    st.markdown("### 📍 点击地图红点")

    m = folium.Map(location=[36.20, 113.80], zoom_start=10, tiles='OpenStreetMap')

    # 画线
    points = [[loc["lat"], loc["lon"]] for loc in locations]
    folium.PolyLine(points, color="#D32F2F", weight=3, opacity=0.8, tooltip="红旗渠干渠走向").add_to(m)

    # 撒点
    for loc in locations:
        folium.Marker(
            [loc["lat"], loc["lon"]],
            tooltip=loc['name'],  # 交互关键：鼠标放上去显示名字
            icon=folium.Icon(color=loc['color'], icon=loc['icon'], prefix='fa')
        ).add_to(m)

    # 渲染地图并获取点击事件
    map_data = st_folium(m, width="100%", height=600)

# --- 右侧：详情展示 ---
with col2:
    st.markdown("### 📜 档案详情")

    # 默认显示第一个
    target_loc = locations[0]

    # 交互逻辑：如果有点击，更新显示对象
    if map_data and map_data.get("last_object_clicked_tooltip"):
        clicked_name = map_data["last_object_clicked_tooltip"]
        for loc in locations:
            if loc["name"] == clicked_name:
                target_loc = loc
                break

    # 使用容器美化右侧显示
    with st.container():
        # 显示地名 (带红色左边框)
        st.markdown(f"""
            <div style="background-color: #FFF0F0; padding: 10px; border-left: 5px solid #D32F2F; border-radius: 5px; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #D32F2F !important; border: none; padding: 0;">📍 {target_loc['name']}</h3>
            </div>
        """, unsafe_allow_html=True)

        # 显示图片
        img_path = os.path.join(PHOTO_DIR, target_loc['img'])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            # 图片下方的文字介绍
            st.info(f"📝 **历史背景：**\n\n{target_loc['desc']}")
        else:
            st.warning("⚠️ 暂无该地点图片")
            st.code(f"期待文件: {target_loc['img']}")

# --- 页脚 ---
st.markdown("---")
st.caption("🔴 红旗渠精神：自力更生，艰苦创业，团结协作，无私奉献。")