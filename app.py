import streamlit as st
from PIL import Image
from gemini_service import analyze_health_document_openai

st.set_page_config(page_title="MedScan AI", page_icon="💊", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Outfit:wght@500;700&display=swap');

    body {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background-color: #e8f0fe;
    }

    .header-card {
        background: #2563eb;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
        border: 1px solid #1d4ed8;
        margin-bottom: 2rem;
    }

    .header-card h1 {
        font-family: 'Outfit', sans-serif !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem;
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        -webkit-text-fill-color: #ffffff !important;
    }

    .title-divider {
        height: 3px;
        width: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
        margin: 1rem auto 1.5rem auto;
        border-radius: 2px;
    }

    .header-card p {
        color: #dbeafe !important;
        font-size: 1.1rem;
    }

    [data-testid="stFileUploader"] label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }

    .result-container {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        border: 1px solid #cbd5e1;
        border-left: 8px solid #2563eb;
        margin-top: 1.5rem;
    }

    /* Forces all text, paragraphs, lists, and general output to solid black */
    .result-container, .result-container p, .result-container li, .result-container span, .result-container div {
        color: #000000 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .result-container h3, .result-container h2, .result-container h1 {
        font-family: 'Outfit', sans-serif !important;
        color: #1d4ed8 !important;
        font-weight: 600;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header-card">
        <h1>AI Health Document & Medication Simplifier</h1>
        <div class="title-divider"></div>
        <p>Upload a photo of your medicine or lab report to get a clear, structured clinical breakdown.</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose an image (Medicine or Lab Report)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document Preview", use_container_width=True)

    if st.button("Analyze Document"):
        with st.spinner("Analyzing with Qwen Vision..."):
            try:
                result = analyze_health_document_openai(image)
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.subheader("📋 Comprehensive Analysis Result:")
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")