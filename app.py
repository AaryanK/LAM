import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# Set page configuration for mobile responsiveness
st.set_page_config(page_title="Camera Stream", layout="wide")

st.title("Mobile-Compatible Camera Stream with WebRTC")

st.write("Access your camera from both desktop and mobile devices. Make sure to allow camera permissions.")

# Define a VideoTransformer class for frame processing
class VideoTransformer(VideoProcessorBase):
    def transform(self, frame):
        # Get the frame as a numpy array
        img = frame.to_ndarray(format="bgr24")

        # Optionally add some processing (e.g., draw a rectangle)
        height, width, _ = img.shape
        cv2.rectangle(img, (10, 10), (width - 10, height - 10), (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Start the WebRTC streamer
webrtc_streamer(
    key="mobile-camera",
    video_processor_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},  # Video only
)
