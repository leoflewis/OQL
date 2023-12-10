import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import {View} from 'react-native';
import Select from 'react-select';

const SampleTable = () => {
  const [tableData, setTableData] = useState([]);
  const [selectedValue, setSelectedValue] = useState('');
  const [joinValue, setJoinValue] = useState('');
  const [columnValue, setColumnValue] = useState('');

  const onInputChange = (inputValue) => {
    setSelectedValue(inputValue.value);
    console.log(inputValue.value);
  };
  const handleDropdownJoin = (value) => {
    console.log(value)
    setJoinValue(value);
  };

  const handleDropdownColumns = (value) => {
    console.log(value)
    setColumnValue(value);
  };
  const columnOptions = [
    {value:"player_id", label: "PlayerPK"},
    {value:"teamid", label: "TeamPK"},
    {value:"playerid", label: "skaterstatsPK"},
    {value:"playerid", label: "draftPK"},
    {value:"playerid", label: "GSAAPPK"}
  ]

  const options = [
    { value: 'SkaterStats', label: 'SkaterStats' },
    { value: 'GoalScorersAboveAverageAtPosition', label: "GSAAP"},
    { value: 'player', label: 'Player' },
    { value: 'team', label: 'Teams' },
    { value: 'draft', label: 'Draft' },
    { value: 'game', label: 'Game' }
  ]

  const handleSearch = async () => {
    // Perform the search or any other action based on the selectedValue
    let url = `http://127.0.0.1:5000/?table=${selectedValue}`;
    if (joinValue.length > 0 && columnValue.length > 0){
      url = `http://127.0.0.1:5000/?table=${selectedValue}` + `&join=${joinValue[0].value},inner` + `,${columnValue[0].value}` + `,${columnValue[0].value}`
      console.log(url)
    } else if (joinValue.length > 0 && columnValue.length > 1){
      url = `http://127.0.0.1:5000/?table=${selectedValue}` + `&join=${joinValue[0].value},inner` + `,${columnValue[0].value}` + `,${columnValue[1].value}`
      console.log(url)
    }
    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }        
        return response.json();
      })
      .then((data) => {
        // Handle the response data as needed
        console.log(data);
        if(data.length > 1 && Array.isArray(data[0]) && typeof data[1] === 'object') {
          setTableData(data);
        }
      })
      .catch((error) => {
        console.error('Error making web request:', error);
      });
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/?table=skaterstats');
        const data = await response.json();
        if (data.length > 1 && Array.isArray(data[0]) && typeof data[1] === 'object') {
          setTableData(data);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const columns = tableData.length > 0 ? tableData[0].map((col) => ({ field: col, headerName: col })) : [];

  return (
    <div>
      <div>
      <View style={{ flexDirection:"row"}}>
      <Select onChange={onInputChange} placeholder="Table" options={options} className="basic-multi-select" classNamePrefix="select"/> 
      <Select onChange={handleDropdownJoin} placeholder="Join" isMulti options={options} className="basic-multi-select" classNamePrefix="join"/>
      <Select onChange={handleDropdownColumns} placeholder="Columns" isMulti options={columnOptions} className="basic-multi-select" classNamePrefix="attributes"/> 
      <Button variant="dark" onClick={handleSearch}>
        Search
      </Button>
      </View>
      </div>
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <h1>Search Hockey Stats</h1>
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <br>
      </br>
      <div>
        <div style={{ height: '80%', width: '100%' }}>
          <DataGrid
            rows={tableData.slice(1)}
            columns={columns}
            getRowId={(row) => row.ID}
          />
        </div>
      </div>
    </div>
  );
};

export default SampleTable;