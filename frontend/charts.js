async function loadCharts() {
    const date = document.getElementById("dateInput").value;

    if (!date) {
        alert("Please select a date first.");
        return;
    }

    loadIncidentChart(date);
    loadTimelineChart(date);
}


// ---------------------------------------------
// BAR CHART: Incident Counts
// ---------------------------------------------
async function loadIncidentChart(date) {
    const response = await fetch(`/api/v1/reports/stats/incident-counts?date=${date}`);
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



// LINE CHART: Calls Over Time

async function loadTimelineChart(date) {
    const response = await fetch(`/api/v1/reports/stats/timeline?date=${date}`);
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
