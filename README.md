# Chat with your pdf

This is a simple chat application that interacts with your documents, powered by LangChain and OpenAI. This project serves as a Retrieval-Augmented Generation (RAG) example.

## Prerequisites

To use this application, you will need:

- An OpenAI API account
- A LangChain account (for LangSmith integration, if desired)
- Python 3.11.9

## Setup

1. **Venv and dependencies**

   In terminal go to project's root folder and activate venv:
   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
  
   Install the necessary dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env File**

   Create a `.env` file in the root directory of your project with the following variables:

   ```plaintext
   OPENAI_API_KEY=<YOUR_KEY>
   ```

   If you would like to enable integration with LangSmith, add these additional variables:

   ```plaintext
   LANGCHAIN_API_KEY=<YOUR_KEY>
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_PROJECT=<YOUR_PROJECT_KEY>
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   ```

4. **Default Document**

   By default, the project loads "The Ultimate History of Video Games" book by Steven L. Kent. You can ask any question regarding this exciting topic!

5. **Customization**

   - **Constants File**: You can change values in the `constants.py` file to use a different URI for your document.
   - **Data Folder**: Alternatively, upload your own documents to the `data` folder and load them from there.

6. **First Query**

   Note that because of initial creating vectore store, the first query may take longer to process, depending on the size of your documents. For example, the default video game history book is 624 pages long, so please be patient.

7. **Run**

   To run app just 
