# BotCore

BotCore é um bot para Discord desenvolvido em Python, projetado para oferecer funcionalidades interativas e moderar servidores de forma eficiente. O bot utiliza a biblioteca `discord.py` e segue uma estrutura modular com suporte a comandos personalizados, eventos e integração com arquivos de configuração.

> **⚠️ Importante:** Este bot ainda está em desenvolvimento. Algumas funcionalidades podem estar incompletas ou sujeitas a alterações.

---

## 🚀 Funcionalidades

- **Moderação**: Bloqueio de palavras inadequadas com respostas automáticas.
- **Comandos Personalizados**: Implementação de diversos comandos com controle de uso e delays configuráveis.
- **Sistema Modular**: Uso de Cogs para organização dos comandos e eventos.
- **Logs e Estatísticas**: Monitoramento de comandos e interações dos usuários.
- **Personalização**: Suporte a variáveis de ambiente para configuração dinâmica.

---

## 🛠️ Estrutura do Projeto

```plaintext
  botCore/
  ├── main.py                 # Arquivo principal do bot (ponto de entrada)
  ├── checks.py               # Funções utilitárias para controle de comandos
  ├── requirements.txt        # Dependências do projeto
  ├── cogs/                   # Diretório com módulos de comandos
  ├── palavroes.json          # Lista de palavras monitoradas e respostas automáticas
  ├── command_counts.json     # Armazena estatísticas de uso dos comandos
  ├── .env                    # Arquivo de configuração com variáveis sensíveis
```

---

## ⚙️ Instalação e Uso
### Pré-requisitos
Python 3.8 ou superior.
Um bot registrado no Discord Developer Portal.
Configuração do arquivo .env com as seguintes variáveis:

```bash
BOT_TOKEN=seu_token_aqui
BOT_ID=seu_bot_id_aqui
```
### Passos para Instalação
Clone este repositório:

```bash
git clone https://github.com/seu-usuario/botCore.git
cd botCore
```
### Instale as dependências:

```bash
pip install -r requirements.txt
```

###Execute o bot:

```bash
python main.py
```

---

# 📂 Arquivos e Configurações
## main.py
O ponto de entrada do bot, responsável por:

Configuração do prefixo e intents.
Carregamento de cogs.
Tratamento de erros e eventos.
checks.py
Contém funções utilitárias como:

Controle de delay entre comandos dos usuários.
palavroes.json
Lista de palavras monitoradas pelo bot. Cada palavra é associada a uma resposta automática:

```json
{
  "palavroes": [
    {
      "word": "(m|M)erda",
      "response": "Por favor, evite usar palavras inadequadas."
    }
  ]
}
```

---

## requirements.txt
Lista de bibliotecas utilizadas no projeto:

### - discord.py
(versão avançada para suporte completo a eventos e comandos)

### - python-dotenv
(para gerenciamento de variáveis de ambiente)

### - yt_dlp
(suporte a downloads de mídia)

---

# 🌟 Contribuição
### Sinta-se à vontade para contribuir! Abra um pull request ou relate problemas na aba issues.

---

# 📜 Licença
### Este projeto é licenciado sob a MIT License. Consulte o arquivo LICENSE para mais detalhes.
