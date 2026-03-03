/* --- GLOBAL CONFIG --- */
const API_URL = "/analyze";
const THREAT_THRESHOLD = 50; // If risk is above 50%, turn everything RED

/* --- DOM ELEMENTS --- */
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const loader = document.getElementById('loader');
const resultsArea = document.getElementById('results-area');
const riskScoreEl = document.getElementById('risk-score');
const statusBadge = document.getElementById('status-badge');
const normalCountEl = document.getElementById('normal-count');
const attackCountEl = document.getElementById('attack-count');
const tableBody = document.getElementById('table-body');

/* --- EVENT LISTENERS --- */
fileInput.addEventListener('change', handleFileUpload);

/* --- MAIN FUNCTION --- */
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    // 1. Show Loader & Hide Previous Results
    loader.style.display = 'block';
    resultsArea.style.display = 'none';

    // 2. Prepare Data
    const formData = new FormData();
    formData.append('file', file);

    try {
        // 3. Send to Python Backend
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // 4. Handle Error
        if (data.error) {
            alert("Error: " + data.error);
            loader.style.display = 'none';
            return;
        }

        // 5. Update Dashboard
        updateDashboard(data);

    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Check console.");
    } finally {
        loader.style.display = 'none';
    }
}

/* --- UI UPDATE LOGIC --- */
function updateDashboard(data) {
    // Reveal Results
    resultsArea.style.display = 'grid';

    // Update Numbers
    riskScoreEl.innerText = `${data.risk_score}%`;
    normalCountEl.innerText = data.normal_traffic;
    attackCountEl.innerText = data.attacks_detected;

    // Update Status Badge (Green vs Red)
    if (data.risk_score > THREAT_THRESHOLD) {
        statusBadge.innerText = "THREAT DETECTED";
        statusBadge.className = "badge danger";
        riskScoreEl.style.color = "var(--accent-red)";
    } else {
        statusBadge.innerText = "SECURE";
        statusBadge.className = "badge safe";
        riskScoreEl.style.color = "var(--accent-green)";
    }

    // Populate Table (First 10 rows)
    tableBody.innerHTML = ""; // Clear old rows
    data.preview.forEach((prediction, index) => {
        const row = document.createElement('tr');
        const statusText = prediction === 1 ? "Attack" : "Normal";
        const statusColor = prediction === 1 ? "color: var(--accent-red);" : "color: var(--accent-green);";
        
        row.innerHTML = `
            <td>#${index + 1}</td>
            <td style="${statusColor} font-weight: bold;">${statusText}</td>
            <td>${prediction === 1 ? "🚨" : "✅"}</td>
        `;
        tableBody.appendChild(row);
    });
}