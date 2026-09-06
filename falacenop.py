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

import base64

# Função para carregar a imagem em Base64 para dentro do cartão HTML
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

img_base64 = get_base64_image("mascote.png")

# Cartão Azul Único com Título e Mascote Integrados
st.markdown(f"""
    <div style="background-color: #003399; padding: 20px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div>
            <span style="background-color: #FCDB00; color: #003399; font-weight: bold; padding: 4px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin-bottom: 8px;">BANCO DO BRASIL</span>
            <h2 style="color: white; margin: 0; font-size: 24px;">FALACENOP — Monitoramento de Clima</h2>
            <p style="color: #E0E0E0; margin: 5px 0 0 0; font-size: 14px;">Plataforma de Escuta Ativa | Cenop Serviços SP 1981</p>
        </div>
        <div>
            <img src="data:image/png;base64,{img_base64}" width="120" style="border-radius: 8px;">
        </div>
    </div>
""", unsafe_allow_html=True)
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


# Navegação lateral para acessar a Visão do Funcionário ou a Visão da Gestão
st.sidebar.title("📌 Navegação")
modo = st.sidebar.radio("Selecione a exibição:", ["Interface do Funcionário (Chat)", "Painel da Gestão (Análises)"])
if modo == "Interface do Funcionário (Chat)":
    # ---------------------------------------------------------
    # MODO 1: INTERFACE DO FUNCIONÁRIO
    # ---------------------------------------------------------
    if 'step' not in st.session_state:
            st.session_state.step = 1
    if 'resposta_farol' not in st.session_state:
        st.session_state.resposta_farol = None
    
        if st.session_state.step == 1:
            st.markdown("""
            **FALACENOP:**
            Olá! Passando para acompanhar o seu dia no Cenop Serviços SP 1981.
    
            Como está o ritmo para conduzir as demandas hoje?
             """)
                
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🟢 Energizado(a)\n\nFluxo normal", use_container_width=True, key="btn_energizado"):
                    salvar_resposta("🟢 Energizado(a)")
                    st.session_state.step = 4
                    st.rerun()
            with col2:
                if st.button("🟡 Em Alerta\n\nGargalos pontuais", use_container_width=True, key="btn_alerta"):
                    st.session_state.resposta_farol = "🟡 Em Alerta"
                    st.session_state.step = 2
                    st.rerun()
            with col3:
                if st.button("🔴 Sob Pressão\n\nPreciso de suporte", use_container_width=True, key="btn_pressao"):
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
            st.session_state.step = 4
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
