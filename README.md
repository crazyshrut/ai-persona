# Shruti Verma — AI Persona

An AI persona that you can call (voice) or chat with (text), grounded on my real resume and GitHub repos. Built for the AI Engineer role hiring assignment.

## Live Links

| What | Link |
|------|------|
| 📞 Voice Agent | Call: `+1 (475) 222 2334` (powered by Vapi.ai) |
| 💬 Chat Interface | [Chat URL](https://huggingface.co/spaces/crazyshrut/shruti_ai_persona_teller) |
| 📅 Book a Call | [cal.com/shruti.verma](https://cal.com/shruti.verma) |

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   VOICE (Part A)                │
│                                                 │
│  Phone Call → Vapi.ai Agent → Knowledge Base    │
│                    ↓                            │
│              Cal.com API (booking)              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│                   CHAT (Part B)                 │
│                                                 │
│  User → Streamlit UI → LangChain RAG Chain      │
│                            ↓                    │
│                   ChromaDB Vector Store          │
│                  (resume + GitHub data)          │
│                            ↓                    │
│                  Groq LLM (Llama 3.3 70B)       │
│                            ↓                    │
│                Cal.com link (booking)            │
└─────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Tool | Why |
|-----------|------|-----|
| Voice Agent | Vapi.ai | Fast response, built-in phone numbers, Cal.com integration |
| Chat LLM | Groq (Llama 3.3 70B) | Free tier, fast inference |
| Embeddings | Google Gemini | Free tier, good quality |
| Vector Store | ChromaDB | Simple, in-memory, no setup |
| Chat UI | Streamlit | Quick to build, free hosting |
| Calendar | Cal.com | Free, API access |
| Deployment | Streamlit Cloud | Free public URL |

## RAG Pipeline

The chat persona is **RAG-grounded** — it reads from:
- `data/resume.txt` — my full resume in plain text
- `data/github_repos.txt` — info about my GitHub repos (tech, purpose, tradeoffs)

Documents are chunked (500 chars, 50 overlap), embedded, and stored in ChromaDB. On each question, the top 4 relevant chunks are retrieved and fed to the LLM along with the question.

The system prompt instructs the LLM to:
- Answer ONLY from the context (no hallucination)
- Say "I don't know" when info is missing
- Be conversational, not robotic

## Setup (Run Locally)

### Prerequisites
- Python 3.9+
- A Groq API key (free at console.groq.com) OR Google AI API key (free at aistudio.google.com)

### Steps

```bash
# clone
git clone https://github.com/crazyshrut/ai-persona.git
cd ai-persona

# install deps
pip install -r requirements.txt

# set API key (pick one)
set GROQ_API_KEY=your_key_here
# OR
set GOOGLE_API_KEY=your_key_here

# run
streamlit run app.py
```

## Voice Agent Setup (Vapi.ai)

1. Create account at vapi.ai
2. Create a new agent with the system prompt from `vapi_prompt.txt`
3. Upload `data/resume.txt` as knowledge base
4. Add Cal.com integration (check availability + book appointment functions)
5. Buy/assign a phone number to the agent
6. Test by calling

## Project Structure

```
ai-persona/
├── app.py                 # Streamlit chat interface
├── rag_engine.py          # RAG pipeline (LangChain + ChromaDB)
├── requirements.txt       # Python dependencies
├── vapi_prompt.txt        # System prompt for voice agent
├── evals_report.md        # Evaluation report
├── data/
│   ├── resume.txt         # Resume data for RAG
│   └── github_repos.txt   # GitHub repos data for RAG
└── README.md
```

## Author

**Shruti Verma**
- GitHub: [@crazyshrut](https://github.com/crazyshrut)
- Email: shrutiverma032003@gmail.com
