# Driftwood Metrics
## Local-first financial analysis with AI-driven insights

### Description
Driftwood’s Python backend uses yFinance, a Yahoo Finance API wrapper, to retrieve historical stock data. This data is then processed entirely on your local machine using lightweight AI models.

The analysis pipeline consists of two main steps:

1.  Sentiment Analysis with FinBERT
    Driftwood collects news articles related to a given stock and analyzes their titles and summaries using FinBERT, a transformer model fine-tuned for financial sentiment analysis. The resulting sentiment scores are embedded as vectors and stored locally for efficient retrieval.

2.  Contextual Insights with an LLM
    Driftwood then uses a quantized large language model based on Hermes 2 Pro. During this step the application employs retrieval-augmented generation (RAG), using the stored sentiment vectors to produce more accurate and relevant insights about a given stock.

### Tech stack
### Installation
### Usage
