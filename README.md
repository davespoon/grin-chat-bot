# Document Chat Application

This is a simple chat application that interacts with your documents, powered by LangChain and OpenAI. This project serves as a Retrieval-Augmented Generation (RAG) example.

## Prerequisites

To use this application, you will need:

- An OpenAI API account
- A LangChain account (for LangSmith integration, if desired)

## Setup

1. **Install Dependencies**

   Install the necessary dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create .env File**

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

3. **Default Document**

   By default, the project loads "The Ultimate History of Video Games" book by Steven L. Kent. You can ask any question regarding this exciting topic!

4. **Customization**

   - **Constants File**: You can change values in the `constants.py` file to use a different URI for your document.
   - **Data Folder**: Alternatively, upload your own documents to the `data` folder and load them from there.

5. **First Query**

   Note that because of initial creating vectore store, the first query may take longer to process, depending on the size of your documents. For example, the default video game history book is 624 pages long, so please be patient.

6. **Enjoy!**

   Have fun exploring and interacting with your documents!
