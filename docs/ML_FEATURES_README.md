# CS2 Machine Learning Feature Engineering Guide

This document explains the feature engineering process and machine learning models for CS2 (Counter-Strike 2) match data analysis.

## Overview

This project creates specialized feature sets for **four types of machine learning models**:

1. **Frequent Pattern Mining** (Apriori, FP-Growth)
2. **Classification** (Decision Trees, SVM, k-NN, Naïve Bayes)
3. **Clustering** (K-Means, DBSCAN, Hierarchical)
4. **Regression** (Linear, Ridge, Logistic)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Features

```bash
python feature_engineering_ml.py
```

This creates the `ml_features/` directory with specialized feature sets for each model type.

### 3. Train Models

```bash
python ml_models_examples.py
```

This trains all four types of models and saves results to `ml_results/`.

## Data Sources

The feature engineering pipeline processes two types of data:

- **Rounds data** (`hltv_data/*_rounds.csv`): Round outcomes, reasons, bomb events
- **Deaths data** (`hltv_data/*_deaths.csv`): Kill events with weapon, distance, damage, etc.

Total dataset: **289 rounds** from **13 matches** with **2,707 death events** from **105 unique players**.

## Feature Engineering Details

### Base Features (38 features)

Created for all models from round-level aggregations:

#### Kill Statistics
- `total_kills`: Total kills in round
- `headshot_kills`: Number of headshot kills
- `headshot_rate`: Headshot percentage
- `unique_killers`: Number of different players with kills
- `unique_victims`: Number of different victims

#### Weapon Categories
- `rifle_kills`: AK47, M4A1, M4A4, Famas, Galil, AUG, SG553
- `awp_kills`: AWP, SSG08 (Scout)
- `pistol_kills`: Glock, USP, P2000, P250, Deagle, Five-Seven, Tec-9, CZ75
- `smg_kills`: MP7, MP9, MP5, MAC-10, UMP-45, Bizon, P90
- `shotgun_kills`: Nova, XM1014, Sawed-Off, MAG-7
- `knife_kills`: Knife kills
- `grenade_kills`: HE grenade, Molotov, Incendiary

#### Situational Kills
- `smoke_kills`: Kills through smoke
- `noscope_kills`: AWP no-scope kills
- `wallbang_kills`: Kills through walls (penetrated > 0)
- `blind_kills`: Kills while attacker is blind
- `airborne_kills`: Kills while attacker is airborne

#### Distance Metrics
- `avg_kill_distance`: Average distance of kills
- `max_kill_distance`: Maximum kill distance
- `min_kill_distance`: Minimum kill distance
- `std_kill_distance`: Standard deviation of kill distances

#### Damage Metrics
- `total_damage`: Total damage dealt in round
- `avg_damage_per_kill`: Average damage per kill
- `max_damage`: Maximum single damage
- `armor_damage`: Total armor damage

#### Hitgroup Analysis
- `head_hits`: Headshots
- `chest_hits`: Chest hits
- `limb_hits`: Arm/leg hits

#### Timing Features
- `first_kill_tick`: Game tick of first kill
- `last_kill_tick`: Game tick of last kill
- `kill_spread`: Tick difference between first and last kill
- `kill_tempo`: Kills per tick interval

#### Metadata
- `match`: Match identifier
- `round`: Round number
- `map`: Map name (inferno, mirage, dust2, etc.)
- `winner`: T or CT
- `reason`: Round end reason

---

## 1. Frequent Pattern Mining Features

**Files**: `fpm_binary_features.csv`, `fpm_transactions.csv`

**Purpose**: Discover patterns in weapon usage, playstyles, and round outcomes.

### Binary Items (35 items)

Each round is transformed into a transaction with binary items:

#### Weapon Items
- `item_rifle_used`: At least 1 rifle kill
- `item_awp_used`: At least 1 AWP kill
- `item_pistol_only`: Only pistol kills (no rifles/AWP)
- `item_smg_used`: At least 1 SMG kill
- `item_shotgun_used`: At least 1 shotgun kill
- `item_knife_kill`: At least 1 knife kill
- `item_grenade_kill`: At least 1 grenade kill

#### Performance Items
- `item_high_headshot`: Headshot rate > 50%
- `item_perfect_headshot`: Headshot rate = 100%
- `item_multi_kill`: 5+ kills in round
- `item_dominant`: 7+ kills in round
- `item_quick_round`: Kill spread < 25th percentile
- `item_long_round`: Kill spread > 75th percentile

