from openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os
import re
from dotenv import load_dotenv

from agents.grammar_agent import correct
from agents.practice_agent import handle_practice_step
from memory.user_memory import get_user_profile, reset_interview

load_dotenv()

# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Prompt para gerar o roadmap final
final_prompt = PromptTemplate(
    input_variables=[
        "goal",
        "answer_description",
        "answer_construction",
        "specific_context"
    ],
    template="""
You are an English interviewer who quickly assesses the student's level and creates a personalized roadmap.

Student's goal: {goal}

Answer 1: {answer_description}
Answer 2: {answer_construction}

Specific situation chosen: {specific_context}

Based on this information, respond in English with:
- Estimated student level (beginner, basic, pre-intermediate, intermediate)
- Very short feedback on vocabulary, phrase usage, and sentence construction
- Roadmap with 3 simple steps to advance to the desired situation
- two practical study tips the student can start using immediately

Instructions:
- Be concise and supportive.
- Use simple and clear English.
- Limit each section to 1–2 short sentences.
- Avoid long explanations, technical grammar terms, or large paragraphs.
- Focus on actionable and motivating guidance. 

FORMAT:
Level: ...
Feedback: ...
Roadmap:
1. ...
2. ...
3. ...
Tips: ...
"""
)

# Prompt para gerar palavras e estruturas de prática
practice_prompt = PromptTemplate(
    input_variables=["topic", "subtopic"],
    template="""
You are an English tutor preparing practice material for a Brazilian student.
The student wants to practice the topic: "{topic}" with focus on the subtopic: "{subtopic}".

Choose 15 common English words related to this specific topic and subtopic, and 10 useful sentence structures or short phrases the student should know by heart.
Keep the list simple and beginner-friendly.

Respond in this exact plain format:

WORDS:
1) ...
2) ...
...
...
15)

STRUCTURES:
1) ...
2) ...
...
10) ...
"""
)


def parse_practice_items(response):
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    items = []
    section = None

    for line in lines:
        if line.upper().startswith("WORDS:"):
            section = "words"
            continue
        if line.upper().startswith("STRUCTURES:"):
            section = "structures"
            continue

        match = re.match(r"^\d+\)\s*(.+)$", line)
        if match and section:
            items.append({
                "type": section,
                "text": match.group(1).strip()
            })

    return items


def generate_practice_items(topic, subtopic):
    final_prompt = practice_prompt.format(topic=topic, subtopic=subtopic)
    completion = client.chat.completions.create(
        model=os.getenv("MODEL_NAME"),
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0.2
    )

    content = completion.choices[0].message.content.strip()
    return parse_practice_items(content)

# Perguntas da entrevista (inglês)
questions = {
    1: "What is your main goal with English? For example: travel, work, studies or talk to friends.",
    2: "Now write 1 or 2 sentences in English about you or your routine. Use as much English as you can.",
    3: "Complete in English: 'Yesterday I ...' or 'Tomorrow I will ...' and say something about your day. Remember, use the most advanced English you can, don't worry about mistakes!",
    4: "What specific situation do you want to practice first in English? For example: order food, job interview, travel, talk to colleagues.",
    5: "Great! Now tell me the specific subtopic within that area. For example, if you chose 'job interview', what field? Technology, administration, engineering?"
}

# Traduções das perguntas para uso nos hidden_pt
questions_pt = {
    1: "Qual é o seu principal objetivo com o inglês? Por exemplo: viajar, trabalhar, estudar ou conversar com amigos.",
    2: "Agora escreva 1 ou 2 frases em inglês sobre você ou a sua rotina. Use o máximo de inglês que conseguir.",
    3: "Complete em inglês: 'Yesterday I ...' ou 'Tomorrow I will ...' e diga algo sobre o seu dia. Lembre-se: use o inglês mais avançado que puder, não se preocupe com erros!",
    4: "Qual situação específica você quer praticar primeiro em inglês? Por exemplo: pedir comida, entrevista de emprego, viajar, conversar com colegas.",
    5: "Ótimo! Agora me diga o subtópico específico dentro dessa área. Por exemplo, se você escolheu 'entrevista de emprego', qual é a área? Tecnologia, administração, engenharia?"
}


def should_start_interview(text):
    normalized = text.lower()
    triggers = [
        "start interview",
        "interview",
        "assess my level"
    ]
    return any(trigger in normalized for trigger in triggers)


