# 🏦 JSL Bank - Laboratorio pessoal Bancário Digital

O **JSL Bank** é uma aplicação completa de simulação de banco digital que combina uma interface web dinâmica de usuário (Frontend) e um serviço de API RESTful (Backend), ambos desenvolvidos em **Python** utilizando o framework **Flask**. 

Os dados são armazenados localmente e de forma estruturada em arquivos JSON simples, servindo como uma excelente demonstração de arquitetura cliente-servidor em Flask.

---

## 🎨 Funcionalidades do Sistema

- **Cadastro de Clientes**: Criação de novas contas com dados pessoais e endereço.
- **Geração de Cartão Fictício**: O sistema cria automaticamente um cartão de crédito/débito fictício para o novo usuário com bandeira (Visa, Mastercard, Amex ou Discover) e limite de crédito randômico.
- **Autenticação de Usuários**: Login e logout controlados por sessões do Flask.
- **Painel de Controle (Dashboard)**: Exibição visual do saldo da conta, pontos de fidelidade acumulados, dados do cartão de crédito fictício e o extrato com o histórico de transações.
- **Módulo de Transferências**: Permite transferências financeiras via **Pix** ou **TED**, com validação de saldo no backend.
- **Acessibilidade com Leitor de Tela**: Integração inteligente com a **Web Speech API** no frontend para guiar e narrar o status de transações e ações importantes para o usuário.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem Principal**: Python 3.x
- **Framework Web & API**: [Flask](https://flask.palletsprojects.com/) (v3.1.3)
- **Interface Gráfica (Frontend)**: HTML5, CSS3 personalizado, Templates Jinja2
- **Lógica Frontend**: JavaScript (Vanilla JS) com uso da **Web Speech API** para áudio/narração
- **Comunicação Cliente-Servidor**: Biblioteca [Requests](https://requests.readthedocs.io/)
- **Banco de Dados**: Flat-file JSON (armazenado em `database/`)

---

## 📂 Estrutura de Arquivos

Abaixo está o mapeamento dos componentes mais importantes do projeto:

```
JSLBANK/
│
├── database/                # Diretório onde as tabelas JSON simuladas são mantidas
│   ├── usuarios.json        # Cadastro e saldos de clientes
│   ├── cartoes.json         # Cartões de crédito vinculados
│   └── transacoes.json      # Logs e histórico de Pix/TED
│
├── templates/               # Páginas HTML renderizadas pelo Flask (Jinja2)
│   ├── index.html           # Tela principal / Apresentação do banco
│   ├── cadastro.html        # Tela de formulário de registro de novos clientes
│   ├── sucesso.html         # Confirmação de cadastro e exibição do novo cartão
│   ├── login.html           # Tela de autenticação
│   ├── dashboard.html       # Painel do cliente logado (Saldo, Cartão, Extrato)
│   └── transferir.html      # Tela para envio de Pix e TED
│
├── static/                  # Recursos estáticos
│   └── js/
│       └── speech.js        # Script de acessibilidade para conversão de texto em fala
│
├── api.py                   # API REST (Backend) rodando na porta 5001
├── app.py                   # Aplicação Web (Frontend) rodando na porta 5000
├── database.py              # Operações de leitura, escrita e atualização dos arquivos JSON
├── utils.py                 # Funções auxiliares (ex: gerador dinâmico de cartão de crédito)
└── requrements.txt          # Dependências do ecossistema Python
```

---

## 🚀 Como Executar a Aplicação

Siga o passo a passo para rodar os servidores da API e do aplicativo web localmente.

### Passo 1: Preparar o Ambiente

Navegue até a pasta do projeto e configure um ambiente virtual para instalar as dependências de forma isolada:

**No Windows (PowerShell):**
```powershell
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
.\venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
# Cria o ambiente virtual
python3 -m venv venv

# Ativa o ambiente virtual
source venv/bin/activate
```

### Passo 2: Instalar as Dependências

Com o ambiente virtual ativado, rode:
```bash
pip install -r requrements.txt
```
> 💡 *Nota: Se houver problemas com o encoding do arquivo `requrements.txt`, execute alternativamente:*
> `pip install Flask requests`

### Passo 3: Iniciar a API (Backend)

A API REST do JSL Bank é responsável por conectar as operações ao "banco de dados" JSON. Execute-a na porta padrão `5001`:

```bash
python api.py
```

### Passo 4: Iniciar o Servidor Web (Frontend)

Abra uma **nova janela de terminal** (ativando o venv novamente) e inicie a interface de usuário na porta padrão `5000`:

```bash
python app.py
```

### Passo 5: Acessar a Aplicação

Abra o seu navegador de preferência e digite o endereço:
👉 [http://localhost:5000](http://localhost:5000)

---

## 🔌 Referência de Rotas da API (Porta 5001)

| Método | Rota | Descrição | Payload Exemplo |
| :--- | :--- | :--- | :--- |
| `POST` | `/cadastrar` | Registra usuário, gera cartão e define saldo inicial de R$ 1.000,00. | `{"nome": "Maria", "sobrenome": "Silva", "email": "maria@email.com", ...}` |
| `POST` | `/login` | Valida as credenciais e fornece dados cadastrados. | `{"email": "maria@email.com", "senha": "123"}` |
| `GET` | `/usuario/<id>` | Busca dados, cartões e transações de um usuário específico. | *Nenhum* |
| `POST` | `/transferir` | Efetua uma transação Pix/TED atualizando o saldo se houver fundos. | `{"usuario_id": 1, "tipo": "Pix", "destinatario_nome": "João", "valor": 150.00}` |

---

## 🔒 Considerações de Segurança (Simulação)

- **Fins Educativos**: O projeto foi projetado para fins puramente acadêmicos e de demonstração.
- **Senhas em texto limpo**: As credenciais dos usuários no banco de dados JSON estão atualmente armazenadas em texto limpo para fins de simplificação. Em um sistema de produção, deve-se criptografar as senhas no backend antes do armazenamento (ex: com a biblioteca `werkzeug.security` ou `bcrypt`), conforme indicado nas marcações de comentários em `api.py`.
