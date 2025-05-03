import streamlit as st
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tabela Menstrual", layout="centered")

# Estilo visual melhorado
st.markdown("""
    <style>
        .main {
            background-color: #fafafa;
        }
        .block-container {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        }
        h1 {
            color: #d6336c;
        }
        .stButton>button {
            background-color: #d6336c;
            color: white;
            border-radius: 10px;
            font-weight: bold;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #a61e4d;
        }
        table, th, td {
            color: #333 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título estilizado
st.markdown("<h1 style='text-align: center; color: #d6336c;'>Tabela Menstrual Simples</h1>", unsafe_allow_html=True)

st.markdown("Preencha os dados abaixo para gerar a previsão do seu ciclo menstrual:")

# Inputs
data_menstruacao = st.date_input("Data da última menstruação")
duracao_ciclo = st.number_input("Duração média do ciclo (dias)", min_value=21, max_value=35, value=28)

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Botão de previsão
if st.button("Gerar Previsão"):
    st.markdown("### Resultado do Ciclo")

    ciclos = []
    for i in range(3):  # Próximos 3 ciclos
        inicio = data_menstruacao + datetime.timedelta(days=duracao_ciclo * i)
        fim = inicio + datetime.timedelta(days=duracao_ciclo)
        ovulacao = inicio + datetime.timedelta(days=duracao_ciclo - 14)
        fertil_ini = ovulacao - datetime.timedelta(days=2)
        fertil_fim = ovulacao + datetime.timedelta(days=2)

        ciclos.append({
            "inicio": inicio,
            "fim": fim,
            "ovulacao": ovulacao,
            "fertil_ini": fertil_ini,
            "fertil_fim": fertil_fim,
            "prox_menstruacao": fim
        })

        # Exibe o ciclo atual
        if i == 0:
            st.success(f"**Próxima menstruação:** {fim.strftime('%d/%m/%Y')}")
            st.info(f"**Período fértil estimado:** {fertil_ini.strftime('%d/%m')} a {fertil_fim.strftime('%d/%m')}")
            st.warning(f"**Ovulação prevista:** {ovulacao.strftime('%d/%m/%Y')}")
            st.session_state.historico.append({
                "Data da última": inicio.strftime('%d/%m/%Y'),
                "Próxima menstruação": fim.strftime('%d/%m/%Y'),
                "Ovulação": ovulacao.strftime('%d/%m/%Y'),
                "Período fértil": f"{fertil_ini.strftime('%d/%m')} - {fertil_fim.strftime('%d/%m')}"
            })

    # Gráfico dos ciclos
    fig, ax = plt.subplots(figsize=(12, 2))
    for ciclo in ciclos:
        dias = [ciclo["inicio"] + datetime.timedelta(days=i) for i in range(duracao_ciclo)]
        cores = [
            '#ffb3c6' if d == ciclo["inicio"] else
            '#ffdfba' if ciclo["fertil_ini"] <= d <= ciclo["fertil_fim"] else
            '#cdb4db' if d == ciclo["ovulacao"] else
            '#eeeeee' for d in dias
        ]
        ax.bar(dias, [1]*len(dias), color=cores)

    ax.set_yticks([])
    ax.set_xticks([c["inicio"] for c in ciclos] + [c["prox_menstruacao"] for c in ciclos])
    ax.set_xticklabels([f'Ciclo {i+1} Início' for i in range(3)] + [f'Ciclo {i+1} Fim' for i in range(3)], rotation=45)
    ax.set_title('Visualização dos Próximos 3 Ciclos')
    st.pyplot(fig)

# Histórico
if st.session_state.historico:
    st.markdown("### Histórico de Ciclos")
    st.table(st.session_state.historico)

# Botão de reset
if st.button("Redefinir Previsões"):
    st.session_state.historico = []
    st.success("Histórico resetado com sucesso.")

# Rodapé
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
        &copy; Produced by <strong>Samucj Technology</strong>
    </div>
""", unsafe_allow_html=True)
