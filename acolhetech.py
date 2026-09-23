import streamlit as st
import time
import os
import base64
import random

# -----------------------------------------------------------------------------
# 1. Configuração da Página e Estilo CSS (Tom Azul Noite Acolhedor)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AcolheTech - Assistente de Bem-Estar",
    page_icon="💙",
    layout="centered"
)

# Estilização CSS
st.markdown("""
    <style>
    /* Força o fundo para Azul Noite Acolhedor */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0D1B2A !important;
    }
    
    /* Textos em tom suave de branco/azul claro */
    html, body, p, span, div, label, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #E0E1DD !important;
    }
    
    /* Botões em tom Azul Turquesa / Marinho */
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 3.2em !important;
        background-color: #1B263B !important;
        color: #E0E1DD !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border: 1px solid #415A77 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #415A77 !important;
        border-color: #778DA9 !important;
        color: #ffffff !important;
    }
    
    /* Inputs e Caixas */
    .stTextInput input, .stTextArea textarea {
        color: #ffffff !important;
        background-color: #1B263B !important;
        border: 1px solid #415A77 !important;
        border-radius: 8px !important;
    }
    
    /* ANIMAÇÕES DO MASCOTE */
    @keyframes flutuar {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes respirarMascote {
        0% { transform: scale(0.88); }
        50% { transform: scale(1.12); }
        100% { transform: scale(0.88); }
    }
    
    .robo-estatico img {
        animation: flutuar 3.5s ease-in-out infinite;
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
# 2. Função de Limpeza para Reiniciar o Atendimento do Zero
# -----------------------------------------------------------------------------
def reiniciar_atendimento():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Inicialização das variáveis
if "passo" not in st.session_state: st.session_state.passo = 0
if "nome" not in st.session_state: st.session_state.nome = ""
if "sintomas" not in st.session_state: st.session_state.sintomas = []
if "crise" not in st.session_state: st.session_state.crise = False

palavras_alerta = ["machucar", "desistir", "morrer", "socorro", "suicidio", "corta", "bater", "panico"]

def verificar_seguranca(texto):
    if not texto: return False
    texto_lc = texto.lower()
    for palavra in palavras_alerta:
        if palavra in texto_lc: return True
    return False

# Banco de Frases Motivacionais e Inspiradoras
frases_positivas = [
    "🌟 'Sua jornada é única. Não se compare com o ritmo dos outros.'",
    "🌿 'Respirar fundo é o primeiro passo para reorganizar o mundo ao seu redor.'",
    "💡 'Mesmo nos dias mais difíceis, você está aprendendo e crescendo.'",
    "✨ 'Pequenos passos todos os dias levam a grandes transformações.'",
    "🛡️ 'Pedir ajuda não é sinal de fraqueza, mas sim de grande coragem e autoconhecimento.'",
    "🌈 'Tempestades passam. O céu azul sempre esteve lá atrás das nuvens.'",
    "🎯 'Você é muito mais forte do que qualquer pensamento de insegurança.'"
]

# -----------------------------------------------------------------------------
# 3. SELETOR E PLAYER DE MÚSICA (PIANO OU SEM MÚSICA)
# -----------------------------------------------------------------------------
url_piano = "[https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=meditation-piano-112191.mp3](https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=meditation-piano-112191.mp3)"

with st.expander("🎵 Trilha Sonora de Acolhimento"):
    opcao_musica = st.radio(
        "Fundo Musical de Relaxamento:",
        ["🎹 Piano Calmo e Suave", "🔇 Sem Música de Fundo"],
        key="radio_musica"
    )

if opcao_musica == "🎹 Piano Calmo e Suave":
    st.markdown(
        f"""
        <div style="background-color: #1B263B; padding: 10px; border-radius: 10px; margin-bottom: 15px; border: 1px solid #415A77;">
            <p style="margin: 0 0 5px 0; font-size: 0.85rem; color: #778DA9;">🔊 Tocando agora: <b>Piano Suave de Relaxamento</b></p>
            <audio autoplay loop controls style="width: 100%; height: 32px;">
                <source src="{url_piano}" type="audio/mp3">
            </audio>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 4. Cabeçalho e Mascote
# -----------------------------------------------------------------------------
st.title("💙 AcolheTech")
st.caption("Do algoritmo ao acolhimento • Assistente de Bem-Estar Escolar")

# Busca pela imagem do robô
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
            classe_div = "robo-respirando" if animado else "robo-estatico"
            try:
                with open(imagem_encontrada, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                st.markdown(
                    f'<div class="{classe_div}"><img src="data:image/png;base64,{data}" width="160"></div>',
                    unsafe_allow_html=True
                )
            except:
                st.image(imagem_encontrada, width=160)

# Exibe o mascote estático nas telas padrão (exceto na respiração)
if st.session_state.passo != 8:
    mostrar_mascote(animado=False)

# -----------------------------------------------------------------------------
# 5. Alerta de Crise
# -----------------------------------------------------------------------------
if st.session_state.crise:
    st.error("🚨 **ATENÇÃO E APOIO IMEDIATO**")
    st.write("Percebi que você está passando por um momento muito difícil. Você não está sozinho(a)! Por favor, procure **AGORA** mesmo um professor, a coordenação ou a psicologia da escola.")
    if st.button("Reiniciar Atendimento", on_click=reiniciar_atendimento):
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# 6. JORNADA DE 15 PASSAGENS INTERATIVAS
# -----------------------------------------------------------------------------

# ETAPA 1: BOAS-VINDAS E NOME
if st.session_state.passo == 0:
    st.subheader("👋 Etapa 1/15: Boas-vindas ao seu espaço seguro!")
    st.write("Olá! Eu sou o **AcolheTech**. Estou aqui para conversar, te ouvir e te ajudar a organizar seus pensamentos hoje.")
    
    nome_input = st.text_input("Como prefere ser chamado(a)?")
    if st.button("Iniciar Atendimento"):
        if verificar_seguranca(nome_input):
            st.session_state.crise = True; st.rerun()
        elif nome_input.strip():
            st.session_state.nome = nome_input
            st.session_state.passo = 1; st.rerun()
        else:
            st.warning("Por favor, digite seu nome ou apelido para continuar.")

# ETAPA 2: MENSAGEM INSPIRADORA DE BOAS-VINDAS
elif st.session_state.passo == 1:
    st.subheader(f"✨ Etapa 2/15: Uma mensagem para você, {st.session_state.nome}")
    frase_sorteada = random.choice(frases_positivas)
    st.info(f"**Pílula de Positividade do Dia:**\n\n{frase_sorteada}")
    st.write("Lembre-se de ler esta frase com carinho antes de avançar.")
    if st.button("Guardar frase e Avançar"):
        st.session_state.passo = 2; st.rerun()

# ETAPA 3: AVALIAÇÃO DE ENERGIA/HUMOR
elif st.session_state.passo == 2:
    st.write("### Etapa 3/15: Checagem de Bateria Emocional")
    st.write(f"Como está sua energia para enfrentar o dia de hoje?")
    col1, col2 = st.columns(2)
    if col1.button("🔋 100% - Cheio(a) de energia"): st.session_state.passo = 3; st.rerun()
    if col2.button("⚡ 50% - Cansado(a), mas levando"): st.session_state.passo = 3; st.rerun()
    if col1.button("🪫 20% - Perto de esgotar"): st.session_state.passo = 3; st.rerun()
    if col2.button("⚠️ 0% - Totalmente sobrecarregado(a)"): st.session_state.passo = 3; st.rerun()

# ETAPA 4: CHECKLIST DE SINTOMAS CORPO/MENTE
elif st.session_state.passo == 3:
    st.write("### Etapa 4/15: Checklist de Sensações Físicas")
    st.write("Marque o que você tem sentido no corpo no dia de hoje:")
    s1 = st.checkbox("Coração acelerado ou aperto no peito")
    s2 = st.checkbox("Músculos tensos (ombros/pescoço rígidos)")
    s3 = st.checkbox("Sensação de cansaço ou peso na cabeça")
    s4 = st.checkbox("Nenhuma das opções acima")
    if st.button("Confirmar Sensações"):
        st.session_state.sintomas = [s1, s2, s3, s4]
        st.session_state.passo = 4; st.rerun()

# ETAPA 5: CHECKLIST DE SINTOMAS EMOCIONAIS
elif st.session_state.passo == 4:
    st.write("### Etapa 5/15: Checklist de Pensamentos")
    st.write("O que tem passado pela sua mente?")
    st.checkbox("Pensamentos repetitivos sobre provas/tarefas")
    st.checkbox("Vontade de ficar quieto(a) no seu canto")
    st.checkbox("Sensação de agitação sem motivo claro")
    st.checkbox("Mente calma e tranquila")
    if st.button("Avançar para Origem"):
        st.session_state.passo = 5; st.rerun()

# ETAPA 6: IDENTIFICAÇÃO DA ORIGEM
elif st.session_state.passo == 5:
    st.write("### Etapa 6/15: Qual a principal fonte dessa tensão?")
    col1, col2 = st.columns(2)
    if col1.button("📚 Desafios Acadêmicos / Provas"): st.session_state.passo = 6; st.rerun()
    if col2.button("🤝 Relações com Colegas / Amigos"): st.session_state.passo = 6; st.rerun()
    if col1.button("🏠 Questões Familiares ou Pessoais"): st.session_state.passo = 6; st.rerun()
    if col2.button("❓ Não sei explicar, apenas sinto"): st.session_state.passo = 6; st.rerun()

# ETAPA 7: SEGUNDA PÍLULA DE INSPIRAÇÃO
elif st.session_state.passo == 6:
    st.write("### Etapa 7/15: Pausa Reflexiva 💡")
    st.success("🌱 **Lembrete de Autocompaixão:**\n\n'Você não precisa ter o controle de tudo o tempo todo. Fazer o seu melhor com o que você tem hoje já é o suficiente.'")
    if st.button("Compreendo, quero fazer uma pausa"):
        st.session_state.passo = 7; st.rerun()

# ETAPA 8: TEMPO PARA REFLETIR E TEMPORIZADOR
elif st.session_state.passo == 7:
    st.write("### Etapa 8/15: Temporizador de Desaceleração ⏱️")
    st.write("Vamos fazer uma pausa consciente de 10 segundos antes do exercício de respiração.")
    if st.button("Iniciar Temporizador (10s)"):
        relogio = st.empty()
        for t in range(10, 0, -1):
            relogio.subheader(f"⏱️ Desacelerando... {t} segundos")
            time.sleep(1)
        relogio.success("✨ Excelente! Mente pronta para respirar.")
        time.sleep(1)
        st.session_state.passo = 8; st.rerun()

# ETAPA 9: EXERCÍCIO DE RESPIRAÇÃO COM MASCOTE ANIMADO
elif st.session_state.passo == 8:
    st.write("### Etapa 9/15: Respiração Guiada (5 Ciclos)")
    st.write("Observe o **AcolheTech** abaixo: ele encolhe e expande no ritmo da sua respiração.")
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
        st.session_state.passo = 9; st.rerun()

# ETAPA 10: TÉCNICA DE ATERRAMENTO (GROUNDING)
elif st.session_state.passo == 9:
    st.write("### Etapa 10/15: Técnica de Aterramento (Foco no Presente)")
    st.write("Para organizar seus pensamentos, olhe ao seu redor agora:")
    st.write("1. 👁️ Encontre **3 objetos azuis** ou claros perto de você.")
    st.write("2. 👂 Note **2 sons ao fundo** no ambiente.")
    if st.button("Concluí o exercício visual"):
        st.session_state.passo = 10; st.rerun()

# ETAPA 11: ORIENTAÇÃO SOCIOEMOCIONAL DO ACOLHETECH
elif st.session_state.passo == 10:
    st.write("### Etapa 11/15: Dica Prática de Bem-Estar")
    st.info("💡 **A REGRA DOS 5 MINUTOS:**\n\nQuando uma tarefa escolar ou problema parecer grande e assustador, comprometa-se a mexer nele por apenas 5 minutos. Se quiser parar depois, pare. A maior barreira é sempre começar!")
    if st.button("Entendi a Dica"):
        st.session_state.passo = 11; st.rerun()

# ETAPA 12: PLANO DE AÇÃO INDIVIDUAL
elif st.session_state.passo == 11:
    st.write("### Etapa 12/15: Seu Compromisso de Autocuidado")
    st.write("Escolha 2 atitudes práticas para fazer por você hoje:")
    st.checkbox("Beber um copo de água e caminhar um pouco")
    st.checkbox("Conversar com um amigo ou professor de confiança")
    st.checkbox("Anotar tarefas num papel para tirar o peso da cabeça")
    st.checkbox("Ouvir uma música relaxante sem olhar redes sociais")
    if st.button("Confirmar Compromisso"):
        st.session_state.passo = 12; st.rerun()

# ETAPA 13: MENSAGEM FINAL DE INSPIRAÇÃO
elif st.session_state.passo == 12:
    st.write("### Etapa 13/15: Afirmação Positiva")
    st.success("💙 'Você é capaz, inteligente e resistente. Lembre-se de comemorar as pequenas vitórias do seu dia!'")
    if st.button("Avançar para Avaliação"):
        st.session_state.passo = 13; st.rerun()

# ETAPA 14: AVALIAÇÃO DE 1 A 5
elif st.session_state.passo == 13:
    st.write("### Etapa 14/15: Avaliação da Experiência")
    st.write(f"**{st.session_state.nome}**, chegamos à penúltima etapa do nosso acolhimento.")
    nota = st.slider("De 1 a 5, quanto esta conversa te ajudou a desacelerar?", 1, 5, 5)
    if st.button("Finalizar e Enviar Avaliação"):
        st.session_state.passo = 14; st.rerun()

# ETAPA 15: ENCERRAMENTO E REINÍCIO
elif st.session_state.passo == 14:
    st.success("💙 **ATENDIMENTO CONCLUÍDO COM SUCESSO!**")
    st.balloons()
    st.write("---")
    st.warning("⚠️ **AVISO IMPORTANTE:** O AcolheTech é uma ferramenta de apoio e autorregulação e **não substitui** o acompanhamento profissional de psicólogos ou psiquiatras. Procure a orientação da escola sempre que precisar!")
    if st.button("🔄 Iniciar Novo Atendimento", on_click=reiniciar_atendimento):
        st.rerun()
