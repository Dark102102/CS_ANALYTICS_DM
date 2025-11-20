# CS2 Machine Learning Feature Engineering Guide

This document explains the feature engineering process and machine learning models for CS2 (Counter-Strike 2) match data analysis.

## Overview

This project creates specialized feature sets for **three types of machine learning models**:

1. **Classification** (Decision Trees, SVM, k-NN, Naïve Bayes) - Predict round winners
2. **Clustering** (K-Means, DBSCAN, Hierarchical) - Discover play style patterns
3. **Regression** (Linear, Ridge, Logistic) - Predict kills, damage, and win probability

Features are organized at **three granularities**:
- **Player-level**: Individual player performance metrics across all matches
- **Round-level**: Round-by-round features for classification and regression
- **Match-level**: Aggregate match statistics

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Parse Demo Files

```bash
python parse_demos_final.py
```

This parses `.dem` files from the `demos/` folder and generates:
- `hltv_data/*_rounds.csv` - Round outcomes with tick boundaries
- `hltv_data/*_deaths.csv` - Kill events properly mapped to rounds
- `hltv_data/*_players.csv` - Per-match player statistics

### 3. Generate Features

```bash
python feature_engineering_redesigned.py
```

This creates the `ml_features/` directory with specialized feature sets for each model type.

### 4. Train Models

```bash
python ml_models_examples.py
```

This trains all three types of models and saves results to `ml_results/`.

## Data Sources

The feature engineering pipeline processes three types of parsed data:

- **Rounds data** (`hltv_data/*_rounds.csv`): Round outcomes, reasons, bomb events, tick boundaries
- **Deaths data** (`hltv_data/*_deaths.csv`): Kill events with weapon, distance, damage, properly mapped to rounds via tick ranges
- **Players data** (`hltv_data/*_players.csv`): Per-match player aggregations

**Current dataset**: **248 rounds** from **11 matches** with **1,956 death events** from **80 unique players**.

### Key Data Improvements

The parsing pipeline now:
- Maps deaths to rounds using **tick boundaries** (not percentile guessing)
- Includes `round_num` in death events for accurate feature engineering
- Filters corrupt/incomplete demo files (>1MB size check)
- Extracts player-level statistics per match

## Feature Engineering Details

The pipeline generates features at three granularities:

---

## 1. Player-Level Features

**File**: `ml_features/player_features.csv`

**Purpose**: Aggregate player performance across all matches for player clustering and skill analysis.

### Features (26 features)

#### Core Statistics
- `attacker_steamid`: Unique Steam ID
- `player_name`: Player name
- `matches_played`: Number of matches played
- `kills`: Total kills across all matches
- `deaths`: Total deaths across all matches
- `headshot_kills`: Total headshot kills
- `overall_kd`: Overall K/D ratio
- `kills_per_match`: Average kills per match

#### Consistency Metrics
- `kd_ratio_std`: Standard deviation of K/D ratio (consistency indicator)
- `kd_ratio_min`: Minimum K/D ratio
- `kd_ratio_max`: Maximum K/D ratio
- `headshot_pct_std`: Standard deviation of headshot percentage
- `kills_std`: Standard deviation of kills per match

#### Weapon Usage
- `ak47_usage_pct`: Percentage of kills with AK47
- `m4a1_usage_pct`: Percentage of kills with M4A1
- `awp_usage_pct`: Percentage of kills with AWP
- `deagle_usage_pct`: Percentage of kills with Deagle
- `famas_usage_pct`: Percentage of kills with Famas
- `glock_usage_pct`: Percentage of kills with Glock

#### Damage Metrics
- `total_damage`: Total damage dealt
- `avg_damage_per_kill`: Average damage per kill
- `damage_per_match`: Average damage per match

#### Special Skills
- `avg_kill_distance`: Average kill distance
- `headshot_rate`: Overall headshot percentage
- `preferred_weapon`: Most frequently used weapon

### Usage

```python
# Load player features
player_df = pd.read_csv('ml_features/player_features.csv')

# Filter active players (2+ matches for consistency)
active_players = player_df[player_df['matches_played'] >= 2]

# Top performers by K/D
top_players = active_players.nlargest(10, 'overall_kd')

# Most consistent players (low K/D std deviation)
consistent = active_players.nsmallest(10, 'kd_ratio_std')

# AWP specialists
awpers = active_players[active_players['awp_usage_pct'] > 10]
```

