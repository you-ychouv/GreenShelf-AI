"""
Configuration file for Plant-Based Optimizer
"""

import os

# API Configuration
BLACKBOX_API_KEY = os.getenv("BLACKBOX_API_KEY", "your_api_key_here")
BLACKBOX_API_URL = "https://api.blackbox.ai/v1/chat/completions"

# Model Configuration
LLM_MODEL = "blackboxai"
LLM_TEMPERATURE = 0.3  # Lower for more deterministic outputs
LLM_MAX_TOKENS = 2000

# Data Paths
DATA_DIR = "data"
USDA_NUTRITION_PATH = os.path.join(DATA_DIR, "usda_nutrition.csv")
AGRIBALYSE_CARBON_PATH = os.path.join(DATA_DIR, "agribalyse_carbon.csv")
PLANT_ALTERNATIVES_PATH = os.path.join(DATA_DIR, "plant_based_alternatives.csv")
TASTE_PROFILES_PATH = os.path.join(DATA_DIR, "taste_profiles.csv")
SHELF_LIFE_PATH = os.path.join(DATA_DIR, "shelf_life_data.csv")

# Optimization Weights (sum = 1.0)
WEIGHTS = {
    "shelf_life": 0.30,      # 30% - Durée de conservation
    "nutrition": 0.25,       # 25% - Apports nutritionnels
    "carbon": 0.25,          # 25% - Empreinte carbone
    "taste": 0.20            # 20% - Goût
}

# Thresholds
MIN_NUTRITION_SIMILARITY = 0.85  # 85% minimum similarity
MAX_CARBON_INCREASE = 0.0        # No carbon increase allowed
MIN_TASTE_SCORE = 6.0            # Minimum taste score (0-10)

# Shelf Life Calculation Parameters
SHELF_LIFE_PARAMS = {
    "base_temperature": 4,    # °C (refrigeration)
    "q10": 2.0,              # Temperature coefficient
    "ph_optimal": 6.5,       # Optimal pH
    "aw_optimal": 0.95       # Optimal water activity
}

# Categories
INGREDIENT_CATEGORIES = [
    "protein",
    "fat",
    "carbohydrate",
    "preservative",
    "additive",
    "sweetener",
    "thickener",
    "emulsifier",
    "colorant",
    "flavor"
]

# Non-plant-based indicators
NON_PLANT_BASED_KEYWORDS = [
    "lait", "milk", "dairy", "cream", "crème",
    "beurre", "butter", "fromage", "cheese",
    "oeuf", "egg", "blanc d'oeuf", "jaune d'oeuf",
    "viande", "meat", "poulet", "chicken", "boeuf", "beef", "porc", "pork",
    "poisson", "fish", "saumon", "salmon", "thon", "tuna",
    "gélatine", "gelatin", "collagène", "collagen",
    "miel", "honey", "cire d'abeille", "beeswax",
    "lactose", "caséine", "casein", "whey", "lactosérum"
]

# Preservatives and additives (E-numbers)
PRESERVATIVES_ADDITIVES = [
    "E120", "E322", "E441", "E542", "E901", "E904", "E910", "E913", "E920", "E921",
    "gélatine", "gelatin", "cochenille", "carmine", "shellac"
]

# Output Configuration
OUTPUT_DIR = "results"
GENERATE_REPORT = True
REPORT_FORMAT = "json"  # json, pdf, html

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "optimizer.log"

# Number of candidate formulations to generate
NUM_CANDIDATES = 5

# Debug mode
DEBUG = True
