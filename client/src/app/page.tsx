"use client";

import React, { useState } from "react";

interface StockResponse {
  decision: string;
  reasoning: string;
}

const StockSearch: React.FC = () => {
  const [stockName, setStockName] = useState<string>("");
  const [response, setResponse] = useState<StockResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!stockName) return;
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`http://127.0.0.1:5000/quote/${stockName.toUpperCase()}`);

      if (!res.ok) throw new Error("API request failed");

      const data: StockResponse = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
      setResponse(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", textAlign: "center" }}>
      <h2>Stock Analyzer</h2>

      <input
        type="text"
        placeholder="Enter stock symbol..."
        value={stockName}
        onChange={(e) => setStockName(e.target.value)}
        style={{ width: "70%", padding: "0.5rem", fontSize: "1rem" }}
      />

      <button
        onClick={handleSearch}
        style={{ padding: "0.5rem 1rem", marginLeft: "0.5rem" }}
      >
        Analyze
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {response && (
        <div style={{ marginTop: "2rem", textAlign: "left" }}>
          <h3>Decision: {response.decision}</h3>
          <p>
            <strong>Reasoning:</strong> {response.reasoning}
          </p>
        </div>
      )}
    </div>
  );
};

export default StockSearch;