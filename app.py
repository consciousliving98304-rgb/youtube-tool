import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viral YouTube Content Machine", layout="wide")
st.title("🎬 Viral YouTube Retention Engine")

# Helper & API Key input
col_k1, col_k2 = st.columns([3, 1])
with col_k1:
    api_key_input = st.text_input(
        "🔑 Enter Gemini API Key(s):",
        type="password",
        placeholder="Key1, Key2 (Comma se alag karke daalein)",
        help="Ek key ka quota khatam hone par agla automatic switch hoga."
    )
with col_k2:
    st.write("")
    st.write("")
    st.link_button("➕ Get Free API Key", "https://aistudio.google.com/app/apikey")

def call_gemini(keys_list, prompt):
    models_to_try = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    for idx, current_key in enumerate(keys_list):
        try:
            genai.configure(api_key=current_key)
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    return response.text
                except Exception as model_err:
                    if "429" in str(model_err) or "quota" in str(model_err).lower():
                        continue
                    else:
                        raise model_err
        except Exception as e:
            if "quota" in str(e).lower() or "429" in str(e):
                continue
            else:
                raise e
    return None

tab1, tab2 = st.tabs(["🚀 Viral Script & Visual Pack", "🔥 5 Retention-Engine Shorts Ideas"])

with tab2:
    st.subheader("🔥 Ultra-Viral Trending Concepts")
    st.caption("Aise concepts jisme pehle 20-30 second viewer screen se palke na jhapka sake:")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        trend_niche = st.selectbox("Category:", [
            "Horror / Skinwalker Mystery with Cute/Innocent Kid Hook",
            "Attractive Lead Character Drama / Suspense Encounter",
            "Akbar-Birbal & Tenali Rama Unsolved Riddles (High Comments)",
            "Mind-Bending Psychological Shorts with Plot Twist"
        ])
    with col_t2:
        trend_lang = st.selectbox("Language for Trend:", [
            "Hinglish (Hindi in English letters)",
            "Pure Hindi (हिंदी देवनागरी)",
            "English (USA/Global Audience)"
        ])
        
    if st.button("✨ Generate 5 Viral Retention Hooks"):
        if not api_key_input:
            st.error("Pehle apni Gemini API Key daalein!")
        else:
            keys_list = [k.strip() for k in api_key_input.split(",") if k.strip()]
            with st.spinner("Viral psychology research chal rahi hai..."):
                t_prompt = f"""
                You are a master YouTube retention strategist and viral algorithm hacker.
                Generate 5 high-retention concepts for niche: '{trend_niche}'.
                Output Language: {trend_lang}.

                Strict Rules for Each Concept:
                1. 👁️ The Visual Magnet (First 3 seconds visual: e.g., adorable innocent kid with big expressive eyes, striking attractive character, or spine-chilling visual hook).
                2. ⏱️ 0-25 Seconds Retention Trap: Exact lines that freeze scrolling and make dropping off impossible.
                3. 🌀 Mid-Story Loop: What sudden twist or mystery keeps them watching till the end.
                4. ❓ Next-Video / Comment Bait Ending: An unsolved riddle, shocking cliffhanger, or funny twist where answer is promised in the NEXT video.
                5. 🎵 Sound & SFX Trigger: Exact background music and sound cue.
                """
                res = call_gemini(keys_list, t_prompt)
                if res:
                    st.markdown(res)
                else:
                    st.error("API Key quota issue. Please check keys or generate a fresh key.")

with tab1:
    topic = st.text_input("Story Idea / Core Mystery:", placeholder="e.g. Masoom bacche ne aaine mein kuch dekha / Akbar ne pucha adbhoot sawal")

    col1, col2 = st.columns(2)
    with col1:
        video_type = st.selectbox("Video Format:", ["YouTube Shorts / Reel", "YouTube Long Video"])
    with col2:
        if video_type == "YouTube Shorts / Reel":
            duration = st.selectbox("Duration:", ["30 Seconds (Fast hook)", "60 Seconds (Full retention story)"])
        else:
            duration = st.selectbox("Duration:", ["3 Minutes (Tight pacing)", "5 Minutes (Standard story)", "8-10 Minutes (Deep narrative)", "10+ Minutes (Documentary)"])

    col3, col4 = st.columns(2)
    with col3:
        char_lead = st.selectbox("Magnet Lead Character:", [
            "👶 Super-Cute / Innocent Expressive Child (High Emotional Attachment)",
            "✨ Stunning / Attractive Mysterious Protagonist (High Visual Appeal)",
            "👑 Sharp Witty Folk Characters (Birbal, Tenali Rama, Clever Villager)",
            "🕵️ Gritty Detective / Haunted Survivor",
            "✏️ Custom (Apna character type likhein)"
        ])
    with col4:
        char_visual = st.selectbox("Visual Art Style:", [
            "🎨 2D Expressive Cartoon Animation (Pixar/Anime mix)",
            "🧸 3D Cute Pixar/Disney Style (High quality eyes & facial expressions)",
            "🎬 Cinematic Hyper-Realistic (Real human drama look)",
            "👤 Dark Noir Minimalist / Manga Silhouette"
        ])

    custom_char_detail = ""
    if char_lead.startswith("✏️"):
        custom_char_detail = st.text_input("Custom Character Details:", placeholder="e.g. 5 saal ki cute gudiya Ananya aur uska ajeeb dost")

    col5, col6, col7 = st.columns(3)
    with col5:
        language = st.selectbox("Script Language:", [
      
