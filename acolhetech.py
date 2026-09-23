import streamlit as st
import time

# -----------------------------------------------------------------------------
# Configuração da Página e Estilo Visual
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AcolheTech - Assistente de Bem-Estar",
    page_icon="💙",
    layout="centered"
)

# Estilização em CSS para deixar o visual aconchegante e responsivo no celular
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f9fc;
    }
    .main-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
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
# Dicionários e Variáveis de Segurança
# -----------------------------------------------------------------------------
palavras_alerta = [
    "machucar", "desistir", "morrer", "socorro", 
    "suicidio", "corta", "bater", "panico"
]

def verificar_seguranca(texto):
    """Verifica se há termos de risco alto no texto digitado."""
    if not texto:
        return False
    texto_lc = texto.lower()
    for palavra in palavras_alerta:
        if palavra in texto_lc:
            return True
    return False

# -----------------------------------------------------------------------------
# Controle de Estado da Sessão (Session State)
# -----------------------------------------------------------------------------
if "passo" not in st.session_state:
    st.session_state.passo = 0
if "nome" not in st.session_state:
    st.session_state.nome = ""
if "opcao1" not in st.session_state:
    st.session_state.opcao1 = ""
if "opcao2" not in st.session_state:
    st.session_state.opcao2 = ""
if "opcao3" not in st.session_state:
    st.session_state.opcao3 = ""
if "crise" not in st.session_state:
    st.session_state.crise = False

# -----------------------------------------------------------------------------
# Cabeçalho Principal
# -----------------------------------------------------------------------------
st.title("💙 AcolheTech")
st.caption("Do algoritmo ao acolhimento • Assistente de Bem-Estar Escolar")

# -----------------------------------------------------------------------------
# Tela de Alerta de Crise (Redirecionamento Imediato)
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
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# Fluxo das 5 Passagens de Diálogo
# -----------------------------------------------------------------------------

# --- PASSO 0: BOAS-VINDAS E IDENTIFICAÇÃO ---
if st.session_state.passo == 0:
    st.subheader("Bem-vindo(a) ao seu espaço seguro!")
    st.write("Olá! Eu sou o **AcolheTech**, seu assistente virtual de bem-estar.")
    
    nome_input = st.text_input("Como você prefere ser chamado(a)?")
    if st.button("Iniciar Conversa"):
        if verificar_seguranca(nome_input):
            st.session_state.crise = True
            st.rerun()
        elif nome_input.strip() != "":
            st.session_state.nome = nome_input
            st.session_state.passo = 1
            st.rerun()
        else:
            st.warning("Por favor, digite seu nome ou apelido para continuar.")

# --- PASSAGEM 1: SONDAGEM DA EMOÇÃO PRINCIPAL ---
elif st.session_state.passo == 1:
    st.info(f"Prazer em te conhecer, **{st.session_state.nome}**! Este é um espaço seguro e sem julgamentos.")
    st.write("### Passagem 1 de 5: Como está seu dia?")
    st.write("Qual destas situações está mais presente no seu dia de hoje?")
    
    col1, col2 = st.columns(2)
    if col1.button("1 - Conflito ou desentendimento na escola"):
        st.session_state.opcao1 = "1"
        st.session_state.passo = 2
        st.rerun()
    if col2.button("2 - Ansiedade ou preocupação constante"):
        st.session_state.opcao1 = "2"
        st.session_state.passo = 2
        st.rerun()
    if col1.button("3 - Sobrecarga com provas e estudos"):
        st.session_state.opcao1 = "3"
        st.session_state.passo = 2
        st.rerun()
    if col2.button("4 - Tristeza, desmotivação ou solidão"):
        st.session_state.opcao1 = "4"
        st.session_state.passo = 2
        st.rerun()

# --- PASSAGEM 2: APROFUNDAMENTO DO PROBLEMA ---
elif st.session_state.passo == 2:
    st.write("### Passagem 2 de 5: Entendendo a situação")
    
    if st.session_state.opcao1 == "1":
        st.write("Entendo. Conflitos desgastam muito o nosso dia. Me conte mais:")
        if st.button("Foi um mal-entendimento ou fofoca"):
            st.session_state.opcao2 = "fofoca"; st.session_state.passo = 3; st.rerun()
        if st.button("Me senti excluído(a) de um grupo"):
            st.session_state.opcao2 = "exclusao"; st.session_state.passo = 3; st.rerun()
        if st.button("Houve uma discussão com falta de respeito"):
            st.session_state.opcao2 = "discussao"; st.session_state.passo = 3; st.rerun()
            
    elif st.session_state.opcao1 == "2":
        st.write("A ansiedade faz o coração acelerar e a mente dar voltas. O que está pesando?")
        if st.button("Medo do que os outros vão pensar de mim"):
            st.session_state.opcao2 = "julgamento"; st.session_state.passo = 3; st.rerun()
        if st.button("Insegurança com o futuro ou notas"):
            st.session_state.opcao2 = "futuro"; st.session_state.passo = 3; st.rerun()
        if st.button("Sensação de agitação sem motivo claro"):
            st.session_state.opcao2 = "corpo"; st.session_state.passo = 3; st.rerun()

    elif st.session_state.opcao1 == "3":
        st.write("A rotina escolar pode ser bem puxada. Qual é o maior obstáculo hoje?")
        if st.button("Tenho muitas tarefas acumuladas"):
            st.session_state.opcao2 = "tarefas"; st.session_state.passo = 3; st.rerun()
        if st.button("Medo de ir mal em uma prova importante"):
            st.session_state.opcao2 = "prova"; st.session_state.passo = 3; st.rerun()
        if st.button("Sinto que não consigo concentrar minha atenção"):
            st.session_state.opcao2 = "foco"; st.session_state.passo = 3; st.rerun()

    else:
        st.write("Sinto muito que esteja se sentindo assim. O que reflete melhor o momento?")
        if st.button("Aconteceu algo em casa que me deixou mal"):
            st.session_state.opcao2 = "casa"; st.session_state.passo = 3; st.rerun()
        if st.button("Sinto que ninguém me entende na escola"):
            st.session_state.opcao2 = "isoliamento"; st.session_state.passo = 3; st.rerun()
        if st.button("Apenas uma sensação de cansaço emocional e tristeza"):
            st.session_state.opcao2 = "tristeza"; st.session_state.passo = 3; st.rerun()

