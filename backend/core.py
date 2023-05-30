import os
from typing import Any, Dict, List

from langchain.embeddings       import OpenAIEmbeddings
from langchain.chat_models      import ChatOpenAI
from langchain.chains          import ConversationalRetrievalChain
from langchain.vectorstores     import Chroma
#from langchain.llms            import OpenAI
from langchain.chains          import RetrievalQA
from langchain.prompts         import PromptTemplate
# Import Azure OpenAI
from langchain.llms           import AzureOpenAI

# Create an instance of Azure OpenAI
# Replace the deployment name with your own

os.environ["OPENAI_API_TYPE"]    = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"]    = os.getenv("AZURE_OPENAI_ENDPOINT") 
os.environ["OPENAI_API_KEY"]    = os.getenv("AZURE_OPENAI_KEY")

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer in Korean:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

persist_directory = './vectordb'
#embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"] )
embeddings = OpenAIEmbeddings( chunk_size=1 )

# load the persisted database from disk, and use it as normal. 
vectordb  = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectordb.as_retriever( search_kwargs={"k":4} )

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Dict[str, Any]:

    chat = AzureOpenAI(
        deployment_name="unibot",
        model_name="gpt-35-turbo",
        max_tokens=512,
        temperature=0
    )

    chain_type_kwargs = {"prompt": PROMPT}
    
    qa = RetrievalQA.from_chain_type( llm=chat, 
        chain_type="stuff", 
        retriever= retriever, 
        chain_type_kwargs=chain_type_kwargs, 
        return_source_documents=True)

    return qa({"query": query , "chat_history": chat_history})

def run_llm2(query: str):

    chat = ChatOpenAI(
        verbose=True,
        temperature=0.1,
        model_name="gpt-3.5-turbo", 
        max_tokens=370
    )

    chain_type_kwargs = {"prompt": PROMPT}
    
    qa = RetrievalQA.from_chain_type( llm=chat, 
        chain_type="stuff", 
        retriever= retriever, 
        chain_type_kwargs=chain_type_kwargs, 
        return_source_documents=True)

    return qa({"query": query })