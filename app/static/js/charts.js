/**
 * AI Resume Analyser & Job Assistant - Visual Charts & Score Gauges (Chart.js)
 */

document.addEventListener("DOMContentLoaded", () => {
    initATSScoreGauge();
    initSkillsRadarChart();
});

function initATSScoreGauge() {
    const canvas = document.getElementById("atsScoreGauge");
    if (!canvas) return;

    const score = parseInt(canvas.getAttribute("data-score"), 10) || 0;
    const remaining = 100 - score;

    // Determine color based on score
    let scoreColor = "#f43f5e"; // rose
    if (score >= 80) {
        scoreColor = "#10b981"; // emerald
    } else if (score >= 60) {
        scoreColor = "#14b8a6"; // teal
    } else if (score >= 40) {
        scoreColor = "#f59e0b"; // amber
    }

    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "doughnut",
        data: {
            datasets: [{
                data: [score, remaining],
                backgroundColor: [
                    scoreColor,
                    "rgba(255, 255, 255, 0.08)"
                ],
                borderWidth: 0,
                borderRadius: [8, 0]
            }]
        },
        options: {
            cutout: "78%",
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                animateRotate: true,
                duration: 1200
            },
            plugins: {
                tooltip: { enabled: false },
                legend: { display: false }
            }
        }
    });
}

function initSkillsRadarChart() {
    const canvas = document.getElementById("skillsRadarChart");
    if (!canvas) return;

    const langCount = parseInt(canvas.getAttribute("data-languages"), 10) || 0;
    const fwCount = parseInt(canvas.getAttribute("data-frameworks"), 10) || 0;
    const cloudCount = parseInt(canvas.getAttribute("data-cloud"), 10) || 0;
    const dbCount = parseInt(canvas.getAttribute("data-databases"), 10) || 0;
    const aiCount = parseInt(canvas.getAttribute("data-ai"), 10) || 0;
    const softCount = parseInt(canvas.getAttribute("data-soft"), 10) || 0;

    const isDarkMode = document.documentElement.getAttribute("data-theme") !== "light";
    const gridColor = isDarkMode ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.1)";
    const labelColor = isDarkMode ? "#94a3b8" : "#475569";

    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "radar",
        data: {
            labels: [
                "Languages",
                "Frameworks",
                "Cloud/DevOps",
                "Databases",
                "AI/Data",
                "Soft Skills"
            ],
            datasets: [{
                label: "Domain Skill Density",
                data: [langCount, fwCount, cloudCount, dbCount, aiCount, softCount],
                backgroundColor: "rgba(99, 102, 241, 0.25)",
                borderColor: "#6366f1",
                pointBackgroundColor: "#38bdf8",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "#6366f1",
                borderWidth: 2,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: gridColor },
                    grid: { color: gridColor },
                    pointLabels: {
                        color: labelColor,
                        font: {
                            family: "'Plus Jakarta Sans', sans-serif",
                            size: 11,
                            weight: "600"
                        }
                    },
                    ticks: {
                        display: false,
                        stepSize: 2
                    },
                    suggestedMin: 0,
                    suggestedMax: 6
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
