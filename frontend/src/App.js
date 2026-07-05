import { useState } from "react";
import Auth from "./Auth";

function App() {
  const [sport, setSport] = useState("");
  const [discipline, setDiscipline] = useState("");
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isLog, setIsLog] = useState(!!localStorage.getItem("token"));

  const analyse = async () => {
    setLoading(true);
    setResult(null);

    const token = localStorage.getItem("token");

    const res = await fetch("http://localhost:8000/analysis", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        sport,
        discipline,
        input_text: inputText,
      }),
    });

    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

if (!isLog) {
  return <Auth onLogin={() => setIsLog(true)} />;
}
  
  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Sport Intelligence API</h1>

      <input
        placeholder="Deporte (ej: fútbol)"
        value={sport}
        onChange={(e) => setSport(e.target.value)}
        style={{ width: "100%", padding: 10, marginBottom: 10 }}
      />
      <input
        placeholder="Disciplina (ej: portero)"
        value={discipline}
        onChange={(e) => setDiscipline(e.target.value)}
        style={{ width: "100%", padding: 10, marginBottom: 10 }}
      />
      <textarea
        placeholder="Describe tu actuación..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        rows={5}
        style={{ width: "100%", padding: 10, marginBottom: 10 }}
      />
      <button
        onClick={analyse}
        style={{ padding: "10px 24px", background: "#1a1a2e", color: "white", border: "none", cursor: "pointer" }}
      >
        {loading ? "Analizando..." : "Analizar"}
      </button>

      {result && (
        <div style={{ marginTop: 30, padding: 20, background: "#f5f5f5", borderRadius: 8 }}>
          <h2>Score: {result.score} / 100</h2>
          <p><strong>Fortalezas:</strong> {result.strengths}</p>
          <p><strong>Mejoras:</strong> {result.improvements}</p>
          <p><strong>Recomendaciones:</strong> {result.recommendations}</p>
        </div>
      )}
    </div>
  );
}

export default App;