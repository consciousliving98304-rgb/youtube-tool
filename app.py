
import streamlit as st
import requests
import json
import time

st.set_page_config(
    page_title="Viral YouTube Retention Engine",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Viral YouTube Retention Engine")
st.caption("Create engaging YouTube scripts, titles, SEO and visual prompts.")

# Gemini API settings
API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-2.5-flash:generateContent"
)

# Read API key from Streamlit Secrets
try:
    SECRET_KEY = st.secrets.get("KEY1", "")
except Exception:
    SECRET_KEY = ""

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input(
        "Gemini API Key",
        value=SECRET_KEY,
        type="password",
        help="Your key is used only for API requests."
    )
    st.caption("Keep your API key private.")

def ask_gemini(prompt):
    """Send one request to Gemini and return its text."""
    if not api_key.strip():
        return "ERROR: Please enter your Gemini API key in the sidebar."

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
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
            headers={
                **headers,
                "x-goog-api-key": api_key.strip()
            },
            json=payload,
            timeout=120
        )

        if response.status_code == 429:
            return (
                "ERROR: Gemini API quota or rate limit reached. "
                "Check your API quota and billing, then try again later."
            )

        if response.status_code == 400:
            return (
                "ERROR: Invalid request or API key. "
                "Check the key and Gemini API access. Details: "
                + response.text[:800]
            )

        if response.status_code in (401, 403):
            return (
                "ERROR: API access denied. Check your API key, "
                "permissions and project settings."
            )

        response.raise_for_status()
        data = response.json()

        candidates = data.get("candidates", [])
        if not candidates:
            return "ERROR: Gemini returned no answer. Please try again."

        parts = candidates[0].get("content", {}).get("parts", [])
        answer = "\n".join(
            part["text"] for part in parts if "text" in part
        ).strip()

        return answer or "ERROR: Gemini returned an empty response."

    except requests.exceptions.Timeout:
        return "ERROR: Request timed out. Please try again."
    except requests.exceptions.RequestException as error:
        return f"ERROR: Network/API request failed: {error}"
    except (ValueError, KeyError, TypeError) as error:
        return f"ERROR: Could not read the API response: {error}"


def show_result(result):
    if result.startswith("ERROR:"):
        st.error(result.replace("ERROR: ", "", 1))
    else:
        st.markdown(result)
        st.download_button(
            "📥 Download result as TXT",
            data=result,
            file_name="youtube_creator_result.txt",
            mime="text/plain"
        )


tab1, tab2 = st.tabs([
    "🎬 Viral Script & Visual Pack",
    "🔥 5 Retention Shorts Ideas"
])

with tab1:
    st.subheader("Create a YouTube video package")

    topic = st.text_input(
        "Video topic",
        placeholder="Example: A magical suit that creates a stock market genius"
    )

    audience = st.selectbox(
        "Target audience",
        ["USA audience", "Global English audience", "Hindi audience"]
    )

    video_type = st.selectbox(
        "Video type",
        ["YouTube Shorts", "Long-form YouTube video", "Horror story",
         "Funny animal story", "Motivational story", "Spirituality"]
    )

    duration = st.selectbox(
        "Video duration",
        ["30 seconds", "45 seconds", "60 seconds", "3 minutes",
         "5 minutes", "10 minutes"]
    )

    language = st.selectbox(
        "Script language",
        ["Natural American English", "Simple English", "Hindi"]
    )

    if st.button("🚀 Generate Viral Video Pack", type="primary"):
        if not topic.strip():
            st.warning("Please enter a video topic first.")
        elif not api_key.strip():
            st.error("Enter your Gemini API key in the sidebar.")
        else:
            prompt = f"""
You are an expert YouTube scriptwriter and audience-retention strategist.

Create a complete YouTube content package.

Topic: {topic}
Target audience: {audience}
Video type: {video_type}
Duration: {duration}
Language: {language}

Include:
1. Three clickable, honest title options.
2. One strong opening hook for the first 1-3 seconds.
3. A complete, engaging script suited to the requested duration.
4. Retention techniques, curiosity gaps and pattern interrupts.
5. Suggested on-screen captions and sound effects.
6. Scene-by-scene visual prompts for AI image/video tools.
7. Thumbnail concept and thumbnail text.
8. SEO description and relevant keywords.
9. Relevant hashtags.
10. A short call to action.

Use original ideas. Avoid fake claims, misleading titles,
copyrighted dialogue, and copying existing creators.
Make the content suitable for the specified audience.
"""
            with st.spinner("Creating your video package..."):
                result = ask_gemini(prompt)
            show_result(result)

with tab2:
    st.subheader("Generate 5 engaging Shorts ideas")

    idea_topic = st.text_input(
        "Niche or topic for Shorts",
        placeholder="Example: Horror stories, funny puppies, life lessons",
        key="idea_topic"
    )

    idea_audience = st.selectbox(
        "Shorts audience",
        ["USA audience", "Global audience", "Hindi audience"],
        key="idea_audience"
    )

    if st.button("🔥 Generate 5 Shorts Ideas", type="primary"):
        if not idea_topic.strip():
            st.warning("Please enter a niche or topic first.")
        elif not api_key.strip():
            st.error("Enter your Gemini API key in the sidebar.")
        else:
            prompt = f"""
You are a YouTube Shorts strategist.

Generate exactly 5 original Shorts ideas.
Niche: {idea_topic}
Audience: {idea_audience}

For each idea provide:
- A catchy title
- A 1-3 second hook
- A short story or video concept
- A simple scene-by-scene outline
- An ending that encourages comments or rewatching
- Three relevant hashtags

Make each idea distinct, engaging and suitable for short-form video.
Do not promise virality or copy existing videos.
"""
            with st.spinner("Finding five creative ideas..."):
                result = ask_gemini(prompt)
            show_result(result)

st.divider()
st.caption(
    "Note: This app generates text and visual prompts. "
    "It does not render or export actual video files."
)
  
