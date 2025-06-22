# app.py - ENHANCED VISUAL VERSION WITH MOBILE OPTIMIZATION
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re
import time
import base64
from io import BytesIO
import json

from toolkit_logic import SDGAssessmentToolkit

@st.cache_resource
def get_toolkit():
    """This function creates a single instance of the toolkit."""
    return SDGAssessmentToolkit()

toolkit = get_toolkit()

# --- Constants ---
UIA_RED = "#E63946"
UIA_BLUE = "#1D3557"
UIA_LIGHT_BLUE = "#457B9D"
UIA_ACCENT = "#F1FAEE"
SECTIONS = list(toolkit.sdg_questions.keys())
TOTAL_SECTIONS = len(SECTIONS)

# Enhanced color palette for better visualizations
CHART_COLORS = {
    'primary': UIA_RED,
    'secondary': UIA_BLUE,
    'accent': UIA_LIGHT_BLUE,
    'success': '#10B981',
    'warning': '#F59E0B',
    'info': '#3B82F6',
    'light': '#F8FAFC',
    'gradient_start': UIA_RED,
    'gradient_end': UIA_BLUE
}

# --- Page Configuration and Enhanced CSS ---
st.set_page_config(
    page_title="UIA SDG Assessment Toolkit", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.uia-architectes.org',
        'Report a bug': None,
        'About': "UIA SDG Assessment Toolkit - Architecture for Sustainability"
    }
)

# ADD THIS LINE: Meta tag to signal color scheme preference
st.markdown("<meta name='color-scheme' content='light'>", unsafe_allow_html=True)

