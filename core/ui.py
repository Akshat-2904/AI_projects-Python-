import streamlit as st
import torch
import torch.nn as nn
import numpy as np
import socket
import time
from collections import deque

# ================= MODEL =================
class GloveNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(6, 20),
            nn.ReLU(),
            nn.Linear(20, 12),
            nn.ReLU(),
            nn.Linear(12, 7)
        )

    def forward(self, x):
        return self.model(x)

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    m = GloveNN()
    m.load_state_dict(torch.load("glove.pt", map_location="cpu"))
    m.eval()
    return m

model = load_model()

# ================= LABELS =================
labels = [
    "Yes", "No", "Domain Expansion",
    "Everyone", "Hi", "We Are", "Radiant Coders"
]

# ================= UDP =================
UDP_IP = "0.0.0.0"
UDP_PORT = 12346

@st.cache_resource
def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((UDP_IP, UDP_PORT))
    s.setblocking(False)
    return s

sock = get_socket()

# ================= STREAMLIT =================
st.set_page_config(page_title="AI Glove", layout="wide")

# ===== CUSTOM STYLE =====
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #111;
    box-shadow: 0 0 15px rgba(0,255,150,0.2);
}
.sensor-box {
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Sign Language Glove</div>', unsafe_allow_html=True)

# ================= STATE =================
if "buffer" not in st.session_state:
    st.session_state.buffer = deque(maxlen=5)

if "history" not in st.session_state:
    st.session_state.history = []

# ================= RECEIVE =================
values = None
try:
    data, _ = sock.recvfrom(1024)
    parts = data.decode().strip().split(",")
    if len(parts) == 6:
        values = [int(p) for p in parts]
except:
    pass

# ================= UI =================
if values is not None:

    # ===== PREDICT =====
    x_np = np.array(values) / 4095.0
    x = torch.tensor(x_np, dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        output = model(x)
        probs = torch.softmax(output, dim=1)
        pred = torch.argmax(probs, dim=1).item()

    confidence = probs[0][pred].item()

    # smoothing
    if confidence > 0.7:
        st.session_state.buffer.append(pred)

    if len(st.session_state.buffer) > 0:
        final_pred = max(set(st.session_state.buffer), key=st.session_state.buffer.count)
        gesture = labels[final_pred]
    else:
        gesture = "..."

    # history
    if confidence > 0.85:
        st.session_state.history.append(gesture)
        st.session_state.history = st.session_state.history[-10:]

    # ===== LAYOUT =====
    col1, col2 = st.columns([1, 1])

    # ================= LEFT: GLOVE =================
    with col1:
        st.subheader("🖐 Sensor Activity")

        cols = st.columns(6)

        for i, val in enumerate(values):
            v = val / 4095.0
            r = int(255 * v)
            g = int(255 * (1 - v))
            color = f"rgb({r},{g},80)"

            cols[i].markdown(f"""
            <div class="sensor-box" style="background:{color}">
            H{i+1}<br>{val}
            </div>
            """, unsafe_allow_html=True)

        st.bar_chart(values)

    # ================= RIGHT: PREDICTION =================
    with col2:
        st.subheader("🧠 Prediction")

        st.markdown(f"""
        <div class="card">
            <h1 style="color:#00ffcc;">{gesture}</h1>
            <p>Confidence: {confidence:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📊 Confidence")

        for i, p in enumerate(probs[0]):
            st.progress(float(p), text=f"{labels[i]}: {p.item():.2f}")

        st.subheader("🕒 History")
        st.write(" → ".join(st.session_state.history))

    # ===== STATUS =====
    st.success("🟢 LIVE DATA STREAM")

else:
    st.warning("🔴 Waiting for ESP32...")

# ================= REFRESH =================
time.sleep(0.05)
st.rerun()