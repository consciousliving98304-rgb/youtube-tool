import streamlit as st
import google.generativeai as genai

# API key configure karein
genai.configure(api_key="AQ.Ab8RN6LeKXC537PjjBk_TdFGE2Pi3gn143UVGjszyk8yngLTiQ")
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="YouTube Creator Tool", layout="wide")
st.title("🎬 YouTube Video Content Generator")

# Inputs
topic = st.text_input("Video Topic / Idea:", placeholder="e.g. AI tools in 2024 for students")
video_type = st.selectbox("Video Format:", ["YouTube Long Video", "YouTube Shorts / Reel"])
tone = st.selectbox("Style / Tone:", ["Engaging & Energetic", "Educational & Serious", "Storytelling / Casual"])

if st.button("Generate Complete Video Pack"):
    if not topic:
        st.warning("Pehle koi topic likhiye!")
    else:
        with st.spinner("Writing script, titles & SEO..."):
            prompt = f"""
            You are an expert YouTube strategist and scriptwriter.
            Format: {video_type}
            Topic: {topic}
            Tone: {tone}
            Language: Hinglish (Hindi written in English alphabets) + English where appropriate.

            Provide the output structured into these 5 sections:
            1. 🎯 5 Viral Click-Worthy Titles (High CTR)
            2. 🖼️ Thumbnail Concepts (Text overlay + Visual scene idea)
            3. 📜 Full Script (with a strong 3-second hook, structured body, and Call to Action)
            4. 🎥 B-roll / Visual cues (What footage/images to show on screen while speaking)
            5. 🔍 SEO Pack (Optimized Description, 15 relevant tags, and top 5 hashtags)
            """
            
            response = model.generate_content(prompt)
            st.markdown(response.text)
