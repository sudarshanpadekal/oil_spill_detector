document.addEventListener('DOMContentLoaded', async () => {
    // 1. Initialize Map
    const map = L.map('map').setView([20.0, 0.0], 2); // Center world
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    const customIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    // 2. Fetch Data
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        // Update Stats
        document.getElementById('totalScans').textContent = data.total_scans;
        document.getElementById('spillsFound').textContent = data.spills_found;

        // Plot Map Markers & Build Report List
        const reportsList = document.getElementById('reportsList');
        reportsList.innerHTML = ''; // clear

        data.recent_detections.forEach(det => {
            // Add marker
            const marker = L.marker([det.lat, det.lng], { icon: customIcon }).addTo(map);
            marker.bindPopup(`
                <strong>Oil Spill Detected</strong><br>
                Confidence: ${(det.confidence * 100).toFixed(1)}%<br>
                Time: ${det.timestamp}
            `);

            // Add report link
            if (det.pdf_url) {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span style="font-size: 0.85rem; color: #bfdbfe;">${det.timestamp.split(' ')[1] || det.timestamp} - ${(det.confidence*100).toFixed(0)}% Match</span>
                    <div>
                        ${det.snapshot_url ? `<a href="${det.snapshot_url}" target="_blank" class="report-link" style="margin-right: 10px;">IMG &rarr;</a>` : ''}
                        <a href="${det.pdf_url}" target="_blank" class="report-link">PDF &rarr;</a>
                    </div>
                `;
                reportsList.appendChild(li);
            }
        });

        if (data.recent_detections.length === 0) {
            reportsList.innerHTML = '<li><span style="color: #bfdbfe; font-size: 0.9rem;">No recent reports</span></li>';
        }

        // 3. Initialize Chart
        const ctx = document.getElementById('statsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.historical.labels,
                datasets: [{
                    label: 'Spills Detected',
                    data: data.historical.data,
                    backgroundColor: 'rgba(251, 113, 133, 0.8)',
                    borderColor: 'rgba(251, 113, 133, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: { color: '#eff6ff' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#bfdbfe' },
                        grid: { color: 'rgba(148, 163, 184, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#bfdbfe' },
                        grid: { display: false }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Failed to load dashboard data", error);
    }
});
