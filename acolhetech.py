# -----------------------------------------------------------------------------
# 3. Cabeçalho e Exibição do Mascote
# -----------------------------------------------------------------------------
st.title("💙 AcolheTech")
st.caption("Do algoritmo ao acolhimento • Assistente de Bem-Estar Escolar")

# Busca automática pelo arquivo da nova imagem do robô
nomes_possiveis_imagem = [
    "acolhetech robo.png",
    "acolhetech_robo.png",
    "acolhetech robo.jpg",
    "acolhetech_robo.jpg",
    "acolhetech robo.jpeg",
    "acolhetech_robo.jpeg",
    "mascote.png",
    "robo.png"
]

imagem_encontrada = None

for nome_file in nomes_possiveis_imagem:
    if os.path.exists(nome_file):
        imagem_encontrada = nome_file
        break

if imagem_encontrada:
    col_i1, col_i2, col_i3 = st.columns([1, 2, 1])
    with col_i2:
        st.image(imagem_encontrada, width=180)
