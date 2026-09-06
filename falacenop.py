import streamlit as st
import pandas as pd
import os
import tempfile
from datetime import datetime

# Configuração inicial
st.set_page_config(
    page_title="FALACENOP - Cenop Serviços SP 1981",
    page_icon="🔵",
    layout="centered"
)

# Cabeçalho com mascote à direita
col_texto, col_mascote = st.columns([3, 1])

with col_texto:
    st.title("FALACENOP — Monitoramento de Clima")
    st.caption("Plataforma de Escuta Ativa | Cenop Serviços SP 1981")

with col_mascote:
    st.image("mascote.png", width=140)


# Define o caminho do banco de dados na pasta temporaria do servidor
DB_FILE = os.path.join(tempfile.gettempdir(),  "respostas_clima.csv")

# Função para salvar a resposta no arquivo de dados
def salvar_resposta(status, motivo="N/A", comentario=""):
    novo_registro = {
        "Data_Hora": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Status": [status],
        "Motivo": [motivo],
        "Comentario": [comentario]
    }
    df_novo = pd.DataFrame(novo_registro)
    
    if not os.path.exists(DB_FILE):
        df_novo.to_csv(DB_FILE, index=False)
    else:
        df_novo.to_csv(DB_FILE, mode='a', header=False, index=False)

# Estilização CSS Banco do Brasil
st.markdown("""
    <style>
    .stApp { background-color: #F4F5F8; }
    .bb-header {
        background: linear-gradient(135deg, #003399 0%, #002266 100%);
        color: white; padding: 20px; border-radius: 10px;
        border-bottom: 5px solid #FCF800; margin-bottom: 25px;
    }
    .bb-tag {
        background-color: #FCF800; color: #003399;
        font-weight: 900; font-size: 0.75rem; padding: 3px 8px;
        border-radius: 4px; text-transform: uppercase;
    }
    .bb-title { font-size: 1.5rem; font-weight: bold; margin-top: 5px; margin-bottom: 0px; }
    .bb-subtitle { font-size: 0.85rem; color: #E2E8F0; }
    .agent-card {
        background-color: white; padding: 18px; border-radius: 8px;
        border-left: 4px solid #003399; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Navegação lateral para acessar a Visão do Funcionário ou a Visão da Gestão
st.sidebar.title("📌 Navegação")
modo = st.sidebar.radio("Selecione a exibição:", ["Interface do Funcionário (Chat)", "Painel da Gestão (Análises)"])

# Cabeçalho Principal
st.markdown("""
    <div class="bb-header">
        <span class="bb-tag">Banco do Brasil</span>
        <div class="bb-title">FALACENOP — Monitoramento de Clima</div>
        <div class="bb-subtitle">Plataforma de Escuta Ativa | Cenop Serviços SP 1981</div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MODO 1: INTERFACE DO FUNCIONÁRIO
# ---------------------------------------------------------
if modo == "Interface do Funcionário (Chat)":
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'resposta_farol' not in st.session_state:
        st.session_state.resposta_farol = None

    if st.session_state.step == 1:
        st.markdown("""
            <div class="agent-card">
                <strong>🤖 FALACENOP:</strong><br>
                Olá! Passando para acompanhar o seu dia no <strong>Cenop Serviços SP 1981</strong>.<br><br>
                Como está o seu ritmo para conduzir as demandas hoje?
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🟢 Energizado(a)\n\n(Fluxo normal)", use_container_width=True):
                salvar_resposta("🟢 Energizado(a)")
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("🟡 Em Alerta\n\n(Gargalos pontuais)", use_container_width=True):
                st.session_state.resposta_farol = "🟡 Em Alerta"
                st.session_state.step = 2
                st.rerun()
        with col3:
            if st.button("🔴 Sob Pressão\n\n(Preciso de suporte)", use_container_width=True):
                st.session_state.resposta_farol = "🔴 Sob Pressão"
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.markdown(f"""
            <div class="agent-card">
                <strong>🤖 FALACENOP:</strong><br>
                Entendido! Você registrou o status <strong>{st.session_state.resposta_farol}</strong>.<br><br>
                Para atuarmos na solução do problema, qual é o <strong>principal fator</strong> de impacto no momento?
            </div>
        """, unsafe_allow_html=True)

        motivos = [
            "📦 Volume de Demandas",
            "🖥️ Instabilidade de Sistemas",
            "📑 Complexidade de Processos / Dúvidas",
            "💬 Comunicação / Alinhamento Interno",
            "👤 Fatores Pessoais / Bem-estar"
        ]
        motivo_selecionado = st.radio("Selecione o causador principal:", motivos)
        comentario = st.text_area("Observação opcional para a gestão (privado):", placeholder="Escreva detalhes aqui se desejar...")

        if st.button("Enviar Registro", type="primary", use_container_width=True):
            salvar_resposta(st.session_state.resposta_farol, motivo_selecionado, comentario)
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        st.success("✅ Registro computado com sucesso no indicador geral da equipe!")
        st.markdown("""
            <div class="agent-card">
                <strong>🤖 FALACENOP:</strong><br>
                Obrigado pelo seu retorno! Seu relato é fundamental para mapearmos os ofensores operacionais e mantermos o equilíbrio da equipe.<br><br>
                <strong>Tenha um ótimo trabalho! 💛💙</strong>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Simular Novo Teste", type="secondary"):
            st.session_state.step = 1
            st.session_state.resposta_farol = None
            st.rerun()

# ---------------------------------------------------------
# MODO 2: PAINEL DA GESTÃO (ANÁLISES E INDICADORES)
# ---------------------------------------------------------
else:
    st.subheader("📊 Consolidação do Clima da Equipe")
    
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        # Métricas gerais
        total_respostas = len(df)
        verdes = len(df[df['Status'] == '🟢 Energizado(a)'])
        amarelos = len(df[df['Status'] == '🟡 Em Alerta'])
        vermelhos = len(df[df['Status'] == '🔴 Sob Pressão'])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total de Votos", total_respostas)
        c2.metric("🟢 Energizado(a)", f"{verdes} ({(verdes/total_respostas)*100:.0f}%)" if total_respostas else 0)
        c3.metric("🟡 Em Alerta", f"{amarelos} ({(amarelos/total_respostas)*100:.0f}%)" if total_respostas else 0)
        c4.metric("🔴 Sob Pressão", f"{vermelhos} ({(vermelhos/total_respostas)*100:.0f}%)" if total_respostas else 0)

        st.divider()

        # Distribuição de Motivos
        st.markdown("### ⚠️ Principais Ofensores Operacionais")
        df_motivos = df[df['Motivo'] != "N/A"]
        if not df_motivos.empty:
            st.bar_chart(df_motivos['Motivo'].value_counts())
        else:
            st.info("Nenhum gargalo registrado até o momento.")

        # Tabela com histórico de respostas
        st.markdown("### 📋 Histórico Detalhado")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("Nenhuma resposta registrada ainda. Realize testes na aba 'Interface do Funcionário (Chat)' para alimentar o painel.")
