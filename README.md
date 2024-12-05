# RAG ReRanker 🤖

> Implementation of Compression RAG techniques to teach GPT about Escape from Tarkov ammo items.

## Tools

The project uses the following tools to work:

- [LangChain](https://python.langchain.com/docs/introduction/)
- [Chroma as Vector DB](https://www.trychroma.com/)
- [GPT 3.5 Turbo as LLM](https://platform.openai.com/docs/models#gpt-3-5-turbo)
- [Cohere Rerank](https://cohere.com/rerank)
- [ADA 002 for Text Embedding](https://platform.openai.com/docs/models#embeddings)

## Running

To run the project first create a new Python environment and activate it. I'm using [Anaconda](https://www.anaconda.com/) for setting the python version that pipenv should use to set up the environment. The command bellow will automatically setup the environment with conda and pipenv:

```shell
make env
```

Now install all the project dependencies:

```shell
make install-all
```

Clone the repositories you want the model to code review:

```shell
make clone
```

Insert the file chunks in Chroma database by running:

```shell
make insert 
```

Ask something by running the following:

```shell
make ask
```

You can change your question inside `bin/ask.py`.
