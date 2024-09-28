import React, { useState } from 'react';
import './App.css';  // Import App.css for styling
import MonthlyTripChart from './components/MonthlyTripChart';
import TripsByBoroughChart from './components/TripsByBoroughChart';

function App() {
  // State to track which chart is currently active
  const [activeChart, setActiveChart] = useState('monthly');

  return (
    <div>
      <h1>Taxi Trips Data</h1>
      
      {/* Toggle buttons to switch between the two charts */}
      <div className="toggle-buttons">
        <button onClick={() => setActiveChart('monthly')}>Monthly Trip Count</button>
        <button onClick={() => setActiveChart('borough')}>Trips by Borough</button>
      </div>

      {/* Conditionally render the charts based on the activeChart state */}
      <div className="chart-container">
        {activeChart === 'monthly' && <MonthlyTripChart />}
        {activeChart === 'borough' && <TripsByBoroughChart />}
      </div>
    </div>
  );
}

export default App;