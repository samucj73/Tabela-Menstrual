import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Tabela Menstrual", layout="centered")

st.markdown("<h1 style='text-align: center;'>Tabela Menstrual Simples</h1>", unsafe_allow_html=True)
st.write("Informe a data da última menstruação e veja as previsões para diferentes durações de ciclo (21 a 35 dias):")

# Input de data
data_menstruacao = st.date_input("Data da última menstruação", format="DD/MM/YYYY")

# Histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Botão de previsão
if st.button("Gerar Previsões"):
    st.subheader("Resultados para Ciclos de 21 a 35 dias")

    todos_ciclos = []

    for duracao_ciclo in range(21, 36):  # de 21 a 35 dias
        inicio = data_menstruacao
        fim = inicio + datetime.timedelta(days=duracao_ciclo)
        ovulacao = inicio + datetime.timedelta(days=duracao_ciclo - 14)
        fertil_ini = ovulacao - datetime.timedelta(days=2)
        fertil_fim = ovulacao + datetime.timedelta(days=2)

        ciclo_info = {
            "Duração do Ciclo": duracao_ciclo,
            "Próxima Menstruação": fim.strftime('%d/%m/%Y'),
            "Ovulação": ovulacao.strftime('%d/%m/%Y'),
            "Período Fértil": f"{fertil_ini.strftime('%d/%m')} - {fertil_fim.strftime('%d/%m')}"
        }

        todos_ciclos.append(ciclo_info)
        st.session_state.historico.append(ciclo_info)

    # Mostra a primeira previsão como exemplo
    primeiro = todos_ciclos[0]
    st.success(f"[Ciclo 21 dias] Próxima menstruação: {primeiro['Próxima Menstruação']}")
    st.info(f"Período fértil estimado: {primeiro['Período Fértil']}")
    st.warning(f"Ovulação prevista: {primeiro['Ovulação']}")

    # Tabela completa
    st.dataframe(pd.DataFrame(todos_ciclos), use_container_width=True)

    # Gráfico com os primeiros 3 ciclos para diferentes durações
    st.subheader("Visualização de Ciclos (21, 28 e 35 dias)")
    fig, ax = plt.subplots(figsize=(10, 2))
    for duracao in [21, 28, 35]:
        inicio = data_menstruacao
        dias = [inicio + datetime.timedelta(days=i) for i in range(duracao)]
        ovulacao = inicio + datetime.timedelta(days=duracao - 14)
        fertil_ini = ovulacao - datetime.timedelta(days=2)
        fertil_fim = ovulacao + datetime.timedelta(days=2)

        cores = [
            '#ff9999' if d == inicio else
            '#ffd699' if fertil_ini <= d <= fertil_fim else
            '#cc99ff' if d == ovulacao else
            '#dddddd' for d in dias
        ]
        ax.bar(dias, [1]*len(dias), label=f'{duracao} dias', color=cores, alpha=0.6)

    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title('Exemplo de Ciclos com Durações Variadas')
    ax.legend()
    st.pyplot(fig)

# Histórico
if st.session_state.historico:
    st.subheader("Histórico de Previsões")
    historico_df = pd.DataFrame(st.session_state.historico)
    historico_df.index += 1
    historico_df.index.name = "Ciclo"
    st.dataframe(historico_df, use_container_width=True)

# Botão de reset
if st.button("Redefinir Previsões"):
    st.session_state.historico = []
    st.success("Histórico resetado com sucesso.")

# Rodapé
st.markdown("---")
st.markdown("<div style='text-align: center;'>© <strong>Samucj Technology</strong><br>Todos os direitos reservados.</div>", unsafe_allow_html=True)
