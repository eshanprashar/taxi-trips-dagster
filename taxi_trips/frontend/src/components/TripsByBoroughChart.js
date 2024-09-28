import React, { useEffect, useState } from 'react';
import axios from 'axios';  // Add this import
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,  // Register Bar element
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

// Register necessary Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const TripsByBoroughChart = () => {
  const [boroughData, setBoroughData] = useState([]);

  useEffect(() => {
    // Fetch data from FastAPI backend
    axios.get('http://localhost:8000/monthly_trips_by_borough')  // Use your backend URL
      .then(response => {
        setBoroughData(response.data);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  // Extract unique boroughs and months from the data
  const boroughs = [...new Set(boroughData.map(item => item.borough))];
  const months = [...new Set(boroughData.map(item => item.partition_date))];

  // Prepare datasets for each month
  const datasets = months.map(month => {
    return {
      label: month,  // Label for each dataset will be the month
      data: boroughs.map(borough => {
        const boroughMonthData = boroughData.find(
          item => item.borough === borough && item.partition_date === month
        );
        return boroughMonthData ? boroughMonthData.num_trips : 0;
      }),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    };
  });

  const data = {
    labels: boroughs,  // Boroughs as X-axis labels
    datasets,  // Data for each month as separate datasets
  };

  return (
    <div>
      <h2>Monthly Trips by Borough</h2>
      <Bar data={data} />
    </div>
  );
};

export default TripsByBoroughChart;
