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
            "Horror / Skinwalker Mystery with Cute Kid Hook",
            "Attractive Lead Character Drama / Suspense Encounter",
            "Akbar-Birbal & Tenali Rama Unsolved Riddles",
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
                1. The Visual Magnet (First 3 seconds visual: e.g., adorable innocent kid with big expressive eyes, striking attractive character, or spine-chilling visual hook).
                2. 0-25 Seconds Retention Trap: Exact lines that freeze scrolling and make dropping off impossible.
                3. Mid-Story Loop: What sudden twist or mystery keeps them watching till the end.
                4. Next-Video / Comment Bait Ending
