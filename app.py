import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF
import os

# 1. Configurações de Segurança e Conexão
# Certifique-se de que estas chaves estão no seu Secrets do Streamlit
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Configuração da página
st.set_page_config(page_title="Chá de Bebê", page_icon="👶")

st.title("👶 Chá de Bebê - Lista de Presença")
st.write("📅 **Dia 14/03 das 10h até 17h**")

# --- 2. BOTÃO PARA LISTA DE FRALDAS ---
# Definimos o nome fixo do arquivo para evitar erros de digitação
NOME_ARQUIVO_PDF = "Lista-de-Fraldas.pdf"

if os.path.exists(NOME_ARQUIVO_PDF):
    with open(NOME_ARQUIVO_PDF, "rb") as file:
        st.download_button(
            label="🍼 Baixar Lista de Sugestões (Fraldas)",
            data=file,
            file_name="Lista-de-Fraldas.pdf",
            mime="application/pdf",
            type="primary" # Deixa o botão em destaque
        )
else:
    st.error(f"⚠️ O arquivo '{NOME_ARQUIVO_PDF}' não foi encontrado na pasta do projeto.")

st.divider()

# --- 3. FORMULÁRIO DE INSCRIÇÃO ---
with st.form("form_presenca", clear_on_submit=True):
    st.subheader("Confirme sua presença aqui:")
    nome = st.text_input("Seu nome completo:")
    status = st.radio("Você poderá vir?", ["Confirmar Presença", "Não poderei ir"])
    submit = st.form_submit_button("Enviar Resposta")

    if submit:
        if nome:
            status_db = "Presente" if status == "Confirmar Presença" else "Não vai dar"
            data = {"nome": nome, "status": status_db, "ativo": 1}
            try:
                supabase.table("convidados").insert(data).execute()
                st.success(f"Confirmado! Obrigado, {nome}.")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar no banco: {e}")
        else:
            st.error("Por favor, digite seu nome antes de enviar.")

st.divider()

# --- 4. LISTAGEM E EXCLUSÃO LÓGICA (SOFT DELETE) ---
st.subheader("Lista de Confirmados")

try:
    # Busca apenas quem está ativo
    response = supabase.table("convidados").select("*").eq("ativo", 1).order("created_at").execute()
    dados = response.data

    if dados:
        for item in dados:
            col_nome, col_btn = st.columns([0.85, 0.15])
            
            with col_nome:
                emoji = "✅" if item['status'] == "Presente" else "❌"
                st.write(f"{emoji} **{item['nome']}**")
            
            with col_btn:
                if st.button("🗑️", key=f"del_{item['id']}"):
                    supabase.table("convidados").update({"ativo": 0}).eq("id", item['id']).execute()
                    st.toast(f"Removido: {item['nome']}")
                    st.rerun()

        # --- 5. EXPORTAR PDF DA LISTA ---
        st.write("---")
        if st.button("📊 Gerar PDF da Lista Final"):
            confirmados = [d['nome'] for d in dados if d['status'] == "Presente"]
            
            if confirmados:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, txt="Lista de Confirmados - Chá de Bebê", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=12)
                
                for i, nome_convidado in enumerate(confirmados, 1):
                    pdf.cell(200, 10, txt=f"{i}. {nome_convidado}", ln=True)
                
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.download_button(
                    label="📥 Clique aqui para baixar o PDF da lista",
                    data=pdf_output,
                    file_name="lista_final_presenca.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("Ainda não há ninguém confirmado como 'Presente'.")
    else:
        st.info("A lista ainda está vazia.")

except Exception as e:
    st.error(f"Erro ao carregar lista: {e}")