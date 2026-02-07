import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
import requests  # 新增：用于下载模型文件

# --- 1. 页面基础设置 ---
st.set_page_config(page_title="AI修复体验", page_icon="🎨", layout="wide")

st.title("🎨 AI 影像修复实验室 (云端引擎)")
st.markdown("---")

# --- 2. 定义模型路径 ---
# 文件夹路径
MODEL_DIR = "assets/models"
# 三个关键文件路径
PROTOTXT = os.path.join(MODEL_DIR, "colorization_deploy_v2.prototxt")
POINTS_PATH = os.path.join(MODEL_DIR, "pts_in_hull.npy")
MODEL_PATH = os.path.join(MODEL_DIR, "colorization_release_v2.caffemodel")  # 这个是你删掉的大文件

# 模型下载链接 (Dropbox直链，速度快且稳定)
MODEL_URL = "https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1"


# --- 3. 核心功能：加载模型 (带自动下载功能) ---
@st.cache_resource
def load_model():
    # 1. 检查文件夹是否存在，不存在则创建
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 2. 【关键修改】如果大模型文件不存在，自动下载
    if not os.path.exists(MODEL_PATH):
        with st.spinner("🚀 首次运行，正在云端部署 AI 模型 (约120MB)..."):
            try:
                r = requests.get(MODEL_URL, stream=True)
                with open(MODEL_PATH, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            except Exception as e:
                st.error(f"❌ 模型下载失败，请检查网络。错误信息: {e}")
                return None

    # 3. 检查其他小配置文件 (这些你应该上传到GitHub了)
    if not os.path.exists(PROTOTXT) or not os.path.exists(POINTS_PATH):
        st.error("❌ 缺少配置文件！请检查 assets/models 里有没有 .prototxt 和 .npy 文件。")
        return None

    # 4. 加载 Caffe 模型
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL_PATH)
    pts = np.load(POINTS_PATH)

    # 设置色彩中心
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    return net


# --- 4. 核心功能：AI 上色 ---
def colorize_image(image_input, net):
    img = np.array(image_input)
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    normalized = img_bgr.astype("float32") / 255.0
    lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    ab = cv2.resize(ab, (img_bgr.shape[1], img_bgr.shape[0]))
    L_orig = cv2.split(lab)[0]

    colorized = np.concatenate((L_orig[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    return Image.fromarray((colorized * 255).astype("uint8"))


# --- 5. 辅助功能：滤镜 ---
def apply_filters(image, saturation, brightness, temp_shift):
    enhancer = ImageEnhance.Color(image)
    img = enhancer.enhance(saturation)
    enhancer_b = ImageEnhance.Brightness(img)
    img = enhancer_b.enhance(brightness)
    if temp_shift != 0:
        r, g, b = img.split()
        r = r.point(lambda i: i + temp_shift)
        b = b.point(lambda i: i - temp_shift)
        img = Image.merge('RGB', (r, g, b))
    return img


# --- 6. 页面交互 ---
with st.sidebar:
    st.header("⚙️ 修复控制台")
    st.info("💡 提示：模型会在首次运行时自动下载，请稍候。")
    st.markdown("### 🛠️ 后期精修")
    sat_val = st.slider("🎨 色彩饱和度", 0.0, 3.0, 1.3)
    bright_val = st.slider("☀️ 画面亮度", 0.5, 2.0, 1.1)
    temp_val = st.slider("🌡️ 色温修正", -50, 50, 30)

uploaded_file = st.file_uploader("📂 请上传黑白照片", type=["jpg", "png", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns(2)
    image = Image.open(uploaded_file).convert("RGB")
    with col1:
        st.subheader("🎞️ 原始影像")
        st.image(image, use_container_width=True)

    if st.button("🚀 启动 AI 修复", type="primary"):
        # 调用加载函数（这里会触发自动下载）
        net = load_model()

        if net:
            with st.spinner("🤖 正在处理..."):
                try:
                    raw_img = colorize_image(image, net)
                    final_img = apply_filters(raw_img, sat_val, bright_val, temp_val)
                    with col2:
                        st.subheader("✨ 修复效果")
                        st.image(final_img, use_container_width=True)
                        st.success("修复成功！")
                except Exception as e:
                    st.error(f"处理出错: {e}")
else:
    st.info("👈 请上传照片开始")