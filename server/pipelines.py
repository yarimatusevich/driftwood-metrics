# from typing import Tuple, Optional

from llm import Hermes2Pro
from sentiment import Finbert
# from data_models import StockSnapshot
from finance_data import create_stock_snapshot
from vectorstore import VectorstoreManager

from langchain_core.runnables import RunnableLambda, Runnable

def create_chain() -> Runnable:
    create_snapshot = RunnableLambda(lambda ticker_sym: create_stock_snapshot(ticker_symbol=ticker_sym))

    finbert = Finbert()
    sentiment_model = RunnableLambda(lambda snapshot: finbert.invoke(snapshot=snapshot))

    vectorstore_manager = VectorstoreManager()
    update_vectorspace = RunnableLambda(lambda snapshot: vectorstore_manager.add_articles_to_vectorstore(snapshot=snapshot))
    retrieve_documents = RunnableLambda(lambda snapshot: vectorstore_manager.retrieve_documents(snapshot=snapshot))

    hermes = Hermes2Pro()
    llm = RunnableLambda(lambda data_bundle: hermes.invoke(input=data_bundle))

    return create_snapshot | sentiment_model | update_vectorspace | retrieve_documents | llm

chain = create_chain()

while True:
    # Getting user input
    user_in = input("Write a ticker: \n").upper()

    if user_in == "Q":
        break

    res = chain.invoke(user_in)

    print(res)