#### Situational Items
- `item_smoke_kill`: At least 1 smoke kill
- `item_wallbang`: At least 1 wallbang kill
- `item_noscope`: At least 1 no-scope kill
- `item_blind_kill`: At least 1 blind kill

#### Range Items
- `item_long_range`: Avg distance > 75th percentile
- `item_close_range`: Avg distance < 25th percentile
- `item_mixed_range`: High distance variance (> 75th percentile)

#### Team Coordination
- `item_team_spread`: 3+ different killers
- `item_carry_performance`: ≤2 different killers

#### Outcomes
- `item_t_win`: T-side won
- `item_ct_win`: CT-side won
- `item_elimination`: Round ended by elimination
- `item_bomb_exploded`: Bomb exploded
- `item_bomb_defused`: Bomb defused
- `item_time_out`: Time ran out

#### Map Items
- `item_map_inferno`, `item_map_mirage`, `item_map_dust2`, etc.

### Transaction Format

`fpm_transactions.csv` contains:
- `round_id`: Unique identifier (match_round)
- `items`: Comma-separated list of items
- `n_items`: Number of items in transaction

### Usage with Apriori/FP-Growth

```python
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import pandas as pd

# Load binary features
fpm_binary = pd.read_csv("ml_features/fpm_binary_features.csv")
item_cols = [c for c in fpm_binary.columns if c.startswith('item_')]
items_df = fpm_binary[item_cols].astype(bool)

# Run Apriori
frequent_itemsets = apriori(items_df, min_support=0.1, use_colnames=True)

# Generate rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

# Find patterns predicting wins
win_rules = rules[rules['consequents'].apply(lambda x: 'item_t_win' in str(x))]
```

### Example Patterns to Discover

- `{awp_used, long_range}` → `{t_win}` (Confidence: 0.75)
- `{rifle_used, high_headshot}` → `{dominant}` (Lift: 2.5)
- `{quick_round, team_spread}` → `{ct_win}` (Confidence: 0.68)

---

## 2. Classification Features

**Files**: `classification_features.csv`, `classification_features_scaled.csv`, `feature_importance_mi.csv`

**Purpose**: Predict round winners (T vs CT) using discriminative features.

### Additional Features (48 total)

Built on top of base features with:

#### Ratio Features
- `headshot_efficiency`: Headshot kills / total kills
- `rifle_ratio`: Rifle kills / total kills
- `awp_ratio`: AWP kills / total kills
- `pistol_ratio`: Pistol kills / total kills
- `special_kills_ratio`: (Smoke + wallbang + noscope) / total kills

#### Interaction Features
- `awp_long_range`: AWP kills × avg distance
- `rifle_headshot`: Rifle kills × headshot rate
- `damage_per_distance`: Total damage / avg distance
- `kills_per_tick`: Total kills / kill spread × 1000

#### Categorical Discretization
- `kill_level`: {low, medium, high, dominant} based on total kills
- `distance_level`: {close, medium, long, sniper} based on avg distance
- `headshot_level`: {low, medium, high} based on headshot rate

#### Encodings
- `map_encoded`: Label-encoded map name
- `reason_encoded`: Label-encoded round end reason
- One-hot encoded maps: `map_inferno`, `map_mirage`, etc.

#### Polynomial Features
- `kills_squared`: total_kills²
- `distance_squared`: avg_kill_distance²
- `headshot_squared`: headshot_rate²

#### Momentum Features
- `prev_round_kills`: Kills in previous round
- `prev_round_won`: Won previous round (binary)
- `cumulative_kills`: Cumulative kills in match
- `win_streak`: Current win streak

### Model-Specific Usage

#### Decision Tree / Naïve Bayes
Use **unscaled** features from `classification_features.csv`:

```python
from sklearn.tree import DecisionTreeClassifier

# Load data
clf_features = pd.read_csv("ml_features/classification_features.csv")
X = clf_features[feature_cols]  # Exclude metadata
y = clf_features['t_win']

# Train
dt = DecisionTreeClassifier(max_depth=10, min_samples_split=5)
dt.fit(X, y)
```

#### SVM / k-NN
Use **scaled** features from `classification_features_scaled.csv`:

```python
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

clf_scaled = pd.read_csv("ml_features/classification_features_scaled.csv")
X_scaled = clf_scaled[feature_cols]

# SVM with RBF kernel
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_scaled, y)

# k-NN
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_scaled, y)
```

### Feature Importance

Top 10 features by Mutual Information (see `feature_importance_mi.csv`):

