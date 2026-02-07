import streamlit as st
st.set_page_config(page_title="英雄谱", page_icon="📜", layout="wide")
st.title("📜 红旗渠·英雄谱")

heroes = [
    {"name": "吴祖太", "title": "总设计师", "img": "wuzutai.jpg", "desc": "全县唯一的科班水利技术员，27岁牺牲于王家庄隧洞。"},
    {"name": "任羊成", "title": "除险队长", "img": "renyangcheng.jpg", "desc": "“飞虎神鹰”，带伤凌空除险，砸断牙齿往肚里咽。"},
    {"name": "杨贵", "title": "老县委书记", "img": "yanggui.jpg", "desc": "红旗渠总决策者，顶住压力誓要“重新安排林县河山”。"},
    {"name": "李改云", "title": "妇女营长", "img": "ligaiyun.jpg", "desc": "舍己救人，被落石砸断右腿落下终身残疾。"},
    {"name": "常虎根", "title": "神炮手", "img": "changhugen.jpg", "desc": "“爬山虎”，带领炮手在悬崖开凿，炸开太行山。"},
    {"name": "马有金", "title": "黑老马", "img": "mayoujin.jpg", "desc": "任职最长的指挥长，常年奔波工地，与民工同吃同住。"}
]

cols = st.columns(3)
for i, hero in enumerate(heroes):
    with cols[i % 3]:
        st.markdown("---")
        try:
            st.image(f"assets/photos/{hero['img']}", caption=hero['title'], use_container_width=True)
            st.subheader(hero['name'])
            st.write(hero['desc'])
        except:
            st.error(f"缺失图片: {hero['img']}")