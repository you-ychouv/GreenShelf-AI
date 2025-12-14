/**
 * Exemple d'intégration React pour Plant-Based Optimizer
 * 
 * Ce composant montre comment intégrer l'API dans une application React
 */

import React, { useState } from 'react';

// ============================================================================
// COMPOSANT PRINCIPAL
// ============================================================================

function PlantBasedOptimizer() {
  const [product, setProduct] = useState({
    name: '',
    ingredients: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState([]);

  const API_URL = 'http://localhost:8000';

  // Validation du produit
  const validateProduct = async () => {
    try {
      const response = await fetch(`${API_URL}/validate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product)
      });

      const data = await response.json();
      
      if (!data.valid) {
        setValidationErrors(data.issues);
        return false;
      }
      
      setValidationErrors([]);
      return true;
    } catch (err) {
      console.error('Erreur de validation:', err);
      return false;
    }
  };

  // Optimisation du produit
  const handleOptimize = async () => {
    setError(null);
    setResult(null);

    // Valider d'abord
    const isValid = await validateProduct();
    if (!isValid) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/optimize?return_format=simple`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product),
        signal: AbortSignal.timeout(120000) // 2 minutes timeout
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erreur lors de l\'optimisation');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  // Réinitialiser le formulaire
  const handleReset = () => {
    setProduct({ name: '', ingredients: '' });
    setResult(null);
    setError(null);
    setValidationErrors([]);
  };

  // Charger un exemple
  const loadExample = () => {
    setProduct({
      name: 'Yaourt aux fruits',
      ingredients: 'lait entier, sucre, fraises, gélatine, arômes naturels, colorant E120'
    });
    setResult(null);
    setError(null);
    setValidationErrors([]);
  };

  return (
    <div className="optimizer-container">
      <h1>🌱 Optimiseur Plant-Based</h1>
      <p className="subtitle">
        Transformez vos produits avec des alternatives végétales
      </p>

      {/* FORMULAIRE */}
      <div className="form-section">
        <div className="form-group">
          <label htmlFor="product-name">Nom du produit</label>
          <input
            id="product-name"
            type="text"
            placeholder="Ex: Yaourt aux fruits"
            value={product.name}
            onChange={(e) => setProduct({ ...product, name: e.target.value })}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="ingredients">
            Ingrédients (séparés par des virgules)
          </label>
          <textarea
            id="ingredients"
            rows="4"
            placeholder="Ex: lait entier, sucre, fraises, gélatine, arômes naturels"
            value={product.ingredients}
            onChange={(e) => setProduct({ ...product, ingredients: e.target.value })}
            disabled={loading}
          />
        </div>

        {/* ERREURS DE VALIDATION */}
        {validationErrors.length > 0 && (
          <div className="validation-errors">
            <h4>⚠️ Problèmes détectés:</h4>
            <ul>
              {validationErrors.map((err, i) => (
                <li key={i}>{err}</li>
              ))}
            </ul>
          </div>
        )}

        {/* BOUTONS */}
        <div className="button-group">
          <button
            onClick={handleOptimize}
            disabled={loading || !product.name || !product.ingredients}
            className="btn-primary"
          >
            {loading ? '⏳ Optimisation en cours...' : '🚀 Optimiser'}
          </button>
          
          <button
            onClick={loadExample}
            disabled={loading}
            className="btn-secondary"
          >
            📋 Charger un exemple
          </button>
          
          <button
            onClick={handleReset}
            disabled={loading}
            className="btn-secondary"
          >
            🔄 Réinitialiser
          </button>
        </div>
      </div>

      {/* ERREUR */}
      {error && (
        <div className="error-message">
          <h3>❌ Erreur</h3>
          <p>{error}</p>
        </div>
      )}

      {/* RÉSULTATS */}
      {result && (
        <div className="results-section">
          <h2>📊 Résultats de l'optimisation</h2>

          {/* STRATÉGIE */}
          <div className="result-card">
            <h3>🎯 Stratégie</h3>
            <p className="strategy-badge">{result.strategy}</p>
          </div>

          {/* REMPLACEMENTS */}
          <div className="result-card">
            <h3>🔄 Remplacements ({result.replacements.length})</h3>
            <div className="replacements-list">
              {result.replacements.map((repl, i) => (
                <div key={i} className="replacement-item">
                  <div className="replacement-original">
                    <span className="label">Original:</span>
                    <span className="value">{repl.original}</span>
                  </div>
                  <div className="replacement-arrow">→</div>
                  <div className="replacement-new">
                    <span className="label">Nouveau:</span>
                    <span className="value highlight">{repl.replacement}</span>
                  </div>
                  <div className="replacement-reason">
                    <small>{repl.reason}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* SCORES */}
          <div className="result-card">
            <h3>📈 Métriques</h3>
            <div className="metrics-grid">
              <MetricCard
                icon="⏱️"
                title="Conservation"
                value={result.scores.shelf_life_improvement}
                unit="%"
                color="blue"
              />
              <MetricCard
                icon="🥗"
                title="Nutrition"
                value={result.scores.nutrition_similarity}
                unit="%"
                color="green"
              />
              <MetricCard
                icon="🌍"
                title="Carbone"
                value={result.scores.carbon_reduction}
                unit="%"
                color="green"
              />
              <MetricCard
                icon="😋"
                title="Goût"
                value={result.scores.taste_score}
                unit="/10"
                color="orange"
              />
            </div>
            
            <div className="total-score">
              <h4>Score Total</h4>
              <div className="score-value">
                {result.scores.total_score.toFixed(3)}
              </div>
              <div className="score-bar">
                <div
                  className="score-fill"
                  style={{ width: `${result.scores.total_score * 100}%` }}
                />
              </div>
            </div>
          </div>

          {/* RÉSUMÉ */}
          <div className="result-card">
            <h3>💡 Résumé</h3>
            <p className="summary-text">{result.summary}</p>
          </div>

          {/* RECOMMANDATIONS */}
          <div className="result-card">
            <h3>🔬 Recommandations</h3>
            <ul className="recommendations-list">
              {result.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* LOADING */}
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner" />
          <p>Optimisation en cours...</p>
          <small>Cela peut prendre 30-60 secondes</small>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// COMPOSANT MÉTRIQUE
// ============================================================================

function MetricCard({ icon, title, value, unit, color }) {
  const getColorClass = () => {
    if (value > 80) return 'metric-excellent';
    if (value > 60) return 'metric-good';
    if (value > 40) return 'metric-average';
    return 'metric-low';
  };

  return (
    <div className={`metric-card ${getColorClass()}`}>
      <div className="metric-icon">{icon}</div>
      <div className="metric-title">{title}</div>
      <div className="metric-value">
        {value > 0 ? '+' : ''}{value.toFixed(1)}{unit}
      </div>
    </div>
  );
}

// ============================================================================
// STYLES CSS (à ajouter dans votre fichier CSS)
// ============================================================================

const styles = `
.optimizer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.form-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4CAF50;
}

.button-group {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #45a049;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

.validation-errors {
  background: #fff3cd;
  border: 1px solid #ffc107;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.error-message {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.results-section {
  margin-top: 2rem;
}

.result-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 1.5rem;
}

.replacements-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.replacement-item {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 4px;
  align-items: center;
}

.replacement-arrow {
  font-size: 1.5rem;
  color: #4CAF50;
}

.highlight {
  color: #4CAF50;
  font-weight: 600;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric-card {
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.metric-excellent { background: #d4edda; }
.metric-good { background: #d1ecf1; }
.metric-average { background: #fff3cd; }
.metric-low { background: #f8d7da; }

.metric-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.total-score {
  text-align: center;
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 8px;
}

.score-value {
  font-size: 3rem;
  font-weight: 700;
  color: #4CAF50;
  margin: 0.5rem 0;
}

.score-bar {
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 1rem;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  transition: width 0.5s ease;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
`;

export default PlantBasedOptimizer;
