import React, { useEffect, useState } from "react";
import Chart from "react-apexcharts";
import { Table } from "react-bootstrap";


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
          <td>Maximum Loss</td>
          <td>0</td>
        </tr>
        <tr>
          <td>Maximum Drawdown</td>
          <td>0</td>
        </tr>
        <tr>
          <td>Expected Profit</td>
          <td>0</td>
        </tr>
        <tr>
          <td>Win/Loss</td>
          <td>0</td>
        </tr>
        <tr>
          <td>Maximum Win</td>
          <td>0</td>
        </tr>
        <tr>
          <td>Maximum Loss</td>
          <td>0</td>
        </tr>
      </tbody>
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
