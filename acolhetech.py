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
    
    /* Cartão de Frase Motivacional */
    .phrase-card {
        background-color: #1B263B;
        border-left: 5px solid #4A90E2;
        padding: 18px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
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
# 2. Banco de Frases Inspiradoras e Motivacionais
# -----------------------------------------------------------------------------
frases_positivas = [
    "✨ 'Você não precisa ter todas as respostas hoje. Dar o seu melhor a cada passo já é uma grande vitória.'",
    "🌱 'Dias difíceis também constroem pessoas fortes. Respire fundo e respeite o seu próprio tempo.'",
    "💡 'Não compare o seu bastidor com o palco dos outros. Sua jornada é única e valiosa.'",
    "🛡️ 'Erros não definem quem você é; eles são apenas degraus no seu aprendizado.'",
    "🌈 'Você é muito mais resistente e capaz do que os seus pensamentos de dúvida tentam te convencer.'",
    "🌊 'Assim como as ondas do mar, as emoções difíceis vêm e vão. Permita-se ter momentos de pausa.'",
    "🤝 'Pedir ajuda não é sinal de fraqueza, mas sim de profunda coragem e sabedoria.'",
    "☀️ 'Pequenos progressos diários acumulam grandes resultados no final. Celebre cada pequena conquista!'"
]

# -----------------------------------------------------------------------------
# 3. Função de Limpeza para Reiniciar o Atendimento
# -----------------------------------------------------------------------------
def reiniciar_atendimento():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Inicialização limpa das variáveis
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

# -----------------------------------------------------------------------------
# 4. SELETOR E PLAYER DE MÚSICA (PIANO OU SEM MÚSICA)
# -----------------------------------------------------------------------------
url_piano = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=meditation-piano-112191.mp3"

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
# 5. Cabeçalho e Mascote
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

# Exibe o mascote estático nas telas padrão
if st.session_state.passo != 8:
    mostrar_mascote(animado=False)

# -----------------------------------------------------------------------------
# 6. Alerta de Crise
# -----------------------------------------------------------------------------
if st.session_state.crise:
    st.error("🚨 **ATENÇÃO E APOIO IMEDIATO**")
    st.write("Percebi que você está passando por um momento muito difícil. Você não está sozinho(a)! Por favor, procure **AGORA** mesmo um professor, a coordenação ou a psicologia da escola.")
    if st.button("Reiniciar Atendimento", on_click=reiniciar_atendimento):
        st.rerun()
    st.stop()

# -----------------------------------------------------------------------------
# 7. JORNADA DE 15 PASSAGENS INTERATIVAS
# -----------------------------------------------------------------------------

# ETAPA 1: BOAS-VINDAS E NOME
if st.session_state.passo == 0:
    st.subheader("👋 Etapa 1/15: Boas-vindas ao seu espaço seguro!")
    st.write("Olá! Eu sou o **AcolheTech**. Estou aqui para te ouvir, acolher seus sentimentos e organizar sua mente hoje.")
    
    nome_input = st.text_input("Como prefere ser chamado(a)?")
    if st.button("Iniciar Atendimento"):
        if verificar_seguranca(nome_input):
            st.session_state.crise = True
            st.rerun()
        elif nome_input.strip():
            st.session_state.nome = nome_input
            st.session_state.passo = 1
            st.rerun()
        else:
            st.warning("Por favor, digite seu nome ou apelido para continuar.")

# ETAPA 2: FRASE INSPIRADORA DE BOAS-VINDAS
elif st.session_state.passo == 1:
    st.write(f"### Etapa 2/15: Mensagem de Boas-Vindas, {st.session_state.nome}! 🌟")
    
    frase_sorteada = random.choice(frases_positivas)
    st.markdown(f'<div class="phrase-card"><h4>💭 Pílula de Positividade:</h4><p style="font-size: 1.1rem;">{frase_sorteada}</p></div>', unsafe_allow_html=True)
    
    if st.button("Guardar esta mensagem e continuar"):
        st.session_state.passo = 2; st.rerun()

# ETAPA 3: AVALIAÇÃO DE ENERGIA/HUMOR
elif st.session_state.passo == 2:
    st.write("### Etapa 3/15: Checagem de Bateria Emocional")
    st.write("Como está a sua energia para enfrentar o dia de hoje?")
    
    col1, col2 = st.columns(2)
    if col1.button("🔋 100% - Cheio(a) de disposição"): st.session_state.passo = 3; st.rerun()
    if col2.button("⚡ 50% - Cansado(a), mas levando"): st.session_state.passo = 3; st.rerun()
    if col1.button("🪫 20% - Perto de esgotar"): st.session_state.passo = 3; st.rerun()
    if col2.button("⚠️ 0% - Totalmente sobrecarregado(a)"): st.session_state.passo = 3; st.rerun()

# ETAPA 4: CHECKLIST DE SINTOMAS CORPO/MENTE
elif st.session_state.passo == 3:
    st.write("### Etapa 4/15: Checklist de Sensações")
    st.write("Marque o que você tem sentido no corpo ou na mente hoje:")
    
    s1 = st.checkbox("Coração acelerado ou aperto no peito")
    s2 = st.checkbox("Músculos tensos (ombros/pescoço rígidos)")
    s3 = st.checkbox("Pensamentos repetitivos ou difíceis de desligar")
    s4 = st.checkbox("Cansaço excessivo ou vontade de isolar-se")
    s5 = st.checkbox("Irritabilidade ou paciência curta")
    
    if st.button("Confirmar Sensações"):
        st.session_state.sintomas = [s1, s2, s3, s4, s5]
        st.session_state.passo = 4; st.rerun()

# ETAPA 5: IDENTIFICAÇÃO DA ORIGEM
elif st.session_state.passo == 4:
    st.write("### Etapa 5/15: Fonte Principal de Tensão")
    st.write("Qual área da sua vida mais tem exigido de você no momento?")
    col1, col2 = st.columns(2)
    if col1.button("📚 Desafios Acadêmicos / Provas"): st.session_state.passo = 5; st.rerun()
    if col2.button("🤝 Relações com Colegas / Amigos"): st.session_state.passo = 5; st.rerun()
    if col1.button("🏠 Questões Familiares ou Pessoais"): st.session_state.passo = 5; st.rerun()
    if col2.button("❓ Um turbilhão de coisas ao mesmo tempo"): st.session_state.passo = 5; st.rerun()

# ETAPA 6: SONDAGEM DE PENSAMENTOS AUTOMÁTICOS
elif st.session_state.passo == 5:
    st.write("### Etapa 6/15: Mapeando Pensamentos")
    st.write("Qual destas frases mais se aproxima do que sua mente está dizendo?")
    if st.button("'Tenho medo de não dar conta de tudo.'"): st.session_state.passo = 6; st.rerun()
    if st.button("'Sinto que cobram demais de mim.'"): st.session_state.passo = 6; st.rerun()
    if st.button("'Acho que ninguém entende o que sinto.'"): st.session_state.passo = 6; st.rerun()
    if st.button("'Preciso apenas de um momento para respirar.'"): st.session_state.passo = 6; st.rerun()

# ETAPA 7: FRASE MOTIVACIONAL INTERMEDIÁRIA
elif st.session_state.passo == 6:
    st.write("### Etapa 7/15: Lembrete Importante do AcolheTech 💡")
    st.markdown(
        """
        <div class="phrase-card">
            <h4>💙 Lembre-se:</h4>
            <p style="font-size: 1.15rem;">"Você não precisa carregar o peso do mundo nas suas costas. Está tudo bem dar um passo de cada vez e fazer pausas para se cuidar."</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    if st.button("Ir para o Exercício de Desaceleração"):
        st.session_state.passo = 7; st.rerun()

# ETAPA 8: TEMPO PARA REFLETIR E PAUSA CONSCIENTE
elif st.session_state.passo == 7:
    st.write("### Etapa 8/15: Tempo para Refletir ⏳")
    st.write("Vamos fazer uma pausa consciente de 10 segundos para desconectar do ambiente externo.")
    
    if st.button("Iniciar Temporizador de Reflexão (10s)"):
        relogio = st.empty()
        for t in range(10, 0, -1):
            relogio.subheader(f"⏱️ Desacelerando... {t} segundos")
            time.sleep(1)
        relogio.success("✨ Excelente! Mente preparada para a respiração.")
        time.sleep(1)
        st.session_state.passo = 8; st.rerun()

# ETAPA 9: EXERCÍCIO DE RESPIRAÇÃO COM MASCOTE ANIMADO
elif st.session_state.passo == 8:
    st.write("### Etapa 9/15: Respiração Guiada (5 Ciclos)")
    st.write("Observe o **AcolheTech** abaixo: ele encolhe e expande acompanhando o ritmo do seu pulmão.")
    
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
            
        container_msg.success("✨ Perfeito! Seu ritmo cardíaco desacelerou.")
        time.sleep(2)
        st.session_state.passo = 9; st.rerun()

# ETAPA 10: TÉCNICA DE ATERRAMENTO (GROUNDING 5-4-3-2-1)
elif st.session_state.passo == 9:
    st.write("### Etapa 10/15: Técnica de Aterramento (Foco no Presente)")
    st.write("Para tirar a mente dos pensamentos acelerados, olhe ao seu redor:")
    st.info("👁️ Identifique **3 objetos** de cor azul no lugar onde você está agora.")
    st.info("👂 Note **2 sons** ao fundo no ambiente.")
    
    if st.button("Concluí o Exercício de Foco"):
        st.session_state.passo = 10; st.rerun()

# ETAPA 11: DICA SOCIOEMOCIONAL PERSONALIZADA
elif st.session_state.passo == 10:
    st.write("### Etapa 11/15: Recurso Psicoeducacional")
    st.info("💡 **A REGRA DOS 5 MINUTOS:**")
    st.write("Quando uma tarefa parecer assustadora, comprometa-se a fazer apenas 5 minutos dela. Se quiser parar depois disso, tudo bem. Na maioria das vezes, o mais difícil é apenas começar!")
    
    if st.button("Avançar para o Desabafo Seguro"):
        st.session_state.passo = 11; st.rerun()

# ETAPA 12: ESPAÇO PARA DESABAFO LIVRE (OPCIONAL)
elif st.session_state.passo == 11:
    st.write("### Etapa 12/15: Espaço Seguro para Escrita")
    st.write("Se desejar, escreva abaixo em poucas palavras o que mais tirou a sua paz hoje (este texto não fica salvo):")
    
    desabafo = st.text_area("Seu desabafo confidencial:")
    if st.button("Liberar Pensamentos"):
        if verificar_seguranca(desabafo):
            st.session_state.crise = True
            st.rerun()
        else:
            st.success("Colocar sentimentos em palavras ajuda a organizar o caos interno!")
            time.sleep(1.5)
            st.session_state.passo = 12; st.rerun()

# ETAPA 13: PLANO DE AÇÃO INDIVIDUAL (CHECKLIST)
elif st.session_state.passo == 12:
    st.write("### Etapa 13/15: Compromisso de Autocuidado")
    st.write("Escolha pelo menos 2 ações práticas que você vai realizar por você ainda hoje:")
    
    st.checkbox("Beber um copo de água e respirar ar puro por 5 minutos")
    st.checkbox("Conversar com um amigo, professor ou familiar de confiança")
    st.checkbox("Organizar minhas tarefas em uma lista no papel")
    st.checkbox("Ouvir uma música relaxante antes de dormir sem olhar o celular")
    
    if st.button("Confirmar Meu Plano"):
        st.session_state.passo = 13; st.rerun()

# ETAPA 14: AVALIAÇÃO DO ATENDIMENTO
elif st.session_state.passo == 13:
    st.write("### Etapa 14/15: Avaliação do Acolhimento")
    st.write(f"**{st.session_state.nome}**, chegamos à etapa final da nossa conversa!")
    
    nota = st.slider("De 1 a 5, quanto este momento te ajudou a se sentir mais calmo(a)?", 1, 5, 5)
    
    if st.button("Finalizar e Enviar Avaliação"):
        st.session_state.passo = 14
        st.rerun()

# ETAPA 15: MENSAGEM FINAL DE MOTIVAÇÃO E ENCERRAMENTO
elif st.session_state.passo == 14:
    st.success("💙 **ATENDIMENTO CONCLUÍDO COM SUCESSO!**")
    st.balloons()
    
    st.markdown(
        """
        <div class="phrase-card">
            <h4>🌟 Mensagem Final do AcolheTech:</h4>
            <p style="font-size: 1.15rem;">"Nunca se esqueça: você é forte, sua voz importa e a sua saúde mental é uma prioridade. Tenha um excelente dia!"</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("---")
    st.warning("⚠️ **AVISO IMPORTANTE:** O AcolheTech é um assistente de autorregulação e **não substitui** profissionais de psicologia. Se precisar de apoio contínuo, procure a equipe de orientação da escola.")
    
    if st.button("🔄 Iniciar Novo Atendimento", on_click=reiniciar_atendimento):
        st.rerun()
``` eof

---

### O que mudou nesta versão final:
1. **15 Passagens Completas de Diálogo:** O aplicativo agora conduz o usuário por uma jornada em 15 etapas sequenciais, passando por acolhimento, frases de positividade, triagem de humor, identificação de causas, respiração animada, aterramento 5-4-3-2-1, desabafo confidencial, plano de autocuidado e avaliação de 1 a 5.
2. **Pílulas de Positividade Dinâmicas:** Adicionado um banco de dados com frases motivacionais de autocompaixão, superação e autoestima que surgem logo nas etapas iniciais e no encerramento.
3. **Fluxo de Reinício Consertado:** O botão final limpa todas as variáveis e reseta para a Etapa 1/15 imediatamente.
