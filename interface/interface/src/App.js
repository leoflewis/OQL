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

  const handleDropdownSelect = (value) => {
    setSelectedValue(value);
  };

  const options = [
    { value: 'SkaterStats', label: 'SkaterStats' },
    { value: 'GoalieStats', label: 'GoalieStats' },
    { value: 'TeamStats', label: 'TeamStats' },
    { value: 'player', label: 'Player' },
    { value: 'team', label: 'Teams' },
    { value: 'draft', label: 'Draft' }
  ]

  const handleSearch = async () => {
    // Perform the search or any other action based on the selectedValue
    const url = `http://127.0.0.1:5000/?table=${selectedValue}`;

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
          console.log(data);
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
      <Dropdown onSelect={handleDropdownSelect}>
        <Dropdown.Toggle variant="success" id="dropdown-basic">Table</Dropdown.Toggle>
        <Dropdown.Menu class = "submenu">
          <Dropdown.Item eventKey="SkaterStats">SkaterStats</Dropdown.Item>
          <Dropdown.Item eventKey="GoalieStats">GoalieStats</Dropdown.Item>
          <Dropdown.Item eventKey="TeamStats">TeamStats</Dropdown.Item>
          <Dropdown.Item eventKey="Game">Games</Dropdown.Item>
          <Dropdown.Item eventKey="Draft">Drafts</Dropdown.Item>
          <Dropdown.Item eventKey="Team">Teams</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      <Select placeholder="Join" isMulti name="colors" options={options} className="basic-multi-select" classNamePrefix="select"/> 
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