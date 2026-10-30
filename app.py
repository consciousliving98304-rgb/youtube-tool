
import streamlit as st
import requests
import json
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Viral YouTube Creator Tool",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Viral YouTube Creator Tool")
st.write("Create engaging YouTube content with AI.")
st.divider()

# ---------------- GEMINI API SETTINGS ----------------

API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.8-flash:generateContent"
)

try:
    SECRET_KEY = st.secrets.get("KEY1", "")
except Exception:
    SECRET_KEY = ""

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "Gemini API Key",
        value=SECRET_KEY,
        type="password"
    )

    st.info("Your API key is kept private.")

    st.markdown("---")
    st.write("🎯 Target: USA Audience")
    st.write("📱 Platform: YouTube Shorts")
    st.write("🤖 AI: Gemini")

# ---------------- AI FUNCTION ----------------

def ask_gemini(prompt):

    if not api_key.strip():
        return "ERROR: Please enter your Gemini API Key."

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key.strip()
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 8192
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = error_data.get(
                    "error", {}
                ).get("message", response.text)
            except ValueError:
                error_message = response.text

            return (
                f"ERROR: API Error {response.status_code}: "
                f"{error_message}"
            )

        data = response.json()

        candidates = data.get("candidates", [])

        if not candidates:
            return "ERROR: Gemini returned no response."

        parts = candidates[0].get(
            "content", {}
        ).get("parts", [])

        result = "\n".join(
            part.get("text", "")
            for part in parts
            if part.get("text")
        )

        if not result.strip():
            return "ERROR: Empty AI response."

        return result

    except requests.exceptions.Timeout:
        return "ERROR: Request timed out. Try again."

    except requests.exceptions.RequestException as e:
        return f"ERROR: Network/API request failed: {e}"

    except Exception as e:
        return f"ERROR: {str(e)}"


# ---------------- RESULT DISPLAY ----------------

def display_result(result, filename):

    if result.startswith("ERROR:"):
        st.error(result)
    else:
        st.success("Content generated successfully!")

        st.markdown(result)

        st.download_button(
            label="📥 Download TXT File",
            data=result,
            file_name=filename,
            mime="text/plain"
        )


# ---------------- MAIN TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎬 Script Generator",
    "🐱 AI Animals",
    "👻 Horror Stories",
    "🔥 Viral Ideas",
    "🔍 SEO & Titles"
])


# ==================================================
# TAB 1: SCRIPT GENERATOR
# ==================================================

with tab1:

    st.header("🎬 YouTube Script Generator")

    topic = st.text_input(
        "Enter Video Topic",
        placeholder="Example: A magical suit makes a man a genius"
    )

    duration = st.selectbox(
        "Video Duration",
        ["30 Seconds", "45 Seconds", "60 Seconds",
         "3 Minutes", "5 Minutes", "10 Minutes"]
    )

    language = st.selectbox(
        "Language",
        ["Natural American English", "Simple English", "Hindi"]
    )

    if st.button("🚀 Generate Script", key="script"):

        if not topic.strip():
            st.warning("Please enter a topic.")

        else:

            prompt = f"""
You are a professional USA YouTube storyteller.

Create an original and engaging YouTube script.

TOPIC: {topic}
DURATION: {duration}
LANGUAGE: {language}

Include:

1. Powerful opening hook.
2. Interesting storytelling.
3. Emotional and funny moments where suitable.
4. Curiosity and suspense.
5. Scene-by-scene narration.
6. Strong ending.
7. Call to action.

Make it engaging for American viewers.
Use natural American English when English is selected.
Avoid copying existing stories or copyrighted dialogue.
"""

            with st.spinner("Creating your script..."):
                result = ask_gemini(prompt)

            display_result(result, "youtube_script.txt")


# ==================================================
# TAB 2: AI ANIMALS
# ==================================================

