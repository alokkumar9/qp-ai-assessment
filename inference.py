from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


# Load the language model
llm = OllamaLLM(model="llama3.2")
output_parser = StrOutputParser()
# Create a retrieval QA chain
prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an AI assistant expert in providing answers based on the given context.
        Say 'I do not know' if answer can't be found from the context.
     """),
    ("human", """Following is the context: 
     {context}
     
     Following is the query:
     {input}
    """)
])

def query_to_chain_with_chunks(retriever, query):

    # Create a document chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Create a retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Run the query
    response = retrieval_chain.invoke({"input": query})
    print(response)
    return response