def parse_final_response(response):
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    result = []
    collecting = False

    for line in lines:
        if line.startswith("Level:") or line.startswith("Feedback:") or line.startswith("Roadmap:") or line.startswith("Tips:"):
            collecting = True
        if collecting:
            result.append(line)

    return "\n".join(result).strip() if result else response.strip()


def format_practice_list(items):
    words = [item["text"] for item in items if item["type"] == "words"]
    structures = [item["text"] for item in items if item["type"] == "structures"]
    
    output = "📚 **Words you need to know:**\n"
    for i, word in enumerate(words, 1):
        output += f"{i}. {word}\n"
    
    output += "\n🎯 **Sentence structures you need to master:**\n"
    for i, struct in enumerate(structures, 1):
        output += f"{i}. {struct}\n"
    
    return output


def format_practice_item(item, current_index, total_items):
    """Formata um único item de prática para exibição"""
    item_type = "word" if item["type"] == "words" else "sentence structure"
    return f"**Item {current_index + 1}/{total_items}** ({item_type}): {item['text']}"


def interview(text, user_id):
    profile = get_user_profile(user_id)
    normalized = text.lower().strip()

    if profile["mode"] == "practice":
        return handle_practice_step(text, user_id)

    if profile["mode"] != "interview" and not should_start_interview(text):
        return None, None, None, None

    if profile["mode"] != "interview":
        profile["mode"] = "interview"
        profile["interview_stage"] = 1
        profile["interview_responses"] = []
        profile["pending_response"] = None
        profile["goal"] = None
        profile["roadmap"] = None
        profile["awaiting_confirmation"] = False

        output = (
            "Let's start a quick interview to understand your English level and your goal.\n\n"
            "Feel free to use the most advanced English you can — show me what you've got! No need to keep it simple. Ready?\n\n"
            f"1) {questions[1]}"
        )
        hidden_pt = (
            "Vamos começar uma entrevista rápida para entender seu nível de inglês e seu objetivo.\n\n"
            "Sinta-se livre para usar o inglês mais avançado que puder — me mostre o que você sabe! Não precisa manter simples. Pronto?\n\n"
            f"1) {questions_pt[1]}"
        )
        return output, output, hidden_pt, None

    if normalized in ["cancelar", "cancel", "sair", "parar"]:
        reset_interview(user_id)
        output = "Interview canceled. When you want, we can start again."
        hidden_pt = "Entrevista cancelada. Quando quiser, podemos começar novamente."
        return output, output, hidden_pt, None

    stage = profile["interview_stage"]
    pending_response = profile.get("pending_response")

    # Se há uma resposta pendente, aguarda ação dos botões
    if pending_response is not None:
        # Sempre mostra os botões de confirmação para qualquer resposta pendente
        if stage == 1:
            question_text = "your goal"
        elif stage == 2:
            question_text = "your sentences"
        elif stage == 3:
            question_text = "your sentence"
        elif stage == 4:
            question_text = "your chosen situation"
        elif stage == 5:
            question_text = "the subtopic"
        else:
            question_text = "this"

        output = f"Is this {question_text} correct?\n\n\"{pending_response}\""
        hidden_pt = f"Isto está correto?\n\n\"{pending_response}\""
        buttons = [
            {"id": "confirm", "text": "✅ Yes, it's correct"},
            {"id": "retry", "text": "❌ No, let me try again"}
        ]
        return output, output, hidden_pt, buttons

    # Se não há resposta pendente, processa a ação do botão ou nova resposta
    action = normalized.strip()
    
    # Processa ações dos botões
    if action == "confirm":
        # Confirma a última resposta pendente (já foi limpa, mas precisamos confirmar a atual)
        # Isso não deve acontecer normalmente, pois sempre há pending_response antes
        return None, None, None, None
    
    elif action == "retry":
        # Limpa qualquer pending e pede para responder novamente
        profile["pending_response"] = None
        next_stage = profile["interview_stage"]
        output = f"No problem! Let's try again.\n\n{questions[next_stage]}"
        hidden_pt = f"Tudo bem! Vamos tentar de novo.\n\n{questions_pt[next_stage]}"
        return output, output, hidden_pt, None

    # Se chegou aqui, é uma nova resposta do usuário para a pergunta atual
    if stage <= 5:
        profile["pending_response"] = text.strip()
        
        # Retorna imediatamente com botões de confirmação
        if stage == 1:
            question_text = "your goal"
        elif stage == 2:
            question_text = "your sentences"
        elif stage == 3:
            question_text = "your sentence"
        elif stage == 4:
            question_text = "your chosen situation"
        elif stage == 5:
            question_text = "the subtopic"
        
        output = f"Is this {question_text} correct?\n\n\"{text.strip()}\""
        hidden_pt = f"Isto está correto?\n\n\"{text.strip()}\""
        buttons = [
            {"id": "confirm", "text": "✅ Yes, it's correct"},
            {"id": "retry", "text": "❌ No, let me try again"}
        ]
        return output, output, hidden_pt, buttons

    if stage == 6:
        # Para o estágio 6 (após roadmap), também usar botões
        output = "Do you want to see the essential words and sentence structures for practicing this topic?"
        hidden_pt = "Quer ver as palavras essenciais e estruturas de frases para praticar este tópico?"
        buttons = [
            {"id": "confirm", "text": "✅ Yes, show me"},
            {"id": "retry", "text": "⏭️ Not yet"}
        ]
        return output, output, hidden_pt, buttons

    return None, None, None, None


