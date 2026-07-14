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
                backgroundColor: "rgba(223, 13, 31, 0.6)",
                borderColor: "rgb(108, 54, 235)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
             scales: {
        x: {
            ticks: {
                color: "#000000",
                font: {
                    size: 14,
                    weight: "bold"
                }
            }
        },
        y: {
            ticks: {
                color: "#000000",
                font: {
                    size: 14,
                    weight: "bold"
                }
            }
        }
    },
            plugins: {
                legend: {
                    position: "top"
                }
            }
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
                borderColor: "rgb(99, 255, 195)",
                backgroundColor: "rgba(219, 99, 255, 0.51)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
             scales: {
        x: {
            ticks: {
                color: "#000000",
                font: {
                    size: 12,
                    weight: "bold"
                }
            }
        },
        y: {
            ticks: {
                color: "#000000",
                font: {
                    size: 14,
                    weight: "bold"
                }
            }
        }
    },
            plugins: {
                legend: {
                    position: "top"
                }
            }
        }
    });
}


loadIncidentChart();
loadTimelineChart();