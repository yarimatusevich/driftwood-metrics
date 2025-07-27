import os

from data_models import StockSnapshot

from sentence_transformers import SentenceTransformer

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

class VectorstoreManager():
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        self.folder_path = "faiss_index"
        self._load_vectorstore
    
    def _load_vectorstore(self):
        if os.path.exists(self.folder_path):
            self.vectorstore = FAISS.load_local(folder_path=self.folder_path, embeddings=self.embedding_model)
        else:
            self.vectorstore = None
    
    def add_articles_to_vectorstore(self, snapshot: StockSnapshot) -> StockSnapshot:
        docs = self.convert_articles_to_documents(input=snapshot)

        if self.vectorstore:
            self.vectorstore.add_documents(docs)
        else:
            self.vectorstore = FAISS.from_documents(documents=docs, embedding=self.embedding_model)
        
        self.vectorstore.save_local(folder_path=self.folder_path)

        return snapshot
    
    def convert_articles_to_documents(self, input: StockSnapshot) -> list[Document]:
        articles = input.sentiment.articles
        documents = []
        
        for article in articles:
            new_doc = Document(
                page_content=article.summary,
                metadata={
                        "title": article.title,
                        "sentiment": article.sentiment.label,
                        "url": article.url
                }
            )
            documents.append(new_doc)

        return documents
    
    def retrieve_documents(self, snapshot: StockSnapshot) -> tuple[str, StockSnapshot]:
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized, add documents first.")

        # retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        retriever = self.vectorstore.as_retriever()
        query = snapshot.profile.name
        docs = retriever.invoke(query)

        context = self.process_docs(docs)

        return (context, snapshot)
    
    def process_docs(self, docs: list[Document]) -> str:
        context = []

        for doc in docs:
            context.append(doc.page_content)
        
        return " ".join(context)