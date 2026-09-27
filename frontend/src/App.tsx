import { useState } from "react";

type Review = {
  summary: string;
  bugs: string[];
  performance: string[];
  quality: string[];
  suggestions: string[];
};

type AnalysisResult = {
  ast_analysis: {
    functions: string[];
    loops: number;
    nested_loops: number;
    builtin_shadowing: string[];
    bare_exceptions: number;
    issues: {
      type: string;
      severity: string;
      message: string;
    }[];
  };
  ai_review: Review;
};

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError("Please enter some Python code.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: code,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed");
      }

      if (data.error) {
        throw new Error(data.error);
      }

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1>CodeLens AI</h1>
        <p>AI-powered Python Code Review</p>
      </header>

      <main style={styles.container}>
        <section style={styles.editorSection}>
          <h2>Enter Python Code</h2>

          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder={`def process(data):
    for i in data:
        for j in data:
            print(i, j)`}
            style={styles.editor}
          />

          <button
            onClick={analyzeCode}
            disabled={loading}
            style={styles.button}
          >
            {loading ? "Analyzing..." : "Analyze Code"}
          </button>

          {error && <p style={styles.error}>{error}</p>}
        </section>

        {result && (
          <section style={styles.results}>
            <h2>Analysis Results</h2>

            <div style={styles.card}>
              <h3>Summary</h3>
              <p>{result.ai_review.summary}</p>
            </div>

            <div style={styles.card}>
              <h3>Bugs</h3>
              {result.ai_review.bugs.length === 0 ? (
                <p>No bugs detected.</p>
              ) : (
                <ul>
                  {result.ai_review.bugs.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>

            <div style={styles.card}>
              <h3>Performance</h3>
              {result.ai_review.performance.length === 0 ? (
                <p>No performance issues detected.</p>
              ) : (
                <ul>
                  {result.ai_review.performance.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>

            <div style={styles.card}>
              <h3>Code Quality</h3>
              {result.ai_review.quality.length === 0 ? (
                <p>No quality issues detected.</p>
              ) : (
                <ul>
                  {result.ai_review.quality.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>

            <div style={styles.card}>
              <h3>Suggestions</h3>
              {result.ai_review.suggestions.length === 0 ? (
                <p>No suggestions.</p>
              ) : (
                <ul>
                  {result.ai_review.suggestions.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              )}
            </div>

            <div style={styles.card}>
              <h3>Static AST Analysis</h3>

              <p>
                <strong>Functions:</strong>{" "}
                {result.ast_analysis.functions.length}
              </p>

              <p>
                <strong>Loops:</strong>{" "}
                {result.ast_analysis.loops}
              </p>

              <p>
                <strong>Nested Loops:</strong>{" "}
                {result.ast_analysis.nested_loops}
              </p>

              <p>
                <strong>Builtin Shadowing:</strong>{" "}
                {result.ast_analysis.builtin_shadowing.length}
              </p>

              <p>
                <strong>Bare Exceptions:</strong>{" "}
                {result.ast_analysis.bare_exceptions}
              </p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#f4f4f5",
    fontFamily: "Arial, sans-serif",
    color: "#18181b",
  },

  header: {
    backgroundColor: "#eeeef6",
    color: "Black",
    padding: "30px",
    textAlign: "center" as const,
  },

  container: {
    maxWidth: "1000px",
    margin: "30px auto",
    padding: "0 20px",
  },

  editorSection: {
    backgroundColor: "white",
    padding: "25px",
    borderRadius: "12px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
  },

  editor: {
    width: "100%",
    height: "300px",
    padding: "15px",
    boxSizing: "border-box" as const,
    fontFamily: "monospace",
    fontSize: "15px",
    borderRadius: "8px",
    border: "1px solid #d4d4d8",
    resize: "vertical" as const,
  },

  button: {
    marginTop: "15px",
    padding: "12px 25px",
    border: "none",
    borderRadius: "8px",
    backgroundColor: "#18181b",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
  },

  error: {
    color: "#dc2626",
    marginTop: "15px",
  },

  results: {
    marginTop: "30px",
  },

  card: {
    backgroundColor: "white",
    padding: "20px",
    marginBottom: "15px",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.06)",
  },
};

export default App;