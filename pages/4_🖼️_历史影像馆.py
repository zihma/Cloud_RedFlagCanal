import streamlit as st
st.set_page_config(page_title="历史影像", page_icon="🖼️", layout="wide")
st.title("🖼️ 历史影像馆 - 震撼现场")

photos = [
    {"file": "jiemei.jpg", "desc": "姐妹同力：妇女能顶半边天"},
    {"file": "xuanyashigong.jpg", "desc": "悬崖施工：腰系绳索，凌空作业"},
    {"file": "dulunche.jpg", "desc": "独轮车：红旗渠是推出来的"},
    {"file": "zhizao.jpg", "desc": "自力更生：没有工具自己造"},
    {"file": "yexue.jpg", "desc": "以地为床：蓝天为被，睡在山洞"},
    {"file": "tianfeng.jpg", "desc": "一丝不苟：姑娘们精心填补渠缝"},
    {"file": "tongshui.jpg", "desc": "圆梦时刻：1966年竣工通水典礼"}
]

c1, c2 = st.columns(2)
for i, p in enumerate(photos):
    with (c1 if i % 2 == 0 else c2):
        try:
            st.image(f"assets/photos/{p['file']}", use_container_width=True)
            st.caption(f"📸 {p['desc']}")
        except:
            pass