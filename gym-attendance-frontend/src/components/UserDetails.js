import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import CalendarHeatmap from 'react-calendar-heatmap';
import 'react-calendar-heatmap/dist/styles.css';
import './UserDetails.css';

export default function UserDetails() {
    const { id } = useParams();
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Fetch user details by card ID
        fetch(`http://localhost:5000/api/user/${id}`)
            .then((res) => res.json())
            .then((data) => setUser(data));
    }, [id]);

    if (!user) return <div>Loading...</div>;

    // Group attendances by year
    const groupAttendancesByYear = () => {
        const grouped = {};

        user.attendances.forEach((attendance) => {
            const dateParts = attendance.split(' ')[0].split('-');
            const year = dateParts[0];

            if (!grouped[year]) {
                grouped[year] = [];
            }

            const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
            grouped[year].push({
                date: date,
                count: 1,  // Mark each attendance date with a count of 1
            });
        });

        return grouped;
    };

    const groupedAttendances = groupAttendancesByYear();

    // Format the date to a readable string (e.g., 'YYYY-MM-DD')
    const formatDate = (date) => {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${year}-${month}-${day}`;
    };

    // Function to calculate presence statistics
    const calculateStatistics = () => {
        const now = new Date();
        
        // Sorting attendances in ascending order to ensure the first attendance is the earliest
        const sortedAttendances = user.attendances.sort((a, b) => new Date(a.split(' ')[0]) - new Date(b.split(' ')[0]));
    
        // Get the first attendance date
        const firstAttendanceDate = new Date(sortedAttendances[0].split(' ')[0]);
    
        // Calculate the total number of weeks and months since the first attendance
        const weeksSinceStart = Math.ceil((now - firstAttendanceDate) / (1000 * 60 * 60 * 24 * 7));
        const monthsSinceStart = (now.getFullYear() - firstAttendanceDate.getFullYear()) * 12 + (now.getMonth() - firstAttendanceDate.getMonth());
    
        let totalPresenceThisWeek = 0;
        let totalPresenceThisMonth = 0;
        let daysOfWeekCount = Array(7).fill(0); // Array to track attendance for each day (0 - Sunday, 6 - Saturday)
    
        // Iterate over each attendance and calculate the statistics
        sortedAttendances.forEach((attendance) => {
            const dateParts = attendance.split(' ')[0].split('-');
            const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
            const dayOfWeek = date.getDay();  // 0 - Sunday, 6 - Saturday
    
            // Check if the attendance is this week
            if (date >= new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay())) {
                totalPresenceThisWeek++;
            }
    
            // Check if the attendance is this month
            if (date >= new Date(now.getFullYear(), now.getMonth(), 1)) {
                totalPresenceThisMonth++;
            }
    
            // Count the attendance per day of the week
            daysOfWeekCount[dayOfWeek]++;
        });
    
        // Calculate the day with the most attendance
        const maxDayIndex = daysOfWeekCount.indexOf(Math.max(...daysOfWeekCount));
        const mostFrequentDay = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][maxDayIndex];
    
        // Calculate the total presence overall
        const totalPresenceOverall = user.attendances.length;
    
        // Calculate the average attendance per week since start
        const averagePresencePerWeek = totalPresenceOverall / weeksSinceStart;
    
        // Calculate the average attendance per month since start
        const averagePresencePerMonth = totalPresenceOverall / monthsSinceStart;
    
        return {
            totalPresenceThisWeek,
            totalPresenceThisMonth,
            totalPresenceOverall,
            averagePresencePerWeek,
            averagePresencePerMonth,
            mostFrequentDay,
        };
    };

    // Calculate statistics based on the user's attendance
    const {
        totalPresenceThisWeek,
        totalPresenceThisMonth,
        averagePresencePerWeek,
        averagePresencePerMonth,
        mostFrequentDay,
    } = calculateStatistics();

    return (
        <div className="user-details">
            <h1>{`${user.firstName} ${user.lastName}`}</h1>
            <p>Membership: {user.paidMembership ? 'Paid' : 'Unpaid'}</p>

            {/* Attendance Heatmap for Each Year */}
            {Object.keys(groupedAttendances).map((year) => {
                const heatmapData = groupedAttendances[year];

                // Define the start and end date for each year heatmap
                const startDate = new Date(year, 0, 1);  // January 1st of the year
                
                const endDate = new Date(year, 11, 31);  // December 31st of the year

                return (
                    <div key={year}>
                        <h2>Attendance Heatmap for {year}</h2>
                        <CalendarHeatmap
                            startDate={startDate}
                            endDate={endDate}
                            values={heatmapData}
                            showWeekdayLabels
                            titleForValue={(value) => {
                                if (!value) return `No attendance`;
                                const formattedDate = formatDate(value.date);
                                return `${formattedDate}: ${value.count} attendance`; // Tooltip showing date
                            }} 
                            classForValue={(value) => {
                                if (!value) return 'color-empty';  // No attendance
                                if (value.count === 1) return 'color-1';  // One attendance
                                return 'color-2';  // Two or more attendances
                            }}
                        />
                    </div>
                );
            })}

            {/* Additional Statistics */}
            <h2>Statistics</h2>
            <p>Total Presence This Week: {totalPresenceThisWeek}</p>
            <p>Total Presence This Month: {totalPresenceThisMonth}</p>
            <p>Average Presence Per Week: {averagePresencePerWeek.toFixed(2)}</p>
            <p>Average Presence Per Month: {averagePresencePerMonth.toFixed(2)}</p>
            <p>Most Frequent Day of the Week: {mostFrequentDay}</p>

            {/* Total Attendance Count */}
            <h3>Total Attendances: {user.attendances.length}</h3>

            {/* List of Attendances */}
            <h2>Attendance List</h2>
            <ul>
                {user.attendances.map((attendance, idx) => {
                    const dateParts = attendance.split(' ')[0].split('-');
                    const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
                    return (
                        <li key={idx}>
                            {formatDate(date)} - {attendance}
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}