# Função para processar ações dos botões
def handle_interview_action(action, user_id):
    """Processa ações dos botões de confirmação/negação na entrevista"""
    profile = get_user_profile(user_id)
    
    if profile["mode"] != "interview":
        return None, None, None, None
    
    stage = profile["interview_stage"]
    pending_response = profile.get("pending_response")
    
    if action == "confirm":
        if stage == 6:
            # Estágio 6: mostrar lista de prática
            if pending_response is None:
                # Gera a lista de prática
                practice_items = generate_practice_items(
                    profile["practice_topic"],
                    profile["practice_subtopic"]
                )
                if not practice_items:
                    practice_items = [
                        {"type": "words", "text": "Hello"},
                        {"type": "structures", "text": "Can I have... ?"}
                    ]
                
                # Salva os itens no perfil
                profile["practice_items"] = practice_items
                profile["mode"] = "practice"
                profile["interview_stage"] = 0
                profile["pending_response"] = None
                
                # Configura o estado para o diálogo sequencial
                profile["practice_mode"] = "sequential_dialogue"
                profile["practice_user_last_item"] = None
                profile["practice_tutor_last_item"] = None
                profile["practice_next_tutor_index"] = 1  # o próximo item que o tutor usará
                profile["practice_last_user_sentence"] = ""
                profile["practice_last_tutor_sentence"] = ""
                
                # Primeiro item da lista (será usado pelo usuário)
                first_item = practice_items[0]
                output = (
                    "Perfect! Here are the essential words and sentence structures for your topic:\n\n"
                    f"{format_practice_list(practice_items)}\n\n"
                    "Let's start a dialogue. First, write a sentence using:\n"
                    f"👉 {first_item['text']}"
                )
                hidden_pt = (
                    "Perfeito! Aqui estão as palavras e estruturas essenciais para seu tópico:\n\n"
                    f"{format_practice_list(practice_items)}\n\n"
                    "Vamos começar um diálogo. Primeiro, escreva uma frase usando:\n"
                    f"👉 {first_item['text']}"
                )
                return output, output, hidden_pt, None
            else:
                # Caso haja pending_response no estágio 6 (fluxo alternativo)
                profile["interview_responses"].append({
                    "question": questions[5],
                    "answer": pending_response
                })
                profile["pending_response"] = None
                
                # Gera o roadmap (igual ao código original)
                answer_description = profile["interview_responses"][1]["answer"]
                answer_construction = profile["interview_responses"][2]["answer"]
                specific_context = profile["interview_responses"][3]["answer"]
                goal = profile["goal"] or "aprender inglês"
                
                final_prompt_text = final_prompt.format(
                    goal=goal,
                    answer_description=answer_description,
                    answer_construction=answer_construction,
                    specific_context=specific_context
                )
                
                completion = client.chat.completions.create(
                    model=os.getenv("MODEL_NAME"),
                    messages=[
                        {
                            "role": "user",
                            "content": final_prompt_text
                        }
                    ],
                    temperature=0.2
                )
                
                summary = completion.choices[0].message.content
                roadmap_text = parse_final_response(summary)
                
                profile["roadmap"] = roadmap_text
                profile["interview_stage"] = 6
                
                output = (
                    "Thank you! I created a short roadmap for you based on your answers.\n\n"
                    f"{roadmap_text}\n\n"
                    "Do you want to see the essential words and sentence structures for practicing this topic?"
                )
                hidden_pt = (
                    "Obrigado! Criei um pequeno roadmap para você com base em suas respostas.\n\n"
                    "Quer ver as palavras essenciais e estruturas de frases para praticar este tópico?"
                )
                buttons = [
                    {"id": "confirm", "text": "✅ Yes, show me"},
                    {"id": "retry", "text": "⏭️ Not yet"}
                ]
                return output, output, hidden_pt, buttons
        
        elif pending_response is None:
            # Não há resposta pendente para confirmar
            return None, None, None, None
        
        # Confirma a resposta pendente e avança (estágios 1 a 5)
        profile["interview_responses"].append({
            "question": questions[stage],
            "answer": pending_response
        })
        profile["pending_response"] = None
        
        # Avança para a próxima pergunta
        if stage == 1:
            profile["goal"] = pending_response
            profile["interview_stage"] = 2
            output = (
                "Great! Now I want to see how you write in English.\n\n"
                f"2) {questions[2]}"
            )
            hidden_pt = (
                "Ótimo! Agora quero ver como você escreve em inglês.\n\n"
                f"2) {questions_pt[2]}"
            )
            return output, output, hidden_pt, None
            
        elif stage == 2:
            profile["interview_stage"] = 3
            output = (
                "Nice. Let's assess a verbal construction now.\n\n"
                f"3) {questions[3]}"
            )
            hidden_pt = (
                "Legal. Vamos avaliar uma construção verbal agora.\n\n"
                f"3) {questions_pt[3]}"
            )
            return output, output, hidden_pt, None
            
        elif stage == 3:
            profile["interview_stage"] = 4
            output = (
                "Excellent. Now tell me what specific situation you want to practice.\n\n"
                f"4) {questions[4]}"
            )
            hidden_pt = (
                "Excelente. Agora me diga qual situação específica você quer praticar.\n\n"
                f"4) {questions_pt[4]}"
            )
            return output, output, hidden_pt, None
            
        elif stage == 4:
            profile["practice_topic"] = pending_response
            profile["interview_stage"] = 5
            output = (
                "Perfect! Now tell me the specific subtopic within that area.\n\n"
                f"5) {questions[5]}"
            )
            hidden_pt = (
                "Perfeito! Agora me diga o subtema específico dentro dessa área.\n\n"
                f"5) {questions_pt[5]}"
            )
            return output, output, hidden_pt, None
            
        elif stage == 5:
            profile["practice_subtopic"] = pending_response
            profile["interview_stage"] = 6
            
            # Gera o roadmap
            answer_description = profile["interview_responses"][1]["answer"]
            answer_construction = profile["interview_responses"][2]["answer"]
            specific_context = profile["interview_responses"][3]["answer"]
            goal = profile["goal"] or "aprender inglês"
            
            final_prompt_text = final_prompt.format(
                goal=goal,
                answer_description=answer_description,
                answer_construction=answer_construction,
                specific_context=specific_context
            )
            
            completion = client.chat.completions.create(
                model=os.getenv("MODEL_NAME"),
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt_text
                    }
                ],
                temperature=0.2
            )
            
            summary = completion.choices[0].message.content
            roadmap_text = parse_final_response(summary)
            
            profile["roadmap"] = roadmap_text
            
            output = (
                "Thank you! I created a short roadmap for you based on your answers.\n\n"
                f"{roadmap_text}\n\n"
                "Do you want to see the essential words and sentence structures for practicing this topic?"
            )
            hidden_pt = (
                "Obrigado! Criei um pequeno roadmap para você com base em suas respostas.\n\n"
                "Quer ver as palavras essenciais e estruturas de frases para praticar este tópico?"
            )
            buttons = [
                {"id": "confirm", "text": "✅ Yes, show me"},
                {"id": "retry", "text": "⏭️ Not yet"}
            ]
            return output, output, hidden_pt, buttons
    
    elif action == "retry":
        # Limpa a resposta pendente e pede para tentar novamente
        profile["pending_response"] = None
        
        if stage <= 5:
            output = f"No problem! Let's try again.\n\n{questions[stage]}"
            hidden_pt = f"Tudo bem! Vamos tentar de novo.\n\n{questions_pt[stage]}"
            return output, output, hidden_pt, None
        elif stage == 6:
            output = "No problem! Just let me know when you're ready. Do you want to see the practice list?"
            hidden_pt = "Tudo bem! Me avise quando estiver pronto. Quer ver a lista de prática?"
            buttons = [
                {"id": "confirm", "text": "✅ Yes, show me"},
                {"id": "retry", "text": "⏭️ Not yet"}
            ]
            return output, output, hidden_pt, buttons
    
    return None, None, None, None