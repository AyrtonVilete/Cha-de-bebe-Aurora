# Chá de Bebê - Lista de Presença

Este é um aplicativo Streamlit para coletar e exibir a lista de convidados de um chá de bebê usando Supabase como backend e permitir	exportar um PDF dos confirmados.

## Rodando localmente

1. Clone/baixe este repositório.
2. Crie um ambiente virtual e ative-o:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1    # PowerShell
   # ou .\venv\Scripts\activate.bat  (cmd)
   ```
3. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente ou forneça `SUPABASE_URL` e `SUPABASE_KEY` no [secrets do Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data)

5. Execute:
   ```powershell
   streamlit run app.py
   ```

6. Acesse `http://localhost:8501` no navegador.

## Deploy no Streamlit Cloud

1. Faça push deste repositório para GitHub.
2. Vá para https://streamlit.io/cloud e conecte sua conta GitHub.
3. Crie um novo app apontando para este repositório.
4. Adicione `SUPABASE_URL` e `SUPABASE_KEY` como **secrets** no painel do app.

O Streamlit Cloud irá instalar automaticamente a partir de `requirements.txt` e rodar `app.py`.

## Estrutura

- `app.py` – aplicação principal
- `requirements.txt` – dependências Python
- `venv/` – ambiente virtual (não commitado normalmente)
- `README.md` – este arquivo

---

</code>