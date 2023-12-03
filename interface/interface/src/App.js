import React, { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

const SampleTable = () => {
  const [tableData, setTableData] = useState([]);

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
      <Dropdown>
        <Dropdown.Toggle variant="success" id="dropdown-basic">Table</Dropdown.Toggle>
        <Dropdown.Menu>
          <Dropdown.Item >SkaterStats</Dropdown.Item>
          <Dropdown.Item >GoalieStats</Dropdown.Item>
          <Dropdown.Item >TeamStats</Dropdown.Item>
          <Dropdown.Item >Games</Dropdown.Item>
          <Dropdown.Item >Drafts</Dropdown.Item>
          <Dropdown.Item >Teams</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      <Button variant="dark">Search</Button>

    <div style={{ height: '100%', width: '100%' }}>
      <DataGrid
        rows={tableData.slice(1)}
        columns={columns}
        getRowId={(row) => row.PLAYER}
      />
    </div>
    </div>
  );
};

export default SampleTable;