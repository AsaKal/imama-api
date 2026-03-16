from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool



def indexing():
    # load retrievers
    urls = [
        "https://ada.com/sw/conditions/urinary-tract-infection/",
        "https://www.ulyclinic.com/elimu-kwa-mjamzito-magonjwa/uti-kwa-mjamzito",
        "https://globalpublishers.co.tz/hatari-ya-maambukizi-ya-uti-kwa-mjamzito/",
        "https://bongoclass.com/uti-na-ujauzito-395"
    ]
    loader = WebBaseLoader(urls)
    docs = loader.load()

    embeddings = OpenAIEmbeddings()
    # build the index
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    docs = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(docs, embeddings)
    retriever1 = vector.as_retriever()

    file_loader = DirectoryLoader('docs/', glob="**/*.txt")
    file_docs = file_loader.load()
    # build the index
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=0)
    docs = text_splitter.split_documents(file_docs)
    vector = FAISS.from_documents(docs, embeddings)
    retriever2 = vector.as_retriever()

    # create tools
    retriever_tool1 = create_retriever_tool(
        retriever1,
        "uti_searcher1",
        "Use this tool to search for information on urinary tract infection."
        " Also use this, to score if a patient is in the risk or likelihood of getting the"
        " disease based on the symptoms given by the user. Do all this in swahili language",
    )
    retriever_tool2 = create_retriever_tool(
        retriever2,
        "uti_searcher2",
        "Use this tool to search for doctors' contacts."
    )

    return [retriever_tool1, retriever_tool2]