1. `win_streak` (0.694) - Current win streak
2. `std_kill_distance` (0.117) - Kill distance variance
3. `rifle_headshot` (0.082) - Rifle × headshot interaction
4. `headshot_kills` (0.068) - Total headshot kills
5. `kills_squared` (0.063) - Kills polynomial term
6. `avg_damage_per_kill` (0.062) - Damage efficiency
7. `head_hits` (0.057) - Head hitgroup count
8. `total_damage` (0.056) - Total damage dealt
9. `awp_long_range` (0.055) - AWP × distance interaction
10. `damage_per_distance` (0.054) - Damage-distance ratio

---

## 3. Clustering Features

**Files**: `clustering_features_normalized.csv`, `clustering_features_standardized.csv`

**Purpose**: Discover play style patterns without predefined labels.

### Additional Features (21 total)

#### Proportional Features
- `prop_headshot`: Headshot kills / total kills
- `prop_rifle`: Rifle kills / total kills
- `prop_awp`: AWP kills / total kills
- `prop_pistol`: Pistol kills / total kills
- `prop_smg`: SMG kills / total kills
- `prop_special`: Special kills / total kills

#### Play Style Indices
- `aggression_index`: (damage/100) × (kills/5) / (kill_spread/1000 + 1)
- `precision_index`: Headshot rate × (avg_damage/100)
- `range_preference`: Normalized avg kill distance (0-1)
- `team_play_index`: Unique killers / 5

#### Consistency Metrics
- `kill_consistency`: 1 - (std_distance / avg_distance)
- `damage_consistency`: Avg damage / max damage

#### Composite Features
- `economy_tier`: Weighted weapon tier score
  - Rifles: 3 points
  - AWP: 4 points
  - SMG: 2 points
  - Pistol: 1 point
- `skill_expression`: 0.4×headshot_rate + 0.3×awp_ratio + 0.3×special_ratio

### Model-Specific Usage

#### K-Means
Use **MinMax normalized** features from `clustering_features_normalized.csv`:

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

clust_norm = pd.read_csv("ml_features/clustering_features_normalized.csv")
X = clust_norm[feature_cols]

# K-Means
kmeans = KMeans(n_clusters=5, random_state=42)
labels = kmeans.fit_predict(X)

# Evaluate
silhouette = silhouette_score(X, labels)
```

#### DBSCAN
Use **StandardScaler normalized** features from `clustering_features_standardized.csv`:

```python
from sklearn.cluster import DBSCAN

clust_std = pd.read_csv("ml_features/clustering_features_standardized.csv")
X = clust_std[feature_cols]

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)
```

#### Hierarchical Clustering
Works with either normalized version:

```python
from sklearn.cluster import AgglomerativeClustering

agg = AgglomerativeClustering(n_clusters=5, linkage='ward')
labels = agg.fit_predict(X)
```

### Expected Clusters

Potential play style clusters to discover:

1. **AWP Sniper**: High `range_preference`, high `prop_awp`
2. **Aggressive Rifler**: High `aggression_index`, high `prop_rifle`
3. **Eco Round**: High `prop_pistol`, low `economy_tier`
4. **Team Player**: High `team_play_index`, moderate skills
5. **Carry Player**: Low `team_play_index`, high `skill_expression`

---

## 4. Regression Features

**Files**: `regression_features.csv`, `regression_correlations.csv`

**Purpose**: Predict continuous outcomes (kills, damage) and probabilities (win probability).

### Additional Features (51 total)

#### Target Variables
- `target_kills`: Total kills (continuous)
- `target_damage`: Total damage (continuous)
- `target_headshot_rate`: Headshot rate (continuous 0-1)
- `prob_t_win`: T-win probability (binary→float)

#### Map Statistics
- `map_avg_total_kills`: Average kills on this map
- `map_avg_headshot_rate`: Average headshot rate on this map
- `map_avg_avg_kill_distance`: Average distance on this map

#### Log Transformations
- `total_kills_log`: log(1 + total_kills)
- `total_damage_log`: log(1 + total_damage)
- `avg_kill_distance_log`: log(1 + avg_distance)
- `kill_spread_log`: log(1 + kill_spread)

#### Interaction Terms
- `rifle_x_headshot`: Rifle kills × headshot rate
- `awp_x_distance`: AWP kills × avg distance
- `kills_x_damage`: Total kills × avg damage

#### Polynomial Terms
- `kills_poly2`: total_kills²
- `distance_poly2`: avg_kill_distance²
- `damage_poly2`: total_damage²

#### Round Context
- `round_normalized`: Round number / 30
- `is_early_round`: Round ≤ 5 (binary)
- `is_late_round`: Round ≥ 25 (binary)

#### Rolling Statistics (lagged to avoid leakage)
- `rolling_kills_avg`: Rolling 3-round average of kills
- `rolling_damage_avg`: Rolling 3-round average of damage
- `rolling_headshot_avg`: Rolling 3-round average of headshot rate

### Model-Specific Usage

#### Linear Regression (Predict Total Kills)

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

reg_features = pd.read_csv("ml_features/regression_features.csv")
X = reg_features[feature_cols]
y = reg_features['target_kills']

lr = LinearRegression()
lr.fit(X, y)
predictions = lr.predict(X)

print(f"R²: {r2_score(y, predictions):.4f}")
print(f"MSE: {mean_squared_error(y, predictions):.4f}")
```

