import React, { useState } from "react";

const UserInput = () => {
  const [startDate, setStartDate] = useState(0);
  const [endDate, setEndDate] = useState(0);
  

  const submitValue = () => {
    const frmdetails = {
      "Start Date": startDate,
      "End Date": endDate,
    };
    console.log(frmdetails);
  };

  return (
    <>
      <h1> Enter a value</h1>
     <label>Start Date</label> <input
        type="text"
        placeholder="starting date"
        onChange={(e) => setStartDate(e.target.value)}
      />
      <label>Ending Date</label><input
        type="text"
        placeholder="ending date"
        onChange={(e) => setEndDate(e.target.value)}
      />
      
      
      <button onClick={submitValue}>Generate</button>
    </>
  );
};

export default UserInput