---

## 2. Round-Level Features

**File**: `ml_features/round_features.csv`

**Purpose**: Round-by-round features for classification and regression models.

### Features (39 features)

#### Core Statistics
- `match_id`: Match identifier
- `round_num`: Round number
- `map_name`: Map name
- `total_kills`: Total kills in round
- `headshot_kills`: Headshot kills
- `headshot_rate`: Headshot percentage
- `unique_killers`: Number of different players with kills

#### Weapon Usage
- `rifle_kills`: AK47, M4A1, M4A4, etc.
- `awp_kills`: AWP kills
- `pistol_kills`: Pistol kills
- `smg_kills`: SMG kills
- `knife_kills`: Knife kills
- `grenade_kills`: Grenade kills

#### Special Events
- `smoke_kills`: Kills through smoke
- `wallbang_kills`: Kills through walls
- `noscope_kills`: No-scope kills
- `airborne_kills`: Airborne kills
- `blind_kills`: Blind kills

#### Distance & Damage
- `avg_kill_distance`: Average kill distance
- `total_damage`: Total damage dealt
- `avg_damage_per_kill`: Average damage per kill

#### Timing & Tempo
- `round_duration`: Round duration in ticks
- `kill_tempo`: Kills per second
- `first_kill_tick`: Tick of first kill
- `time_to_first_kill`: Time to first kill

#### First Kill Analysis
- `first_kill_attacker`: First kill attacker side (T/CT)
- `first_kill_weapon`: Weapon used for first kill
- `first_blood_headshot`: Was first kill a headshot?

#### Momentum Features
- `prev_t_win`: Did T win previous round? (binary)
- `prev_ct_win`: Did CT win previous round? (binary)
- `t_win_streak`: Current T win streak
- `ct_win_streak`: Current CT win streak
- `score_diff`: T rounds won - CT rounds won

#### Bomb Events
- `bomb_planted`: Was bomb planted? (binary)

#### Round Outcome (targets)
- `t_win`: Did T win? (binary, classification target)
- `ct_win`: Did CT win? (binary)
- `winner`: T or CT
- `reason`: Round end reason

---

## 3. Match-Level Features

**File**: `ml_features/match_features.csv`

**Purpose**: Aggregate match statistics for match outcome prediction.

### Features (16 features)

- `match_id`: Match identifier
- `map_name`: Map name
- `total_rounds`: Total rounds played
- `total_kills`: Total kills in match
- `total_deaths`: Total deaths (should equal kills)
- `avg_kills_per_round`: Average kills per round
- `total_headshots`: Total headshot kills
- `headshot_rate`: Overall headshot percentage
- `total_rifle_kills`: Total rifle kills
- `total_awp_kills`: Total AWP kills
- `total_pistol_kills`: Total pistol kills
- `avg_kill_distance`: Average kill distance
- `total_damage`: Total damage dealt
- `t_rounds_won`: T-side rounds won
- `ct_rounds_won`: CT-side rounds won
- `match_winner`: T or CT (based on rounds won)

---

## 4. Classification Features

**Files**: `ml_features/classification_features.csv`

**Purpose**: Predict round winners (T vs CT) using round-level features with momentum and context.

### Features (238 samples, balanced: T=111, CT=127)

This dataset combines round-level features with momentum indicators to predict round winners.

**Important**: Excludes outcome-based features (bomb_exploded, bomb_defused) to prevent data leakage. Only includes bomb_planted as a contextual feature.

### Usage

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data
clf_df = pd.read_csv('ml_features/classification_features.csv')

# Separate features and target
feature_cols = [c for c in clf_df.columns if c not in
                ['match_id', 'round_num', 't_win', 'ct_win', 'winner', 'reason']]
X = clf_df[feature_cols]
y = clf_df['t_win']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

# Decision Tree (no scaling needed)
dt = DecisionTreeClassifier(max_depth=10, min_samples_split=5, class_weight='balanced')
dt.fit(X_train, y_train)
dt_score = dt.score(X_test, y_test)

