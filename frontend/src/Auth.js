import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function Auth({ onLogin }) {
  const [userName, setUserName] = useState("");
  const [pass, setPass] = useState("");
  const [email, setEmail] = useState("");
  const [pestana, setPestana] = useState("login");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setLoading(true);
    setError("");
    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: pass }),
    });
    const data = await res.json();
    setLoading(false);
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      onLogin();
    } else {
      setError("Email o contraseña incorrectos");
    }
  };

  const handleRegister = async () => {
    setLoading(true);
    setError("");
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: userName, email, password: pass }),
    });
    const data = await res.json();
    setLoading(false);
    if (res.ok) {
      setPestana("login");
      setError("✓ Cuenta creada. Inicia sesión.");
    } else {
      setError(data.detail || "Error al registrarse");
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden"
    }}>

      {/* Glow de fondo */}
      <div style={{
        position: "absolute",
        width: 600,
        height: 600,
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(80,0,120,0.15) 0%, transparent 70%)",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        pointerEvents: "none"
      }} />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        style={{
          width: 420,
          padding: "48px 40px",
          background: "rgba(255,255,255,0.02)",
          border: "1px solid rgba(255,255,255,0.06)",
          borderRadius: 16,
          backdropFilter: "blur(20px)",
          position: "relative",
          zIndex: 1
        }}
      >
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: 40 }}>
          <div style={{
            fontSize: 11,
            letterSpacing: "0.4em",
            color: "rgba(255,255,255,0.25)",
            textTransform: "uppercase",
            marginBottom: 12
          }}>
            Sport Intelligence
          </div>
          <div style={{
            fontSize: 36,
            fontWeight: 700,
            background: "linear-gradient(135deg, #fff 0%, rgba(180,80,255,0.8) 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            letterSpacing: "-0.02em"
          }}>
            力
          </div>
        </div>

        {/* Pestañas */}
        <div style={{
          display: "flex",
          background: "rgba(255,255,255,0.03)",
          borderRadius: 8,
          padding: 4,
          marginBottom: 32
        }}>
          {["login", "register"].map((tab) => (
            <button
              key={tab}
              onClick={() => { setPestana(tab); setError(""); }}
              style={{
                flex: 1,
                padding: "10px 0",
                borderRadius: 6,
                fontSize: 13,
                fontWeight: 500,
                letterSpacing: "0.05em",
                background: pestana === tab ? "rgba(100,0,160,0.5)" : "transparent",
                color: pestana === tab ? "#fff" : "rgba(255,255,255,0.3)",
                border: pestana === tab ? "1px solid rgba(120,0,180,0.3)" : "1px solid transparent",
                transition: "all 0.2s"
              }}
            >
              {tab === "login" ? "Iniciar sesión" : "Registrarse"}
            </button>
          ))}
        </div>

        {/* Formularios */}
        <AnimatePresence mode="wait">
          <motion.div
            key={pestana}
            initial={{ opacity: 0, x: pestana === "login" ? -10 : 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            style={{ display: "flex", flexDirection: "column", gap: 12 }}
          >
            {pestana === "register" && (
              <input
                placeholder="Username"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
              />
            )}
            <input
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              placeholder="Contraseña"
              type="password"
              value={pass}
              onChange={(e) => setPass(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && (pestana === "login" ? handleLogin() : handleRegister())}
            />
          </motion.div>
        </AnimatePresence>

        {/* Botón */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={pestana === "login" ? handleLogin : handleRegister}
          style={{
            width: "100%",
            padding: "14px 0",
            marginTop: 20,
            borderRadius: 8,
            background: "linear-gradient(135deg, #5a0090 0%, #3a0060 100%)",
            color: "#fff",
            fontSize: 14,
            fontWeight: 600,
            letterSpacing: "0.08em",
            border: "1px solid rgba(120,0,180,0.4)",
            boxShadow: "0 0 30px rgba(80,0,120,0.3)"
          }}
        >
          {loading ? "..." : pestana === "login" ? "ENTRAR" : "CREAR CUENTA"}
        </motion.button>

        {/* Error / éxito */}
        {error && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{
              marginTop: 16,
              textAlign: "center",
              fontSize: 13,
              color: error.startsWith("✓") ? "rgba(100,255,150,0.8)" : "rgba(255,80,80,0.8)"
            }}
          >
            {error}
          </motion.p>
        )}
      </motion.div>
    </div>
  );
}

export default Auth;