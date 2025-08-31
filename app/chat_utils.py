# from euriai.langchain import create_chat_model
# from euriai import ChatEuri
# chat_model = ChatEuri()
# from euriai import ChatEuri




# chat_model = EuriaiChatModel(
#     api_key="euri-088f3f95ae17e68a8a5703efcddf13e801566cde7521d2d26a1ee9162380970b",
#     model="gpt-4.1-nano",
#     temperature=0.7
# )


# def get_chat_model(api_key: str):
#     return create_chat_model(api_key=api_key,
#                              model = "gpt-4.1-nano",
#                              temperature=0.7)
    
    
# def ask_chat_model(chat_model, prompt: str):
#     response = chat_model.invoke(prompt)
#     return response.content




from euriai.langchain import create_chat_model

def get_chat_model(api_key: str):
    """
    Returns a chat model via EuriAI's LangChain wrapper.
    Adjust model/temperature as needed.
    """
    return create_chat_model(api_key=api_key, model="gpt-4.1-nano", temperature=0.7)

def ask_chat_model(chat_model, prompt: str) -> str:
    """
    Sends a single-turn prompt to the model and returns string content.
    """
    resp = chat_model.invoke(prompt)
    # Some LangChain models return an object with .content
    return getattr(resp, "content", str(resp))