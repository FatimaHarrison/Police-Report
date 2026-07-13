async function loadIncidentChart() {
    const response = await fetch("/api/v1/reports/stats/incident-counts");
    const data = await response.json();

    const labels = data.map(item => item.type);
    const counts = data.map(item => item.count);

    new Chart(document.getElementById("incidentChart"), {
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
        }
    });
}

async function loadTimelineChart() {
    const response = await fetch("/api/v1/reports/stats/timeline");
    const data = await response.json();

    const labels = data.map(item => item.time);
    const counts = data.map(item => item.count);

    new Chart(document.getElementById("timelineChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Calls Over Time",
                data: counts,
                borderColor: "rgb(255, 187, 99)",
                backgroundColor: "rgba(219, 99, 255, 0.51)",
                fill: true,
                tension: 0.3
            }]
        }
    });
}

loadIncidentChart();
loadTimelineChart();
