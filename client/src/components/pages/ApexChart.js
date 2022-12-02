import React from 'react';
import Chart from 'react-apexcharts'
import Table from 'react-bootstrap/Table';
import UserInput from '../UserInput';

const TableCoin=()=> {
    return (
      <Table  className='table'   striped="columns">
        <thead>
          <tr>
            <th>#</th>
            <th>#</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>18000</td>
            <td>3600</td>
          </tr>
          <tr>
            <td>18000</td>
            <td>3600</td>
          </tr>
          <tr>
            <td>18000</td>
            <td>3600</td>
          </tr>
          <tr>
            <td>18000</td>
            <td>3600</td>
          </tr>
        </tbody>
      </Table>
    );
  }

//async function setChart(){
//  //I want the 3 inputs (start time, end time, and api key) to be variables to 
//  const graphData = await fetch('http://localhost:5000/graphdata/2022-01-01/2022-01-02/C8840AED-9AC5-4F51-B1F3-8212FC3F5F0A/false').then(res => res.json());
//  console.log(graphData);
//  for (let i = 0; i < graphData["data"].length; i++) {
//    graphData["data"][i]["x"] =  new Date(graphData["data"][i]["x"])
//  }
//  console.log(graphData);
//}

class ApexChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
      
        series: [{
          data: []
        }],
        options: {
          chart: {
            type: 'candlestick',
            height: 350
          },
          title: {
            text: 'CandleStick Chart',
            align: 'left'
          },
          xaxis: {
            type: 'datetime'
          },
          yaxis: {
            tooltip: {
              enabled: true
            }
          }
        },
      
      
      };
    }
    async setChart(){
      //I want the 3 inputs (start time, end time, and api key) to be variables to 
      const graphData = await fetch('http://localhost:5000/graphdata/2022-01-01/2022-01-02/C8840AED-9AC5-4F51-B1F3-8212FC3F5F0A/false').then(res => res.json());
      console.log(graphData);
      for (let i = 0; i < graphData["data"].length; i++) {
        graphData["data"][i]["x"] =  new Date(graphData["data"][i]["x"])
      } 
      this.setState({series:graphData})
    }
    
    render() {
      return (
          <>
            <h1 className='text-center'>Apex CandleStick Chart</h1>
            <div id="chart" className='d-flex flex-row'>
                <Chart className="chart-custom" options={this.state.options} series={this.state.series} type="candlestick" width={500} height={315}/>
                <TableCoin/>
            </div>
            <button onClick={this.setChart}>Test</button>
            <div className='user-input-div'>
               <UserInput className="text-center"/>
            </div>
           
            

            </>
      );
    }
  }
  export default ApexChart