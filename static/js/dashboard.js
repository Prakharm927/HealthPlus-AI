// Simple, error-safe JavaScript
console.log('Dashboard JS loaded');

// API Base
const API_BASE = window.location.origin;

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing...');
    loadDashboard();
});

// Load dashboard data
async function loadDashboard() {
    try {
        // Fetch model info
        const response = await fetch(`${API_BASE}/model-info`);
        if (!response.ok) throw new Error('Failed to fetch models');

        const data = await response.json();
        console.log('Models loaded:', data);

        renderModels(data.models || []);

        // Fetch metrics
        const metricsResponse = await fetch(`${API_BASE}/metrics`);
        if (metricsResponse.ok) {
            const metrics = await metricsResponse.json();
            updateMetrics(metrics);
        }

    } catch (error) {
        console.error('Dashboard load error:', error);
        document.getElementById('models-grid').innerHTML = `
            <div style="padding: 2rem; text-align: center; color: #ff3b30;">
                <p>⚠️ Could not load models. API may not be ready.</p>
                <p style="font-size: 13px; color: var(--text-secondary); margin-top: 0.5rem;">
                    Check console for details
                </p>
            </div>
        `;
    }
}

// Render models
function renderModels(models) {
    const grid = document.getElementById('models-grid');

    if (!models || models.length === 0) {
        grid.innerHTML = '<p style="padding: 2rem; text-align: center; color: var(--text-secondary);">No models available</p>';
        return;
    }

    grid.innerHTML = models.map(model => `
        <div class="model-card">
            <div class="model-header">
                <h3 class="model-name">${formatModelName(model.name)}</h3>
                <span class="model-status">${model.loaded ? '● Loaded' : '○ Not Loaded'}</span>
            </div>
            <p class="model-description">${getModelDescription(model.name)}</p>
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-tertiary); margin-top: 1rem;">
                <span>v${model.version}</span>
                <span>Threshold: ${(model.confidence_threshold * 100).toFixed(0)}%</span>
            </div>
        </div>
    `).join('');
}

// Update metrics
function updateMetrics(metrics) {
    try {
        // Total predictions
        const predictions = metrics.predictions || {};
        let total = 0;
        Object.values(predictions).forEach(model => {
            total += (model.success || 0) + (model.failure || 0);
        });

        const totalEl = document.getElementById('total-predictions');
        if (totalEl) totalEl.textContent = total;

        // Average latency
        const latencies = metrics.latencies || {};
        const latencyValues = Object.values(latencies);
        if (latencyValues.length > 0) {
            const avg = latencyValues.reduce((sum, l) => sum + (l.mean || 0), 0) / latencyValues.length;
            const latencyEl = document.getElementById('avg-latency');
            if (latencyEl) latencyEl.textContent = `${avg.toFixed(0)}ms`;
        }

    } catch (error) {
        console.error('Metrics update error:', error);
    }
}

// Helper functions
function formatModelName(name) {
    return name.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

function getModelDescription(name) {
    const desc = {
        'brain_tumor': 'MRI-based tumor detection',
        'heart': 'Heart disease risk assessment',
        'diabetes': 'Diabetes prediction',
        'kidney': 'Kidney disease detection',
        'liver': 'Liver disease screening',
        'breast_cancer': 'Breast cancer detection',
        'parkinsons': 'Parkinson\'s detection'
    };
    return desc[name] || 'Disease detection';
}

// Auto-refresh metrics every 10 seconds
setInterval(() => {
    fetch(`${API_BASE}/metrics`)
        .then(r => r.json())
        .then(updateMetrics)
        .catch(e => console.error('Metrics refresh failed:', e));
}, 10000);

console.log('Dashboard initialized successfully');
