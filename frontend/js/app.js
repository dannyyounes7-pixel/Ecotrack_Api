// Configuration API
const API_BASE_URL = 'http://127.0.0.1:8000';

// État de l'application
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let airChart = null;
let co2Chart = null;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        showDashboard();
        loadUserData();
    } else {
        showAuthPage();
    }

    setupEventListeners();
});

// Configuration des écouteurs d'événements
function setupEventListeners() {
    // Onglets d'authentification
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchAuthTab(btn.dataset.tab));
    });

    // Formulaires d'authentification
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('signup-form').addEventListener('submit', handleSignup);

    // Déconnexion
    document.getElementById('logout-btn').addEventListener('click', handleLogout);

    // Navigation du dashboard
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    // Filtres
    document.getElementById('apply-filters').addEventListener('click', loadIndicators);
}

// Gestion de l'authentification
function switchAuthTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(form => form.classList.remove('active'));

    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    document.getElementById(`${tab}-form`).classList.add('active');
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) throw new Error('Identifiants invalides');

        const data = await response.json();
        authToken = data.access_token;
        localStorage.setItem('authToken', authToken);

        showDashboard();
        loadUserData();
    } catch (error) {
        showError('login-error', error.message);
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur lors de l\'inscription');
        }

        // Auto-login après inscription
        document.getElementById('login-email').value = email;
        document.getElementById('login-password').value = password;
        switchAuthTab('login');
        document.getElementById('login-form').dispatchEvent(new Event('submit'));
    } catch (error) {
        showError('signup-error', error.message);
    }
}

function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showAuthPage();
}

// Navigation
function showAuthPage() {
    document.getElementById('auth-page').classList.add('active');
    document.getElementById('dashboard-page').classList.remove('active');
}

function showDashboard() {
    document.getElementById('auth-page').classList.remove('active');
    document.getElementById('dashboard-page').classList.add('active');
}

function switchView(view) {
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

    document.querySelector(`[data-view="${view}"]`).classList.add('active');
    document.getElementById(`${view}-view`).classList.add('active');

    // Charger les données selon la vue
    if (view === 'overview') loadOverview();
    if (view === 'zones') loadZones();
    if (view === 'sources') loadSources();
    if (view === 'indicators') loadIndicators();
}

// Chargement des données
async function loadUserData() {
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (!response.ok) throw new Error('Session expirée');

        currentUser = await response.json();
        document.getElementById('user-email').textContent = currentUser.email;

        loadOverview();
    } catch (error) {
        handleLogout();
    }
}

async function loadOverview() {
    try {
        const [zones, sources, indicators] = await Promise.all([
            apiGet('/zones/'),
            apiGet('/sources/'),
            apiGet('/indicators/?limit=100')
        ]);

        document.getElementById('zones-count').textContent = zones.length;
        document.getElementById('sources-count').textContent = sources.length;
        document.getElementById('indicators-count').textContent = indicators.length;

        document.getElementById('indicators-count').textContent = indicators.length;

        // Charger les graphiques
        loadCharts(indicators);

        // Charger les zones dans le filtre
        const filterZone = document.getElementById('filter-zone');
        filterZone.innerHTML = '<option value="">Toutes les zones</option>';
        zones.forEach(zone => {
            const option = document.createElement('option');
            option.value = zone.id;
            option.textContent = zone.name;
            filterZone.appendChild(option);
        });
    } catch (error) {
        console.error('Erreur lors du chargement:', error);
    }
}

async function loadZones() {
    try {
        const zones = await apiGet('/zones/');
        const container = document.getElementById('zones-list');

        container.innerHTML = zones.map(zone => `
            <div class="data-card">
                <h3>${zone.name}</h3>
                <p><strong>Code postal:</strong> ${zone.postal_code}</p>
                <p><strong>ID:</strong> ${zone.id}</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function loadSources() {
    try {
        const sources = await apiGet('/sources/');
        const container = document.getElementById('sources-list');

        container.innerHTML = sources.map(source => `
            <div class="data-card">
                <h3>${source.name}</h3>
                <p><strong>Description:</strong> ${source.description}</p>
                <p><strong>URL:</strong> <a href="${source.url}" target="_blank">${source.url}</a></p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function loadIndicators() {
    try {
        const zoneId = document.getElementById('filter-zone').value;
        const type = document.getElementById('filter-type').value;

        let url = '/indicators/?limit=50';
        if (zoneId) url += `&zone_id=${zoneId}`;
        if (type) url += `&type=${type}`;

        const indicators = await apiGet(url);
        const container = document.getElementById('indicators-list');

        if (indicators.length === 0) {
            container.innerHTML = '<div class="loading">Aucun indicateur trouvé</div>';
            return;
        }

        container.innerHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Zone</th>
                        <th>Source</th>
                        <th>Valeur</th>
                        <th>Unité</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    ${indicators.map(ind => `
                        <tr>
                            <td><span class="badge badge-${ind.type}">${ind.type.toUpperCase()}</span></td>
                            <td>Zone ${ind.zone_id}</td>
                            <td>Source ${ind.source_id}</td>
                            <td>${ind.value}</td>
                            <td>${ind.unit}</td>
                            <td>${new Date(ind.timestamp).toLocaleDateString('fr-FR')}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function loadCharts(indicators) {
    const airCtx = document.getElementById('air-chart');
    const co2Ctx = document.getElementById('co2-chart');

    // Grouper par type et prendre les 50 derniers de chaque
    const airData = indicators.filter(i => i.type === 'air').slice(0, 50).reverse();
    const co2Data = indicators.filter(i => i.type === 'co2').slice(0, 50).reverse();

    // Configuration commune
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false,
        },
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleColor: '#f1f5f9',
                bodyColor: '#cbd5e1',
                borderColor: '#334155',
                borderWidth: 1,
                padding: 12,
                displayColors: true
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                ticks: { color: '#94a3b8', font: { size: 11 } }
            },
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                ticks: { color: '#94a3b8', font: { size: 11 }, maxRotation: 45, minRotation: 45 }
            }
        }
    };

    // Graphique Air
    if (airChart) airChart.destroy();
    airChart = new Chart(airCtx, {
        type: 'line',
        data: {
            labels: airData.map(i => new Date(i.timestamp).toLocaleDateString('fr-FR', { month: 'short', day: 'numeric', hour: '2-digit' })),
            datasets: [{
                label: 'Qualité de l\'air (µg/m³)',
                data: airData.map(i => i.value),
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#f59e0b',
                pointBorderColor: '#fff'
            }]
        },
        options: commonOptions
    });

    // Graphique CO2
    if (co2Chart) co2Chart.destroy();
    co2Chart = new Chart(co2Ctx, {
        type: 'line',
        data: {
            labels: co2Data.map(i => new Date(i.timestamp).toLocaleDateString('fr-FR', { month: 'short', day: 'numeric', hour: '2-digit' })),
            datasets: [{
                label: 'CO₂ (kgCO2)',
                data: co2Data.map(i => i.value),
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff'
            }]
        },
        options: commonOptions
    });
}


// Utilitaires API
async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    });

    if (!response.ok) {
        if (response.status === 401) {
            handleLogout();
            throw new Error('Session expirée');
        }
        throw new Error('Erreur lors de la requête');
    }

    return response.json();
}

function showError(elementId, message) {
    const errorEl = document.getElementById(elementId);
    errorEl.textContent = message;
    errorEl.classList.add('show');
    setTimeout(() => errorEl.classList.remove('show'), 5000);
}
