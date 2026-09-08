import streamlit as st
import markdown as md
from PIL import Image
from gemini_service import analyze_health_document_openai

st.set_page_config(
    page_title="MedScan Pro | AI Medical Document Analysis",
    page_icon="🏥",
    layout="wide"
)

# ==================== CUSTOM CSS ====================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background: #f0f4f8;
    }

    .hero {
        background: linear-gradient(135deg, #0a1628 0%, #1a3a6a 100%);
        padding: 3rem 4rem;
        border-radius: 16px;
        margin: 0 2rem 2rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px rgba(10, 22, 40, 0.25);
    }

    .hero-content h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }

    .hero-content h1 span {
        color: #60a5fa;
    }

    .hero-content p {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        max-width: 550px;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(37, 99, 235, 0.2);
        color: #60a5fa;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border: 1px solid rgba(37, 99, 235, 0.3);
    }

    .hero-stats {
        display: flex;
        gap: 2.5rem;
        margin-top: 1.5rem;
    }

    .hero-stats .stat {
        text-align: center;
    }

    .hero-stats .stat .number {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .hero-stats .stat .label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .hero-icon {
        background: rgba(37, 99, 235, 0.15);
        padding: 1.5rem;
        border-radius: 50%;
        border: 2px solid rgba(37, 99, 235, 0.3);
        font-size: 4rem;
    }

    .main-container {
        padding: 0 2rem 2rem 2rem;
    }

    .upload-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }

    .upload-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border-color: #93c5fd;
    }

    .upload-card h3 {
        color: #0a1628;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .upload-card p {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .upload-card .supported-formats {
        display: inline-block;
        background: #f1f5f9;
        color: #475569;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .upload-card .file-limits {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }

    [data-testid="stFileUploader"] label {
        display: none !important;
    }

    [data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"] {
        display: none !important;
    }

    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        background: #fafbfc;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #2563eb;
        background: #f1f5f9;
    }

    [data-testid="stFileUploader"] .stAlert {
        display: none !important;
    }

    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        border-left: 6px solid #2563eb;
        margin-top: 1.5rem;
    }

    .result-card .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
    }

    .result-card .result-header h3 {
        color: #0a1628;
        font-weight: 700;
        font-size: 1.3rem;
    }

    .result-card .result-header .badge {
        background: #dcfce7;
        color: #166534;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .result-content {
        color: #0a1628 !important;
        font-size: 1rem;
        line-height: 1.8;
    }

    .result-content p,
    .result-content li,
    .result-content div,
    .result-content span {
        color: #0a1628 !important;
    }

    .result-content strong {
        color: #1e293b !important;
    }

    .result-content h1,
    .result-content h2,
    .result-content h3 {
        color: #2563eb !important;
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .result-content ul,
    .result-content ol {
        padding-left: 1.4rem;
        margin-bottom: 0.8rem;
    }

    .result-content li {
        margin-bottom: 0.4rem;
    }

    .result-content hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 1.2rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }

    .footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }

    .footer a {
        color: #2563eb;
        text-decoration: none;
    }

    @media (max-width: 768px) {
        .hero {
            flex-direction: column;
            text-align: center;
            padding: 2rem;
        }
        .hero-content p {
            max-width: 100%;
        }
        .hero-stats {
            justify-content: center;
        }
        .main-container {
            padding: 0 1rem 1rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== HERO SECTION ====================
st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">⚡ AI-POWERED ANALYSIS</div>
            <h1>Medical Document <br><span>Intelligence</span> Simplified</h1>
            <p>Upload a photo of your medicine or lab report and get a clear, structured clinical breakdown in plain language — instantly.</p>
            <div class="hero-stats">
                <div class="stat">
                    <div class="number">AI</div>
                    <div class="label">Vision Powered</div>
                </div>
                <div class="stat">
                    <div class="number">7</div>
                    <div class="label">Key Sections</div>
                </div>
                <div class="stat">
                    <div class="number">Free</div>
                    <div class="label">To Use</div>
                </div>
            </div>
        </div>
        <div class="hero-icon">🧬</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================== MAIN CONTENT ====================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Upload Section ---
st.markdown(
    """
    <div class="upload-card">
        <h3>📤 Upload Document</h3>
        <p>Upload a photo of your medicine label, prescription box, or lab report for AI-powered analysis.</p>
        <div class="supported-formats">📷 Supported: JPG, JPEG, PNG</div>
        <div class="file-limits">📄 Max 200MB per file</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===== UPLOAD OR CAMERA =====
tab1, tab2 = st.tabs(["📁 Upload File", "📷 Use Camera"])

uploaded_file = None
camera_file = None

with tab1:
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    st.markdown(
        """
        <div style="text-align: center; margin-top: -10px; padding-bottom: 10px;">
            <span style="color: #0a1628; font-weight: 500;">📁 Drag & drop your file here</span>
            <br>
            <span style="color: #94a3b8; font-size: 0.8rem;">or click to browse files</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab2:
    camera_file = st.camera_input("Take a photo of the medicine or lab report", label_visibility="collapsed")

image_source = uploaded_file if uploaded_file is not None else camera_file

if image_source is not None:
    image = Image.open(image_source)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="📸 Document Preview", use_container_width=True)

    if st.button("🔍 Analyze Document", use_container_width=True):
        with st.spinner("🧠 AI is analyzing your document..."):
            try:
                result = analyze_health_document_openai(image)
                result_html = md.markdown(result, extensions=["extra", "sane_lists"])

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-header">
                            <h3>📋 Analysis Report</h3>
                            <span class="badge">✓ Complete</span>
                        </div>
                        <div class="result-content">
                            {result_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"⚠️ Analysis failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown(
    """
    <div class="footer">
        <p>
            ⚕️ <strong>MedScan Pro</strong> — AI-powered medical document analysis for healthcare professionals and patients.
            <br>
            <span style="font-size:0.75rem; color:#94a3b8;">
                This is not a diagnosis. Always consult your healthcare provider for medical decisions.
            </span>
            <br><br>
            © 2026 MedScan Pro
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
