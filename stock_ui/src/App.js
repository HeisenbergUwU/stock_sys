import logo from "./logo.svg";
import "./App.css";
import mockData from "./mock/stock.json";
import Chart from "./components/Chart";
import { useState, useEffect } from "react";
import { getData } from "./mock/utils";

function App() {

  const [data, setData] = useState(null);
  useEffect(() => {
    getData().then((data) => {
        console.log(data);
        
      setData(data);
    });
  }, []);  if (data == null) {
    return <div>Loading...</div>;
  }
  return (
    <div className="App">
      <Chart data={data} type="svg" />
    </div>
  );
}

export default App;
