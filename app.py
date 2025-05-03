import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Tabela Menstrual", layout="centered")

# Cabeçalho centralizado
st.markdown("<h1 style='text-align: center;'>Tabela Menstrual Simples</h1>", unsafe_allow_html=True)
st.write("Preencha os dados abaixo para gerar a previsão do seu ciclo menstrual:")

# Inputs
data_menstruacao = st.date_input("Data da última menstruação", format="DD/MM/YYYY")
duracao_ciclo = st.number_input("Duração média do ciclo (dias)", min_value=21, max_value=35, value=28)

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Função da tabela de fases
def gerar_fases_ciclo(data_menstruacao):
    return [
        {
            "Dia do Ciclo": "Dia 1",
            "Data (aproximada)": (data_menstruacao).strftime('%d/%m/%Y'),
            "Fase do Ciclo": "Início da menstruação"
        },
        {
            "Dia do Ciclo": "Dia 5-6",
            "Data (aproximada)": f"{(data_menstruacao + datetime.timedelta(days=4)).strftime('%d')}–{(data_menstruacao + datetime.timedelta(days=5)).strftime('%d/%m/%Y')}",
            "Fase do Ciclo": "Fim da menstruação"
        },
        {
            "Dia do Ciclo": "Dia 10-12",
            "Data (aproximada)": f"{(data_menstruacao + datetime.timedelta(days=9)).strftime('%d')}–{(data_menstruacao + datetime.timedelta(days=11)).strftime('%d/%m/%Y')}",
            "Fase do Ciclo": "Fase fértil começa"
        },
        {
            "Dia do Ciclo": "Dia 13-15",
            "Data (aproximada)": f"{(data_menstruacao + datetime.timedelta(days=12)).strftime('%d')}–{(data_menstruacao + datetime.timedelta(days=14)).strftime('%d/%m/%Y')}",
            "Fase do Ciclo": "Ovulação (máxima fertilidade)"
        },
        {
            "Dia do Ciclo": "Dia 16-22",
            "Data (aproximada)": f"{(data_menstruacao + datetime.timedelta(days=15)).strftime('%d/%m')} – {(data_menstruacao + datetime.timedelta(days=21)).strftime('%d/%m')}",
            "Fase do Ciclo": "Pós-ovulação"
        },
        {
            "Dia do Ciclo": "Dia 1 novo",
            "Data (aproximada)": (data_menstruacao + datetime.timedelta(days=duracao_ciclo)).strftime('%d/%m/%Y'),
            "Fase do Ciclo": "Nova menstruação"
        }
    ]

# Botão de previsão
if st.button("Gerar Previsão"):
    st.subheader("Resultado do Ciclo")

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

        if i == 0:
            st.success(f"Próxima menstruação: {fim.strftime('%d/%m/%Y')}")
            st.info(f"Período fértil estimado: {fertil_ini.strftime('%d/%m')} a {fertil_fim.strftime('%d/%m')}")
            st.warning(f"Ovulação prevista: {ovulacao.strftime('%d/%m/%Y')}")
            st.session_state.historico.append({
                "Data da Última": inicio.strftime('%d/%m/%Y'),
                "Próxima Menstruação": fim.strftime('%d/%m/%Y'),
                "Ovulação": ovulacao.strftime('%d/%m/%Y'),
                "Período Fértil": f"{fertil_ini.strftime('%d/%m')} - {fertil_fim.strftime('%d/%m')}"
            })

    # Gráfico dos ciclos
    fig, ax = plt.subplots(figsize=(10, 2))
    for ciclo in ciclos:
        dias = [ciclo["inicio"] + datetime.timedelta(days=i) for i in range(duracao_ciclo)]
        cores = [
            '#ff9999' if d == ciclo["inicio"] else
            '#ffd699' if ciclo["fertil_ini"] <= d <= ciclo["fertil_fim"] else
            '#cc99ff' if d == ciclo["ovulacao"] else
            '#dddddd' for d in dias
        ]
        ax.bar(dias, [1]*len(dias), color=cores)

    ax.set_yticks([])
    ax.set_xticks([c["inicio"] for c in ciclos] + [c["prox_menstruacao"] for c in ciclos])
    ax.set_xticklabels(
        [f'Ciclo {i+1} Início' for i in range(3)] +
        [f'Ciclo {i+1} Fim' for i in range(3)],
        rotation=45
    )
    ax.set_title('Visualização dos Próximos 3 Ciclos')
    st.pyplot(fig)

    # Tabela com as fases do ciclo
    st.subheader("Fases do Ciclo Atual")
    fases_df = pd.DataFrame(gerar_fases_ciclo(data_menstruacao))
    st.dataframe(fases_df, use_container_width=True)

# Histórico
if st.session_state.historico:
    st.subheader("Histórico de Ciclos")

    historico_df = pd.DataFrame(st.session_state.historico)
    historico_df.index += 1
    historico_df.index.name = "Ciclo"
    st.dataframe(historico_df, use_container_width=True)

# Botão de reset
if st.button("Redefinir Previsões"):
    st.session_state.historico = []
    st.success("Histórico resetado com sucesso.")

# Rodapé centralizado
st.markdown("---")
st.markdown("<div style='text-align: center;'>© <strong>Samucj Technology</strong><br>Todos os direitos reservados.</div>", unsafe_allow_html=True)