# SVM (requires scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm = SVC(kernel='rbf', C=1.0, gamma='scale', class_weight='balanced')
svm.fit(X_train_scaled, y_train)
svm_score = svm.score(X_test_scaled, y_test)
```

---

## 5. Regression Features

**Files**: `ml_features/regression_features.csv`

**Purpose**: Predict continuous outcomes (kills, damage) for each round.

### Features (238 samples)

Same as classification features but structured for regression tasks:
- **Target 1**: `total_kills` - Predict number of kills in round
- **Target 2**: `total_damage` - Predict total damage dealt in round
- **Target 3**: `headshot_rate` - Predict headshot percentage

### Usage

```python
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error

reg_df = pd.read_csv('ml_features/regression_features.csv')

# Predict total kills
feature_cols = [c for c in reg_df.columns if c not in
                ['match_id', 'round_num', 'total_kills', 'total_damage', 'headshot_rate']]
X = reg_df[feature_cols]
y_kills = reg_df['total_kills']

# Linear Regression
lr = LinearRegression()
lr.fit(X, y_kills)
predictions = lr.predict(X)
print(f"R²: {r2_score(y_kills, predictions):.4f}")

# Ridge Regression (with regularization)
ridge = Ridge(alpha=1.0)
ridge.fit(X, y_kills)
```

---

## 6. Clustering Features

**Files**: `ml_features/clustering_players.csv`, `ml_features/clustering_rounds.csv`

**Purpose**: Discover patterns in player performance and round playstyles without predefined labels.

### Player Clustering (26 players, 2+ matches)

Clusters players based on performance metrics and weapon preferences:

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler

# Load player clustering data
player_clust = pd.read_csv('ml_features/clustering_players.csv')

# Select features for clustering
feature_cols = ['overall_kd', 'headshot_rate', 'avg_kill_distance',
                'ak47_usage_pct', 'awp_usage_pct', 'damage_per_match']
X = player_clust[feature_cols]

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
player_clust['cluster'] = kmeans.fit_predict(X_scaled)

# Expected clusters:
# Cluster 0: Entry fraggers (high K/D, low AWP usage)
# Cluster 1: AWP specialists (high AWP usage, long range)
# Cluster 2: Support players (moderate stats)
```

### Round Clustering (238 rounds)

Clusters rounds based on playstyle, tempo, and weapon usage:

```python
# Load round clustering data
round_clust = pd.read_csv('ml_features/clustering_rounds.csv')

# Select features
feature_cols = ['total_kills', 'headshot_rate', 'rifle_kills', 'awp_kills',
                'kill_tempo', 'avg_kill_distance', 'bomb_planted']
X = round_clust[feature_cols]

# Normalize
X_scaled = scaler.fit_transform(X)

# Hierarchical Clustering
from sklearn.cluster import AgglomerativeClustering
agg = AgglomerativeClustering(n_clusters=4, linkage='ward')
round_clust['cluster'] = agg.fit_predict(X_scaled)

# Expected clusters:
# Cluster 0: Eco rounds (low kills, pistols)
# Cluster 1: Rifle rounds (balanced, medium kills)
# Cluster 2: AWP-heavy rounds (snipers, long range)
# Cluster 3: Dominant rounds (high kills, quick tempo)
```

---

## Complete Workflow Example

### Step 1: Parse Demo Files

```bash
cd machine_learning
python parse_demos_final.py
```

This processes all `.dem` files in `demos/` and generates properly structured CSVs in `hltv_data/`.

### Step 2: Generate Features

```bash
python feature_engineering_redesigned.py
```

Output:
- `ml_features/player_features.csv` (80 players × 26 features)
- `ml_features/round_features.csv` (248 rounds × 39 features)
- `ml_features/match_features.csv` (11 matches × 16 features)
- `ml_features/classification_features.csv` (238 samples)
- `ml_features/regression_features.csv` (238 samples)
- `ml_features/clustering_players.csv` (26 players, 2+ matches)
- `ml_features/clustering_rounds.csv` (238 rounds)

### Step 3: Train Models

```bash
python ml_models_examples.py
```

Output (when implemented):
- `ml_results/classification_results.csv`
- `ml_results/clustering_results.csv`
- `ml_results/regression_results.csv`

