import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# Configurações do Supabase (No Streamlit Cloud, use Secrets!)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("👶 Chá de Bebê da Aurora - Lista de Presença - 14/03 de 10h as 17h")

# --- FORMULÁRIO DE INSCRIÇÃO ---
with st.form("form_presenca", clear_on_submit=True):
    nome = st.text_input("Seu nome completo:")
    status = st.radio("Você poderá vir?", ["Confirmar Presença", "Não poderei ir"])
    submit = st.form_submit_button("Enviar")

    if submit:
        if nome:
            status_db = "Presente" if status == "Confirmar Presença" else "Não vai dar"
            data = {"nome": nome, "status": status_db}
            supabase.table("convidados").insert(data).execute()
            st.success(f"Obrigado, {nome}! Resposta enviada.")
        else:
            st.error("Por favor, preencha seu nome.")

# --- VISUALIZAÇÃO E EXPORTAÇÃO ---
st.subheader("Lista de Convidados")

# Busca dados do Supabase
response = supabase.table("convidados").select("*").execute()
dados = response.data

if dados:
    # Exibe na tela
    for item in dados:
        cor = "✅" if item['status'] == "Presente" else "❌"
        st.write(f"{cor} **{item['nome']}** - {item['status']}")

    # Lógica do PDF
    if st.button("Gerar PDF de Confirmados"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Lista de Confirmados - Chá de Bebê", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", size=12)
        confirmados = [d['nome'] for d in dados if d['status'] == "Presente"]
        
        for i, nome_convidado in enumerate(confirmados, 1):
            pdf.cell(200, 10, txt=f"{i}. {nome_convidado}", ln=True)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(label="📥 Baixar PDF", data=pdf_output, file_name="convidados_cha_de_bebe.pdf", mime="application/pdf")
else:
    st.info("Ainda não há respostas.")