from dependency_injector.wiring import inject, Provide
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import VectorStore
from langsmith import Client

import constants
from containers import Container
from prompts import prompt_templates

chat_history = []


@inject
def response(human_input,
             chroma_db: VectorStore = Provide[Container.chroma_db],
             chat_openai: BaseChatModel = Provide[Container.chat_openai]):
    langchain_client = Client
    vectorstore = chroma_db
    retriever = vectorstore.as_retriever(search_type=constants.SEARCH_TYPE,
                                         search_kwargs={"k": constants.SEARCH_K})
    model = chat_openai

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_templates.contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        model, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt_templates.qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    response_msg = rag_chain.invoke({"input": human_input, "chat_history": chat_history})

    chat_history.append(HumanMessage(content=human_input))
    chat_history.extend([HumanMessage(content=human_input), response_msg["answer"]])
    if len(chat_history) > constants.CHAT_HISTORY_SIZE:
        chat_history.pop(0)

    return response_msg["answer"]
