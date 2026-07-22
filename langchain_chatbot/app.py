import streamlit as st
from chatbot import YouTubeChatBot

st.set_page_config(
    page_title="YouTube Video ChatBot",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Video Q&A ChatBot")
st.write("Ask questions about any YouTube video.")

# Create chatbot object once
if "bot" not in st.session_state:
    st.session_state.bot = YouTubeChatBot()

# Track whether a video has been loaded
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

# --------------------------
# Load Video
# --------------------------
video_url = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=xxxxxxxx"
)

if st.button("Load Video"):

    if video_url.strip() == "":
        st.warning("Please enter a YouTube URL.")

    else:
        with st.spinner("Loading transcript and creating embeddings..."):
            try:
                st.session_state.bot.load_video(video_url)
                st.session_state.video_loaded = True
                st.success("✅ Video loaded successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# --------------------------
# Ask Questions
# --------------------------
st.divider()

question = st.text_input(
    "Ask a question about the video"
)

if st.button("Get Answer"):

    if not st.session_state.video_loaded:
        st.warning("Please load a video first.")

    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:
        with st.spinner("Thinking..."):
            try:
                answer = st.session_state.bot.ask(question)

                st.success("Answer")

                st.write(answer)

            except Exception as e:
                st.error(e)