# Chat with Your Documents

This is a simple chat application that interacts with your documents, powered by LangChain and OpenAI. This project serves as a Retrieval-Augmented Generation (RAG) example.

## Prerequisites

To use this application, you will need:

- An OpenAI API account
- A LangChain account (for LangSmith integration, if desired)
- Python 3.13

## Setup

### 1. Install Poetry

Ensure that Poetry is installed on your system. If it's not installed, you can install it using the following command:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install Dependencies

Navigate to your project's root directory and install the dependencies:

```sh
poetry install
```

This command will create a virtual environment and install all required dependencies as specified in the `pyproject.toml` file.

### 3. Activate the Virtual Environment

To activate the virtual environment created by Poetry, use:

```sh
poetry shell
```

Alternatively, you can execute commands within the virtual environment without activating it:

```sh
poetry run <command>
```

### 4. Create a `.env` File

Create a `.env` file in the root directory of your project with the following variables:

```env
OPENAI_API_KEY=<YOUR_KEY>
```

If you would like to enable integration with LangSmith, add these additional variables:

```env
LANGCHAIN_API_KEY=<YOUR_KEY>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=<YOUR_PROJECT_KEY>
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### 5. Run the Application

Set the `PYTHONPATH` environment variable to your project's root path:

```sh
export PYTHONPATH=$(pwd):$PYTHONPATH  # On macOS/Linux
```

For Windows, set the `PYTHONPATH` environment variable accordingly.

Then, run the application:

```sh
poetry run python application/app.py
```

Your chat should be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 6. Default Document

By default, the project loads *The Ultimate History of Video Games* by Steven L. Kent. You can ask any questions regarding this exciting topic!

### 7. Customization

- **Constants File:** You can change values in the `constants.py` file to use a different URI for your document.
- **Data Folder:** Alternatively, upload your own documents to the `data` folder and load them from there.

### 8. First Query

Note that because of the initial creation of the vector store, the first query may take longer to process, depending on the size of your documents. For example, the default video game history book is 624 pages long, so please be patient.

### 9. Enjoy!

By following these steps, your project will be set up using Poetry, streamlining dependency management and virtual environment handling.
