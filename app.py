import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np

# Sahifa sozlamalari
st.set_page_config(page_title="Gesture Drawing App", layout="wide")
st.title("🎨 Gesture Drawing App (Streamlit Edition)")

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.score = 0
        self.w, self.h = 640, 480
        # Chizma uchun qatlam (canvas)
        self.canvas_draw = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self.prev_x, self.prev_y = None, None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1) # Oyna effekti
        img = cv2.resize(img, (self.w, self.h))

        # Marker (ekran markazi)
        x, y = self.w // 2, self.h // 2
        cv2.circle(img, (x, y), 15, (0, 255, 0), -1)

        # CLICK tugmasi
        cv2.rectangle(img, (20, 20), (180, 80), (255, 0, 0), 2)
        cv2.putText(img, "CLICK", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # CLEAR tugmasi
        cv2.rectangle(img, (20, 100), (180, 160), (0, 255, 255), 2)
        cv2.putText(img, "CLEAR", (45, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Chizish mantiqi
        if self.prev_x is not None:
            cv2.line(self.canvas_draw, (self.prev_x, self.prev_y), (x, y), (0, 0, 255), 5)
        
        self.prev_x, self.prev_y = x, y

        # Tugmalarni tekshirish
        if 20 < x < 180:
            if 20 < y < 80:
                self.score += 1
            elif 100 < y < 160:
                self.canvas_draw = np.zeros((self.h, self.w, 3), dtype=np.uint8)

        # Tasvirlarni birlashtirish
        img = cv2.add(img, self.canvas_draw)
        cv2.putText(img, f"Score: {self.score}", (self.w - 200, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return img

# WebRTC komponentini chiqarish
webrtc_streamer(key="gesture-draw", video_transformer_factory=VideoTransformer)

st.sidebar.info("Nuqtani (markazni) tugmalar ustiga olib boring va havoda chizing!")
