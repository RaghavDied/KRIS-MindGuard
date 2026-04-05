import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);

  
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");


  const handleLogin = async () => {
  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();

  if (data.error) {
    alert(data.error);
  } else {
    setUser(username);
    setHistory(data.history || []);

    const loadedMessages = [];

    (data.history || []).forEach((item) => {
      
      loadedMessages.push({
        type: "user",
        text: item.text,
      });

      
      loadedMessages.push({
        type: "bot",
        data: item,
      });
    });

    setMessages(loadedMessages);
  }
};

  const handleSignup = async () => {
    const res = await fetch("http://127.0.0.1:8000/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    alert(data.message || data.error);
  };

  const handleLogout = () => {
    setUser(null);
    setMessages([]);
    setHistory([]);
  };

  const handleSubmit = async () => {
    if (!text.trim()) return;

    const userMessage = { type: "user", text };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text, username: user }), 
      });

      const data = await response.json();

      const botMessage = { type: "bot", data };
      setMessages((prev) => [...prev, botMessage]);

      setHistory((prev) => [...prev, data]);
    } catch (error) {
      console.error("Error:", error);
    }

    setText("");
  };

  const getRiskColor = (risk) => {
    if (risk === "CRITICAL") return "#ff4d4d";
    if (risk === "HIGH") return "#ff944d";
    if (risk === "TOXIC") return "#cc66ff";
    if (risk === "MODERATE") return "#4da6ff";
    return "#4dff88";
  };

  const generateAdvice = (data) => {
    if (data.risk_level === "CRITICAL") {
      return "🚨 Please reach out to someone immediately. You are not alone.";
    }
    if (data.risk_level === "HIGH") {
      return "💛 Talk to someone you trust.";
    }
    if (data.risk_level === "TOXIC") {
      return "⚠️ Try to reframe your thoughts positively.";
    }
    if (data.risk_level === "MODERATE") {
      return "🙂 Take care and stay mindful.";
    }
    return "😊 You're doing well!";
  };

  if (!user) {
    return (
      <div className="login">
        <h1 className="title">🧠 KRIS MindGuard</h1>
        <h2>Login / Signup</h2>

        <input
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <br></br><br></br>
        <button onClick={handleLogin}>Login</button>
        <button onClick={handleSignup}>New User</button>
      </div>
    );
  }



  return (
    <div className="app">
      <h1 className="title">🧠 KRIS MindGuard</h1>

      <button onClick={handleLogout} className="logout">
        Logout ({user})
      </button>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.type === "user" ? (
              <div className="user-text">{msg.text}</div>
            ) : (
              <div className="card">
                <p><b>🧾 Text:</b> {msg.data.text}</p>

                <p><b>☣️ Toxicity:</b> {msg.data.toxicity}</p>
                <div className="bar">
                  <div
                    className="fill"
                    style={{
                      width: `${msg.data.toxicity_confidence * 100}%`,
                    }}
                  ></div>
                </div>

                <p><b>🧠 Mental State:</b> {msg.data.mental_state}</p>
                <div className="bar">
                  <div
                    className="fill mental"
                    style={{
                      width: `${msg.data.mental_confidence * 100}%`,
                    }}
                  ></div>
                </div>

                <p
                  className="risk"
                  style={{
                    backgroundColor: getRiskColor(msg.data.risk_level),
                  }}
                >
                  {msg.data.risk_level}
                </p>

                <p className="advice">
                  {generateAdvice(msg.data)}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your thoughts..."
        />
        <button onClick={handleSubmit}>Send</button>
      </div>

      <div className="stats">
        <h3>Session Stats</h3>

        <p>Total Messages: {history.length}</p>

        <p>
          🔴 High Risk:{" "}
          {history.filter(
            (h) =>
              h.risk_level === "HIGH" ||
              h.risk_level === "CRITICAL"
          ).length}
        </p>

        <p>
          🟣 Toxic Messages:{" "}
          {history.filter((h) => h.toxicity === 1).length}
        </p>

        <p>
          🧠 Critical Mental States:{" "}
          {history.filter(
            (h) =>
              h.mental_state === "Depression" ||
              h.mental_state === "Suicidal"
          ).length}
        </p>
      </div>
    </div>
  );
}

export default App;