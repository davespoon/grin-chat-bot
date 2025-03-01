from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

base_template = """
Use the following context to answer the question at the end.
If you don't know the answer, replay "I don't know", do not make up an answer.
Context: {context}

Question: {input}
"""

contextualize_q_system_prompt = """
Given a chat history and the latest user question 
which might reference context in the chat history, formulate a standalone question
which can be understood without the chat history. Do NOT answer the question,
just reformulate it if needed and otherwise return it as is.
"""

qa_system_prompt = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.
{context}
"""

extract_info_from_cv = ChatPromptTemplate.from_template(
    """
    You are an AI specialized in extracting structured information from resumes. Analyze the provided resume text and extract the following details in JSON format:
    - **name**: Full name of the candidate.
    - **email**: Email address.
    - **phone**: Phone number.
    - **summary**: A brief summary or objective statement of the candidate.
    - **education**: An array of educational qualifications, including degrees, institutions, and graduation dates.
    - **experience**: An array of work experiences, including job titles, company names, durations, and key responsibilities.
    - **skills**: An array of key skills and proficiencies relevant to the candidate's field.
    - **another_useful_information**: Any additional pertinent information not covered above, such as certifications, languages spoken, volunteer work, or notable projects.

    **Important Guidelines:**

    1. **No Assumptions**: Only extract information explicitly stated in the resume. If a specific detail is not present, omit that field from the JSON output.
    2. **Additional Information**: Include any other valuable details under "another_useful_information" to provide a comprehensive view of the candidate's qualifications.


    CV Content:
    {cv_text}

    {format_instructions}
    """
)