with tab2:

    st.header("🐱 AI Animals Story Generator")

    animal_type = st.selectbox(
        "Choose Animals",
        [
            "Funny Cats",
            "Cute Puppies",
            "Dogs and Cats",
            "Wild Animals",
            "Baby Animals",
            "Custom Animals"
        ]
    )

    animal_topic = st.text_input(
        "Story Idea",
        placeholder="Example: Two cats go fishing"
    )

    animal_duration = st.selectbox(
        "Story Duration",
        ["30 Seconds", "45 Seconds", "60 Seconds"]
    )

    if st.button("🐾 Create Animal Story", key="animals"):

        if not animal_topic.strip():
            st.warning("Enter an animal story idea.")

        else:

            prompt = f"""
You are an expert funny AI animal story creator
for a USA YouTube Shorts channel.

Animals: {animal_type}
Story idea: {animal_topic}
Duration: {animal_duration}

Create an original funny story.

Include:

1. A strong first-second hook.
2. Funny animal reactions.
3. Clear visual actions.
4. Scene-by-scene descriptions.
5. Funny expressions and surprises.
6. An entertaining ending.

Write in natural American English.

Also provide separate AI video prompts for every scene.
Keep animal appearances consistent across scenes.
"""

            with st.spinner("Creating animal story..."):
                result = ask_gemini(prompt)

            display_result(result, "ai_animals_story.txt")


# ==================================================
# TAB 3: HORROR STORIES
# ==================================================

with tab3:

    st.header("👻 USA Horror Story Generator")

    horror_topic = st.text_input(
        "Horror Story Idea",
        placeholder="Example: A strange knocking at 3 AM"
    )

    horror_type = st.selectbox(
        "Horror Style",
        [
            "Psychological Horror",
            "Paranormal Horror",
            "Haunted House",
            "Mystery Horror",
            "Scary Creature",
            "Twist Ending Horror"
        ]
    )

    if st.button("👻 Generate Horror Story", key="horror"):

        if not horror_topic.strip():
            st.warning("Enter a horror topic.")

        else:

            prompt = f"""
You are a professional American horror storyteller.

Create an original horror story.

Topic: {horror_topic}
Style: {horror_type}

Include:

1. Terrifying opening hook.
2. Suspenseful atmosphere.
3. Unexpected events.
4. Strong storytelling.
5. Scary climax.
6. Surprising ending.
7. Scene-by-scene AI video prompts.
8. Sound effect suggestions.

Write in natural American English.
Make it suitable for YouTube Shorts.
Avoid copying existing horror stories.
"""

            with st.spinner("Creating scary story..."):
                result = ask_gemini(prompt)

            display_result(result, "horror_story.txt")


# ==================================================
# TAB 4: VIRAL IDEAS
# ==================================================

with tab4:

    st.header("🔥 YouTube Viral Shorts Ideas")

    niche = st.text_input(
        "Enter Your Channel Niche",
        placeholder="Example: Funny Animals"
    )

    if st.button("🔥 Generate 10 Ideas", key="ideas"):

        if not niche.strip():
            st.warning("Enter your channel niche.")

        else:

            prompt = f"""
You are a YouTube Shorts content strategist.

Generate exactly 10 original video ideas.

Channel niche: {niche}
Target audience: USA

For each idea provide:

1. Catchy title.
2. First 2-second hook.
3. Short video concept.
4. Scene outline.
5. Funny or surprising ending.
6. Comment engagement question.

Use natural American English.
Make all 10 ideas different.
Do not promise viral results.
"""

            with st.spinner("Generating ideas..."):
                result = ask_gemini(prompt)

            display_result(result, "viral_shorts_ideas.txt")


# ==================================================
# TAB 5: SEO AND TITLES
# ==================================================

with tab5:

    st.header("🔍 YouTube SEO & Title Generator")

    seo_topic = st.text_input(
        "Enter Video Topic",
        placeholder="Example: Scary night in a haunted house"
    )

    if st.button("🔍 Generate SEO", key="seo"):

        if not seo_topic.strip():
            st.warning("Enter a video topic.")

        else:

            prompt = f"""
You are a professional YouTube SEO expert.

Video topic: {seo_topic}
Target audience: USA

Generate:

1. 10 attractive YouTube titles.
2. SEO-friendly description.
3. 20 relevant keywords.
4. 15 relevant hashtags.
5. Thumbnail text ideas.
6. Three thumbnail visual prompts.

Use natural American English.
Keep titles accurate and not misleading.
"""

            with st.spinner("Generating SEO..."):
                result = ask_gemini(prompt)

            display_result(result, "youtube_seo.txt")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Viral YouTube Creator Tool | Powered by Gemini AI"
)

st.caption(
    "This app generates text and AI video prompts. "
    "It does not directly create MP4 video files."
)

st.caption(
    "Generated content should be reviewed before publishing."
)
