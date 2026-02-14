import { useMemo, useState } from "react";
import "./App.css";

export default function App() {
  const [question, setQuestion] = useState("Can this drug cause dizziness?");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const apiBase = useMemo(() => "http://127.0.0.1:8000", []);

  async function onAsk() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(`${apiBase}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`API error ${res.status}: ${text}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e?.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: 16, fontFamily: "Arial" }}>
      <h2>Medical Drug GenAI POC</h2>
      <p style={{ opacity: 0.8 }}>
        React UI (Amplify-ready) → FastAPI → RAG Flow → Answer with citations
      </p>

      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about a drug..."
          style={{
            flex: 1,
            padding: 12,
            borderRadius: 8,
            border: "1px solid #ccc",
            fontSize: 16,
          }}
        />
        <button
          onClick={onAsk}
          disabled={loading || !question.trim()}
          style={{
            padding: "12px 18px",
            borderRadius: 8,
            border: "none",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: 16,
          }}
        >
          {loading ? "Asking..." : "Ask"}
        </button>
      </div>

      {error && (
        <div style={{ marginTop: 16, color: "crimson" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div style={{ marginTop: 20, padding: 16, border: "1px solid #ddd", borderRadius: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
            <div><strong>Mode:</strong> {result.mode}</div>
          </div>

          <h3 style={{ marginTop: 14 }}>Answer</h3>
          <p style={{ lineHeight: 1.5 }}>{result.answer}</p>

          <h3>Citations</h3>
          {result.citations?.length ? (
            <ul>
              {result.citations.map((c, idx) => (
                <li key={idx}>
                  doc_id: <code>{c.doc_id}</code>, chunk_id: <code>{c.chunk_id}</code>
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ opacity: 0.8 }}>No citations</p>
          )}

          {result.retrieved_context_preview && (
            <>
              <h3>Retrieved Context Preview</h3>
              <pre style={{ whiteSpace: "pre-wrap", background: "#f7f7f7", padding: 12, borderRadius: 8 }}>
                {result.retrieved_context_preview}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}
