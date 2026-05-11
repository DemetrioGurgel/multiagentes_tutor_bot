from langchain_community.chat_message_histories import ChatMessageHistory

# memória por usuário
user_memories = {}

def get_memory(user_id):

    if user_id not in user_memories:

        user_memories[user_id] = ChatMessageHistory()

    return user_memories[user_id]