# MOBILE-ACCESSIBLE STREAMLIT CSS - BLACK TEXT FIX
# Updated CSS with maximum text visibility and accessibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --uia-red: #E63946;
        --uia-blue: #1D3557;
        --uia-light-blue: #457B9D;
        --uia-accent: #F1FAEE;
        --background: #F8FAFC;
        --surface: #ffffff;
        --surface-hover: #f1f5f9;
        --border: #e2e8f0;
        --text-primary: #000000;
        --text-secondary: #000000;
        --text-muted: #374151;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --radius: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;

        /* FORCED LIGHT THEME VARIABLES */
        --forced-bg: #ffffff;
        --forced-text: #000000;
        --forced-card-bg: #ffffff;
        --forced-card-border: #e0e0e0;
        --forced-button-bg: #f0f0f0;
        --forced-button-text: #000000;
        --forced-button-border: #000000;

        /* Special elements to keep dark with white text (UIA Branding) */
        --special-dark-bg: linear-gradient(135deg, var(--uia-red) 0%, var(--uia-blue) 100%);
        --special-dark-text: #ffffff;
        
        /* Variables for text shades if you don't want pure black everywhere */
        --text-primary-forced: #000000;
        --text-secondary-forced: #333333;
        --text-muted-forced: #555555;
    }

    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton { visibility: hidden !important; }
    
    /* GENERAL OVERRIDES FOR LIGHT THEME */
    body, .stApp {
        background-color: var(--forced-bg) !important;
        color: var(--forced-text) !important;
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        background-color: var(--forced-bg) !important;
        color: var(--forced-text) !important;
        padding: 1rem 1rem 6rem 1rem;
        max-width: 1200px;
    }
    
    /* Mobile-first responsive design */
    @media (min-width: 768px) {
        .block-container {
            padding: 1rem 2rem 5rem 2rem;
        }
    }

    /* Force all common text-hosting elements to black text */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li, text,
    .stMarkdown, .stMarkdown *,
    .question-title, .intro-container *, .progress-container *,
    .section-title-wrapper *,
    .stAlert *, .stMetric *, .stTabs * {
        color: var(--forced-text) !important;
        background-color: transparent !important;
    }

    /* Ensure links are also black, or a very dark noticeable color */
    a, a:visited {
        color: #0000EE !important;
        text-decoration: underline !important;
    }

    /* LIGHT THEME FOR MOST COMPONENTS */
    .intro-container, .progress-container, .question-card,
    .stCheckbox > div > div > label, .stRadio > div > label,
    .stTabs [data-baseweb="tab-list"], .stTabs [data-baseweb="tab"],
    .stMetric, .chart-container, .stAlert,
    .mobile-nav, .mobile-nav .page-counter,
    .streamlit-expanderHeader, .streamlit-expanderContent {
        background-color: var(--forced-card-bg) !important;
        color: var(--forced-text) !important;
        border: 1px solid var(--forced-card-border) !important;
    }

    /* Ensure text *inside* these components is also black */
    .intro-container *, .progress-container *, .question-card *,
    .stCheckbox > div > div > label *, .stRadio > div > label *,
    .stTabs [data-baseweb="tab-list"] *, .stTabs [data-baseweb="tab"] *,
    .stMetric *, .stAlert *,
    .mobile-nav *, .mobile-nav .page-counter *,
    .streamlit-expanderHeader *, .streamlit-expanderContent * {
        color: var(--forced-text) !important;
    }

    /* Enhanced Button Styling - SIMPLIFIED FOR VISIBILITY */
    .stButton > button,
    .mobile-next-button-container .stButton > button,
    .desktop-submit-button-container .stButton > button {
        background-color: var(--forced-button-bg) !important;
        color: var(--forced-button-text) !important;
        border: 2px solid var(--forced-button-border) !important;
        border-radius: var(--radius);
        font-weight: 700 !important;
        box-shadow: var(--shadow);
        transition: all 0.2s ease;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: none !important;
    }
    
    .stButton > button:hover {
        background-color: #e0e0e0 !important;
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: #374151 !important;
    }

    /* Text inside buttons */
    .stButton > button *,
    .mobile-next-button-container .stButton > button *,
    .desktop-submit-button-container .stButton > button * {
        color: var(--forced-button-text) !important;
    }

    /* Mobile-specific button enhancements */
    @media (max-width: 768px) {
        .stButton > button {
            font-size: 1.1rem !important;
            padding: 1rem 1.5rem !important;
            min-height: 56px !important;
            font-weight: 700 !important;
            border: 3px solid var(--forced-button-border) !important;
        }
    }

    /* Enhanced intro page styling - LIGHT BACKGROUND */
    .intro-container {
        background: var(--forced-card-bg) !important;
        border-radius: var(--radius-lg) !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: var(--shadow-lg) !important;
        border: 2px solid var(--forced-card-border) !important;
    }

    .intro-container h2 {
        color: var(--forced-text) !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.5rem !important;
    }

    .intro-container p {
        color: var(--forced-text) !important;
        line-height: 1.6 !important;
        margin-bottom: 1rem !important;
        font-size: 1rem !important;
    }

    /* RADIO AND CHECKBOX OPTIONS - LIGHT BACKGROUNDS */
    .stCheckbox > div > div > label {
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
        padding: 1rem !important;
        background: var(--forced-card-bg) !important;
        border: 2px solid var(--forced-card-border) !important;
        border-radius: var(--radius) !important;
        transition: all 0.2s ease-in-out;
        box-sizing: border-box !important;
        margin-bottom: 0.75rem !important;
        font-size: 0.9rem !important;
        color: var(--forced-text) !important;
    }

    .stRadio > div > label {
        display: flex !important;
        align-items: flex-start !important;
        padding: 1rem !important;
        background: var(--forced-card-bg) !important;
        border: 2px solid var(--forced-card-border) !important;
        border-radius: var(--radius) !important;
        margin-bottom: 0.75rem !important;
        transition: all 0.2s ease-in-out;
        width: 100% !important;
        box-sizing: border-box !important;
        font-size: 0.9rem !important;
        color: var(--forced-text) !important;
    }

    /* Force text in radio/checkbox options to be black */
    .stRadio > div > label *,
    .stCheckbox > div > div > label * {
        color: var(--forced-text) !important;
        font-weight: 500 !important;
    }

    /* Hover effects - light backgrounds */
    .stRadio > div > label:hover, 
    .stCheckbox > div > div > label:hover {
        background: #f9fafb !important;
        border-color: #6b7280 !important;
        box-shadow: var(--shadow);
    }

    /* Selected states - light backgrounds */
    .stRadio > div > label:has(input:checked),
    .stCheckbox > div > div > label:has(input:checked) {
        background: #f0f9ff !important;
        border-color: #3b82f6 !important;
        box-shadow: var(--shadow) !important;
    }

    /* SPECIAL ELEMENTS TO KEEP DARK WITH WHITE TEXT (UIA Branding) */
    .uia-header {
        background: var(--special-dark-bg) !important;
        color: var(--special-dark-text) !important;
        padding: 2rem 1.5rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-xl);
        border: 3px solid #e5e7eb !important;
    }
    
    .uia-header h1 {
        color: var(--special-dark-text) !important;
        font-size: 2rem;
        font-weight: 900;
        margin: 0 !important;
    }
    
    .uia-header p {
        color: var(--special-dark-text) !important;
        margin: 0.5rem 0 0 0 !important;
    }

    /* Mobile header optimization */
    @media (max-width: 768px) {
        .uia-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1.5rem;
        }
        .uia-header h1 {
            font-size: 1.5rem !important;
        }
    }

    /* Enhanced Progress Container - LIGHT BACKGROUND */
    .progress-container {
        background: var(--forced-card-bg) !important;
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow);
        margin-bottom: 2rem;
        border: 2px solid var(--forced-card-border) !important;
    }

    /* Enhanced Question Cards - LIGHT BACKGROUNDS */
    .question-card {
        background: var(--forced-card-bg) !important;
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid var(--forced-card-border) !important;
        box-shadow: var(--shadow);
        transition: all 0.2s ease-in-out;
    }
    
    .question-card:hover {
        border-color: #9ca3af !important;
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
        background: #f9fafb !important;
    }

    .question-title {
        font-weight: 600 !important;
        color: var(--forced-text) !important;
        font-size: 1.1rem;
        margin-bottom: 1.25rem;
        line-height: 1.5;
    }

    /* Mobile question card optimization */
    @media (max-width: 768px) {
        .question-card {
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        }
        
        .question-title {
            font-size: 1rem;
            margin-bottom: 1rem;
            line-height: 1.4;
        }
    }

    /* Mobile Navigation - LIGHT THEME */
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--forced-card-bg) !important;
        padding: 12px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
        z-index: 1000;
        border-top: 3px solid var(--forced-card-border) !important;
    }
    
    .nav-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 10px;
        align-items: center;
    }
    
    .mobile-nav button {
        background: var(--forced-card-bg) !important;
        border: 2px solid var(--forced-card-border) !important;
        border-radius: 10px;
        padding: 12px 8px;
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--forced-text) !important;
        transition: all 0.3s ease;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .mobile-nav button:hover {
        background: #f9fafb !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: #6b7280 !important;
    }
    
    .mobile-nav button:disabled {
        background: #f3f4f6 !important;
        color: #9ca3af !important;
        cursor: not-allowed;
        transform: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-color: #e5e7eb !important;
    }
    
    /* Style the page counter */
    .mobile-nav .page-counter {
        text-align: center;
        color: var(--forced-text) !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 8px;
        background: #f3f4f6 !important;
        border-radius: 8px;
        border: 2px solid var(--forced-card-border) !important;
    }

    /* Force mobile navigation button text to be black */
    .mobile-nav .stButton > button,
    .mobile-nav .stButton > button *,
    .mobile-nav .stButton > button span,
    .mobile-nav .stButton > button div {
        background: var(--forced-card-bg) !important;
        color: var(--forced-text) !important;
        font-weight: 700 !important;
        border: 2px solid var(--forced-card-border) !important;
    }

    /* Better spacing for mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-bottom: 8rem !important;
        }
    }

    /* Tab styling enhancements - LIGHT THEME */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--forced-card-bg) !important;
        padding: 0.5rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        margin-bottom: 1.5rem;
        border: 2px solid var(--forced-card-border) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid var(--forced-card-border) !important;
        background: var(--forced-card-bg) !important;
        color: var(--forced-text) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #f3f4f6 !important;
        color: var(--forced-text) !important;
        border-color: #6b7280 !important;
        box-shadow: var(--shadow);
    }

    /* Enhanced metrics and info boxes - LIGHT BACKGROUNDS */
    .stMetric {
        background: var(--forced-card-bg) !important;
        padding: 1rem;
        border-radius: var(--radius);
        border: 2px solid var(--forced-card-border) !important;
        box-shadow: var(--shadow);
    }

    /* Force metric text to be black */
    .stMetric *,
    .stMetric > div > div > label,
    .stMetric div[data-testid="stMetricValue"],
    .stMetric div[data-testid="stMetricLabel"] {
        color: var(--forced-text) !important;
    }

    /* Chart container enhancements - LIGHT BACKGROUND */
    .chart-container {
        background: var(--forced-card-bg) !important;
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid var(--forced-card-border) !important;
        box-shadow: var(--shadow);
    }

    /* Enhanced section headers */
    .section-header {
        color: var(--forced-text) !important;
        font-weight: 700 !important;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid var(--forced-text) !important;
        display: inline-block;
    }

    /* Section title wrapper - specific targeting for section titles */
    .section-title-wrapper {
        background: transparent !important;
        color: var(--forced-text) !important;
        margin-bottom: 2rem !important;
        padding: 1rem 0 !important;
    }

    .section-title-wrapper h2 {
        color: var(--forced-text) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.3 !important;
        background: transparent !important;
    }

    .section-title-wrapper * {
        color: var(--forced-text) !important;
        background: transparent !important;
    }

    /* Mobile optimization for section titles */
    @media (max-width: 768px) {
        .section-title-wrapper h2 {
            font-size: 1.5rem !important;
        }
    }

    /* Enhanced info, success, warning, error boxes - LIGHT BACKGROUNDS */
    .stAlert {
        border-radius: var(--radius) !important;
        border: 2px solid var(--forced-card-border) !important;
        box-shadow: var(--shadow) !important;
        background: var(--forced-card-bg) !important;
    }

    /* Force alert text to be black */
    .stAlert *,
    .stAlert p,
    .stAlert div,
    .stAlert ul, 
    .stAlert li {
        color: var(--forced-text) !important;
    }

    /* INPUTS (st.text_input, st.selectbox etc.) */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input,
    div[data-baseweb="input"] input {
        background-color: #ffffff !important;
        color: var(--forced-text) !important;
        border: 1px solid var(--forced-card-border) !important;
    }

    /* Focus states for inputs */
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus,
    .stNumberInput input:focus,
    div[data-baseweb="input"] input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    /* Slider styling */
    .stSlider > div > div > div > div {
        background: var(--forced-card-bg) !important;
    }

    /* Expander styling - LIGHT BACKGROUND */
    .streamlit-expanderHeader {
        background: var(--forced-card-bg) !important;
        border: 2px solid var(--forced-card-border) !important;
        color: var(--forced-text) !important;
    }

    .streamlit-expanderContent {
        background: var(--forced-card-bg) !important;
        border: 2px solid var(--forced-card-border) !important;
        border-top: none !important;
    }

    /* Custom scrollbar - LIGHT THEME */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f4f6;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #9ca3af;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #6b7280;
    }

    /* Print styles for PDF generation */
    @media print {
        .mobile-nav, .stButton { display: none !important; }
        .block-container { padding: 0 !important; }
        .question-card, .results-card { break-inside: avoid; }
        * { color: var(--forced-text) !important; background: var(--forced-bg) !important; }
    }

    /* High contrast mode support */
    @media (prefers-contrast: high) {
        * {
            color: var(--forced-text) !important;
            background: var(--forced-bg) !important;
        }
        
        .stButton > button {
            border: 3px solid var(--forced-text) !important;
            background: var(--forced-bg) !important;
            color: var(--forced-text) !important;
        }
    }

    /* OVERRIDE BROWSER DARK MODE ATTEMPTS */
    @media (prefers-color-scheme: dark) {
        body, .stApp {
            background-color: var(--forced-bg) !important;
            color: var(--forced-text) !important;
        }
        
        .block-container {
            background-color: var(--forced-bg) !important;
            color: var(--forced-text) !important;
        }

        /* Re-assert light theme for most components */
        h1,h2,h3,h4,h5,h6,p,span,div,label,li,text, .stMarkdown, .stMarkdown *, .question-title,
        .intro-container, .progress-container, .question-card,
        .stCheckbox > div > div > label, .stRadio > div > label,
        .stTabs [data-baseweb="tab-list"], .stTabs [data-baseweb="tab"],
        .stMetric, .chart-container, .stAlert,
        .mobile-nav, .mobile-nav .page-counter,
        .streamlit-expanderHeader, .streamlit-expanderContent,
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input,
        div[data-baseweb="input"] input {
            background-color: var(--forced-card-bg) !important;
            color: var(--forced-text) !important;
            border-color: var(--forced-card-border) !important;
        }
        
        /* Re-assert text within components */
        .intro-container *, .progress-container *, .question-card *,
        .stCheckbox > div > div > label *, .stRadio > div > label *,
        .stTabs [data-baseweb="tab-list"] *, .stTabs [data-baseweb="tab"] *,
        .stMetric *, .stAlert *,
        .mobile-nav *, .mobile-nav .page-counter *,
        .streamlit-expanderHeader *, .streamlit-expanderContent * {
            color: var(--forced-text) !important;
        }

        /* Re-assert button styles */
        .stButton > button,
        .mobile-next-button-container .stButton > button,
        .desktop-submit-button-container .stButton > button {
            background-color: var(--forced-button-bg) !important;
            color: var(--forced-button-text) !important;
            border: 2px solid var(--forced-button-border) !important;
        }
        
        .stButton > button *,
        .mobile-next-button-container .stButton > button *,
        .desktop-submit-button-container .stButton > button * {
            color: var(--forced-button-text) !important;
        }

        /* Re-assert SPECIAL DARK ELEMENTS */
        .uia-header {
            background: var(--special-dark-bg) !important;
            color: var(--special-dark-text) !important;
        }
        
        .uia-header h1, .uia-header p {
            color: var(--special-dark-text) !important;
        }

        /* Re-assert section title wrapper styles */
        .section-title-wrapper {
            background: transparent !important;
            color: var(--forced-text) !important;
        }

        .section-title-wrapper h2 {
            color: var(--forced-text) !important;
            background: transparent !important;
        }

        .section-title-wrapper * {
            color: var(--forced-text) !important;
            background: transparent !important;
        }
    }

    /* ADDITIONAL FORCE LIGHT THEME OVERRIDES */
    /* Extra certainty for critical elements */
    .stApp {
        background-color: white !important;
        color: black !important;
    }
    
    .stMarkdown, .stText, p, span, div {
        color: black !important;
    }
    
    /* Ensure form elements are visible */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: white !important;
        color: black !important;
    }
    
    .stRadio > div {
        background-color: white !important;
        color: black !important;
    }

    /* Additional input field overrides */
    .stTextArea > div > div > textarea {
        background-color: white !important;
        color: black !important;
    }

    .stNumberInput > div > div > input {
        background-color: white !important;
        color: black !important;
    }

    /* Force all Streamlit widgets to light theme */
    .stWidget > div {
        background-color: white !important;
        color: black !important;
    }

    /* Ensure all text elements are black */
    .stMarkdown *, .stText *, p *, span *, div * {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'current_section_idx' not in st.session_state:
    st.session_state.current_section_idx = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'results' not in st.session_state:
    st.session_state.results = None
if 'started_assessment' not in st.session_state:
    st.session_state.started_assessment = False
if 'just_changed_section' not in st.session_state:
    st.session_state.just_changed_section = False

# --- App Helper Functions ---
def change_section(delta):
    new_index = st.session_state.current_section_idx + delta
    if 0 <= new_index < TOTAL_SECTIONS:
        st.session_state.current_section_idx = new_index
        st.session_state.just_changed_section = True  # Set the flag

def reset_assessment():
    st.session_state.current_section_idx = 0
    st.session_state.responses = {}
    st.session_state.results = None
    st.session_state.started_assessment = False
    st.session_state.just_changed_section = False
    st.rerun()

def calculate_and_show_results():
    valid_responses = {k: v for k, v in st.session_state.responses.items() if v and v != "Not applicable to this project"}
    if not valid_responses:
        st.error("⚠️ Please answer at least one question to generate results.")
        return

    with st.spinner("🏗️ Analyzing sustainability performance..."):
        results = toolkit.calculate_assessment_results(st.session_state.responses)
        if 'error' in results:
            st.error(f"❌ Calculation Error: {results['error']}")
            return
        st.session_state.results = results
    st.rerun()

def all_current_questions_answered() -> bool:
    """Checks if all questions in the current visible section have been answered."""
    if 'current_section_idx' not in st.session_state or \
       not st.session_state.get('started_assessment', False) or \
       st.session_state.get('results') is not None:
        return True # Not in an active assessment question section

    section_name = SECTIONS[st.session_state.current_section_idx]
    questions_in_section = toolkit.sdg_questions[section_name]

    for q in questions_in_section:
        q_id = q['id']
        response_value = st.session_state.responses.get(q_id)

        if response_value is None:
            # This means the question widget might not have even initialized its response in session state,
            # or it was somehow cleared. Definitely unanswered.
            return False

        if q['type'] == 'radio':
            # For radio buttons, Streamlit ensures a value is present if an index is provided.
            # "Not applicable to this project" is a valid answer.
            # We just need to ensure the response isn't an empty string if that were possible.
            if str(response_value).strip() == "": # Should be rare with st.radio
                return False
        elif q['type'] in ['checkbox', 'multiselect', 'multiple-checkboxes']:
            # For checkboxes, an empty list means no options were selected by the user.
            # We consider this "unanswered" for the purpose of this check.
            if not isinstance(response_value, list) or not response_value:
                return False
        # Add checks for other question types if you introduce them
    return True

# --- Enhanced Chart Creation Functions ---
def create_enhanced_sdg_radar_chart(scores_df: pd.DataFrame):
    """Create an enhanced radar chart for SDG scores with better mobile optimization"""
    if scores_df.empty: 
        return None
    
    # Prepare data for radar chart
    sdg_names = scores_df['SDG_Name_Short'].tolist()
    scores = scores_df['Final_Score'].tolist()
    colors = scores_df['Performance_Color'].tolist()
    
    # Close the radar chart by adding first point at the end
    sdg_names_closed = sdg_names + [sdg_names[0]]
    scores_closed = scores + [scores[0]]
    
    fig = go.Figure()
    
    # Add the main radar trace
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=sdg_names_closed,
        fill='toself',
        name='SDG Performance',
        line=dict(color=UIA_RED, width=3),
        fillcolor=f'rgba(227, 30, 36, 0.2)',
        marker=dict(size=8, color=UIA_RED),
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}/10<br><extra></extra>'
    ))
    
    # Add reference circles at different score levels
    for score_level in [2, 4, 6, 8, 10]:
        fig.add_trace(go.Scatterpolar(
            r=[score_level] * len(sdg_names_closed),
            theta=sdg_names_closed,
            mode='lines',
            line=dict(color='rgba(100, 116, 139, 0.3)', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickmode='linear',
                tick0=0,
                dtick=2,
                tickfont=dict(size=10),
                gridcolor='rgba(100, 116, 139, 0.2)',
                gridwidth=1,
            ),
            angularaxis=dict(
                direction='clockwise',
                period=len(sdg_names),
                tickfont=dict(size=10),
                gridcolor='rgba(100, 116, 139, 0.2)',
                gridwidth=1,
            )
        ),
        showlegend=False,
        title={
            'text': '🎯 SDG Performance Radar (0-10 Scale)',
            'x': 0.5,
            'font': {'size': 16, 'family': 'Inter', 'color': '#1e293b'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        font=dict(family='Inter', size=10),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    # Mobile optimization
    if st.session_state.get('mobile_view', False):
        fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    
    return fig

def create_enhanced_5p_pie_chart(category_scores: dict):
    """Create an enhanced pie chart for 5P framework scores"""
    if not category_scores:
        return None
    
    categories = list(category_scores.keys())
    scores = [category_scores[cat]['Final_Score'] for cat in categories]
    
    # Define colors for each category
    category_colors = {
        'People': '#10B981',
        'Planet': '#059669', 
        'Prosperity': '#F59E0B',
        'Peace': '#3B82F6',
        'Partnership': '#8B5CF6'
    }
    
    colors = [category_colors.get(cat, UIA_BLUE) for cat in categories]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=scores,
        hole=0.4,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3)
        ),
        textinfo='label+value',
        textfont=dict(size=12, family='Inter', color='white'),
        hovertemplate='<b>%{label}</b><br>Score: %{value:.1f}/10<br>Percentage: %{percent}<br><extra></extra>',
        sort=False,
        rotation=90
    )])
    
    # Add center text
    fig.add_annotation(
        text="5Ps<br>Framework",
        x=0.5, y=0.5,
        font_size=14,
        font_family='Inter',
        font_color='#1e293b',
        showarrow=False,
        font=dict(weight='bold')
    )
    
    fig.update_layout(
        title={
            'text': '🌐 5Ps Framework Performance Distribution',
            'x': 0.5,
            'font': {'size': 16, 'family': 'Inter', 'color': '#1e293b'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        font=dict(family='Inter'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        margin=dict(l=40, r=40, t=60, b=80)
    )
    
    # Mobile optimization
    if st.session_state.get('mobile_view', False):
        fig.update_layout(
            height=350,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            margin=dict(l=20, r=120, t=40, b=20)
        )
    
    return fig

# --- Chart Creation Functions (No changes needed) ---
def create_sdg_breakdown_chart(scores_df: pd.DataFrame):
    if scores_df.empty: return None
    sorted_df = scores_df.sort_values('Final_Score', ascending=False)
    fig = go.Figure(go.Bar(
        x=sorted_df['SDG_Name_Short'], y=sorted_df['Final_Score'],
        marker_color=sorted_df['Performance_Color'], text=[f"{s:.1f}" for s in sorted_df['Final_Score']],
        textposition='outside', hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}/10<br>Performance: %{customdata}<extra></extra>',
        customdata=sorted_df['Performance']
    ))
    fig.update_layout(title={'text': '🎯 Individual SDG Performance (0-10 Scale)', 'x': 0.5}, xaxis_title="Sustainable Development Goals", yaxis_title="Final Score (0-10)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_range=[0, 10.5], height=500, font=dict(family='Inter'), xaxis=dict(tickangle=-45))
    return fig
def create_enhanced_radar_chart(category_scores: dict):
    if not category_scores: return None
    categories = list(category_scores.keys())
    scores = [category_scores[cat]['Final_Score'] for cat in categories]
    fig = go.Figure(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line=dict(color=UIA_BLUE, width=3), fillcolor='rgba(74, 144, 184, 0.2)', hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}/10<extra></extra>'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, title={'text': '🌐 5Ps Framework Performance (0-10 Scale)', 'x': 0.5}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500, font=dict(family='Inter'))
    return fig
def create_stacked_sdg_chart(scores_df: pd.DataFrame):
    if scores_df.empty: return None
    sorted_df = scores_df.sort_values('Final_Score', ascending=False)
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Direct Score', x=sorted_df['SDG_Name_Short'], y=sorted_df['Direct_Score'], marker_color=UIA_BLUE, hovertemplate='Direct Score: %{y:.1f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Synergy Bonus', x=sorted_df['SDG_Name_Short'], y=sorted_df['Bonus_Points'], marker_color=UIA_RED, hovertemplate='Synergy Bonus: %{y:.1f}<extra></extra>'))
    fig.update_layout(barmode='stack', title={'text': '🌱 SDG Score Composition: Direct vs. Synergy Bonus', 'x': 0.5}, xaxis_title="Sustainable Development Goals", yaxis_title="Score Points (0-10)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis_range=[0, 10.5], height=500, font=dict(family='Inter'), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5), xaxis=dict(tickangle=-45))
    return fig
def create_performance_distribution_chart(performance_distribution: dict):
    if not performance_distribution: return None
    level_order = ['Exemplary', 'Advanced', 'Basic', 'Minimal', 'No Score']
    labels = sorted(performance_distribution.keys(), key=lambda x: level_order.index(x))
    values = [performance_distribution[k] for k in labels]
    colors = [toolkit.performance_levels[k]['color'] for k in labels]
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.4, marker_colors=colors, textinfo='label+value', hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>', sort=False))
    fig.update_layout(title={'text': '📊 SDG Performance Distribution', 'x': 0.5}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font=dict(family='Inter'), legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
    return fig

# --- UI Rendering Functions ---
def render_header():
    st.markdown("""<div class="uia-header"><h1>🏗️ UIA SDG Assessment Toolkit</h1><p style="font-size: 1.2rem; margin: 0; opacity: 0.95;">Architecture for Sustainability 🌿</p></div>""", unsafe_allow_html=True)

def render_intro():
    st.markdown("""<div class="intro-container"><h2>Welcome to the UIA SDG Assessment Toolkit</h2><p>This tool evaluates your project's alignment with the UN Sustainable Development Goals, using a scoring system designed for architecture that recognizes synergies between goals.</p><p>Complete the questionnaire to receive a detailed sustainability report, including actionable, phase-specific recommendations.</p></div>""", unsafe_allow_html=True)
    if st.button("Begin Assessment", use_container_width=True, type="primary"):
        st.session_state.started_assessment = True
        st.rerun()

def render_progress():
    current_step = st.session_state.current_section_idx + 1
    progress_percent = current_step / TOTAL_SECTIONS
    st.markdown(f"""<div class="progress-container"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"><span style="font-size: 1.1rem; font-weight: 700;">📊 Assessment Progress</span><span style="font-size: 1.2rem; font-weight: 800; color: var(--uia-red);">{int(progress_percent * 100)}%</span></div><div class="stProgress"><div style="width: {progress_percent*100}%; background: linear-gradient(90deg, var(--uia-red) 0%, var(--uia-blue) 100%); height: 8px; border-radius: 4px;"></div></div></div>""", unsafe_allow_html=True)

def render_questions():
    section_name = SECTIONS[st.session_state.current_section_idx]
    questions = toolkit.sdg_questions[section_name]
    # Wrap section title in a div with class for more robust CSS targeting
    st.markdown(f"<div class='section-title-wrapper'><h2>{section_name.replace('_', ' ').title()}</h2></div>", unsafe_allow_html=True)
    
    for q in questions:
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f"<p class='question-title'>Question {q['text']}</p>", unsafe_allow_html=True)
        key = f"{q['id']}_{st.session_state.current_section_idx}"
        
        if q['type'] == 'radio':
            st.session_state.responses[q['id']] = st.radio(
                label=q['id'],
                options=list(q['options'].keys()), 
                key=key, 
                label_visibility="collapsed",
                index=list(q['options'].keys()).index(st.session_state.responses.get(q['id'])) if st.session_state.responses.get(q['id']) in q['options'] else 0
            )
        elif q['type'] in ['checkbox', 'multiselect', 'multiple-checkboxes']:
            if q['id'] not in st.session_state.responses or not isinstance(st.session_state.responses[q['id']], list):
                st.session_state.responses[q['id']] = []
            
            new_selections = []
            for j, option in enumerate(q['options'].keys()):
                checkbox_key = f"{key}_{j}"
                if st.checkbox(option, value=(option in st.session_state.responses[q['id']]), key=checkbox_key):
                    new_selections.append(option)
            st.session_state.responses[q['id']] = new_selections
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- Results, Navigation, and Main flow (No changes needed) ---
def render_results():
    results = st.session_state.results
    if not results:
        st.error("No results found.")
        if st.button("Restart"): reset_assessment()
        return

    overall_score = results.get('overall_score', 0)
    performance_level = toolkit.get_performance_level(overall_score)
    
    # Determine text color for the performance badge based on its background
    perf_bg_color = toolkit.get_performance_color(overall_score)
    # Define light background colors that would need dark text
    light_bgs_for_badge = ['#90ee90', '#F1FAEE', '#ffc107'] # light green, very light accent, yellow
    
    performance_level_text_color = "#000000" if perf_bg_color in light_bgs_for_badge else "white"

    st.markdown(f"""
        <div style="background: linear-gradient(135deg, var(--uia-red) 0%, var(--uia-blue) 100%); color: white; padding: 2rem; border-radius: var(--radius-lg); text-align: center; margin-bottom: 2rem;">
            <h2 style="color: white !important;">Overall Sustainability Score</h2> 
            <div style="font-size: 3.5rem; font-weight: 900; color: white !important;">{overall_score:.1f} / 10</div>
            <p style="font-size: 1.5rem; background: {perf_bg_color}; color: {performance_level_text_color}; display: inline-block; padding: 0.25rem 1rem; border-radius: 20px; font-weight: 600;">
                {performance_level}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🌱 Score Composition", "💡 Insights", "📋 Recommendations"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1: st.plotly_chart(create_performance_distribution_chart(results['performance_distribution']), use_container_width=True)
        with col2: st.plotly_chart(create_enhanced_radar_chart(results['category_scores']), use_container_width=True)
        st.plotly_chart(create_sdg_breakdown_chart(results['scores_df']), use_container_width=True)
    with tab2:
        st.markdown("### How Your Score is Calculated")
        st.markdown("Your final score for each SDG is a combination of a **Direct Score** from your answers and a **Synergy Bonus**. A bonus is awarded when high performance in one SDG contributes to another related SDG.")
        st.plotly_chart(create_stacked_sdg_chart(results['scores_df']), use_container_width=True)
    with tab3:
        st.markdown("### Key Insights")
        for insight in results.get('insights', []): st.info(insight)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Strengths (Top 5)")
            for s in results.get('strengths', []): st.success(f"**{s['SDG_Name_Short']}**: Score {s['Final_Score']}/10 ({s['Performance']})")
        with col2:
            st.markdown("#### Areas for Improvement (Score < 6)")
            weaknesses = results.get('weaknesses', [])
            if weaknesses:
                for w in weaknesses: st.warning(f"**{w['SDG_Name_Short']}**: Score {w['Final_Score']}/10 ({w['Performance']})")
            else: st.info("No SDGs scored below 6. Great work!")
    with tab4:
        st.markdown("### Actionable Recommendations")
        st.info("Focus on your 'Areas for Improvement'. Here are some tailored suggestions:")
        weaknesses = results.get('weaknesses', [])
        if weaknesses:
            sdg_to_improve = st.selectbox("Select an SDG to get recommendations", options=[w['SDG_Name_Short'] for w in weaknesses])
            selected_sdg_id = next((w['SDG_ID'] for w in weaknesses if w['SDG_Name_Short'] == sdg_to_improve), None)
            if selected_sdg_id:
                recs = toolkit.get_all_phase_recommendations(selected_sdg_id)
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("#### Design Phase")
                    if recs.get('design'):
                        for r in recs.get('design', []):
                            st.markdown(f"- {r}")
                    else:
                        st.caption("No specific design phase recommendations.")
                with c2:
                    st.markdown("#### Construction Phase")
                    if recs.get('construction'):
                        for r in recs.get('construction', []):
                            st.markdown(f"- {r}")
                    else:
                        st.caption("No specific construction phase recommendations.")
                with c3:
                    st.markdown("#### Operation Phase")
                    if recs.get('operation'):
                        for r in recs.get('operation', []):
                            st.markdown(f"- {r}")
                    else:
                        st.caption("No specific operation phase recommendations.")
        else: st.success("Your project shows strong performance across all SDGs!")

    st.markdown("---")
    if st.button("🔄 Start New Assessment", use_container_width=True): reset_assessment()

def mobile_navigation():
    st.markdown('<div class="mobile-nav"><div class="nav-grid">', unsafe_allow_html=True)
    
    # Define columns for the new layout: Prev, Home, Page Counter
    cols = st.columns([1, 1, 1])

    with cols[0]: # Previous Button
        if st.button("◀️ Prev", key="prev_mobile", use_container_width=True, help="Go to previous section",
                      disabled=st.session_state.current_section_idx == 0):
            change_section(-1)
            st.rerun()

    with cols[1]: # Home Button
        if st.button("🏠 Home", key="home_mobile", use_container_width=True, help="Start Over / Go to Introduction"):
            reset_assessment()

    with cols[2]: # Page Counter
        st.markdown(f"<div class='page-counter'>{st.session_state.current_section_idx + 1}/{TOTAL_SECTIONS}</div>", unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def mobile_next_button():
    """Separate function for the Next/Submit button that appears after questions"""
    is_last_section = st.session_state.current_section_idx == TOTAL_SECTIONS - 1
    
    if not is_last_section:
        button_text = "Next Section ❯"
        button_key = "next_mobile_separate"
        button_help = "Continue to the next section"
        
        # Add a container div with custom class for better CSS targeting
        st.markdown('<div class="mobile-next-button-container">', unsafe_allow_html=True)
        if st.button(button_text, key=button_key, use_container_width=True, help=button_help):
            if all_current_questions_answered():
                change_section(1)
                st.rerun()
            else:
                st.warning("⚠️ Please answer all questions in this section before proceeding.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        button_text = "View Results 📊"
        button_key = "submit_mobile_separate"
        button_help = "Calculate and view assessment results"
        
        # Add a container div with custom class for better CSS targeting
        st.markdown('<div class="mobile-next-button-container">', unsafe_allow_html=True)
        if st.button(button_text, key=button_key, use_container_width=True, help=button_help):
            if all_current_questions_answered():
                calculate_and_show_results()
            else:
                st.warning("⚠️ Please answer all questions in this section before submitting.")
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    render_header()
    if st.session_state.results:
        render_results()
    elif not st.session_state.started_assessment:
        render_intro()
    else:
        render_progress()
        render_questions()
        
        # Mobile Next/Submit button - placed after questions
        mobile_next_button()
        
        # --- SCROLL TO TOP LOGIC ---
        if st.session_state.get('just_changed_section', False):
            js_scroll_to_top = """
                <script>
                    setTimeout(function() {
                        window.scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });
                        console.log('Scrolled to top via JS'); // For debugging
                    }, 100); // Increased timeout to 100ms (was 50ms)
                </script>
                """
            st.components.v1.html(js_scroll_to_top, height=0)
            st.session_state.just_changed_section = False  # Reset the flag
        # --- END SCROLL TO TOP LOGIC ---
        
        # Placeholder for warning message specific to desktop submit
        desktop_submit_warning_placeholder = st.empty() 

        # Bottom mobile navigation - only Prev, Home, and page counter
        mobile_navigation()

        # Desktop submit button (only on last section)
        if st.session_state.current_section_idx == TOTAL_SECTIONS - 1:
            # Add a class for specific styling if needed, or rely on :has()
            st.markdown('<div class="desktop-submit-button-container">', unsafe_allow_html=True)
            if st.button("📊 Calculate Final Results", key="desktop_submit_final", use_container_width=True, type="primary"):
                if all_current_questions_answered():
                    desktop_submit_warning_placeholder.empty()
                    calculate_and_show_results()
                else:
                    # Use the placeholder to show the warning right above the button
                    desktop_submit_warning_placeholder.warning("⚠️ Please answer all questions on this page before calculating results.")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()