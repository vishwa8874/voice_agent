// White-Labeled Dashboard JavaScript

let currentPage = 1;
let currentStatusFilter = '';
let statusChart = null;
let trendsChart = null;

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
});

function initializeDashboard() {
    loadSummary();
    loadStats();
    loadLogs();
    updateLastUpdateTime();
}

function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', function() {
        this.disabled = true;
        this.textContent = '⟳ Refreshing...';
        initializeDashboard();
        setTimeout(() => {
            this.disabled = false;
            this.textContent = 'Refresh Data';
        }, 1500);
    });

    document.getElementById('daysSelect').addEventListener('change', function() {
        currentPage = 1;
        initializeDashboard();
    });

    document.getElementById('statusFilter').addEventListener('change', function() {
        currentStatusFilter = this.value;
        currentPage = 1;
        loadLogs();
    });

    document.getElementById('prevBtn').addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            loadLogs();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    document.getElementById('nextBtn').addEventListener('click', function() {
        currentPage++;
        loadLogs();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

function getDaysParameter() {
    return document.getElementById('daysSelect').value;
}

function loadSummary() {
    const days = getDaysParameter();
    
    fetch(`/api/summary?days=${days}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalCalls').textContent = formatNumber(data.total_calls);
            document.getElementById('successfulCalls').textContent = formatNumber(data.successful);
            document.getElementById('failedCalls').textContent = formatNumber(data.failed);
            document.getElementById('successRate').textContent = data.success_rate.toFixed(1) + '%';
            document.getElementById('avgDuration').textContent = data.average_duration;
        })
        .catch(error => console.error('Error loading summary:', error));
}

function loadStats() {
    const days = getDaysParameter();
    
    fetch(`/api/logs/stats?days=${days}`)
        .then(response => response.json())
        .then(data => {
            updateStatusChart(data.status_breakdown);
            updateTrendsChart(data.hourly_trends);
        })
        .catch(error => console.error('Error loading stats:', error));
}

function loadLogs() {
    const days = getDaysParameter();
    let url = `/api/logs?page=${currentPage}&per_page=50`;
    
    if (currentStatusFilter) {
        url += `&status=${currentStatusFilter}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderLogsTable(data.logs);
            updatePagination(data.page, data.pages);
        })
        .catch(error => {
            console.error('Error loading logs:', error);
            document.getElementById('logsTableBody').innerHTML = 
                '<tr><td colspan="5" class="text-center">Error loading logs</td></tr>';
        });
}

function renderLogsTable(logs) {
    const tbody = document.getElementById('logsTableBody');
    
    if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No logs found</td></tr>';
        return;
    }
    
    tbody.innerHTML = logs.map(log => `
        <tr>
            <td><span class="call-id">${truncateId(log.call_id)}</span></td>
            <td>${log.duration.toFixed(2)}</td>
            <td><span class="status-badge ${log.status}">${capitalizeStatus(log.status)}</span></td>
            <td>${formatDateTime(log.timestamp)}</td>
            <td>${log.user_id}</td>
        </tr>
    `).join('');
}

function updatePagination(page, pages) {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageInfo = document.getElementById('pageInfo');
    
    pageInfo.textContent = `Page ${page} of ${pages}`;
    prevBtn.disabled = page === 1;
    nextBtn.disabled = page === pages;
}

function updateStatusChart(statusData) {
    const ctx = document.getElementById('statusChart').getContext('2d');
    
    if (statusChart) {
        statusChart.destroy();
    }
    
    const labels = Object.keys(statusData);
    const data = Object.values(statusData);
    const colors = {
        'completed': '#27ae60',
        'failed': '#e74c3c',
        'pending': '#f39c12'
    };
    
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.map(l => capitalizeStatus(l)),
            datasets: [{
                data: data,
                backgroundColor: labels.map(l => colors[l] || '#3498db'),
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: { size: 12 },
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function updateTrendsChart(hourlyData) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    
    if (trendsChart) {
        trendsChart.destroy();
    }
    
    const labels = Object.keys(hourlyData);
    const data = Object.values(hourlyData);
    
    trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Calls per Hour',
                data: data,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#3498db',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return `Calls: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    },
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    document.getElementById('lastUpdate').textContent = timeString;
}

// Utility Functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

function capitalizeStatus(status) {
    return status.charAt(0).toUpperCase() + status.slice(1);
}

function truncateId(id, length = 12) {
    if (id.length <= length) return id;
    return id.substring(0, length) + '...';
}

// Auto-refresh every 5 minutes
setInterval(function() {
    loadSummary();
    loadStats();
    loadLogs();
    updateLastUpdateTime();
}, 5 * 60 * 1000);

// Error handling
window.addEventListener('error', function(event) {
    console.error('Dashboard error:', event.error);
});