### Step 4: Analyze Results

```python
import pandas as pd

# Load and explore player features
players = pd.read_csv("ml_features/player_features.csv")
print(players.nlargest(10, 'overall_kd'))

# Load classification features
clf_df = pd.read_csv("ml_features/classification_features.csv")
print(f"Dataset balance: T={clf_df['t_win'].sum()}, CT={(~clf_df['t_win']).sum()}")

# Load clustering features
clust_players = pd.read_csv("ml_features/clustering_players.csv")
print(f"Players for clustering: {len(clust_players)}")
```

---

## Dataset Statistics

### Parsed Data (from parse_demos_final.py)
- **Total rounds**: 248 rounds
- **Matches**: 11 matches
- **Death events**: 1,956 kills
- **Unique players**: 80 players
- **Players with 2+ matches**: 26 players (for consistent clustering)

### Round-Level Data
- **Maps**: Inferno, Mirage, Dust2, Train, Overpass, Ancient
- **T-side wins**: 111 rounds (46.6%)
- **CT-side wins**: 127 rounds (53.4%)
- **Average kills per round**: 7.9
- **Average round duration**: ~8,000 ticks

### Player Performance
- **Average K/D ratio**: 1.05
- **Average headshot rate**: 48.3%
- **Average kill distance**: 14.2 units
- **Most common weapon**: AK47 (26.4% of kills)

### Data Quality Improvements
- Deaths properly mapped to rounds via tick boundaries
- Corrupt/incomplete demos filtered out
- No percentile-based guessing for round assignments
- Consistent player tracking across matches

---

## Tips & Best Practices

### Feature Selection

