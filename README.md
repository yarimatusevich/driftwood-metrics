# Driftwood Metrics
## Local-first financial analysis with AI-driven insights

### Description
Driftwood’s Python backend uses yFinance, a Yahoo Finance API wrapper, to retrieve historical stock data. This data is then processed entirely on your local machine using lightweight AI models.

The analysis pipeline consists of two main steps:

1.  Sentiment Analysis with FinBERT
    Driftwood collects news articles related to a given stock and analyzes their titles and summaries using FinBERT, a transformer model fine-tuned for financial sentiment analysis. The resulting sentiment scores are embedded as vectors and stored locally for efficient retrieval.

2.  Contextual Insights with an LLM
    Driftwood then uses a quantized large language model based on Hermes 2 Pro. During this step the application employs retrieval-augmented generation (RAG), using the stored sentiment vectors to produce more accurate and relevant insights about a given stock.

## Tech stack
### Frontend
Next.js + React + TypeScript
CSS

### Backend
Python
Flask
LangChain
Transformers

## 🛠️ Installation
**Folder structure:**  
- `client/` – contains all frontend (Next.js) code  
- `server/` – contains all backend (Flask + AI models) code
---

### 🔧 Setup Steps

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yarimatusevich/driftwood-metrics.git
   cd driftwood-metrics
2. Open the destination folder of the cloned repo with two terminals
3. With one terminal use the following commands to run the frontend server
   ```bash
   cd client
   npm install
   npm run dev

4. With the other terminal use the following commands to run the backend server
   ```bash
   cd server
   pip install -r requirements.txt
   python app.py

With both servers running, ensure that both terminals remain open and access the following urls in your browser:

Frontend: http://localhost:3000
Backend: http://localhost:5000

To terminate the servers use ctrl + c in their respective terminals.