#### Ridge Regression (Predict Total Damage)

```python
from sklearn.linear_model import Ridge

y_damage = reg_features['target_damage']

ridge = Ridge(alpha=1.0)
ridge.fit(X, y_damage)
```

#### Logistic Regression (Predict Win Probability)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

y_win = reg_features['t_win']

log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X, y_win)

# Predict probabilities
proba = log_reg.predict_proba(X)[:, 1]
auc = roc_auc_score(y_win, proba)
```

### Feature Correlations with Targets

Top correlations with `target_kills` (see `regression_correlations.csv`):

1. `total_kills` (1.000) - Perfect correlation (target leakage, exclude)
2. `kills_poly2` (0.997)
3. `total_kills_log` (0.997)
4. `total_damage` (0.826)
5. `kills_x_damage` (0.826)
6. `damage_poly2` (0.780)
7. `rolling_damage_avg` (0.761)
8. `rolling_kills_avg` (0.742)
9. `head_hits` (0.663)
10. `headshot_kills` (0.620)

**Note**: Exclude `total_kills`, `kills_poly2`, and `total_kills_log` when predicting `target_kills` to avoid data leakage.

---

## Player-Level Features

**File**: `player_features.csv`

**Purpose**: Aggregate player performance across all rounds.

### Player Metrics (14 features)

- `steamid`: Unique Steam ID
- `name`: Player name
- `total_kills`: Total kills
- `headshot_kills`: Total headshot kills
- `headshot_rate`: Overall headshot percentage
- `avg_distance`: Average kill distance
- `std_distance`: Distance standard deviation
- `max_distance`: Longest kill
- `total_damage`: Total damage dealt
- `avg_damage`: Average damage per kill
- `smoke_kills`: Smoke kills
- `noscope_kills`: No-scope kills
- `wallbang_kills`: Wallbang kills
- `favorite_weapon`: Most used weapon
- `kpr`: Kills per round (approximation)
- `adr`: Average damage per round (approximation)

### Usage

```python
player_features = pd.read_csv("ml_features/player_features.csv")

# Top fraggers
top_players = player_features.sort_values('total_kills', ascending=False).head(10)

# Best headshot players
hs_masters = player_features.sort_values('headshot_rate', ascending=False).head(10)

# AWP specialists
awp_players = player_features[player_features['favorite_weapon'] == 'awp']
```

---

## Complete Workflow Example

### Step 1: Generate Features

```bash
python feature_engineering_ml.py
```

Output:
- `ml_features/fpm_binary_features.csv` (289 rounds × 35 items)
- `ml_features/classification_features.csv` (289 rounds × 48 features)
- `ml_features/clustering_features_normalized.csv` (289 rounds × 21 features)
- `ml_features/regression_features.csv` (289 rounds × 51 features)
- `ml_features/player_features.csv` (105 players × 14 features)

### Step 2: Train All Models

```bash
python ml_models_examples.py
```

Output:
- `ml_results/apriori_rules.csv`
- `ml_results/fpgrowth_win_rules.csv`
- `ml_results/classification_results.csv`
- `ml_results/clustering_results.csv`
- `ml_results/regression_results.csv`

### Step 3: Analyze Results

```python
import pandas as pd

# Classification performance
clf_results = pd.read_csv("ml_results/classification_results.csv")
print(clf_results.sort_values('f1_score', ascending=False))

# Clustering quality
clust_results = pd.read_csv("ml_results/clustering_results.csv")
print(clust_results.sort_values('silhouette', ascending=False))

