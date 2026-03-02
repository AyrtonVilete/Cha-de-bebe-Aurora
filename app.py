import streamlit as st
from supabase import create_client, Client
from fpdf import FPDF

# Configurações do Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("👶 Chá de Bebê - Lista de Presença")

# --- FORMULÁRIO DE INSCRIÇÃO ---
with st.form("form_presenca", clear_on_submit=True):
    nome = st.text_input("Seu nome completo:")
    status = st.radio("Você poderá vir?", ["Confirmar Presença", "Não poderei ir"])
    submit = st.form_submit_button("Enviar")

    if submit:
        if nome:
            status_db = "Presente" if status == "Confirmar Presença" else "Não vai dar"
            # Incluímos o ativo=1 por padrão na inserção
            data = {"nome": nome, "status": status_db, "ativo": 1}
            supabase.table("convidados").insert(data).execute()
            st.success(f"Obrigado, {nome}! Resposta enviada.")
            st.rerun() # Atualiza a lista automaticamente
        else:
            st.error("Por favor, preencha seu nome.")

st.divider()

# --- LISTAGEM COM OPÇÃO DE EXCLUIR ---
st.subheader("Lista de Convidados")

# Filtramos apenas os registros ativos
response = supabase.table("convidados").select("*").eq("ativo", 1).order("created_at").execute()
dados = response.data

if dados:
    for item in dados:
        # Criamos duas colunas: uma larga para o nome e uma estreita para o botão
        col_nome, col_btn = st.columns([0.85, 0.15])
        
        with col_nome:
            cor = "✅" if item['status'] == "Presente" else "❌"
            st.write(f"{cor} **{item['nome']}** - {item['status']}")
        
        with col_btn:
            # Usamos o ID do registro no key para o Streamlit não se perder
            if st.button("🗑️", key=f"del_{item['id']}"):
                # Em vez de delete(), usamos update()
                supabase.table("convidados").update({"ativo": 0}).eq("id", item['id']).execute()
                st.toast(f"Registro de {item['nome']} removido!")
                st.rerun()

    # Botão de PDF (apenas para os presentes e ativos)
    st.write("---")
    if st.button("Gerar PDF de Confirmados"):
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
            st.download_button(label="📥 Baixar PDF", data=pdf_output, file_name="convidados.pdf", mime="application/pdf")
        else:
            st.warning("Não há convidados confirmados para exportar.")
else:
    st.info("Ainda não há respostas ativas.")