import streamlit as st
import time
import os

# -----------------------------------------------------------------------------
# 1. Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AcolheTech - Assistente de Bem-Estar",
    page_icon="💙",
    layout="centered"
)

# Estilização CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4a90e2;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Inicialização Segura das Variáveis de Sessão
# -----------------------------------------------------------------------------
if "passo" not in st.session_state:
    st.session_state.passo = 0
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "opcao1" not in st.session_state:
    st.session_state.opcao1 = ""
if "opcao2" not in st.session_state:
    st.session_state.opcao2 = ""
if "crise" not in st.session_state:
    st.session_state.crise = False

palavras_alerta = ["machucar", "desistir", "morrer", "socorro", "suicidio", "corta", "bater", "panico"]

def verificar_seguranca(texto):
    if not texto: return False
    texto_lc = texto.lower()
    for palavra in palavras_alerta:
        if palavra in texto_lc: return True
    return False

# -----------------------------------------------------------------------------
# 3. Cabeçalho e Exibição do Mascote
# -----------------------------------------------------------------------------
st.title("💙 AcolheTech")
st.caption("Do algoritmo ao acolhimento • Assistente de Bem-Estar Escolar")

# Procura a imagem no projeto (tenta vários nomes comuns)
nomes_possiveis_imagem = ["mascote.png", "mascote.jpeg", "mascote.jpg", "robo.png", "robo.jpeg"]
imagem_encontrada = None

for nome_file in nomes_possiveis_imagem:
    if os.path.exists(nome_file):
        imagem_encontrada = nome_file
        break

if imagem_encontrada:
    col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
    with col_i2:
        st.image(imagem_encontrada, width=180)

# -----------------------------------------------------------------------------
# 4. Tela de Alerta de Crise
# -----------------------------------------------------------------------------
if st.session_state.crise:
    st.error("🚨 **ATENÇÃO E APOIO IMEDIATO**")
    st.write(
        "Percebi que você está passando por um momento muito difícil. "
        "Você não está sozinho(a)! Por favor, procure **AGORA** mesmo um professor, "
        "o psicólogo da escola ou a coordenação. Nós queremos te ajudar!"
    )
    if st.button("Reiniciar Atendimento"):
        st.session_state.crise = False
        st.session_state.passo = 0
        st.session_state.nome = ""
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# 5. Fluxo Passo a Passo
# -----------------------------------------------------------------------------

# PASSO 0: BOAS-VINDAS E PERGUNTA DO NOME
if st.session_state.passo == 0:
    st.subheader("👋 Boas-vindas ao seu espaço seguro!")
    st.write("Olá! Eu sou o **AcolheTech**, o teu assistente virtual de bem-estar e escuta empática.")
    
    nome_input = st.text_input("Como você prefere ser chamado(a)?", key="input_nome_usuario")
    
    if st.button("Iniciar Conversa"):
        if verificar_seguranca(nome_input):
            st.session_state.crise = True
            st.rerun()
        elif nome_input.strip() != "":
            st.session_state.nome = nome_input
            st.session_state.passo = 1
            st.rerun()
        else:
            st.warning("Por favor, digite o seu nome para podermos começar!")

# PASSAGEM 1: TRIAGEM EMOCIONAL
elif st.session_state.passo == 1:
    st.info(f"Prazer em te conhecer, **{st.session_state.nome}**! Este é o teu espaço seguro para conversar sem julgamentos.")
    st.write("### Passagem 1 de 5: Como está o teu dia?")
    st.write("Qual destas situações está mais presente no teu dia de hoje?")
    
    col1, col2 = st.columns(2)
    if col1.button("1 - Conflito na escola"):
        st.session_state.opcao1 = "1"; st.session_state.passo = 2; st.rerun()
    if col2.button("2 - Ansiedade ou preocupação"):
        st.session_state.opcao1 = "2"; st.session_state.passo = 2; st.rerun()
    if col1.button("3 - Sobrecarga com estudos"):
        st.session_state.opcao1 = "3"; st.session_state.passo = 2; st.rerun()
    if col2.button("4 - Tristeza ou solidão"):
        st.session_state.opcao1 = "4"; st.session_state.passo = 2; st.rerun()

