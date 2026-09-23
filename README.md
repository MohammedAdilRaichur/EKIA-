# Enterprise Knowledge Intelligence Agent (EKIA)

## Project Overview

### Project Name
**Enterprise Knowledge Intelligence Agent (EKIA)**

### Short Description
An AI-powered enterprise knowledge assistant for a fictional company called **NovaTech Solutions**. It allows employees to query organizational knowledge spanning HR, IT, Finance, and Engineering policies via a natural language interface.

### Problem Statement
Organizations store large amounts of knowledge in disconnected sources (policies, SOPs, FAQs, structured databases). Employees often need to manually search through these disjointed sources to find answers. 

### Objective
Build a sophisticated agentic AI system that goes beyond a basic "chat with PDF" app. The EKIA will retrieve relevant enterprise documents, reason across multiple sources, query structured databases, utilize tools (like a calculator), provide grounded answers, and cite its sources—all while enforcing enterprise access controls and reducing hallucinations.

---

## Tech Stack

### Programming Languages
- Python 3.11+

### Frameworks / Libraries
- **Backend**: FastAPI
- **Agent Framework**: LangGraph
- **Frontend**: Streamlit
- **Document Processing**: PyMuPDF (or equivalent)
- **Machine Learning / NLP**: PyTorch / Hugging Face

### AI/ML Models
- **LLM**: Configurable (e.g., OpenAI, Anthropic, or open-source)
- **Embeddings**: Configurable Hugging Face / Open-source models (e.g., `all-MiniLM-L6-v2`)

### Database
- **Vector Database**: Chroma (Initial) with future migration path to Qdrant
- **Structured Database**: PostgreSQL (for SQL querying capabilities)

---

## System Architecture

### Simple Architecture Diagram

```text
                         USER
                           |
                           v
                    +-------------+
                    |  AI AGENT   |
                    +------+------+
                           |
                    Understand Intent
                           |
              +------------+------------+
              |                         |
              v                         v
       Knowledge Search             Tool Selection
              |                         |
              v              +----------+----------+
        Vector Database      |          |          |
              |              v          v          v
              |             SQL      Calculator  Document
              |             Tool        Tool       Tool
              |              |          |          |
              +--------------+----------+----------+
                             |
                             v
                      Context Assembly
                             |
                             v
                       LLM Reasoning
                             |
                             v
                    Grounded Response
                             |
                    +--------+--------+
                    |                 |
                    v                 v
                Citations         Confidence
```

### Input → Processing → Output

**1. Input (What the user gives):**
A natural language query. (e.g., "I'm going to Bangalore for 5 days. What accommodation expenses can I claim and what documents do I need?")

**2. Processing (What happens internally):**
- **Intent Detection**: The Agent interprets the question.
- **Tool Selection**: The Agent chooses between Document Search, SQL Query, Calculator, etc.
- **Retrieval**: If searching documents, it embeds the query and searches the Vector DB (Chroma) for relevant chunks, enforcing metadata and RBAC filters.
- **Multi-Step Reasoning**: The Agent extracts values (e.g., ₹4000/day allowance) and uses the Calculator tool (₹4000 * 5) to compute totals.
- **Synthesis**: The LLM constructs a final grounded response with exact citations based on retrieved context.

**3. Output (What the system produces):**
A well-reasoned, factual response containing exact calculations, instructions, and explicit citations to internal policies.

---

## Project Structure

```
EKIA/
├── app/
│   └── config.py          # Application configuration management
├── data/
│   ├── documents/         # Synthetic enterprise documents (PDFs)
│   ├── database/          # SQLite/PostgreSQL structured data
│   └── vectorstore/       # Chroma database storage
├── frontend/
│   └── streamlit_app.py   # Streamlit user interface
├── tests/                 # Unit tests for tools and agent logic
├── evaluation/            # Evaluation datasets and scripts
├── venv/                  # Python virtual environment (ignored in git)
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore list
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## Dataset / Data Sources

### Dataset / Source
Synthetic enterprise documents for a fictional company (**NovaTech Solutions**) spanning multiple departments: Engineering, HR, Finance, IT, Sales, Operations, and Company-wide.

### Number / Type of Data
- Multiple fictional PDFs (e.g., `travel_policy.pdf`, `remote_work_policy.pdf`, `vpn_guide.pdf`).
- Fictional tabular data for the SQL database tool (employees, departments, projects, expenses).

### Preprocessing
- Text extraction from PDFs.
- Semantic chunking (preserving headings, paragraphs, tables).
- Metadata tagging (`document_name`, `department`, `section`, `access_level`).

---

## Model / Algorithms

### Models Used
- **Embeddings**: Open-source sentence transformers (e.g., `all-MiniLM-L6-v2`) via Hugging Face. Used for creating robust semantic vector representations of enterprise knowledge.
- **LLM**: Any state-of-the-art conversational LLM (e.g., GPT-4o, Claude 3.5 Sonnet, or Llama 3) for reasoning and text generation.

### Why They Were Chosen
- Local open-source embeddings allow fast, secure processing of documents without sending sensitive data over the internet.
- A configurable LLM provider allows flexibility and future-proofing the enterprise stack.

### Important Concepts / Algorithms
- **Retrieval-Augmented Generation (RAG)**: Grounding LLM responses in factual, retrieved data to eliminate hallucinations.
- **Semantic Vector Search**: Using Cosine Similarity/Euclidean distance to find relevant knowledge chunks.
- **ReAct (Reasoning + Acting)**: The agent loop paradigm used by LangGraph to determine when to use specific tools (Search vs. SQL vs. Math).

---

## How to Install & Run

**1. Clone the repository**
```bash
git clone https://github.com/MohammedAdilRaichur/EKIA-.git
cd EKIA-
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
*(Edit `.env` to include your required API keys if applicable)*

**5. Run the Streamlit Application (Milestone 1)**
```bash
streamlit run frontend/streamlit_app.py
```

---

## Results
*Note: Results will be populated in later milestones.*
The system is currently in **Milestone 1 (Project Setup)**. Once Milestone 4 (RAG) and Milestone 10 (Evaluation) are completed, this section will detail retrieval accuracy, factual faithfulness, and evaluation scores based on the 50-100 question testing framework.

---

## Limitations & Future Scope

### Current Limitations
- Pure semantic search can struggle with exact keyword matches (IDs, specific codes).
- Relying on basic chunking might split complex tables across chunks.
- Does not currently integrate with live internal APIs (Slack, Jira, etc.).

### Future Scope (Extensions)
- **Hybrid Search**: Combine vector semantic search with BM25 keyword search.
- **Reranking**: Implement a cross-encoder reranker for higher retrieval precision.
- **Graph-based Retrieval**: Build a Knowledge Graph for complex entity relationships.
- **Multimodal Support**: Understand diagrams, flowcharts, and embedded images in enterprise PDFs.
- **Enterprise Integrations**: Connect directly to Slack/Teams for conversational interaction inside the workspace.
