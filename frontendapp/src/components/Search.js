import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';

function Search() {
  const [query, setQuery] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [results, setResults] = useState([]);
  const [time, setTime] = useState("");

  const search = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/search/", {
        params: { query, start, end }
      });
      setResults(res.data.results);
      setTime(res.data.search_time);
    } catch (err) {
      alert("Error fetching data. Is backend running?");
    }
  };

  return (
    <div className="search-container">
      <h2>Search Events</h2>
      <div className="search-inputs">
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search (e.g. srcaddr=1.2.3.4)" />
        <input value={start} onChange={e => setStart(e.target.value)} placeholder="Start Time (epoch)" />
        <input value={end} onChange={e => setEnd(e.target.value)} placeholder="End Time (epoch)" />
        <button onClick={search}>Search</button>
      </div>

      <div className="results-section">
        <h4>Search Time: {time}s</h4>
        <ul>
          {results.map((r, i) => (
            <li key={i}>
              {r.event.srcaddr} → {r.event.dstaddr} | Action: {r.event.action} | File: {r.file}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Search;
