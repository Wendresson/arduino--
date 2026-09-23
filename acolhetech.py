import streamlit as st
import time
import os
import base64

# -----------------------------------------------------------------------------
# 1. Configuração da Página e Animações CSS (Dark Mode & Animação do Mascote)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AcolheTech - Assistente de Bem-Estar",
    page_icon="💙",
    layout="centered"
)

# Estilização CSS incluindo Animação do Mascote
st.markdown("""
    <style>
    /* Força o fundo escuro */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #121824 !important;
    }
    
    /* Textos claros */
    html, body, p, span, div, label, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #f0f4f8 !important;
    }
    
    /* Botões interativos */
    .stButton>button {
        width: 100% !important;
        border-radius: 10px !important;
        height: 3.2em !important;
        background-color: #1f618d !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border: 1px solid #2980b9 !important;
    }
    .stButton>button:hover {
        background-color: #2980b9 !important;
        border-color: #5dade2 !important;
    }
    
    /* Inputs e Caixas */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1c2434 !important;
        border: 1px solid #34495e !important;
    }
    
    /* ANIMAÇÕES DO MASCOTE DO ROBOZINHO */
    @keyframes flutuar {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes respirarMascote {
        0% { transform: scale(0.85); }
        50% { transform: scale(1.15); }
        100% { transform: scale(0.85); }
    }
    
    .robo-estatico img {
        animation: flutuar 3s ease-in-out infinite;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    
    .robo-respirando img {
        animation: respirarMascote 4s ease-in-out infinite;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Inicialização de Sessão
# -----------------------------------------------------------------------------
if "passo" not in st.session_state: st.session_state.passo = 0
if "nome" not in st.session_state: st.session_state.nome = ""
if "sintomas" not in st.session_state: st.session_state.sintomas = []
if "gatilhos" not in st.session_state: st.session_state.gatilhos = []
if "crise" not in st.session_state: st.session_state.crise = False

palavras_alerta = ["machucar", "desistir", "morrer", "socorro", "suicidio", "corta", "bater", "panico"]

def verificar_seguranca(texto):
    if not texto: return False
    texto_lc = texto.lower()
    for palavra in palavras_alerta:
        if palavra in texto_lc: return True
    return False

# -----------------------------------------------------------------------------
# 3. Exibição do Mascote (Corrigida sem vazar texto/código)
# -----------------------------------------------------------------------------
st.title("💙 AcolheTech")
st.caption("Do algoritmo ao acolhimento • Assistente de Bem-Estar Escolar")

nomes_possiveis_imagem = [
    "acolhetech robo.png", "acolhetech_robo.png", "acolhetech robo.jpg",
    "acolhetech_robo.jpg", "mascote.png", "robo.png"
]
imagem_encontrada = None

for nome_file in nomes_possiveis_imagem:
    if os.path.exists(nome_file):
        imagem_encontrada = nome_file
        break

def mostrar_mascote(animado=False):
    if imagem_encontrada:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if animado:
                try:
                    with open(imagem_encontrada, "rb") as f:
                        data = base64.b64encode(f.read()).decode()
                    st.markdown(
                        f'<div class="robo-respirando"><img src="data:image/png;base64,{data}" width="160"></div>',
                        unsafe_allow_html=True
                    )
                except:
                    st.image(imagem_encontrada, width=160)
            else:
                try:
                    with open(imagem_encontrada, "rb") as f:
                        data = base64.b64encode(f.read()).decode()
                    st.markdown(
                        f'<div class="robo-estatico"><img src="data:image/png;base64,{data}" width="160"></div>',
                        unsafe_allow_html=True
                    )
                except:
                    st.image(imagem_encontrada, width=160)

# Exibe o mascote normal nas telas padrão
if st.session_state.passo != 6:
    mostrar_mascote(animado=False)

# -----------------------------------------------------------------------------
# 4. Alerta de Crise
# -----------------------------------------------------------------------------
if st.session_state.crise:
    st.error("🚨 **ATENÇÃO E APOIO IMEDIATO**")
    st.write("Percebi que você está passando por um momento muito difícil. Você não está sozinho(a)! Por favor, procure **AGORA** mesmo um professor, a coordenação ou a psicologia da escola.")
    if st.button("Reiniciar Atendimento"):
        st.session_state.crise = False
        st.session_state.passo = 0
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# 5. JORNADA DE 10 PASSAGENS INTERATIVAS
# -----------------------------------------------------------------------------

# ETAPA 1: BOAS-VINDAS E NOME
if st.session_state.passo == 0:
    st.subheader("👋 Etapa 1/10: Boas-vindas ao seu espaço seguro!")
    st.write("Olá! Eu sou o **AcolheTech**. Estou aqui para conversar, te ouvir e te ajudar a organizar seus pensamentos hoje.")
    
    nome_input = st.text_input("Como prefere ser chamado(a)?")
    if st.button("Iniciar Atendimento"):
        if verificar_seguranca(nome_input):
            st.session_state.crise = True; st.rerun()
        elif nome_input.strip():
            st.session_state.nome = nome_input
            st.session_state.passo = 1; st.rerun()

# ETAPA 2: AVALIAÇÃO DE ENERGIA/HUMOR
elif st.session_state.passo == 1:
    st.write(f"### Etapa 2/10: Checagem de Bateria Emocional")
    st.write(f"Como está sua bateria para enfrentar as atividades de hoje, **{st.session_state.nome}**?")
    
    col1, col2 = st.columns(2)
    if col1.button("🔋 100% - Cheio(a) de energia"): st.session_state.passo = 2; st.rerun()
    if col2.button("⚡ 50% - Cansado(a), mas levando"): st.session_state.passo = 2; st.rerun()
    if col1.button("🪫 20% - Perto de esgotar"): st.session_state.passo = 2; st.rerun()
    if col2.button("⚠️ 0% - Totalmente sobrecarregado(a)"): st.session_state.passo = 2; st.rerun()

# ETAPA 3: CHECKLIST DE SINTOMAS CORPO/MENTE
elif st.session_state.passo == 2:
    st.write("### Etapa 3/10: Checklist de Sensações")
    st.write("Marque o que você tem sentido no corpo ou na mente no dia de hoje (pode marcar mais de um):")
    
    s1 = st.checkbox("Coração acelerado ou aperto no peito")
    s2 = st.checkbox("Músculos tensos (ombros/pescoço rígidos)")
    s3 = st.checkbox("Pensamentos repetitivos ou difíceis de desligar")
    s4 = st.checkbox("Cansaço excessivo ou vontade de isolar-se")
    s5 = st.checkbox("Irritabilidade ou paciência curta")
    
    if st.button("Confirmar Checklist"):
        st.session_state.sintomas = [s1, s2, s3, s4, s5]
        st.session_state.passo = 3; st.rerun()

# ETAPA 4: IDENTIFICAÇÃO DA ORIGEM
elif st.session_state.passo == 3:
    st.write("### Etapa 4/10: Qual a principal fonte dessa tensão?")
    col1, col2 = st.columns(2)
    if col1.button("📚 Desafios Acadêmicos / Provas"): st.session_state.passo = 4; st.rerun()
    if col2.button("🤝 Relações com Colegas / Amigos"): st.session_state.passo = 4; st.rerun()
    if col1.button("🏠 Questões Familiares ou Pessoais"): st.session_state.passo = 4; st.rerun()
    if col2.button("❓ Não sei explicar, apenas sinto"): st.session_state.passo = 4; st.rerun()

# ETAPA 5: SONDAGEM DE PENSAMENTOS AUTOMÁTICOS
elif st.session_state.passo == 4:
    st.write("### Etapa 5/10: Identificando Pensamentos")
    st.write("Qual destas frases mais se aproxima do seu pensamento atual?")
    if st.button("'Tenho medo de não dar conta de tudo.'"): st.session_state.passo = 5; st.rerun()
    if st.button("'Sinto que os outros esperam demais de mim.'"): st.session_state.passo = 5; st.rerun()
    if st.button("'Acho que ninguém entende o que estou passando.'"): st.session_state.passo = 5; st.rerun()
    if st.button("'Preciso de um tempo para respirar e reorganizar a mente.'"): st.session_state.passo = 5; st.rerun()

# ETAPA 6: TEMPO PARA REFLETIR E PAUSA
elif st.session_state.passo == 5:
    st.write("### Etapa 6/10: Tempo para Refletir ⏳")
    st.write("Vamos fazer uma pausa consciente de 10 segundos antes de ir para o exercício prático.")
    
    if st.button("Iniciar Temporizador de Reflexão (10s)"):
        relogio = st.empty()
        for t in range(10, 0, -1):
            relogio.subheader(f"⏱️ Refletindo... {t} segundos")
            time.sleep(1)
        relogio.success("✨ Tempo concluído! Mente pronta para a próxima etapa.")
        time.sleep(1)
        st.session_state.passo = 6; st.rerun()

# ETAPA 7: EXERCÍCIO DE RESPIRAÇÃO COM MASCOTE ANIMADO
elif st.session_state.passo == 6:
    st.write("### Etapa 7/10: Respiração Guiada (5 Ciclos)")
    st.write("Observe o **AcolheTech** abaixo: ele encolhe e expande no ritmo da respiração.")
    
    mostrar_mascote(animado=True)
    
    if st.button("Começar Exercício de Respiração"):
        container_msg = st.empty()
        bar = st.progress(0)
        
        for c in range(1, 6):
            container_msg.info(f"🧘 **Ciclo {c}/5:** INSPIRA devagar pelo nariz...")
            bar.progress(int((c - 0.5) * 20))
            time.sleep(2.5)
            
            container_msg.warning(f"🧘 **Ciclo {c}/5:** SEGURA O AR...")
            time.sleep(1.5)
            
            container_msg.success(f"🧘 **Ciclo {c}/5:** EXPIRA suavemente pela boca...")
            bar.progress(c * 20)
            time.sleep(2.5)
            
        container_msg.success("✨ Excelente! O exercício reduziu seu nível de estresse.")
        time.sleep(2)
        st.session_state.passo = 7; st.rerun()

# ETAPA 8: DICA SOCIOEMOCIONAL PERSONALIZADA
elif st.session_state.passo == 7:
    st.write("### Etapa 8/10: Orientação do AcolheTech")
    st.info("💡 **RECURSO PSICOEDUCACIONAL:**")
    st.write("Quando a pressão parecer grande demais, aplique a **Regra dos 5 Minutos**: Foque em realizar apenas uma pequena parte da tarefa por 5 minutos sem se preocupar com o todo.")
    
    if st.button("Avançar para o Plano de Ação"):
        st.session_state.passo = 8; st.rerun()

# ETAPA 9: PLANO DE AÇÃO INDIVIDUAL (CHECKLIST)
elif st.session_state.passo == 8:
    st.write("### Etapa 9/10: Seu Compromisso de Bem-Estar")
    st.write("Escolha pelo menos 2 ações práticas que você vai fazer hoje por você:")
    
    st.checkbox("Beber um copo de água e caminhar um pouco")
    st.checkbox("Conversar com um amigo ou professor de confiança")
    st.checkbox("Anotar tarefas num papel para tirar o peso da cabeça")
    st.checkbox("Tirar 15 minutos para ouvir uma música relaxante sem celular")
    
    if st.button("Concluir Plano de Ação"):
        st.session_state.passo = 9; st.rerun()

# ETAPA 10: AVALIAÇÃO E ENCERRAMENTO
elif st.session_state.passo == 9:
    st.write("### Etapa 10/10: Avaliação do Acolhimento")
    st.write(f"**{st.session_state.nome}**, completamos nossa jornada de 10 etapas!")
    
    nota = st.slider("De 1 a 5, quanto esse momento te ajudou a desacelerar?", 1, 5, 5)
    
    if st.button("Finalizar e Enviar Avaliação"):
        st.success("💙 **ATENDIMENTO CONCLUÍDO COM SUCESSO!**")
        st.balloons()
        st.write("---")
        st.warning("⚠️ **AVISO IMPORTANTE:** O AcolheTech é um assistente de autorregulação e **não substitui** profissionais de psicologia. Se precisar de apoio contínuo, procure a equipe de orientação da escola.")
        if st.button("Reiniciar Atendimento"):
            st.session_state.passo = 0
            st.session_state.nome = ""
            st.rerun()
