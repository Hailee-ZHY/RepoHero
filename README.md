# RepoHero

RepoHero is a repository question-answering project built with retrieval-augmented generation (RAG). It indexes Python files from a target repository, retrieves relevant code chunks, and uses an LLM to answer questions about the codebase.

## Project Structure

- [main.py](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/main.py):  the main script for running RepoHero. It indexes a repository first, then lets you ask questions about the codebase in the terminal.
- [test.py](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/test.py): evaluation script for running test questions against a repository
- [retriever.py](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/retriever.py): two-stage retriever used by the biencoder mode
- [chunker](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/chunker): AST-based chunking module
- [web/backend/app.py](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/web/backend/app.py): Flask backend for the web app
- [web/frontend](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/web/frontend): React + Vite frontend
- [data](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/data): CSV files used for evaluation

## Requirements

- Python 3.10+
- Node.js and npm for the frontend
- [Ollama](https://ollama.com/) running locally

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd web/frontend
npm install
```

## Ollama Models

The project expects the following models to be available in Ollama:

```bash
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
ollama pull llama3.1:8b
```

If you use the biencoder mode, the project also downloads Hugging Face models through Python libraries when needed.

## Run the Main CLI

From the project root:

```bash
python main.py
```
You will be prompted to enter the path of repo you want to explore.

To use the two-stage retriever instead of the baseline Ollama embedding retriever:

```bash
python main.py --biencoder
```

What this does:

- indexes Python files in the target repository
- stores chunks in ChromaDB
- lets you ask questions interactively in the terminal

## Run Evaluation

Before running the evaluation, please clone a target repository to your local machine, as the system evaluates over a local codebase.
For testing, we cloned and used repositories [FastAPI](https://github.com/fastapi/fastapi), [Pydantic](https://github.com/pydantic/pydantic), and [Requests](https://github.com/request/request).

Use [test.py](/c:/Users/wenry/Documents/CMPT-713-NLP/nlpclass-1261-g-TokenBurgers/RepoHero/test.py) to evaluate RepoHero on a CSV file containing `question` and `expected_answer` columns.

Example:

```bash
python test.py
```

To evaluate the biencoder version:

```bash
python test.py --biencoder
```

Evaluation results are written to:

```text
output/results.csv
```

## Run the Web App

Start the backend from the project root:

```bash
python web/backend/app.py
```

The backend runs at:

```text
http://127.0.0.1:5001
```

Start the frontend in a second terminal:

```bash
cd web/frontend
npm install
npm run dev
```

The frontend usually runs at:

```text
http://localhost:5173
```

## Notes

- RepoHero currently focuses on Python repositories.
- ChromaDB files are stored locally in folders such as `chroma_db/`.
- The default chunking method in `main.py` uses the AST-based chunker.
- During indexing, RepoHero ignores Python files whose names contain test