# PASSAGEM 2: APROFUNDAMENTO
elif st.session_state.passo == 2:
    st.write("### Passagem 2 de 5: Entendendo o desafio")
    
    if st.session_state.opcao1 == "1":
        st.write("Conflitos desgastam muito o nosso dia. O que melhor descreve o que aconteceu?")
        if st.button("Mal-entendimento ou fofoca"): st.session_state.opcao2 = "fofoca"; st.session_state.passo = 3; st.rerun()
        if st.button("Exclusão num trabalho em grupo"): st.session_state.opcao2 = "exclusao"; st.session_state.passo = 3; st.rerun()
        if st.button("Discussão impulsiva"): st.session_state.opcao2 = "discussao"; st.session_state.passo = 3; st.rerun()
        
    elif st.session_state.opcao1 == "2":
        st.write("A ansiedade faz a mente dar voltas. O que está a pesar mais?")
        if st.button("Medo do julgamento dos outros"): st.session_state.opcao2 = "julgamento"; st.session_state.passo = 3; st.rerun()
        if st.button("Insegurança com o futuro/notas"): st.session_state.opcao2 = "futuro"; st.session_state.passo = 3; st.rerun()
        if st.button("Sensação de agitação no corpo"): st.session_state.opcao2 = "corpo"; st.session_state.passo = 3; st.rerun()

    elif st.session_state.opcao1 == "3":
        st.write("A rotina de estudos pode ser pesada. Qual o maior obstáculo hoje?")
        if st.button("Muitas tarefas acumuladas"): st.session_state.opcao2 = "tarefas"; st.session_state.passo = 3; st.rerun()
        if st.button("Medo de ir mal numa prova"): st.session_state.opcao2 = "prova"; st.session_state.passo = 3; st.rerun()
        if st.button("Dificuldade de concentração"): st.session_state.opcao2 = "foco"; st.session_state.passo = 3; st.rerun()

    else:
        st.write("Sinto muito que esteja a sentir-se assim. O que reflete melhor o momento?")
        if st.button("Problemas em casa"): st.session_state.opcao2 = "casa"; st.session_state.passo = 3; st.rerun()
        if st.button("Sensação de não pertencer"): st.session_state.opcao2 = "isolamento"; st.session_state.passo = 3; st.rerun()
        if st.button("Cansaço emocional geral"): st.session_state.opcao2 = "tristeza"; st.session_state.passo = 3; st.rerun()

# PASSAGEM 3: PRÁTICA DE REGULAÇÃO
elif st.session_state.passo == 3:
    st.write("### Passagem 3 de 5: Pausa para autorregulação")
    st.write("Escolha uma atividade para acalmar a mente:")
    
    opcao3 = st.radio("Selecione:", [
        "1 - Respiração Guiada (5 Ciclos)", 
        "2 - Técnica de Aterramento (Foco no Presente)", 
        "3 - Espaço Livre para Desabafo Escrito"
    ])

    if st.button("Iniciar Atividade"):
        if "1 -" in opcao3:
            st.write("#### 🧘 Respiração Guiada")
            bar = st.progress(0)
            for c in range(1, 6):
                st.write(f"**Ciclo {c}/5:** INSPIRA devagar...")
                bar.progress(c * 20)
                time.sleep(1.5)
                st.write("SEGURA O AR...")
                time.sleep(1.5)
                st.write("EXPIRA devagar...")
                time.sleep(1.5)
            st.success("Excelente! O ritmo cardíaco e a tensão diminuíram.")
            time.sleep(2)
        elif "2 -" in opcao3:
            st.write("#### 👁️ Técnica de Aterramento")
            st.write("Olhe ao redor e identifique 3 objetos de cor azul.")
            time.sleep(2)
            st.write("Agora preste atenção em 2 sons ao fundo no ambiente.")
            time.sleep(2)
            st.success("Perfeito! O seu cérebro voltou para o momento presente.")
            time.sleep(2)
        else:
            desabafo = st.text_area("Escreva aqui o que está a pesar no seu coração:")
            if verificar_seguranca(desabafo):
                st.session_state.crise = True
                st.rerun()
            else:
                st.success("Colocar os pensamentos no papel tira o peso da mente!")
                time.sleep(2)

        st.session_state.passo = 4
        st.rerun()

# PASSAGEM 4: ORIENTAÇÃO
elif st.session_state.passo == 4:
    st.write("### Passagem 4 de 5: Orientação do AcolheTech")
    st.info("💡 **DICA DE BEM-ESTAR:**")
    
    if st.session_state.opcao1 == "1":
        st.write("Não tente resolver conflitos no calor do momento. Espere a poeira baixar e expresse os seus sentimentos de forma calma.")
    elif st.session_state.opcao1 == "2":
        st.write("Pensamentos de ansiedade não são fatos reais! Lembre-se de todas as vezes em que superou dias difíceis.")
    elif st.session_state.opcao1 == "3":
        st.write("Divida tarefas grandes em blocos de 15 minutos. Um passo de cada vez já é um grande avanço!")
    else:
        st.write("Seja gentil consigo mesmo(a). Trate as suas emoções com a mesma paciência com que trataria um grande amigo.")

    if st.button("Avançar para a verificação final"):
        st.session_state.passo = 5
        st.rerun()

# PASSAGEM 5: AVALIAÇÃO DE 1 A 5
elif st.session_state.passo == 5:
    st.write("### Passagem 5 de 5: Como você se sente agora?")
    st.write(f"**{st.session_state.nome}**, passamos por várias etapas juntos.")
    
    nota = st.slider("De 1 a 5, quanto esta conversa te ajudou a aliviar a tensão?", 1, 5, 5)
    
    if st.button("Finalizar Acolhimento"):
        st.success("💙 **OBRIGADO POR USAR O ACOLHETECH!**")
        st.balloons()
        st.write("---")
        st.warning(
            "**LEMBRE-SE:** O AcolheTech é uma ferramenta de apoio inicial e **NÃO substitui** "
            "o acompanhamento de profissionais de psicologia ou psiquiatria. "
            "Sempre que precisar, procure a coordenação, os seus professores ou a psicologia da escola!"
        )
        if st.button("Novo Atendimento"):
            st.session_state.passo = 0
            st.session_state.nome = ""
            st.rerun()
