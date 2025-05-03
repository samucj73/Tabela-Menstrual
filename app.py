import streamlit as st
import datetime

st.set_page_config(page_title="Tabela Menstrual", layout="centered")
st.title("Tabela Menstrual Simples")

st.markdown("Preencha os dados abaixo para gerar a previsão do seu ciclo menstrual:")

# Inputs do usuário
data_menstruacao = st.date_input("Data da última menstruação")
duracao_ciclo = st.number_input("Duração média do ciclo (dias)", min_value=21, max_value=35, value=28)

# Inicializa o histórico na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Botão para gerar a previsão
if st.button("Gerar Previsão"):
    prox_menstruacao = data_menstruacao + datetime.timedelta(days=duracao_ciclo)
    ovulacao = data_menstruacao + datetime.timedelta(days=duracao_ciclo - 14)
    fertil_ini = ovulacao - datetime.timedelta(days=2)
    fertil_fim = ovulacao + datetime.timedelta(days=2)

    st.markdown("### Resultado do Ciclo")
    st.write(f"**Próxima menstruação:** {prox_menstruacao.strftime('%d/%m/%Y')}")
    st.write(f"**Período fértil estimado:** {fertil_ini.strftime('%d/%m')} a {fertil_fim.strftime('%d/%m')}")
    st.write(f"**Ovulação prevista:** {ovulacao.strftime('%d/%m/%Y')}")

    # Salva no histórico
    st.session_state.historico.append({
        "Data da última": data_menstruacao.strftime('%d/%m/%Y'),
        "Próxima menstruação": prox_menstruacao.strftime('%d/%m/%Y'),
        "Ovulação": ovulacao.strftime('%d/%m/%Y'),
        "Período fértil": f"{fertil_ini.strftime('%d/%m')} - {fertil_fim.strftime('%d/%m')}"
    })

# Exibe o histórico, se existir
if st.session_state.historico:
    st.markdown("### Histórico de Ciclos")
    st.table(st.session_state.historico)