# Association rules predicting wins
win_rules = pd.read_csv("ml_results/fpgrowth_win_rules.csv")
print(win_rules.sort_values('lift', ascending=False).head(10))
```

---

## Dataset Statistics

### Round-Level Data
- **Total rounds**: 289
- **Matches**: 13
- **Maps**: 7 (Inferno, Mirage, Dust2, Train, Overpass, Nuke, Ancient)
- **T-side wins**: ~45%
- **CT-side wins**: ~55%

### Death Events
- **Total kills**: 2,707
- **Unique players**: 105
- **Average kills per round**: 9.4
- **Headshot rate**: 50.8%
- **Average kill distance**: 17.5 units

### Weapons Distribution
- **Rifles**: 44% of kills
- **AWP**: 8% of kills
- **Pistols**: 30% of kills
- **SMGs**: 12% of kills
- **Other**: 6% of kills

---

## Tips & Best Practices

### Feature Selection

1. **Classification**: Use feature importance from `feature_importance_mi.csv`
2. **Regression**: Check correlations in `regression_correlations.csv`
3. **Clustering**: Use domain knowledge to select meaningful features

### Data Leakage Prevention

**Avoid using these features as predictors**:
- `winner`, `reason` (outcome variables)
- `target_*` columns (regression targets)
- `t_win`, `ct_win` (classification targets)
- `tick` (metadata)

### Handling Imbalance

The dataset is slightly imbalanced (45% T-wins, 55% CT-wins):

```python
from sklearn.utils import resample

# Oversample minority class
X_train, y_train = resample(X_train, y_train, stratify=y_train)
```

Or use class weights:

```python
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(class_weight='balanced')
```

### Cross-Validation

Always use cross-validation for model evaluation:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='f1')
print(f"F1: {scores.mean():.4f} ± {scores.std():.4f}")
```

### Hyperparameter Tuning

Use GridSearchCV for optimal parameters:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5)
grid_search.fit(X, y)
print(f"Best params: {grid_search.best_params_}")
```

---

## Advanced Use Cases

### 1. Match Outcome Prediction

Aggregate round-level predictions:

```python
# Predict each round
round_predictions = model.predict(X)

# Aggregate by match
match_predictions = df.groupby('match')['prediction'].agg(['sum', 'count'])
match_predictions['win_rate'] = match_predictions['sum'] / match_predictions['count']

# Predict match winner (team with >50% round win rate)
match_predictions['predicted_winner'] = match_predictions['win_rate'] > 0.5
```

### 2. Player Performance Clustering

```python
from sklearn.cluster import KMeans

player_features = pd.read_csv("ml_features/player_features.csv")
X = player_features[['headshot_rate', 'avg_distance', 'total_kills']]

kmeans = KMeans(n_clusters=3)
player_features['cluster'] = kmeans.fit_predict(X)

# Cluster 0: Entry fraggers (high kills, low distance)
# Cluster 1: AWPers (low headshot rate, high distance)
# Cluster 2: Support players (low kills, varied distance)
```

### 3. Economy Prediction

Create economy features based on weapon usage:

```python
df['eco_round'] = (df['pistol_kills'] > df['rifle_kills']) & (df['awp_kills'] == 0)
df['full_buy'] = (df['rifle_kills'] + df['awp_kills']) > 3
df['force_buy'] = ~df['eco_round'] & ~df['full_buy']

# Predict next round economy
df['next_round_eco'] = df.groupby('match')['eco_round'].shift(-1)
```

---

## Troubleshooting

### Missing Values

All feature files handle missing values:
- Numeric: Filled with 0
- Categorical: Preserved for proper encoding

### Memory Issues

For large datasets, use chunking:

```python
chunksize = 1000
for chunk in pd.read_csv("large_file.csv", chunksize=chunksize):
    process(chunk)
```

### Version Compatibility

Tested with:
- Python 3.9+
- scikit-learn 1.3+
- mlxtend 0.22+
- pandas 2.0+

---

## References

### Academic Papers
- Agrawal & Srikant (1994) - Apriori Algorithm
- Han et al. (2000) - FP-Growth Algorithm
- Breiman (2001) - Random Forests
- Cortes & Vapnik (1995) - Support Vector Machines

### CS2 Resources
- [HLTV.org](https://www.hltv.org) - Professional CS2 statistics
- [demoparser2](https://github.com/LaihoE/demoparser2) - CS2 demo parser

### Library Documentation
- [scikit-learn](https://scikit-learn.org)
- [mlxtend](http://rasbt.github.io/mlxtend/)
- [pandas](https://pandas.pydata.org)

---

## License & Citation

If you use this feature engineering pipeline in your research, please cite:

```
CS2 Machine Learning Feature Engineering Pipeline
Data Analytics & Data Mining Course Project
2024
```

---

## Contact & Support

For questions or issues:
1. Check this README
2. Review the code comments in `feature_engineering_ml.py`
3. Examine example usage in `ml_models_examples.py`

---

**Last Updated**: 2024-11-19
**Version**: 1.0.0
