import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { Table } from "react-bootstrap";

const generateTrade = async () => {
  try{
    const url = `http://localhost:5000/tradedata`;
    const response = await fetch(url);
    const data = await response.json();
    console.log(data);

    console.log(data);

    if (data["max_drawdown"].toFixed(2) == 0){
      alert("Warning: Please graph at least 5 days worth of data");
    }
    document.getElementById("maxdraw").textContent = data["max_drawdown"].toFixed(2);
    document.getElementById("expectedprofit").textContent = data["profits"].toFixed(2); 
    document.getElementById("winloss").textContent = data["win_loss"].toFixed(2); 
  }

  catch(err){
    alert("Error Calling Trade. This is most likely due to a divideByZero error. Try adding more data");
    document.getElementById("maxdraw").textContent = 0;
    document.getElementById("expectedprofit").textContent = 0;
    document.getElementById("winloss").textContent = 0;

  }
}

const TableCoin = () => {
  return (
    <Table className="table" striped="columns">
      <thead>
        <tr>
          <th>MA Crossover Strategy</th>
          <th>Values</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Maximum Loss</th>
          <td id="maxloss">0</td>
        </tr>
        <tr>
          <th>Maximum Drawdown</th>
          <td id="maxdraw">0</td>
        </tr>
        <tr>
          <th>Expected Profit</th>
          <td id="expectedprofit">0</td>
        </tr>
        <tr>
          <th>Win/Loss</th>
          <td id="winloss">0</td>
        </tr>
        <tr>
          <th>Maximum Win</th>
          <td>0</td>
        </tr>
        <tr>
          <th>Maximum Loss</th>
          <td>0</td>
        </tr>
      </tbody>
      <button onClick={generateTrade}> Generate</button>
    </Table>
  );
};

const ApexChart = () => {
  const [averageTemp, setAverageTemp] = useState([]);

  const [date, setDate] = useState([1999, 1200]);
  const [startDate, setStartDate] = useState("2022-01-01");
  const [endDate, setEndDate] = useState("2022-01-02");
  const [submitClicked, setSubmitClicked] = useState(false);

  // this is where you will be fetching the data and set the state
  useEffect(() => {
    const getData = async () => {
      const url = `http://localhost:5000/graphdata/${startDate}/${endDate}/C8840AED-9AC5-4F51-B1F3-8212FC3F5F0A/false`;
      const response = await fetch(url);
      const data = await response.json();
      try {
        console.log(data);
        for(let i = 0; i < data["data"].length; i++){
          data["data"][i]["x"] = await new Date(data["data"][i]["x"]*1000);
          for(let j = 0; j < data["data"][i]["y"].length; j++){
            data["data"][i]["y"][j] = await data["data"][i]["y"][j].toFixed(2);
          }
        }

        setAverageTemp(data["data"]); 
        //setDate(data?.map((item) => item.date));
      } catch (error) {
        console.log(error);
      }
    };
    getData();
  }, [submitClicked]);

  const series = [
    {
      name: "our candelstick chart",
      data: averageTemp, //this is where you assin the state value
    },
  ];
  const options = {
    chart: {
      height: 350,
      type: "candlestick",
    },
    title: {
      text: "CandleStick Chart - Category X-axis",
      align: "left",
    },
    tooltip: {
      enabled: true,
    },
    xaxis: {
      categories: date,
    },
    yaxis: {
      tooltip: {
        enabled: true,
      },
    },
  };

  //user input method   
  //all states are defined at the top

  const UserInput = () => {
    const submitValue = () => {
      const frmdetails = {
        "Start Date": startDate,
        "End Date": endDate,
      };
      console.log(frmdetails);
      setSubmitClicked(!submitClicked);
    };

    return (
      <>
        <h1> Enter a value</h1>
        <label>Start Date</label>{" "}
        <input
          type="text"
          placeholder="starting date"
          onChange={(e) => setStartDate(e.target.value)}
        />
        <label>Ending Date</label>
        <input
          type="text"
          placeholder="ending date"
          onChange={(e) => setEndDate(e.target.value)}
        />
        <button onClick={submitValue}>Generate</button>
      </>
    );
  };
  return (
    <>
      <div className="d-flex flex-row">
        <div>
          <Chart
            options={options}
            series={series}
            type="candlestick"
            width="700"
            height="450"
          />
        </div>
        <div>
          <TableCoin />
        </div>
      </div>
      <div className="user-input-div">{UserInput()}</div>
    </>
  );
};

export default ApexChart;
