import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register the required Chart.js components and scales
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MonthlyTripChart = () => {
  const [tripData, setTripData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/monthly_trips')
      .then(response => {
        setTripData(response.data);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const data = {
    labels: tripData.map(trip => trip.partition_date),
    datasets: [
      {
        label: 'Trip Count',
        data: tripData.map(trip => trip.trip_count),
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <div>
      <h2>Monthly Trip Count</h2>
      <Line data={data} />
    </div>
  );
};

export default MonthlyTripChart;
