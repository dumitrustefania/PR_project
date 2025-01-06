import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './Statistics.css'; 

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Statistics() {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        fetch('http://localhost:5000/api/statistics')
            .then((res) => res.json())
            .then((data) => setStats(data));
    }, []);

    if (!stats) return <div>Loading...</div>;

    // Prepare daily load data
    const dailyLoadLabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const dailyLoadData = dailyLoadLabels.map(day => stats.daily_load[day] || 0); // Default to 0 if no data exists for that day

    // Prepare hourly load data (for hours from 9:00 to 23:00)
    const hourlyLoadLabels = [];
    const hourlyLoadData = [];

    // Create labels for hourly load (9:00 to 23:00)
    for (let hour = 9; hour <= 23; hour++) {
        hourlyLoadLabels.push(`${hour}:00`);
        hourlyLoadData.push(stats.hourly_load[hour] || 0); // Default to 0 if no data exists for that hour
    }

    // Chart data for daily load
    const dailyData = {
        labels: dailyLoadLabels,
        datasets: [
            {
                label: 'Daily Load',
                data: dailyLoadData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            },
        ],
    };

    // Chart data for hourly load
    const hourlyData = {
        labels: hourlyLoadLabels,
        datasets: [
            {
                label: 'Hourly Load',
                data: hourlyLoadData,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="statistics">
            <h1>Gym Statistics</h1>
            <div className="chart">
                <h2>Daily Load (Monday to Sunday)</h2>
                <Bar data={dailyData} />
            </div>
            <div className="chart">
                <h2>Hourly Load (9:00 - 23:00)</h2>
                <Bar data={hourlyData} />
            </div>
        </div>
    );
}
