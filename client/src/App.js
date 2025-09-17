import React, { useState } from "react";

function App() {
  const [term, setTerm] = useState("");
  const [data, setData] = useState(null);

  const search = () => {
    fetch("http://localhost:5000/search?term=" + term)
      .then(res => res.json())
      .then(d => setData(d))
      .catch(err => console.log(err));
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Twitter Sentiment Analysis</h1>
      <input
        value={term}
        onChange={e => setTerm(e.target.value)}
        placeholder="Enter search term"
      />
      <button onClick={search}>Search</button>

      {data && (
        <div>
          {data.counts && (
            <div>
              <p>Positive: {data.counts.Positive || 0}</p>
              <p>Negative: {data.counts.Negative || 0}</p>
            </div>
          )}
          {data.tweets && data.tweets.map((t, i) => (
            <div key={i}>
              <b>{t.label}:</b> {t.text}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
