# app.py
import streamlit as st
import datetime

st.set_page_config(page_title="Tabela Menstrual", layout="centered")

st.title("Tabela Menstrual Simples")

# Input: data da última menstruação
data_menstruacao = st.date_input("Data da última menstruação")

# Input: duração média do ciclo
duracao_ciclo = st.number_input("Duração média do ciclo (dias)", min_value=21, max_value=35, value=28)

# Cálculo das próximas datas
prox_menstruacao = data_menstruacao + datetime.timedelta(days=duracao_ciclo)
ovulacao = data_menstruacao + datetime.timedelta(days=duracao_ciclo - 14)

st.markdown("### Previsões")
st.write(f"Próxima menstruação: **{prox_menstruacao.strftime('%d/%m/%Y')}**")
st.write(f"Período fértil estimado: **{(ovulacao - datetime.timedelta(days=2)).strftime('%d/%m')} a {(ovulacao + datetime.timedelta(days=2)).strftime('%d/%m')}**")

# Histórico simples
if "historico" not in st.session_state:
    st.session_state.historico = []

if st.button("Salvar este ciclo"):
    st.session_state.historico.append({
        "Última menstruação": data_menstruacao,
        "Próxima prevista": prox_menstruacao
    })

if st.session_state.historico:
    st.markdown("### Histórico")
    st.table(st.session_state.historico)
