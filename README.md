# Company Knowledge Agent

A Python application for finding answers in company documents with traceable sources.

## Stage 1: document search

This first milestone loads Markdown and text documents, splits them into paragraphs, and ranks passages using keyword overlap. Results include filenames and line numbers. It runs locally with Python 3.11+ and has no API costs or external dependencies.

**This stage is a search foundation, not yet an LLM agent or semantic RAG system.** AI-generated answers, embeddings, PostgreSQL/pgvector, and a web interface are planned next.

## Quick start

```bash
git clone https://github.com/ZaidFareed/company-knowledge-agent.git
cd company-knowledge-agent
python -m knowledge_agent "How many days of annual leave do employees get?"
python -m unittest discover -s tests -v
```

On Windows, use `py` instead of `python` if necessary.

## Your documents

```bash
python -m knowledge_agent "What is the remote work policy?" --docs /path/to/documents --limit 3
```

Only `.md` and `.txt` files are supported in this milestone. Files must use UTF-8 encoding. PDF support will be added later. Keep confidential documents outside this public repository. The included policies are fictional demonstration data.

## How it works

1. Read documents from the chosen folder.
2. Split text at blank lines, preserving source line ranges.
3. Rank paragraphs by the fraction of distinct question terms they contain, ignoring common filler words.
4. Print matching passages and source references, or report no matches.

Keyword matches do not prove a passage answers the question. Synonyms, negation, and multi-document questions are limitations of this initial baseline.

## Next milestones

- Add embeddings and PostgreSQL/pgvector retrieval.
- Generate grounded answers with validated citations and abstention.
- Add a FastAPI backend and document upload interface.
- Evaluate supported and unsupported questions with a fixed dataset.
- Add LangGraph when branching or persistent workflow state is needed.
