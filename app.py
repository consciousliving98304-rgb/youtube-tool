import streamlit as st
import google.generativeai as genai

# API key configure karein
genai.configure(api_key="AQ.Ab8RN6LeKXC537PjjBk_TdFGE2Pi3gn143UVGjszyk8yngLTiQ")
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="YouTube Creator Tool", layout="wide")
st.title("🎬 YouTube Video Content Generator")

# Inputs
topic = st.text_input("Video Topic / Idea:", placeholder="e.g. Haunted forest incident / Akbar Birbal witty story")
video_type = st.selectbox("Video Format:", ["YouTube Long Video", "YouTube Shorts / Reel"])
tone = st.selectbox("Style / Tone:", ["Storytelling / Casual", "Dark / Suspenseful / Horror", "Engaging & Energetic", "Educational & Serious"])

if st.button("Generate Complete Video Pack"):
    if not topic:
        st.warning("Pehle koi topic likhiye!")
    else:
        with st.spinner("Writing script, audio cues, titles & SEO..."):
            prompt = f"""
            You are an expert YouTube strategist, sound designer, and scriptwriter.
            Format: {video_type}
            Topic: {topic}
            Tone: {tone}
            Language: Hinglish (Hindi written in English alphabets) + English where appropriate.

            Provide the output structured into these 6 sections:
            1. 🎯 5 Viral Click-Worthy Titles (High CTR)
            2. 🖼️ Thumbnail Concepts (Text overlay + Visual scene idea)
            3. 📜 Full Script (with a strong 3-second hook, engaging body scenes, and Call to Action)
            4. 🎥 Visual Cues (Scene-by-scene animation/image ideas to show on screen)
            5. 🎵 Background Music & Sound Effects (SFX) Cues:
               - For each scene, specify exact Sound Effect (SFX) (e.g., footstep, door creak, heartbeat, swoosh).
               - Exact Background Music mood/genre.
               - Recommended YouTube Audio Library search terms (100% copyright-free).
            6. 🔍 SEO Pack (Optimized Description, 15 relevant tags, and top 5 hashtags)
            """
            
            response = model.generate_content(prompt)
            output_text = response.text
            
            # Display generated content
            st.markdown(output_text)
            
            # Download button to save content directly on mobile/PC
            st.download_button(
                label="📥 Download Complete Script & Pack (.txt)",
                data=output_text,
                file_name=f"{topic.replace(' ', '_')[:25]}_pack.txt",
                mime="text/plain"
            )
