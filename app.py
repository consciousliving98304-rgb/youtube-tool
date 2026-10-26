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
                t_prompt = (
                    f"You are a master YouTube retention strategist and viral algorithm hacker.\n"
                    f"Generate 5 high-retention concepts for niche: '{trend_niche}'.\n"
                    f"Output Language: {trend_lang}.\n\n"
                    f"Strict Rules for Each Concept:\n"
                    f"1. The Visual Magnet (First 3 seconds visual: e.g., adorable innocent kid with big expressive eyes, striking attractive character, or spine-chilling visual hook).\n"
                    f"2. 0-25 Seconds Retention Trap: Exact lines that freeze scrolling and make dropping off impossible.\n"
                    f"3. Mid-Story Loop: What sudden twist or mystery keeps them watching till the end.\n"
                    f"4. Next-Video / Comment Bait Ending: An unsolved riddle, shocking cliffhanger, or funny twist where answer is promised in the NEXT video.\n"
                    f"5. Sound & SFX Trigger: Exact background music and sound cue."
                )
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
            "👶 Super-Cute / Innocent Expressive Child",
            "✨ Stunning / Attractive Mysterious Protagonist",
            "👑 Sharp Witty Folk Characters (Birbal, Tenali Rama)",
            "🕵️ Gritty Detective / Haunted Survivor",
            "✏️ Custom (Apna character type likhein)"
        ])
    with col4:
        char_visual = st.selectbox("Visual Art Style:", [
            "🎨 2D Expressive Cartoon Animation",
            "🧸 3D Cute Pixar/Disney Style",
            "🎬 Cinematic Hyper-Realistic",
            "👤 Dark Noir Minimalist / Manga Silhouette"
        ])

    custom_char_detail = ""
    if char_lead.startswith("✏️"):
        custom_char_detail = st.text_input("Custom Character Details:", placeholder="e.g. 5 saal ki cute gudiya Ananya aur uska ajeeb dost")

    col5, col6, col7 = st.columns(3)
    with col5:
        language = st.selectbox("Script Language:", [
            "Hinglish (Hindi written in English letters)",
            "Pure Hindi (हिंदी देवनागरी)",
            "English (USA/Global Audience)",
            "Indian English"
        ])
    with col6:
        tone = st.selectbox("Vibe / Tone:", [
            "Dark / Suspenseful / Horror with Emotional Core",
            "Witty, Funny & Clever Mind-Games",
            "Mysterious, Shocking & Plot-Twist Heavy",
            "Heartwarming then Sudden Chill / Shock"
        ])
    with col7:
        end_hook = st.selectbox("Ending Retention Hook:", [
            "🧩 Unsolved Riddle / Paheli (Answer in Part 2)",
            "😱 Massive Cliffhanger / Mid-Action Cut (Part 2 Coming)",
            "😂 Unexpected Funny Twist / Sarcastic Punchline",
            "💬 Viewer Debate Question (Make everyone comment their theory)"
        ])

    if st.button("Generate Viral Script Pack"):
        if not api_key_input:
            st.error("Pehle Gemini API Key enter karein!")
        elif not topic:
            st.warning("Pehle koi topic ya story idea likhiye!")
        else:
            keys_list = [k.strip() for k in api_key_input.split(",") if k.strip()]
            selected_char = custom_char_detail if char_lead.startswith("✏️") and custom_char_detail else char_lead

            prompt = (
                f"You are a world-class YouTube viral storytelling genius and retention engineer.\n"
                f"Format: {video_type}\n"
                f"Duration: {duration}\n"
                f"Topic: {topic}\n"
                f"Tone: {tone}\n"
                f"Lead Magnet Character: {selected_char}\n"
                f"Visual Style: {char_visual}\n"
                f"Script Language: {language}\n"
                f"End Trap Hook: {end_hook}\n\n"
                f"RETENTION RULES YOU MUST STRICTLY IMPLEMENT:\n"
                f"1. THUMBNAIL & TITLES: Make titles emotionally irresistible. Thumbnail prompt must focus on the magnet character ({selected_char}) with exaggerated expressions.\n"
                f"2. 0-30 SECONDS HYPNOTIC HOOK: Never start with boring intro. Start mid-action or with a shocking question within first 3 seconds focusing on lead character's look.\n"
                f"3. MID-PACING LOOPS: Every 25 seconds must have a micro-revelation or sonic shift.\n"
                f"4. SCRIPT & DIALOGUE: Write in natural, engaging {language}. Pacing matched to {duration}.\n"
                f"5. THE RETENTION END-TRAP ({end_hook}): Force viewers to comment or watch next video.\n\n"
                f"Deliver the complete pack in these 6 sections:\n"
                f"1. 🎯 5 High-CTR Viral Titles & Psychological Thumbnail Prompts\n"
                f"2. ⚡ The First 25-Second Retention Blueprint\n"
                f"3. 📜 Full Timed Script (Scene by scene with character emotions in {language})\n"
                f"4. 🎥 Scene-by-Scene Visual Prompts matching {char_visual} and {selected_char}\n"
                f"5. 🎵 Sound Design & Background Music\n"
                f"6. 🪝 The Next-Video Bait & SEO"
            )

            output_container = st.empty()
            full_text = ""
            success = False
            models_to_try = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-pro"]

            for idx, current_key in enumerate(keys_list):
                try:
                    genai.configure(api_key=current_key)
                    for model_name in models_to_try:
                        try:
                            model = genai.GenerativeModel(model_name)
                            with st.spinner(f"Viral retention pack taiyar ho raha hai ({duration})..."):
                                response = model.generate_content(prompt, stream=True)
                                for chunk in response:
                                    full_text += chunk.text
                                    output_container.markdown(full_text)
                                success = True
                                break
                        except Exception as model_err:
                            if "429" in str(model_err) or "quota" in str(model_err).lower():
                                continue
                            else:
                                raise model_err

                    if success:
                        break
                except Exception as e:
                    if "quota" in str(e).lower() or "429" in str(e):
                        st.warning(f"Key #{idx+1} quota limit par aa gayi. Agli key check ho rahi hai...")
                        continue
                    else:
                        st.error(f"Error with Key #{idx+1}: {e}")
                        break

            if success:
                st.download_button(
                    label="📥 Download Viral Pack (.txt)",
                    data=full_text,
                    file_name=f"{topic.replace(' ', '_')[:25]}_viral_pack.txt",
                    mime="text/plain"
                )
            elif not success and keys_list:
                st.error("API keys quota reach ho gaya hai. 'Get Free API Key' par tap karke nayi key lein.")
