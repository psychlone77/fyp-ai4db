import os
import json
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from rag_question_generator import LLMRAGQuestionGenerator
from example_input import workload_features, query_plans, inner_metrics
load_dotenv()

# Load documents from resources folder
def load_documents(resources_path: str):
    """Load markdown files from resources folder"""
    loader = DirectoryLoader(
        resources_path,
        glob="*.md",
        show_progress=True
    )
    documents = loader.load()
    return documents

# Split documents into chunks
def create_chunks(documents):
    """Split documents into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

# Create embeddings and vector store
def create_vector_store(chunks, store_path: str = "faiss_index"):
    """Create FAISS vector store"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(store_path)
    return vector_store

# Load vector store
def load_vector_store(store_path: str = "faiss_index"):
    """Load existing FAISS vector store"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        store_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store

# Format documents helper
def format_docs(docs):
    """Format documents for context"""
    return "\n\n".join(doc.page_content for doc in docs)

# Create RAG chain (Simplified LCEL Pattern)
def create_rag_chain(vector_store):
    """Create RAG chain using LCEL (LangChain Expression Language)"""
    
    # Custom prompt for OLAP parameter extraction
    prompt_template = """Use the following context to extract OLAP workload parameters and their optimal values.
    
Context:
{context}

Question: {question}

Please provide:
1. Parameter name
2. Purpose/Description
3. Optimal value or range
4. Impact on OLAP performance
5. Trade-offs or considerations

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # Use Groq LLM
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        temperature=0.3
    )
    
    # Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    
    # Create chain using LCEL
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

# Query function
def query_olap_parameters(rag_chain, retriever, query: str):
    """Query the RAG system for OLAP parameters"""
    # Get answer
    answer = rag_chain.invoke(query)
    
    # Get source documents
    source_docs = retriever.invoke(query)
    
    return {
        "answer": answer,
        "source_documents": source_docs
    }

# Main execution
def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    resources_path = script_dir.parent / "resources"
    
    # Check if vector store already exists
    if os.path.exists("faiss_index"):
        print("Loading existing vector store...")
        vector_store = load_vector_store()
        print("Vector store loaded")
    else:
        # Step 1: Load documents
        print("Loading documents...")
        documents = load_documents(resources_path)
        print(f"Loaded {len(documents)} documents")
        
        # Step 2: Create chunks
        print("\nCreating chunks...")
        chunks = create_chunks(documents)
        print(f"Created {len(chunks)} chunks")
        
        # Step 3: Create vector store
        print("\nCreating vector store...")
        vector_store = create_vector_store(chunks)
        print("Vector store created and saved")
    
    # Step 4: Create RAG chain
    print("\nCreating RAG chain...")
    rag_chain, retriever = create_rag_chain(vector_store)

    # Step 5: Query examples
    generator = LLMRAGQuestionGenerator()
    queries = generator.generate_questions(
        workload_features, query_plans, inner_metrics
    )
   
    # queries = [
    #     "What parameters that mostly affect the query performance in OLAP workloads?",
    #     "What are the key OLAP tuning parameters and their recommended optimal values?",
        
    # ]
    
    print("\n" + "="*60)
    print("OLAP PARAMETER EXTRACTION RAG")
    print("="*60)
    
    # Prepare results list
    results = []
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        result = query_olap_parameters(rag_chain, retriever, query)
        print(f"Answer: {result['answer']}")
        print(f"\nSources: {[doc.metadata.get('source', 'Unknown') for doc in result['source_documents']]}")
        print("="*60)
        
        # Add to results list
        results.append({
            "query": query,
            "answer": result['answer'],
            "sources": [doc.metadata.get('source', 'Unknown') for doc in result['source_documents']]
        })
    
    # Save to JSON file
    output_file = script_dir / "rag_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()