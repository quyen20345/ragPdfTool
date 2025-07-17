// import './App.css';
// import axios from 'axios';
// import { useState, useEffect } from 'react'; // la 2 React Hooks: quan ly state(trang thai du lieu) trong component va xu ly side effects(goi api, dk su kien,...)

// function App() {
//   const [people, setPeople] = useState([]); 
//   useEffect(()=> {
//     axios.get('/api').then(res => setPeople(res.data));
//   }, [])

//   return people.map((p, index) => {
//     return <p key={index}>{p.id} - {p.name} - {p.age}</p>
//   });
  
// }

// export default App;


// src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await axios.post("/prompt", {
        prompt: prompt,
        context: "" // hoặc bạn có thể thêm context nếu có
      });
      setResult(response.data.result);
    } catch (error) {
      console.error(error);
      setResult("Error occurred!");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 30 }}>
      <h2>🧠 Ask AI</h2>
      <textarea
        rows={4}
        cols={60}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your question..."
      />
      <br />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Thinking..." : "Submit"}
      </button>

      <h3>💬 Response:</h3>
      <div style={{ whiteSpace: "pre-wrap", border: "1px solid #ccc", padding: 10 }}>
        {result}
      </div>
    </div>
  );
}

export default App;
