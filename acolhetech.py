import streamlit as st
import time
import os

# -----------------------------------------------------------------------------
# 1. Configuração da Página e Forçamento de Cores Visíveis (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AcolheTech - Assistente de Bem-Estar",
    page_icon="💙",
    layout="centered"
)

# Estilização CSS para garantir texto escuro em fundo claro
st.markdown("""
    <style>
    /* Força o fundo da página claro */
    .stApp {
        background-color: #f7f9fc !important;
    }
    
    /* Força TODOS os textos normais, parágrafos e títulos a serem escuros */
    html, body, [class*="css"], p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #1c2833 !important;
    }
    
    /* Configuração e cor do texto dos botões */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #3498db !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Estilo e visibilidade do campo de texto (Input) */
    .stTextInput input, .stTextArea textarea {
        color: #1c2833 !important;
        background-color: #ffffff !important;
        border: 1px solid #bdc3c7 !important;
    }
    </style>
""", unsafe_allow_html=True)