# --- PASSAGEM 3: ATIVIDADE PRÁTICA / AUTORREGULAÇÃO ---
elif st.session_state.passo == 3:
    st.write("### Passagem 3 de 5: Pausa para autorregulação")
    st.write("Antes de tomarmos qualquer decisão, precisamos acalmar a mente e o corpo. Escolha uma atividade:")

    opcao3 = st.radio(
        "Selecione uma opção:",
        ["1 - Respiração Guiada (5 Ciclos Profundos)", 
         "2 - Técnica 5-4-3-2-1 de Aterramento (Foco no Presente)", 
         "3 - Espaço Livre para Desabafo Escrito"]
    )

    if st.button("Iniciar Atividade"):
        if "1 -" in opcao3:
            st.write("#### 🧘 Respiração Guiada (5 Ciclos)")
            progress_bar = st.progress(0)
            for ciclo in range(1, 6):
                st.write(f"**Ciclo {ciclo}/5:** INSPIRA devagar pelo nariz...")
                progress_bar.progress(ciclo * 20)
                time.sleep(2)
                st.write("SEGURA O AR...")
                time.sleep(2)
                st.write("EXPIRA devagar pela boca...")
                time.sleep(2)
            st.success("Excelente! O ritmo cardíaco e a tensão diminuíram.")
            time.sleep(2)
        elif "2 -" in opcao3:
            st.write("#### 👁️ Técnica de Aterramento")
            st.write("Olhe ao seu redor e identifique **3 objetos** de cor azul.")
            time.sleep(3)
            st.write("Agora preste atenção em **2 sons** ao fundo no ambiente.")
            time.sleep(3)
            st.success("Perfeito! Essa técnica ajuda a trazer o cérebro de volta para o momento presente.")
            time.sleep(2)
        else:
            desabafo = st.text_area("Escreva aqui o que está pesando no seu coração (espaço seguro):")
            if verificar_seguranca(desabafo):
                st.session_state.crise = True
                st.rerun()
            else:
                st.success("Colocar pensamentos no papel tira o peso da mente!")
                time.sleep(2)

        st.session_state.passo = 4
        st.rerun()

# --- PASSAGEM 4: DICA SOCIOEMOCIONAL E ORIENTAÇÃO ---
elif st.session_state.passo == 4:
    st.write("### Passagem 4 de 5: Orientação do AcolheTech")
    
    st.info("💡 **DICA DE BEM-ESTAR:**")
    if st.session_state.opcao1 == "1":
        st.write("Não tente resolver conflitos no calor do momento. Espere a poeira baixar e depois expresse seus sentimentos de forma calma usando: *'Eu me senti chateado quando aconteceu aquilo...'*")
    elif st.session_state.opcao1 == "2":
        st.write("Pensamentos de ansiedade não são fatos reais! Lembre-se de todas as vezes em que você achou que não conseguiria e superou mesmo assim.")
    elif st.session_state.opcao1 == "3":
        st.write("Divida tarefas grandes em blocos de 15 minutos. Você não precisa fazer tudo de uma vez. Um passo de cada vez já é um grande avanço!")
    else:
        st.write("Seja gentil com você mesmo(a). Trate suas emoções com a mesma paciência e respeito com que você trataria o seu melhor amigo.")

    if st.button("Avançar para a verificação final"):
        st.session_state.passo = 5
        st.rerun()

# --- PASSAGEM 5: AVALIAÇÃO DE 1 A 5 E ENCERRAMENTO ---
elif st.session_state.passo == 5:
    st.write("### Passagem 5 de 5: Como você se sente agora?")
    st.write(f"**{st.session_state.nome}**, passamos por várias etapas juntos.")
    
    nota = st.slider("De 1 a 5, quanto esta conversa te ajudou a aliviar a tensão?", 1, 5, 5)
    
    if st.button("Finalizar Acolhimento"):
        st.success("💙 **OBRIGADO POR USAR O ACOLHETECH!**")
        st.balloons() # Efeito de balões de comemoração na tela!
        
        st.write("---")
        st.warning(
            "**LEMBRE-SE:** O AcolheTech é uma ferramenta de apoio inicial e **NÃO substitui** "
            "o acompanhamento de profissionais de psicologia ou psiquiatria. "
            "Sempre que precisar de um abraço ou conversa profunda, procure a coordenação, seus professores ou a psicologia da escola!"
        )
        
        if st.button("Novo Atendimento"):
            st.session_state.passo = 0
            st.rerun()

       
