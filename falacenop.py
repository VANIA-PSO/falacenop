import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="FALACENOP - Cenop Serviços SP 1981", page_icon="🤖", layout="centered")

# Estilo visual moderno e cabeçalho
st.markdown("""
<style>
    .agent-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
        color: #31333F;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar o estado da sessão
if "step" not in st.session_state:
    st.session_state.step = 1
if "resposta_farol" not in st.session_state:
    st.session_state.resposta_farol = None

# Função para salvar resposta
def salvar_resposta(status, motivo="N/A", comentario=""):
    st.session_state.step = 3
    st.rerun()

# MODO 1: INTERAÇÃO COM O USUÁRIO (OPERACIONAL)
if st.session_state.step == 1:
    st.markdown("""
    **FALACENOP:**
    
    Olá! Passando para acompanhar o seu dia no Cenop Serviços SP 1981.
    
    Como está o ritmo para conduzir as demandas hoje?
    """)
    
    humor = st.radio(
        "Selecione a opção que melhor descreve o momento:",
        ["⚡ Energizado(a) / Fluxo normal", "🟡 Em Alerta / Gargalos pontuais", "🔴 Sob Pressão / Preciso de suporte"],
        key="escolha_humor"
    )
    
    if st.button("Avançar para o Registro", type="primary", use_container_width=True):
        if "Energizado" in humor:
            st.session_state.resposta_farol = "⚡ Energizado"
        elif "Alerta" in humor:
            st.session_state.resposta_farol = "🟡 Em Alerta"
        else:
            st.session_state.resposta_farol = "🔴 Sob Pressão"
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    st.markdown(f"""
    <div class="agent-card">
    <strong>FALACENOP</strong><br>
    Entendido! Você registrou o status <strong>{st.session_state.resposta_farol}</strong>.<br><br>
    Para atuarmos na solução do problema, qual é o <strong>principal fator</strong> de impacto no momento?
    </div>
    """, unsafe_allow_html=True)

    motivos = [
        "Volume de Demandas",
        "Instabilidade de Sistemas",
        "Complexidade de Processos / Dúvidas",
        "Comunicação / Alinhamento Interno",
        "Fatores Pessoais / Bem-estar"
    ]
    
    motivo_selecionado = st.radio("Selecione o causador principal:", motivos)
    comentario = st.text_area("Observação opcional para a gestão (privado):", placeholder="Escreva detalhes aqui se desejar...")

    if st.button("Enviar Registro", type="primary", use_container_width=True):
        salvar_resposta(st.session_state.resposta_farol, motivo=motivo_selecionado, comentario=comentario)

elif st.session_state.step == 3:
    st.success("Registro computado com sucesso no indicador geral da equipe!")
    st.markdown("""
    <div class="agent-card">
    <strong>FALACENOP</strong><br>
    Obrigado pelo seu retorno! Seu relato é fundamental para mapearmos os ofensores operacionais e mantermos nosso fluxo saudável.<br><br>
    <strong>Tenha um ótimo trabalho! 💛💙</strong>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Simular Novo Teste", type="secondary"):
        st.session_state.step = 1
        st.session_state.resposta_farol = None
        st.rerun()

# MODO 2: PAINEL DA GESTÃO (ANÁLISES E INDICADORES)
st.markdown("---")
if st.checkbox("🔐 Acessar Painel de Gestão (Consolidação do Clima da Equipe)"):
    st.subheader("Painel Gerencial - Cenop Serviços SP 1981")
    st.info("Aqui você visualiza o consolidado dos faróis e motivos informados pela equipe.")
    df_exemplo = pd.DataFrame({
        "Status": ["⚡ Energizado", "🟡 Em Alerta", "🔴 Sob Pressão"],
        "Quantidade": [12, 5, 2]
    })
    st.dataframe(df_exemplo, use_container_width=True)
