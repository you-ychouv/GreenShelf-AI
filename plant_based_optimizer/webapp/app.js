// ============================================================================
// CONFIGURATION
// ============================================================================

const API_URL = 'http://localhost:8000';
let currentResult = null;

// ============================================================================
// INITIALISATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    attachEventListeners();
    checkAPIStatus();
});

function initializeApp() {
    console.log('🌱 Plant-Based Optimizer - Web App initialisée');
    hideResults();
    hideLoading();
    hideError();
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function attachEventListeners() {
    // Boutons principaux
    document.getElementById('btn-optimize').addEventListener('click', handleOptimize);
    document.getElementById('btn-validate').addEventListener('click', handleValidate);
    document.getElementById('btn-example').addEventListener('click', loadExample);
    document.getElementById('btn-reset').addEventListener('click', resetForm);
    
    // Boutons résultats
    document.getElementById('btn-export-json').addEventListener('click', exportJSON);
    document.getElementById('btn-new-optimization').addEventListener('click', newOptimization);
    
    // Bouton erreur
    document.getElementById('btn-close-error').addEventListener('click', hideError);
}

// ============================================================================
// API CALLS
// ============================================================================

async function checkAPIStatus() {
    const statusElement = document.getElementById('api-status');
    
    try {
        const response = await fetch(`${API_URL}/health`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (response.ok) {
            statusElement.textContent = '✓ En ligne';
            statusElement.className = 'online';
        } else {
            throw new Error('API non disponible');
        }
    } catch (error) {
        statusElement.textContent = '✗ Hors ligne';
        statusElement.className = 'offline';
        console.error('API Status Error:', error);
    }
}

async function validateProduct(name, ingredients) {
    try {
        const response = await fetch(`${API_URL}/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, ingredients })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Validation Error:', error);
        throw error;
    }
}

async function optimizeProduct(name, ingredients) {
    try {
        const response = await fetch(`${API_URL}/optimize?return_format=simple`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, ingredients }),
            signal: AbortSignal.timeout(120000) // 2 minutes timeout
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erreur lors de l\'optimisation');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Optimization Error:', error);
        throw error;
    }
}

// ============================================================================
// HANDLERS
// ============================================================================

async function handleValidate() {
    const name = document.getElementById('product-name').value.trim();
    const ingredients = document.getElementById('ingredients').value.trim();
    
    // Validation basique
    if (!name || !ingredients) {
        showError('Veuillez remplir tous les champs requis');
        return;
    }
    
    try {
        const validation = await validateProduct(name, ingredients);
        
        if (validation.valid) {
            showValidationSuccess();
        } else {
            showValidationErrors(validation.issues, validation.warnings);
        }
    } catch (error) {
        showError('Erreur lors de la validation: ' + error.message);
    }
}

async function handleOptimize() {
    const name = document.getElementById('product-name').value.trim();
    const ingredients = document.getElementById('ingredients').value.trim();
    
    // Validation basique
    if (!name || !ingredients) {
        showError('Veuillez remplir tous les champs requis');
        return;
    }
    
    // Cacher les résultats précédents
    hideResults();
    hideValidationErrors();
    
    // Afficher le loading
    showLoading();
    
    // Simuler la progression des étapes
    simulateProgress();
    
    try {
        const result = await optimizeProduct(name, ingredients);
        currentResult = result;
        
        hideLoading();
        displayResults(result);
    } catch (error) {
        hideLoading();
        showError('Erreur lors de l\'optimisation: ' + error.message);
    }
}

function loadExample() {
    document.getElementById('product-name').value = 'Yaourt aux fruits';
    document.getElementById('ingredients').value = 'lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120';
    hideValidationErrors();
    hideResults();
}

function resetForm() {
    document.getElementById('product-name').value = '';
    document.getElementById('ingredients').value = '';
    hideValidationErrors();
    hideResults();
    currentResult = null;
}

function newOptimization() {
    hideResults();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function exportJSON() {
    if (!currentResult) return;
    
    const dataStr = JSON.stringify(currentResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `optimization_${currentResult.product_name.replace(/\s+/g, '_')}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

// ============================================================================
// UI UPDATES
// ============================================================================

function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    // Réinitialiser les étapes
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
}

function simulateProgress() {
    const steps = ['step-1', 'step-2', 'step-3', 'step-4'];
    const timings = [0, 15000, 30000, 45000]; // 0s, 15s, 30s, 45s
    
    steps.forEach((stepId, index) => {
        setTimeout(() => {
            document.getElementById(stepId).classList.add('active');
        }, timings[index]);
    });
}

function showError(message) {
    document.getElementById('error-text').textContent = message;
    document.getElementById('error-message').style.display = 'block';
}

function hideError() {
    document.getElementById('error-message').style.display = 'none';
}

function showValidationErrors(issues, warnings) {
    const errorsDiv = document.getElementById('validation-errors');
    const errorsList = document.getElementById('validation-list');
    
    errorsList.innerHTML = '';
    
    issues.forEach(issue => {
        const li = document.createElement('li');
        li.textContent = issue;
        errorsList.appendChild(li);
    });
    
    warnings.forEach(warning => {
        const li = document.createElement('li');
        li.textContent = '⚠️ ' + warning;
        li.style.color = '#ff9800';
        errorsList.appendChild(li);
    });
    
    errorsDiv.style.display = 'block';
}

function showValidationSuccess() {
    const errorsDiv = document.getElementById('validation-errors');
    const errorsList = document.getElementById('validation-list');
    
    errorsDiv.style.background = '#d4edda';
    errorsDiv.style.borderColor = '#4CAF50';
    errorsList.innerHTML = '<li style="color: #4CAF50;">✓ Produit valide! Vous pouvez l\'optimiser.</li>';
    errorsDiv.style.display = 'block';
    
    // Réinitialiser après 3 secondes
    setTimeout(() => {
        hideValidationErrors();
    }, 3000);
}

function hideValidationErrors() {
    const errorsDiv = document.getElementById('validation-errors');
    errorsDiv.style.display = 'none';
    errorsDiv.style.background = '#fff3cd';
    errorsDiv.style.borderColor = '#ff9800';
}

function hideResults() {
    document.getElementById('results').style.display = 'none';
}

function displayResults(result) {
    // Afficher la section résultats
    document.getElementById('results').style.display = 'block';
    
    // Stratégie
    displayStrategy(result.strategy);
    
    // Remplacements
    displayReplacements(result.replacements);
    
    // Métriques
    displayMetrics(result.scores);
    
    // Résumé
    displaySummary(result.summary);
    
    // Recommandations
    displayRecommendations(result.recommendations);
    
    // Scroll vers les résultats
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function displayStrategy(strategy) {
    const strategyDiv = document.getElementById('strategy');
    
    const strategyText = strategy === 'replace_all_additives' 
        ? 'Remplacement de tous les additifs non plant-based'
        : 'Remplacement d\'un ingrédient non plant-based';
    
    strategyDiv.textContent = strategyText;
}

function displayReplacements(replacements) {
    const replacementsDiv = document.getElementById('replacements');
    const countSpan = document.getElementById('replacements-count');
    
    countSpan.textContent = replacements.length;
    replacementsDiv.innerHTML = '';
    
    replacements.forEach(repl => {
        const item = document.createElement('div');
        item.className = 'replacement-item';
        
        item.innerHTML = `
            <div class="replacement-original">
                <span class="replacement-label">Original:</span>
                <span class="replacement-value">${repl.original}</span>
            </div>
            <div class="replacement-arrow">→</div>
            <div class="replacement-new">
                <span class="replacement-label">Nouveau:</span>
                <span class="replacement-value">${repl.replacement}</span>
            </div>
            <div class="replacement-reason">${repl.reason}</div>
        `;
        
        replacementsDiv.appendChild(item);
    });
}

function displayMetrics(scores) {
    const metricsGrid = document.getElementById('metrics-grid');
    metricsGrid.innerHTML = '';
    
    // Calculer les valeurs "avant" à partir des valeurs "après" et des pourcentages
    const metrics = [
        {
            icon: '⏱️',
            title: 'Conservation',
            improvement: scores.shelf_life_improvement,
            unit: 'jours',
            key: 'shelf_life',
            calculateBefore: (improvement) => {
                // Supposons une durée de base de 21 jours (typique pour yaourt)
                const baseDays = 21;
                const newDays = baseDays * (1 + improvement / 100);
                return { before: baseDays, after: newDays };
            }
        },
        {
            icon: '🥗',
            title: 'Nutrition',
            improvement: scores.nutrition_similarity,
            unit: 'kcal/100g',
            key: 'nutrition',
            calculateBefore: (similarity) => {
                // Utiliser les vraies valeurs nutritionnelles
                const originalCal = scores.nutrition_original_calories || 100;
                const newCal = scores.nutrition_new_calories || 100;
                return { before: originalCal, after: newCal };
            }
        },
        {
            icon: '🌍',
            title: 'Carbone',
            improvement: scores.carbon_reduction,
            unit: 'kg CO₂',
            key: 'carbon',
            calculateBefore: (reduction) => {
                // Supposons une empreinte de base de 2.5 kg CO₂
                const baseCO2 = 2.5;
                const newCO2 = baseCO2 * (1 - reduction / 100);
                return { before: baseCO2, after: newCO2 };
            }
        },
        {
            icon: '💰',
            title: 'Coût Production',
            improvement: scores.cost_change_percent || 0,
            unit: '€/kg',
            key: 'cost',
            calculateBefore: (change_percent) => {
                // Utiliser les vraies valeurs de coût
                const originalCost = scores.original_cost_eur || 2.50;
                const newCost = scores.new_cost_eur || 2.50;
                return { before: originalCost, after: newCost };
            }
        },
        {
            icon: '😋',
            title: 'Goût',
            improvement: scores.taste_score,
            unit: '/10',
            key: 'taste',
            calculateBefore: (score) => {
                // Le goût est un score absolu, pas une comparaison
                return { before: null, after: score };
            }
        }
    ];
    
    metrics.forEach(metric => {
        const card = document.createElement('div');
        card.className = `metric-card ${getMetricClass(metric.improvement, metric.key)}`;
        
        const values = metric.calculateBefore(metric.improvement);
        
        let valueHTML;
        if (values.before !== null) {
            // Afficher Avant → Après
            valueHTML = `
                <div class="metric-comparison">
                    <span class="metric-before">${values.before.toFixed(1)}</span>
                    <span class="metric-arrow">→</span>
                    <span class="metric-after">${values.after.toFixed(1)}</span>
                    <span class="metric-unit">${metric.unit}</span>
                </div>
                <div class="metric-change ${metric.improvement >= 0 ? 'positive' : 'negative'}">
                    ${formatMetricValue(metric.improvement, metric.key)}%
                </div>
            `;
        } else {
            // Pour le goût, juste le score
            valueHTML = `
                <div class="metric-value">${values.after.toFixed(1)}${metric.unit}</div>
            `;
        }
        
        card.innerHTML = `
            <div class="metric-icon">${metric.icon}</div>
            <div class="metric-title">${metric.title}</div>
            ${valueHTML}
        `;
        
        metricsGrid.appendChild(card);
    });
    
    // Score total
    document.getElementById('total-score').textContent = scores.total_score.toFixed(3);
    document.getElementById('score-fill').style.width = `${scores.total_score * 100}%`;
}

function displaySummary(summary) {
    document.getElementById('summary').textContent = summary;
}

function displayRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = '';
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
}

// ============================================================================
// HELPERS
// ============================================================================

function getMetricClass(value, key) {
    if (key === 'taste') {
        if (value >= 8) return 'metric-excellent';
        if (value >= 6) return 'metric-good';
        if (value >= 4) return 'metric-average';
        return 'metric-low';
    }
    
    // Pour les pourcentages
    if (value >= 80) return 'metric-excellent';
    if (value >= 60) return 'metric-good';
    if (value >= 40) return 'metric-average';
    return 'metric-low';
}

function formatMetricValue(value, key) {
    if (key === 'shelf_life' || key === 'carbon') {
        return value > 0 ? '+' + value.toFixed(1) : value.toFixed(1);
    }
    return value.toFixed(1);
}

// ============================================================================
// VÉRIFICATION PÉRIODIQUE DE L'API
// ============================================================================

// Vérifier l'état de l'API toutes les 30 secondes
setInterval(checkAPIStatus, 30000);
