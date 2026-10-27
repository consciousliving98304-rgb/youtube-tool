import streamlit as st
import requests
import json

st.set_page_config(page_title="Viral YouTube Creator", layout="wide")
st.title("🎬 Viral YouTube Retention Engine")

# Auto-fetch keys from Secrets
s_keys = []
for k_name in ["KEY1", "KEY2", "KEY3", "GEMINI_KEYS"]:
    val = st.secrets.get(k_name, "")
    if isinstance(val, list):
        s_keys.extend(val)
    elif isinstance(val, str) and val.strip():
        s_keys.extend([x.strip() for x in val.split(",") if x.strip()])

col_k1, col_k2 = st.columns([3, 1])
with col_k1:
    api_key_input = st.text_input(
        "🔑 Gemini API Key(s):",
        value=", ".join(s_keys),
        type="password",
        placeholder="AQ... ya AIzaSy... (Comma-separated)",
        help="Google AI Studio se mili keys automatic yahan load hoti hain."
    )
with col_k2:
    st.write("")
    st.write("")
    st.link_button("➕ Get Free API Key", "https://aistudio.google.com/app/apikey")

def clean_key(raw_k):
    return raw_k.strip().strip('"').strip("'").strip()

def run_prompt_rest(keys_list, prompt_text):
    models = ["gemini-flash-latest", "gemini-1.5-flash", "gemini-1.5-pro"]
    last_err = ""
    
    for k in keys_list:
        k_clean = clean_key(k)
        if not k_clean:
            continue
        
        for m in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": k_clean
            }
            payload = {
                "contents": [
                    {
                        "parts": [{"text": prompt_text}]
                    }
                ]
            }
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=60)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        text_part = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                        if text_part:
                            return text_part, None
                else:
                    err_json = resp.json()
                    err_msg = err_json.get("error", {}).get("message", resp.text)
                    last_err = f"{resp.status_code} - {err_msg}"
                    if resp.status_code == 429:
                        break
            except Exception as e:
                last_err = str(e)
                continue
                
    return None, last_err

tab1, tab2 = st.tabs(["🚀 Viral Script & Visual Pack", "🔥 5 Retention Shorts Ideas"])

with tab2:
    st.subheader("🔥 5 Viral Retention Hooks")
    niche = st.selectbox("Category:", [
        "Horror with Cute Kid Hook",
        "Attractive Lead Drama",
        "Akbar-Birbal Riddles",
        "Plot-Twist Mystery"
    ])
    lang_t = st.selectbox("Trend Language:", ["Hinglish", "Pure Hindi", "English"])
    
    if st.button("✨ Generate 5 Viral Concepts"):
        raw_keys = [clean_key(x) for x in api_key_input.split(",") if clean_key(x)]
        if not raw_keys:
            st.error("Pehle API key enter karein!")
        else:
            tp = f"Viral algorithm expert: Generate 5 viral shorts concepts for {niche} in {lang_t}. Include visual magnet hook (0-3s), curiosity loop, comment bait ending, and audio keywords."
            with st.spinner("Trending concepts taiyar ho rahe hain..."):
                out, err = run_prompt_rest(raw_keys, tp)
            if out:
                st.markdown(out)
            else:
                st.error(f"Error Detail: {err}")

with tab1:
    topic = st.text_input("Story Idea / Core Mystery:", placeholder="e.g. Masoom bacche ne aaine mein kuch dekha")
    
    c1, c2 = st.columns(2)
    with c1:
        v_type = st.selectbox("Format:", ["YouTube Shorts / Reel", "YouTube Long Video"])
    with c2:
        dur = st.selectbox("Duration:", ["30 Sec", "60 Sec", "3 Min", "5 Min", "8-10 Min"])
        
    c3, c4 = st.columns(2)
    with c3:
        char_lead = st.selectbox("Magnet Lead Character:", [
            "Super-Cute Innocent Child",
            "Stunning Attractive Lead",
            "Witty Birbal / Folk Hero",
            "Custom"
        ])
    with c4:
        art_style = st.selectbox("Visual Style:", [
            "2D Cartoon Animation",
            "3D Cute Pixar/Disney Style",
            "Cinematic Hyper-Realistic"
        ])
        
    c_custom = ""
    if char_lead == "Custom":
        c_custom = st.text_input("Custom Character Details:")
        
    c5, c6, c7 = st.columns(3)
    with c5:
        lang = st.selectbox("Language:", ["Hinglish", "Pure Hindi (हिंदी)", "English (USA)", "Indian English"])
    with c6:
        tone = st.selectbox("Vibe / Tone:", [
            "Suspense / Horror with Emotional Core",
            "Witty & Clever Humour",
            "Shocking Plot-Twist"
        ])
    with c7:
        hook_end = st.selectbox("Ending Hook:", [
            "Unsolved Riddle (Part 2 Bait)",
            "Massive Cliffhanger",
            "Unexpected Funny Twist",
            "Viewer Debate Question"
        ])
        
    if st.button("Generate Complete Viral Pack"):
        raw_keys = [clean_key(x) for x in api_key_input.split(",") if clean_key(x)]
        if not raw_keys:
            st.error("Kripya Gemini API key daalein!")
        elif not topic:
            st.warning("Pehle koi topic likhiye!")
        else:
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
                result, err = run_prompt_rest(raw_keys, full_prompt)
                
            if result:
                st.markdown(result)
                st.download_button("📥 Download Viral Pack (.txt)", result, f"{topic[:20]}_viral_pack.txt", "text/plain")
            else:
                st.error(f"Error Detail: {err}")
