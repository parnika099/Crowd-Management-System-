const API_BASE = 'http://localhost:8000';
let currentUser = null;

// Check if user is logged in
function checkAuth() {
    const user = localStorage.getItem('user');
    if (!user) {
        window.location.href = 'index.html';
        return null;
    }
    return JSON.parse(user);
}

// Logout function
function logout() {
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Initialize dashboard
async function initDashboard() {
    currentUser = checkAuth();
    if (!currentUser) return;
    
    document.getElementById('user-info').textContent = `Welcome, ${currentUser.name} (${currentUser.role})`;
    
    await loadDashboardData();
    
    // Manual refresh button instead of auto-refresh
    const refreshBtn = document.createElement('button');
    refreshBtn.textContent = '🔄 Refresh Data';
    refreshBtn.className = 'btn-secondary';
    refreshBtn.onclick = loadDashboardData;
    document.querySelector('.header-right').insertBefore(refreshBtn, document.querySelector('.header-right button'));
}

// Load all dashboard data
async function loadDashboardData() {
    await Promise.all([
        loadZones(),
        loadAlerts(),
        loadLogs()
    ]);
    updateStats();
}

// Load zones and their current crowd data
async function loadZones() {
    try {
        const [zonesResponse, crowdDataResponse] = await Promise.all([
            fetch(`${API_BASE}/zones`),
            fetch(`${API_BASE}/crowd-data/latest`)
        ]);
        
        const zones = await zonesResponse.json();
        const crowdData = await crowdDataResponse.json();
        
        // Create a map of zone_id to crowd data
        const crowdMap = {};
        crowdData.forEach(data => {
            crowdMap[data.zone_id] = data;
        });
        
        const container = document.getElementById('zones-container');
        container.innerHTML = '';
        
        zones.forEach(zone => {
            const data = crowdMap[zone.zone_id] || {
                people_count: 0,
                density_level: 'Low',
                timestamp: new Date().toISOString()
            };
            
            const densityClass = data.density_level.toLowerCase();
            const percentage = ((data.people_count / zone.capacity) * 100).toFixed(1);
            
            const zoneCard = document.createElement('div');
            zoneCard.className = `zone-card density-${densityClass}`;
            zoneCard.innerHTML = `
                <div class="zone-header">
                    <div class="zone-name">${zone.location_name}</div>
                    <span class="density-badge ${densityClass}">${data.density_level}</span>
                </div>
                <div class="zone-count">${data.people_count}</div>
                <div class="zone-info">
                    <div>Capacity: ${zone.capacity}</div>
                    <div>Occupancy: ${percentage}%</div>
                    <div>Zone ID: ${zone.zone_id}</div>
                </div>
            `;
            container.appendChild(zoneCard);
        });
    } catch (error) {
        console.error('Error loading zones:', error);
    }
}

// Load alerts
async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        const alerts = await response.json();
        
        const container = document.getElementById('alerts-container');
        container.innerHTML = '';
        
        // Filter only active and acknowledged alerts
        const activeAlerts = alerts.filter(a => a.status !== 'Resolved');
        
        if (activeAlerts.length === 0) {
            container.innerHTML = '<div class="no-data">No active alerts</div>';
            return;
        }
        
        activeAlerts.forEach(alert => {
            const alertItem = document.createElement('div');
            alertItem.className = `alert-item severity-${alert.severity.toLowerCase()}`;
            
            const time = new Date(alert.time).toLocaleString();
            
            alertItem.innerHTML = `
                <div class="alert-header">
                    <div class="alert-title">
                        Alert ${alert.alert_id} - Zone ${alert.zone_id}
                    </div>
                    <span class="alert-status ${alert.status.toLowerCase()}">${alert.status}</span>
                </div>
                <div class="alert-info">
                    <div>Severity: ${alert.severity}</div>
                    <div>Time: ${time}</div>
                    ${alert.responder ? `<div>Responder: ${alert.responder}</div>` : ''}
                </div>
                <div class="alert-actions">
                    ${alert.status === 'Active' ? `
                        <button class="btn-small btn-acknowledge" onclick="updateAlert('${alert.alert_id}', 'Acknowledged')">
                            Acknowledge
                        </button>
                    ` : ''}
                    ${alert.status === 'Acknowledged' ? `
                        <button class="btn-small btn-resolve" onclick="updateAlert('${alert.alert_id}', 'Resolved')">
                            Resolve
                        </button>
                    ` : ''}
                </div>
            `;
            container.appendChild(alertItem);
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

// Update alert status
async function updateAlert(alertId, status) {
    try {
        const response = await fetch(`${API_BASE}/alerts/${alertId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                status: status,
                responder: currentUser.name
            })
        });
        
        if (response.ok) {
            await loadDashboardData();
        }
    } catch (error) {
        console.error('Error updating alert:', error);
    }
}

// Load logs
async function loadLogs() {
    try {
        const response = await fetch(`${API_BASE}/api/logs?limit=10`);
        const logs = await response.json();
        
        const container = document.getElementById('logs-container');
        container.innerHTML = '';
        
        if (logs.length === 0) {
            container.innerHTML = '<div class="no-data">No logs available</div>';
            return;
        }
        
        const table = document.createElement('table');
        table.className = 'logs-table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Action</th>
                    <th>Performed By</th>
                </tr>
            </thead>
            <tbody>
                ${logs.map(log => `
                    <tr>
                        <td>${new Date(log.timestamp).toLocaleString()}</td>
                        <td>${log.action}</td>
                        <td>${log.performed_by}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        container.appendChild(table);
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// Update stats
async function updateStats() {
    try {
        const [zonesResponse, alertsResponse, crowdDataResponse] = await Promise.all([
            fetch(`${API_BASE}/zones`),
            fetch(`${API_BASE}/alerts?status=Active`),
            fetch(`${API_BASE}/crowd-data/latest`)
        ]);
        
        const zones = await zonesResponse.json();
        const activeAlerts = await alertsResponse.json();
        const crowdData = await crowdDataResponse.json();
        
        const highDensityZones = crowdData.filter(d => d.density_level === 'High').length;
        
        document.getElementById('total-zones').textContent = zones.length;
        document.getElementById('active-alerts').textContent = activeAlerts.length;
        document.getElementById('high-density-zones').textContent = highDensityZones;
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Initialize when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}


