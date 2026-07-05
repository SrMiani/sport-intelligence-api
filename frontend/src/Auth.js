import { useState } from "react";


function Auth({ onLogin }) {
  const [userName, setUserName] = useState("");
  const [pass, setPass] = useState("");
  const [email, setEmail] = useState("");
  const [pestana, setPestana] = useState("login");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    const res = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: pass }),
    });
    const data = await res.json();
    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      onLogin();
    } else {
      setError("Email o contraseña incorrectos");
    }
  };

  const handleRegister = async () => {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: userName, email, password: pass }),
    });
    const data = await res.json();
    if (res.ok) {
      setPestana("login");
      setError("Cuenta creada. Ahora inicia sesión.");
    } else {
      setError(data.detail || "Error al registrarse");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h1 style={{ textAlign: "center", color: "#1a1a2e" }}>Sport Intelligence</h1>

      {/* Pestañas */}
      <div style={{ display: "flex", marginBottom: 24 }}>
        <button
          onClick={() => setPestana("login")}
          style={{
            flex: 1, padding: 10, cursor: "pointer",
            background: pestana === "login" ? "#1a1a2e" : "#eee",
            color: pestana === "login" ? "white" : "#333",
            border: "none"
          }}
        >
          Iniciar sesión
        </button>
        <button
          onClick={() => setPestana("register")}
          style={{
            flex: 1, padding: 10, cursor: "pointer",
            background: pestana === "register" ? "#1a1a2e" : "#eee",
            color: pestana === "register" ? "white" : "#333",
            border: "none"
          }}
        >
          Registrarse
        </button>
      </div>

      {/* Formulario login */}
      {pestana === "login" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ padding: 10 }}
          />
          <input
            placeholder="Contraseña"
            type="password"
            value={pass}
            onChange={(e) => setPass(e.target.value)}
            style={{ padding: 10 }}
          />
          <button
            onClick={handleLogin}
            style={{ padding: 12, background: "#1a1a2e", color: "white", border: "none", cursor: "pointer" }}
          >
            Entrar
          </button>
        </div>
      )}

      {/* Formulario registro */}
      {pestana === "register" && (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <input
            placeholder="Username"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            style={{ padding: 10 }}
          />
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ padding: 10 }}
          />
          <input
            placeholder="Contraseña"
            type="password"
            value={pass}
            onChange={(e) => setPass(e.target.value)}
            style={{ padding: 10 }}
          />
          <button
            onClick={handleRegister}
            style={{ padding: 12, background: "#1a1a2e", color: "white", border: "none", cursor: "pointer" }}
          >
            Crear cuenta
          </button>
        </div>
      )}

      {error && (
        <p style={{ color: "red", marginTop: 12, textAlign: "center" }}>{error}</p>
      )}
    </div>
  );
}



export default Auth;