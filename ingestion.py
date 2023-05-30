import os, glob
import pandas as pd
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders import ReadTheDocsLoader, PyPDFDirectoryLoader
from langchain.embeddings      import OpenAIEmbeddings
from langchain.text_splitter   import RecursiveCharacterTextSplitter
from langchain.text_splitter   import CharacterTextSplitter
from langchain.vectorstores    import Chroma

persist_directory = './vectordb'
documents = []  # 전역 documents 리스트 생성
    
def ingest_html():
    # read urls from *.csv file
    file_path = './bskssitemapv1.csv'
    df = pd.read_csv(file_path)
    url_list = df.iloc[:,0].tolist()
    print( url_list )
    
    loaders = UnstructuredURLLoader(urls=url_list)
    raw_data = loaders.load()

    # Text Splitter
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=800, chunk_overlap=80)
    docs_html = text_splitter.split_documents(raw_data)

    # Remove excessive tab characters from docs_html
    for doc in docs_html:
       doc.page_content = doc.page_content.replace('\t', '')
       doc.page_content = doc.page_content.replace('\r\n', ' ')     
       doc.page_content = doc.page_content.replace('\n\n', ' ')
       
    # 749 documents   
    print(f"split {len(docs_html)} documents")
    print( docs_html[150] )
    documents.extend( docs_html )

def ingest_docs():
    # Define the directory and file pattern
    directory = './data'
    file_pattern = "*.pdf"

    # Use os.path.join to combine the directory and file pattern
    search_path = os.path.join(directory, file_pattern)

    # Use glob.glob to find all matching files
    pdf_files = glob.glob(search_path)

    text_data = []
    # Print each file path
    for file_path in pdf_files:
        print(file_path)
        loader = PyMuPDFLoader(file_path)
        doc = loader.load()
        text_data = text_data + doc 
    
    raw_documents = text_data

    text_splitter = RecursiveCharacterTextSplitter( chunk_size=800, chunk_overlap=80 )
    docs_pdf      = text_splitter.split_documents(raw_documents)
    
    print(f"split {len(docs_pdf)} documents")	
    print( docs_pdf[100] )	
    documents.extend( docs_pdf )    

def addDocsToChroma():
    # model 'text-embedding-ada-002' , token limit 8K
    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Chroma")
    print( documents[100] )	
	
    vectordb = Chroma.from_documents( documents, embeddings , persist_directory=persist_directory )
    vectordb.persist()
    vectordb = None
	
    print("****Loading to vectorestore done ***")     
    
if __name__ == "__main__":
    ingest_docs()
    ingest_html()
    addDocsToChroma()