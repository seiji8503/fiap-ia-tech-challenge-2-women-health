# Prepare Environment

### 1) Criar um ambiente virtual (venv)

# Cria uma pasta `.venv/` contendo um Python “isolado” para este projeto.
# Evita conflitos de dependências entre projetos diferentes.  
python -m venv .venv

# Ativa ambiente virtual e troca o python terminal para dentro de .venv
.\.venv\Scripts\Activate.ps1

# Instala bibliotecas
pip install -r requirements.txt

# VS Code
# "Select Kernel" (ou onde aparece a versão do Python, ex: "Python 3.10...")
# "Python Environments...".
# python ou ('venv': venv)

