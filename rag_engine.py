import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    USE_GOOGLE = True
except ImportError:
    USE_GOOGLE = False

try:
    from langchain_groq import ChatGroq
    USE_GROQ = True
except ImportError:
    USE_GROQ = False


SYSTEM_PROMPT = """You are Shruti Verma's AI representative. You speak in first person as if you ARE Shruti.
You are a product-thinking techie girl who loves solving critical problems and has an interest in macro photography.

Rules:
- Answer based ONLY on the context provided below. Do not make up information.
- If you don't know something, say "Hmm I'm not sure about that, you can ask me directly at shrutiverma032003@gmail.com"
- Be conversational and friendly, like a real person chatting. Keep it natural.
- When talking about projects, mention the tech stack, purpose, and any tradeoffs you made.
- For questions about why you're a good fit - talk about your actual experience, not generic stuff.
- Don't be overly formal or salesy. Just be honest.
- If someone asks to book a call or about your availability, tell them to use the Cal.com link: https://cal.com/shruti.verma

Context from resume and GitHub:
{context}

Question: {question}

Answer:"""


def load_documents(data_dir):
    """load all txt files from the data directory"""
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            docs.extend(loader.load())
    return docs


def create_vector_store(docs, embeddings):
    """split docs into chunks and create chroma vector store"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n===\n", "\n---\n", "\n\n", "\n", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks from documents")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="shruti_persona"
    )
    return vectorstore


def get_embeddings():
    """get embedding model - uses google gemini free tier"""
    google_key = os.environ.get("GOOGLE_API_KEY", "")
    if USE_GOOGLE and google_key:
        print("Using Google Gemini embeddings (free tier)")
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=google_key
        )
    else:
        raise ValueError("GOOGLE_API_KEY is required for embeddings. Get one free at aistudio.google.com")


def get_llm():
    """get LLM - groq free tier or google free tier"""
    groq_key = os.environ.get("GROQ_API_KEY", "")
    google_key = os.environ.get("GOOGLE_API_KEY", "")

    if USE_GROQ and groq_key:
        print("Using Groq LLM (free tier)")
        return ChatGroq(
            model_name="llama-3.3-70b-versatile",
            groq_api_key=groq_key,
            temperature=0.3
        )
    elif USE_GOOGLE and google_key:
        print("Using Google Gemini LLM (free tier)")
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=google_key,
            temperature=0.3
        )
    else:
        raise ValueError("Set GROQ_API_KEY or GOOGLE_API_KEY. Both are free.")


def build_rag_chain(data_dir="data"):
    """build the full RAG chain"""
    docs = load_documents(data_dir)
    if not docs:
        raise ValueError(f"No documents found in {data_dir}")
    print(f"Loaded {len(docs)} documents")

    embeddings = get_embeddings()
    vectorstore = create_vector_store(docs, embeddings)
    llm = get_llm()

    prompt = PromptTemplate(
        template=SYSTEM_PROMPT,
        input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )
    return chain


def ask(chain, question):
    """ask a question to the RAG chain"""
    try:
        result = chain.invoke({"query": question})
        return result["result"]
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
