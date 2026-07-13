// Load all charts using a date range
async function loadCharts() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    if (!start || !end) {
        alert("Please select BOTH start and end dates.");
        return;
    }

    loadIncidentChart(start, end);
    loadTimelineChart(start, end);
}



// BAR CHART: Incident Counts (Date Range)

async function loadIncidentChart(start, end) {
    const response = await fetch(`/api/v1/reports/stats/incident-range?start_date=${start}&end_date=${end}`);
    const data = await response.json();

    const labels = data.map(item => item.type);
    const counts = data.map(item => item.count);

    const ctx = document.getElementById("incidentChart").getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Incident Count",
                data: counts,
                backgroundColor: "rgba(235, 232, 54, 0.6)",
                borderColor: "rgb(136, 235, 54)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}


// -----------------------------------------------------
// LINE CHART: Calls Over Time (Date Range)
// -----------------------------------------------------
async function loadTimelineChart(start, end) {
    const response = await fetch(`/api/v1/reports/stats/timeline-range?start_date=${start}&end_date=${end}`);
    const data = await response.json();

    const labels = data.map(item => item.time);
    const counts = data.map(item => item.count);

    const ctx = document.getElementById("timelineChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Calls Over Time",
                data: counts,
                borderColor: "rgb(102, 99, 255)",
                backgroundColor: "rgba(99, 255, 177, 0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
