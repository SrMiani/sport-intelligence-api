import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
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
      body: JSON.stringify({ sport, discipline, input_text: inputText }),
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsLog(false);
    setResult(null);
  };

  if (!isLog) {
    return <Auth onLogin={() => setIsLog(true)} />;
  }

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden",
      padding: "40px 20px"
    }}>

      {/* Glow fondo */}
      <div style={{
        position: "fixed",
        width: 800,
        height: 800,
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(80,0,120,0.1) 0%, transparent 70%)",
        top: "50%", left: "50%",
        transform: "translate(-50%, -50%)",
        pointerEvents: "none"
      }} />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        style={{ width: "100%", maxWidth: 640, position: "relative", zIndex: 1 }}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 40 }}>
          <div>
            <div style={{ fontSize: 10, letterSpacing: "0.4em", color: "rgba(255,255,255,0.25)", textTransform: "uppercase", marginBottom: 6 }}>
              Sport Intelligence
            </div>
            <div style={{
              fontSize: 28,
              fontWeight: 700,
              background: "linear-gradient(135deg, #fff 0%, rgba(180,80,255,0.8) 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              letterSpacing: "-0.02em"
            }}>
              力 Análisis
            </div>
          </div>
          <button
            onClick={logout}
            style={{
              padding: "8px 16px",
              background: "rgba(255,255,255,0.04)",
              border: "1px solid rgba(255,255,255,0.08)",
              color: "rgba(255,255,255,0.3)",
              borderRadius: 6,
              fontSize: 12,
              letterSpacing: "0.05em"
            }}
          >
            SALIR
          </button>
        </div>

        {/* Formulario */}
        <div style={{
          background: "rgba(255,255,255,0.02)",
          border: "1px solid rgba(255,255,255,0.06)",
          borderRadius: 16,
          padding: "32px",
          marginBottom: 24
        }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ display: "flex", gap: 12 }}>
              <input
                placeholder="Deporte"
                value={sport}
                onChange={(e) => setSport(e.target.value)}
              />
              <input
                placeholder="Disciplina"
                value={discipline}
                onChange={(e) => setDiscipline(e.target.value)}
              />
            </div>
            <textarea
              placeholder="Describe tu actuación con el máximo detalle posible..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              rows={5}
            />
            <motion.button
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
              onClick={analyse}
              style={{
                padding: "14px 0",
                borderRadius: 8,
                background: "linear-gradient(135deg, #5a0090 0%, #3a0060 100%)",
                color: "#fff",
                fontSize: 13,
                fontWeight: 600,
                letterSpacing: "0.1em",
                border: "1px solid rgba(120,0,180,0.4)",
                boxShadow: "0 0 30px rgba(80,0,120,0.2)"
              }}
            >
              {loading ? "ANALIZANDO..." : "ANALIZAR"}
            </motion.button>
          </div>
        </div>

        {/* Resultado */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              style={{
                background: "rgba(255,255,255,0.02)",
                border: "1px solid rgba(120,0,180,0.2)",
                borderRadius: 16,
                padding: "32px",
                boxShadow: "0 0 40px rgba(80,0,120,0.1)"
              }}
            >
              {/* Score */}
              <div style={{ textAlign: "center", marginBottom: 32 }}>
                <div style={{ fontSize: 11, letterSpacing: "0.3em", color: "rgba(255,255,255,0.25)", textTransform: "uppercase", marginBottom: 8 }}>
                  Performance Score
                </div>
                <div style={{
                  fontSize: 80,
                  fontWeight: 700,
                  background: "linear-gradient(135deg, #fff 0%, rgba(180,80,255,0.9) 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  lineHeight: 1
                }}>
                  {result.score}
                </div>
                <div style={{ fontSize: 13, color: "rgba(255,255,255,0.2)", marginTop: 4 }}>/ 100</div>
              </div>

              {/* Detalles */}
              {[
                { label: "Fortalezas", value: result.strengths, color: "rgba(100,255,150,0.15)", border: "rgba(100,255,150,0.2)" },
                { label: "Áreas de mejora", value: result.improvements, color: "rgba(255,180,80,0.1)", border: "rgba(255,180,80,0.2)" },
                { label: "Recomendaciones", value: result.recommendations, color: "rgba(120,80,255,0.1)", border: "rgba(120,80,255,0.2)" },
              ].map((item) => (
                <div key={item.label} style={{
                  background: item.color,
                  border: `1px solid ${item.border}`,
                  borderRadius: 10,
                  padding: "16px 20px",
                  marginBottom: 12
                }}>
                  <div style={{ fontSize: 10, letterSpacing: "0.25em", color: "rgba(255,255,255,0.3)", textTransform: "uppercase", marginBottom: 8 }}>
                    {item.label}
                  </div>
                  <div style={{ fontSize: 14, color: "rgba(255,255,255,0.85)", lineHeight: 1.6 }}>
                    {item.value}
                  </div>
                </div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}

export default App;