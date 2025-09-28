import logo from "./logo.svg";
import "./App.css";
import mockData from "./mock/stock.json";
import StockChart from "./components/StockChart";
import { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // 这里替换为你的数据获取逻辑，比如从 API 拿 JSON
    fetch("/api/stock-data")
      .then((res) => res.json())
      .then((json) => {
        // json 应该是类似 [{date: "2025-09-01", open: ..., high: ..., low: ..., close: ...}, ...]
        setData(json);
      });
  }, []);

  if (data.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Stock Chart 示例</h1>
      <StockChart data={data} width={900} height={500} />
    </div>
  );
}

export default App;
