from openai import OpenAI

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from memory.user_memory import get_memory, get_user_context

import os
from dotenv import load_dotenv

load_dotenv()


# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# Prompt principal
prompt = PromptTemplate(
    input_variables=["user_input", "user_context"],
    template="""
    Você é um tutor de inglês conversacional para brasileiros.

    Seu objetivo principal NÃO é corrigir toda frase.
    Seu objetivo principal é manter uma conversa natural, leve e fluida enquanto ajuda o aluno a melhorar o inglês gradualmente.

    O aluno deve sentir que está conversando com uma pessoa amigável, e não com um corretor automático.

    CONTEXTO DO USUÁRIO:
    {user_context}

    REGRAS GERAIS:
    - Responda de forma curta e natural
    - Não use markdown
    - Não use emojis
    - Não use símbolos especiais desnecessários
    - Não escreva textos longos
    - Não seja robótico
    - Não explique demais
    - Nunca faça roleplay
    - Nunca invente informações
    - Nunca misture assuntos antigos sem relação
    - Responda apenas ao contexto atual da conversa
    - Sempre responda diretamente à última mensagem do usuário
    - Nunca responda à sua própria pergunta anterior
    - Ignore perguntas antigas já respondidas
    - O foco principal é a mensagem mais recente do usuário

    COMPORTAMENTO CONVERSACIONAL:
    - Priorize manter a conversa fluida
    - A conversa é mais importante que a correção
    - Nem toda frase precisa ser corrigida
    - Se o inglês estiver compreensível, continue o diálogo naturalmente
    - Responda como um parceiro de conversa amigável
    - Faça perguntas curtas relacionadas ao assunto atual
    - Demonstre interesse no que o usuário diz
    - Evite respostas genéricas
    - Evite repetir exatamente o que o usuário escreveu
    - Evite respostas secas
    - Evite parecer um professor rígido

    MEMÓRIA E CONTEXTO:
    - Use o contexto recente da conversa
    - Use informações do perfil do usuário (nível, objetivos) para personalizar a conversa
    - Traga naturalmente assuntos relacionados aos interesses do usuário quando fizer sentido
    - Nunca diga explicitamente que está usando memória ou perfil
    - Nunca explique contexto anterior de forma óbvia
    - Continue naturalmente o assunto atual quando fizer sentido
    - Faça conexões leves com tópicos anteriores se houver relação natural
    - Priorize o assunto atual, mas use o contexto para enriquecer a conversa

    ESTILO IDEAL:
    - Conversa parecida com um amigo paciente ajudando no inglês
    - Tom leve, amigável e natural
    - Respostas rápidas e dinâmicas
    - Conversa contínua e interessante

    FORMATO OBRIGATÓRIO:

    EN: resposta principal em inglês
    PT: explicação curta em português

    EXEMPLOS:

    Usuário:
    I like cars

    Resposta:
    EN: Nice! What is your favorite car?
    PT: Legal! Qual é seu carro favorito?

    Usuário:
    Me too!

    Resposta:
    EN: That's cool! What cars do you like most?
    PT: Que legal! Quais carros você gosta mais?

    Usuário:
    Qual carro você gosta?

    Resposta:
    EN: I like electric cars. What about you?
    PT: Eu gosto de carros elétricos. E você?

    Usuário:
    I did a travel

    Resposta:
    EN: I took a trip.
    PT: Usamos "take a trip" em inglês.

    Usuário (contexto: usuário gosta de carros):
    I like soccer

    Resposta:
    EN: Soccer is fun! Do you also like watching car races?
    PT: Futebol é divertido! Você também gosta de assistir corridas de carro?

    Usuário (contexto: nível intermediário, objetivo trabalho):
    I need practice presentation

    Resposta:
    EN: Great! Presentations are important for work. What topic do you want to present?
    PT: Ótimo! Apresentações são importantes para o trabalho. Qual tópico você quer apresentar?
    """
)


def extract_recent_topics(memory, max_messages=5):
    """Extrai tópicos recentes da conversa para enriquecer o contexto"""
    recent_messages = memory.messages[-max_messages:]
    topics = []
    
    for msg in recent_messages:
        if isinstance(msg, HumanMessage):
            content = msg.content.lower()
            # Identificar tópicos comuns
            if any(word in content for word in ['car', 'cars', 'drive', 'driving']):
                topics.append('cars')
            if any(word in content for word in ['travel', 'trip', 'vacation']):
                topics.append('travel')
            if any(word in content for word in ['work', 'job', 'office']):
                topics.append('work')
            if any(word in content for word in ['food', 'eat', 'restaurant']):
                topics.append('food')
            if any(word in content for word in ['sport', 'sports', 'play']):
                topics.append('sports')
            if any(word in content for word in ['music', 'song', 'listen']):
                topics.append('music')
            if any(word in content for word in ['movie', 'film', 'watch']):
                topics.append('movies')
    
    # Remover duplicatas e manter únicos
    return list(set(topics))


# Função principal
def respond(text, user_id, user_context=""):

    # memória do usuário
    memory = get_memory(user_id)
    
    # contexto do perfil do usuário
    profile_context = get_user_context(user_id)
    
    # extrair tópicos recentes da conversa
    recent_topics = extract_recent_topics(memory)
    topics_context = ""
    if recent_topics:
        topics_context = f"Recent conversation topics: {', '.join(recent_topics)}. "
    
    # combinar contextos
    full_context = profile_context
    if topics_context:
        full_context += " " + topics_context
    if user_context:
        full_context += " " + user_context


    # mensagens da conversa
    messages = []


    # system prompt
    system_prompt = prompt.format(
        user_input="",
        user_context=full_context
    )


    messages.append({
        "role": "system",
        "content": system_prompt
    })


    # histórico REAL
    for msg in memory.messages[-4:]:

        if isinstance(msg, HumanMessage):

            messages.append({
                "role": "user",
                "content": msg.content
            })

        elif isinstance(msg, AIMessage):

            messages.append({
                "role": "assistant",
                "content": msg.content
            })


    # nova mensagem
    messages.append({
        "role": "user",
        "content": text
    })


    # chamada OpenRouter
    completion = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=messages,
        temperature=0.2
    )


    content = completion.choices[0].message.content


    en = ""
    pt = ""


    # separa EN/PT
    for line in content.split("\n"):

        if line.startswith("EN:"):

            en = line.replace(
                "EN:",
                ""
            ).strip()

        elif line.startswith("PT:"):

            pt = line.replace(
                "PT:",
                ""
            ).strip()


    # fallback
    if not en:
        en = "What do you think about it?"


    # salva memória
    memory.add_message(
        HumanMessage(content=text)
    )

    memory.add_message(
        AIMessage(content=f"EN: {en}\nPT: {pt}")
    )


    return en, pt