1. **Classification**: Focus on momentum features (win_streak, score_diff) and contextual features
2. **Regression**: Exclude target variables from predictors (e.g., don't use total_kills to predict total_kills)
3. **Clustering**: Use normalized/standardized features for distance-based algorithms
4. **Player Analysis**: Filter to players with 2+ matches for consistency metrics

### Data Leakage Prevention

**Avoid using these features as predictors**:
- `winner`, `reason` (outcome variables for classification)
- `t_win`, `ct_win` (classification targets)
- `total_kills`, `total_damage`, `headshot_rate` (when used as regression targets)
- `bomb_defused`, `bomb_exploded` (outcomes, not predictors)
- `bomb_planted` is OK (happens before round ends)

### Handling Class Imbalance

The dataset is slightly imbalanced (46.6% T-wins, 53.4% CT-wins):

```python
from sklearn.tree import DecisionTreeClassifier

# Use class weights to handle imbalance
dt = DecisionTreeClassifier(class_weight='balanced', max_depth=10)
dt.fit(X_train, y_train)
```

Or use stratified sampling:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
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

Aggregate round-level predictions to predict match winners:

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# Load and train on round-level data
clf_df = pd.read_csv("ml_features/classification_features.csv")
feature_cols = [c for c in clf_df.columns if c not in
                ['match_id', 'round_num', 't_win', 'ct_win', 'winner', 'reason']]

X = clf_df[feature_cols]
y = clf_df['t_win']

# Train model
dt = DecisionTreeClassifier(class_weight='balanced', max_depth=10)
dt.fit(X, y)

# Predict each round
clf_df['predicted_t_win'] = dt.predict(X)

# Aggregate by match
match_predictions = clf_df.groupby('match_id').agg({
    'predicted_t_win': 'sum',
    'round_num': 'count'
})
match_predictions['t_win_rate'] = (
    match_predictions['predicted_t_win'] / match_predictions['round_num']
)

# Predict match winner (>50% rounds won)
match_predictions['predicted_winner'] = (
    match_predictions['t_win_rate'] > 0.5
).map({True: 'T', False: 'CT'})
```

### 2. Player Role Identification

Use clustering to automatically identify player roles:

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load player features
players = pd.read_csv("ml_features/clustering_players.csv")

# Select relevant features
feature_cols = ['overall_kd', 'headshot_rate', 'avg_kill_distance',
                'ak47_usage_pct', 'awp_usage_pct', 'damage_per_match']
X = players[feature_cols]

# Normalize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Cluster
kmeans = KMeans(n_clusters=3, random_state=42)
players['role'] = kmeans.fit_predict(X_scaled)

# Interpret clusters
for cluster_id in range(3):
    cluster_players = players[players['role'] == cluster_id]
    print(f"\n=== Cluster {cluster_id} ===")
    print(f"Avg K/D: {cluster_players['overall_kd'].mean():.2f}")
    print(f"Avg AWP usage: {cluster_players['awp_usage_pct'].mean():.1f}%")
    print(f"Avg distance: {cluster_players['avg_kill_distance'].mean():.1f}")
```

### 3. Momentum Analysis

Analyze how win streaks affect round outcomes:

```python
import pandas as pd

rounds = pd.read_csv("ml_features/round_features.csv")

# Analyze win streak impact
for streak in range(5):
    t_streak_rounds = rounds[rounds['t_win_streak'] == streak]
    t_win_pct = (t_streak_rounds['t_win'].sum() / len(t_streak_rounds) * 100)
    print(f"T win streak {streak}: {t_win_pct:.1f}% T wins")
```

---

## Troubleshooting

### Missing Values

All feature files handle missing values appropriately:
- Numeric columns: Filled with 0
- Categorical columns: Preserved as NaN or empty strings

### Parsing Errors

If demo parsing fails:
1. Check demo file size (must be >1MB)
2. Verify demo file is not corrupt
3. Check `parse_output.log` for detailed error messages

Common parsing errors:
- `DemoEndsEarly`: Demo file is incomplete/truncated
- `range end index out of range`: Demo file is corrupt

### Small Dataset Warning

Current dataset (248 rounds, 11 matches) is relatively small for ML:
- **Classification**: Acceptable for basic models, use cross-validation
- **Regression**: Sufficient for simple linear models
- **Clustering**: Limited, especially for player clustering (26 players with 2+ matches)
- **FPM**: Too small for meaningful pattern mining (not included)

To improve results:
1. Parse more demo files from HLTV
2. Use cross-validation to reduce overfitting
3. Use regularization (Ridge, Lasso, class_weight='balanced')

### Version Compatibility

Tested with:
- Python 3.9+
- scikit-learn 1.3+
- pandas 2.0+
- numpy 1.24+
- demoparser2 (latest)

---

## References

### Academic Papers
- Breiman (2001) - Random Forests
- Cortes & Vapnik (1995) - Support Vector Machines
- Hastie et al. (2009) - The Elements of Statistical Learning

### CS2 Resources
- [HLTV.org](https://www.hltv.org) - Professional CS2 statistics and demo files
- [demoparser2](https://github.com/LaihoE/demoparser2) - CS2 demo parser library

### Library Documentation
- [scikit-learn](https://scikit-learn.org) - Machine learning library
- [pandas](https://pandas.pydata.org) - Data manipulation library

---

## Project Structure

```
machine_learning/
├── demos/                      # .dem demo files (not in repo)
├── hltv_data/                  # Parsed CSV data
│   ├── *_rounds.csv           # Round outcomes with tick boundaries
│   ├── *_deaths.csv           # Kill events mapped to rounds
│   └── *_players.csv          # Per-match player stats
├── ml_features/                # Generated feature sets
│   ├── player_features.csv    # Player-level features
│   ├── round_features.csv     # Round-level features
│   ├── match_features.csv     # Match-level features
│   ├── classification_features.csv
│   ├── regression_features.csv
│   ├── clustering_players.csv
│   └── clustering_rounds.csv
├── parse_demos_final.py        # Demo parser (tick-based mapping)
├── feature_engineering_redesigned.py  # Feature generation
├── scraping.py                 # HLTV data scraper
└── requirements.txt            # Python dependencies
```

---

## Contact & Support

For questions or issues:
1. Check this README first
2. Review code comments in [parse_demos_final.py](../machine_learning/parse_demos_final.py)
3. Review code comments in [feature_engineering_redesigned.py](../machine_learning/feature_engineering_redesigned.py)
4. Check [REPRODUCIBILITY_CHECKLIST.md](REPRODUCIBILITY_CHECKLIST.md) for data collection

---

**Last Updated**: 2024-11-20
**Version**: 2.0.0 (Redesigned with proper tick-based round mapping)
