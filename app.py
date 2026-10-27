import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viral YouTube Creator", layout="wide")
st.title("🎬 Viral YouTube Retention Engine")

# Auto-fetch keys from Secrets if available
raw_saved_keys = st.secrets.get("GEMINI_KEYS", "")

col_k1, col_k2 = st.columns([3, 1])
with col_k1:
    api_key_input = st.text_input(
        "🔑 Gemini API Key(s):",
        value=raw_saved_keys,
        type="password",
        placeholder="Key1, Key2, Key3",
        help="Secrets mein save hone par automatic fill rahegi."
    )
with col_k2:
    st.write("")
    st.write("")
    st.link_button("➕ Get Free API Key", "https://aistudio.google.com/app/apikey")

def clean_key(k_str):
    # Quotes, whitespace aur extra symbols ko remove karta hai
    return k_str.strip().strip('"').strip("'").strip()

def run_prompt(keys_list, prompt):
    models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
    last_err = ""
    for k in keys_list:
        k_clean = clean_key(k)
        if not k_clean:
            continue
        try:
            genai.configure(api_key=k_clean)
            for m in models:
                try:
                    model = genai.GenerativeModel(m)
                    res = model.generate_content(prompt)
                    if res and res.text:
                        return res.text, None
                except Exception as me:
                    last_err = str(me)
                    continue
        except Exception as e:
            last_err = str(e)
            continue
    return None, last_err

tab1, tab2 = st.tabs(["🚀 Viral Script & Visual Pack", "🔥 5 Retention Shorts Ideas"])

with tab2:
    st.subheader("🔥 5 Viral Retention Hooks")
    niche = st.selectbox("Category:", ["Horror with Cute Kid Hook", "Attractive Lead Drama", "Akbar-Birbal Riddles", "Plot-Twist Mystery"])
    lang_t = st.selectbox("Trend Language:", ["Hinglish", "Pure Hindi", "English"])
    
    if st.button("✨ Generate 5 Viral Concepts"):
        if not api_key_input:
            st.error("Pehle Gemini API Key enter karein!")
        else:
            keys = [x for x in api_key_input.split(",") if clean_key(x)]
            tp = f"Viral algorithm expert: Generate 5 viral shorts concepts for {niche} in {lang_t}. Include visual magnet hook (0-3s), curiosity loop, comment bait ending, and audio keywords."
            with st.spinner("Trending concepts taiyar ho rahe hain..."):
                out, err = run_prompt(keys, tp)
            if out:
                st.markdown(out)
            else:
                st.error(f"Google Error Detail: {err}")

with tab1:
    topic = st.text_input("Story Idea / Core Mystery:", placeholder="e.g. Masoom bacche ne aaine mein kuch dekha")
    
    c1, c2 = st.columns(2)
    with c1:
        v_type = st.selectbox("Format:", ["YouTube Shorts / Reel", "YouTube Long Video"])
    with c2:
        dur = st.selectbox("Duration:", ["30 Sec", "60 Sec", "3 Min", "5 Min", "8-10 Min"])
        
    c3, c4 = st.columns(2)
    with c3:
        char_lead = st.selectbox("Magnet Lead Character:", ["Super-Cute Innocent Child", "Stunning Attractive Lead", "Witty Birbal / Folk Hero", "Custom"])
    with c4:
        art_style = st.selectbox("Visual Style:", ["2D Cartoon Animation", "3D Cute Pixar/Disney Style", "Cinematic Hyper-Realistic"])
        
    c_custom = ""
    if char_lead == "Custom":
        c_custom = st.text_input("Custom Character Details:")
        
    c5, c6, c7 = st.columns(3)
    with c5:
        lang = st.selectbox("Language:", ["Hinglish", "Pure Hindi (हिंदी)", "English (USA)", "Indian English"])
    with c6:
        tone = st.selectbox("Vibe / Tone:", ["Suspense / Horror with Emotional Core", "Witty & Clever Humour", "Shocking Plot-Twist"])
    with c7:
        hook_end = st.selectbox("Ending Hook:", ["Unsolved Riddle (Part 2 Bait)", "Massive Cliffhanger", "Unexpected Funny Twist", "Viewer Debate Question"])
        
    if st.button("Generate Complete Viral Pack"):
        if not api_key_input:
            st.error("Pehle Gemini API Key enter karein!")
        elif not topic:
            st.warning("Pehle koi topic likhiye!")
        else:
            keys = [x for x in api_key_input.split(",") if clean_key(x)]
            lead = c_custom if char_lead == "Custom" and c_custom else char_lead
            
            full_prompt = f"""
Role: Master YouTube Scriptwriter & Retention Engineer.
Format: {v_type} | Duration: {dur} | Topic: {topic} | Tone: {tone}
Lead Magnet: {lead} | Art Style: {art_style} | Language: {lang} | End Hook: {hook_end}

Deliver high retention script pack in 6 sections:
1. 🎯 5 Viral Titles & Psychological Thumbnail Prompts focusing on {lead}
2. ⚡ The First 25-Second Retention Hook (mid-action start, visual hook)
3. 📜 Full Timed Script in {lang} matching {dur}
4. 🎥 Scene-by-Scene Visual Prompts matching {art_style}
5. 🎵 Sound Design & Background Music
6. 🪝 The Next-Video Bait ({hook_end}) & SEO Tags
"""
            with st.spinner(f"Viral pack taiyar ho raha hai ({dur})..."):
                result, err = run_prompt(keys, full_prompt)
                
            if result:
                st.markdown(result)
                st.download_button("📥 Download Viral Pack (.txt)", result, f"{topic[:20]}_viral_pack.txt", "text/plain")
            else:
                st.error(f"Google Error Detail: {err}")
