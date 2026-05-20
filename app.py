import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="✨",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff7ed 0%, #fdf2f8 45%, #eef2ff 100%);
    color: #1f2937;
}

.main-card {
    background: rgba(255, 255, 255, 0.82);
    padding: 35px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 25px 70px rgba(124,58,237,0.18);
}

.title {
    text-align: center;
    font-size: 54px;
    font-weight: 900;
    background: linear-gradient(90deg, #ec4899, #8b5cf6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 19px;
    color: #475569;
    margin-bottom: 35px;
}

.feature-box {
    background: linear-gradient(135deg, #fce7f3, #ede9fe);
    padding: 18px;
    border-radius: 20px;
    border-left: 6px solid #ec4899;
    color: #334155;
}

.result-box {
    background: linear-gradient(135deg, #ffffff, #f0f9ff);
    padding: 25px;
    border-radius: 22px;
    border: 1px solid #bae6fd;
    color: #0f172a;
    font-size: 22px;
    line-height: 1.8;
    min-height: 120px;
    box-shadow: 0 12px 35px rgba(14,165,233,0.15);
}

.small-card {
    background: linear-gradient(135deg, #ffffff, #fdf2f8);
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #fbcfe8;
    color: #334155;
    box-shadow: 0 8px 25px rgba(236,72,153,0.10);
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 14px;
    margin-top: 35px;
}

div.stButton > button {
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 13px 22px;
    font-weight: 800;
    font-size: 17px;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #db2777, #7c3aed);
    color: white;
    transform: scale(1.01);
}

textarea {
    border-radius: 20px !important;
    background: #ffffff !important;
    color: #111827 !important;
}

.stSelectbox label, .stTextArea label {
    color: #334155 !important;
    font-weight: 700 !important;
}

h1, h2, h3, p, label {
    color: #1f2937 !important;
}
</style>
""", unsafe_allow_html=True)

languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Turkish": "tr",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Urdu": "ur",
    "Romanian": "ro",
    "Dutch": "nl",
    "Greek": "el"
}

tts_supported = {
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Turkish": "tr",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Hindi": "hi",
    "Urdu": "ur",
    "Dutch": "nl",
    "Greek": "el"
}

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown('<div class="title">✨ Smart Language Translator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A clean AI translation app with speech, download, and translation history</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

left_col, right_col = st.columns([1.15, 0.85])

with left_col:
    st.subheader("📝 Write Your Text")

    input_text = st.text_area(
        "Enter text to translate:",
        height=260,
        placeholder="Type or paste your text here..."
    )

    words = len(input_text.split())
    characters = len(input_text)

    stat1, stat2 = st.columns(2)

    with stat1:
        st.markdown(f'<div class="small-card">Words<br><b>{words}</b></div>', unsafe_allow_html=True)

    with stat2:
        st.markdown(f'<div class="small-card">Characters<br><b>{characters}</b></div>', unsafe_allow_html=True)

with right_col:
    st.subheader("🌍 Translation Options")

    source_language = st.selectbox(
        "Source Language",
        list(languages.keys()),
        index=0
    )

    target_language = st.selectbox(
        "Target Language",
        list(languages.keys())[1:],
        index=1
    )

    st.markdown("""
    <div class="feature-box">
    Choose source and target languages. Use <b>Auto Detect</b> if you do not know the original language.
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    translate_btn = st.button("🚀 Translate Text", use_container_width=True)
    clear_btn = st.button("🧹 Clear All", use_container_width=True)

if clear_btn:
    st.session_state.translated_text = ""
    st.session_state.history = []
    st.rerun()

if translate_btn:
    if input_text.strip() == "":
        st.warning("⚠️ Please enter text before translating.")
    elif source_language == target_language:
        st.warning("⚠️ Source and target languages cannot be the same.")
    else:
        try:
            translated = GoogleTranslator(
                source=languages[source_language],
                target=languages[target_language]
            ).translate(input_text)

            st.session_state.translated_text = translated

            st.session_state.history.append({
                "source": source_language,
                "target": target_language,
                "input": input_text,
                "output": translated
            })

            st.success("✅ Translation completed successfully!")

        except Exception as error:
            st.error("❌ Translation failed. Please check your internet connection.")
            st.write(error)

if st.session_state.translated_text:
    st.markdown("---")
    st.subheader("✅ Translation Result")

    st.markdown(
        f'<div class="result-box">{st.session_state.translated_text}</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            label="⬇️ Download Translation",
            data=st.session_state.translated_text,
            file_name="translated_text.txt",
            mime="text/plain",
            use_container_width=True
        )

    with c2:
        st.code(st.session_state.translated_text, language=None)

    st.subheader("🔊 Listen to Translation")

    if target_language in tts_supported:
        try:
            tts = gTTS(
                text=st.session_state.translated_text,
                lang=tts_supported[target_language]
            )

            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)

            with open(temp_audio.name, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
            os.remove(temp_audio.name)

        except Exception:
            st.warning("⚠️ Audio is not available right now.")
    else:
        st.warning("⚠️ Text-to-Speech is not supported for this selected language.")

if len(st.session_state.history) > 0:
    st.markdown("---")
    st.subheader("🕘 Translation History")

    for i, item in enumerate(reversed(st.session_state.history[-5:]), start=1):
        with st.expander(f"Translation {i}: {item['source']} ➜ {item['target']}"):
            st.write("Original Text:")
            st.info(item["input"])

            st.write("Translated Text:")
            st.success(item["output"])

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="footer">Developed for CodeAlpha Artificial Intelligence Internship | Smart Language Translator</div>',
    unsafe_allow_html=True
)