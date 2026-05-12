# Multiagentes Tutor Bot 🤖

Um bot tutor de inglês no Telegram que usa múltiplos agentes especializados para fornecer uma experiência de aprendizado personalizada.

## Funcionalidades 🚀

### 🤖 Agentes Especializados
- **Interviewer Agent**: Avalia nível do aluno e cria roadmap personalizado
- **Conversation Agent**: Mantém conversas naturais em inglês com correções leves
- **Grammar Agent**: Corrige gramática de forma pedagógica
- **Audio Feedback Agent**: Analisa pronúncia em áudios enviados

### 🎯 Biblioteca IPA
Sessão estática com sons do inglês explicados especialmente para falantes portugueses.

#### Como usar:
```
/ipa              # Mostra guia completo
/ipa vowels       # Apenas vogais
/ipa consonants   # Consoantes difíceis
/ipa long_sounds  # Sons longos
/ipa /iː/         # Som específico
```

#### Categorias disponíveis:
- **Vogais**: /iː/, /ɪ/, /æ/, /ʌ/
- **Consoantes difíceis**: /θ/, /ð/, /ɹ/, /ŋ/
- **Sons longos**: /uː/, /ɔː/

Cada som inclui:
- 🇧🇷 Como parece para brasileiros
- 👄 Posição da boca e língua
- 🗣 Exemplos práticos

### 🎤 Recursos de Áudio
- **STT (Speech-to-Text)**: Transcreve áudios enviados
- **TTS (Text-to-Speech)**: Converte respostas em áudio
- **Feedback de pronúncia**: Análise automática da fala

### 💾 Memória Persistente
- Histórico de conversas por usuário
- Perfil personalizado (nível, objetivos, progresso)
- Contexto inteligente nas respostas

## Como executar 🏃‍♂️

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar variáveis de ambiente:**
   Crie um arquivo `.env` com:
   ```
   TELEGRAM_TOKEN=seu_token_aqui
   OPENROUTER_API_KEY=sua_api_key_aqui
   MODEL_NAME=nome_do_modelo
   ```

3. **Executar:**
   ```bash
   python main.py
   ```

## Comandos do Bot 💬

- `/start` - Inicia o bot e mostra dicas
- `/ipa` - Biblioteca de sons IPA
- `interview` - Inicia avaliação de nível
- Envie texto ou áudio para conversar

## Arquitetura 🏗️

```
├── main.py                 # Bot principal do Telegram
├── agents/                 # Agentes especializados
│   ├── orchestrator.py     # Coordena os agentes
│   ├── conversation_agent.py
│   ├── interviewer_agent.py
│   ├── grammar_agent.py
│   └── audio_feedback_agent.py
├── audio/                  # Processamento de áudio
│   ├── stt.py             # Speech-to-Text
│   └── tts.py             # Text-to-Speech
├── memory/                # Sistema de memória
│   └── user_memory.py     # Perfis e histórico
└── ipa_library.py         # Biblioteca IPA estática
```

## Tecnologias 🛠️

- **Python** - Linguagem principal
- **Telegram API** - Interface do bot
- **OpenRouter** - API de IA
- **LangChain** - Framework de conversação
- **python-telegram-bot** - SDK do Telegram

## CREDITS

- **Áudios IPA** - retirados do https://americanipachart.com
