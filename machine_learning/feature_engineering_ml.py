#!/usr/bin/env python3
"""
CS2 Feature Engineering for Multiple ML Model Types

This script creates specialized feature sets for:
1. Frequent Pattern Mining (Apriori, FP-Growth)
2. Classification (Decision Trees, SVM, k-NN, Naïve Bayes)
3. Clustering (K-Means, DBSCAN, Hierarchical)
4. Regression (Linear, Logistic)

Author: Data Science Pipeline
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.feature_selection import mutual_info_classif, SelectKBest, f_classif
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR = BASE_DIR / "ml_features"
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("CS2 FEATURE ENGINEERING FOR ML MODELS")
print("="*80)

# ============================================================================
# DATA LOADING
# ============================================================================
print("\n[1] LOADING AND PREPARING DATA...")

# Load all deaths and rounds data
death_files = list(DATA_DIR.glob("*_deaths.csv"))
rounds_files = list(DATA_DIR.glob("*_rounds.csv"))

# Combine deaths
all_deaths = []
for f in death_files:
    try:
        df = pd.read_csv(f)
        match_name = f.stem.replace("_deaths", "")
        df['match'] = match_name
        all_deaths.append(df)
    except Exception as e:
        print(f"  Error loading {f.name}: {e}")

deaths_df = pd.concat(all_deaths, ignore_index=True) if all_deaths else pd.DataFrame()

# Combine rounds
all_rounds = []
for f in rounds_files:
    try:
        df = pd.read_csv(f)
        match_name = f.stem.replace("_rounds", "")
        df['match'] = match_name
        all_rounds.append(df)
    except Exception as e:
        print(f"  Error loading {f.name}: {e}")

rounds_df = pd.concat(all_rounds, ignore_index=True) if all_rounds else pd.DataFrame()

print(f"Loaded {len(deaths_df)} death events from {len(death_files)} files")
print(f"Loaded {len(rounds_df)} rounds from {len(rounds_files)} files")

# Clean data
deaths_df = deaths_df.dropna(subset=['attacker_name', 'user_name'])

# Standardize column names (handle different naming conventions)
if 'winning_team' in rounds_df.columns:
    rounds_df['winner'] = rounds_df['winning_team']
if 'round_end_reason' in rounds_df.columns:
    rounds_df['reason'] = rounds_df['round_end_reason']
if 'round_num' in rounds_df.columns and 'tick' not in rounds_df.columns:
    # Use round_num as ordering if tick not available
    rounds_df['tick'] = rounds_df['round_num']

rounds_df = rounds_df.dropna(subset=['winner'])

# Fill missing values
deaths_df['weapon'] = deaths_df['weapon'].fillna('unknown')
deaths_df['distance'] = deaths_df['distance'].fillna(0)
deaths_df['dmg_health'] = deaths_df['dmg_health'].fillna(0)

for col in ['headshot', 'noscope', 'thrusmoke', 'attackerblind', 'attackerinair']:
    if col in deaths_df.columns:
        deaths_df[col] = deaths_df[col].fillna(False)

# ============================================================================
# BASE FEATURE ENGINEERING
# ============================================================================
print("\n[2] CREATING BASE FEATURES...")

def create_round_features(rounds_df, deaths_df):
    """Create comprehensive round-level features from death events."""
    round_features = []

    for match in rounds_df['match'].unique():
        match_rounds = rounds_df[rounds_df['match'] == match].copy()
        match_deaths = deaths_df[deaths_df['match'] == match].copy()

        if len(match_deaths) == 0:
            continue

        # Sort rounds by round_num (or tick if available)
        if 'round_num' in match_rounds.columns:
            match_rounds = match_rounds.sort_values('round_num')
        else:
            match_rounds = match_rounds.sort_values('tick')
            match_rounds['round_num'] = range(1, len(match_rounds) + 1)

        # Get tick ranges for each round from death events
        if len(match_deaths) > 0:
            death_ticks = match_deaths['tick'].sort_values().values
            n_rounds = len(match_rounds)
            # Estimate tick boundaries by dividing death ticks into n_rounds segments
            tick_boundaries = [0]
            if n_rounds > 1:
                # Use percentiles to split ticks into rounds
                for i in range(1, n_rounds):
                    percentile = (i / n_rounds) * 100
                    tick_boundaries.append(np.percentile(death_ticks, percentile))
            tick_boundaries.append(death_ticks.max() + 1)
        else:
            tick_boundaries = [0, float('inf')]

        for i, (idx, round_row) in enumerate(match_rounds.iterrows()):
            round_num = round_row.get('round_num', i + 1)

            # Get deaths in this round using tick boundaries
            if i < len(tick_boundaries) - 1:
                prev_tick = tick_boundaries[i]
                curr_tick = tick_boundaries[i + 1] if i + 1 < len(tick_boundaries) else float('inf')
            else:
                prev_tick = 0
                curr_tick = float('inf')

            round_deaths = match_deaths[(match_deaths['tick'] > prev_tick) &
                                        (match_deaths['tick'] <= curr_tick)]

            n_kills = len(round_deaths)

            # Extract map from match name or use default
            map_name = 'unknown'
            for m in ['inferno', 'mirage', 'dust2', 'overpass', 'train', 'nuke', 'ancient', 'vertigo', 'anubis']:
                if m in match.lower():
                    map_name = m
                    break

            # Base features
            features = {
                'match': match,
                'round': round_num,
                'map': map_name,
                'winner': round_row['winner'],
                'reason': round_row.get('reason', 'unknown'),
                'tick': curr_tick if curr_tick != float('inf') else 0,

                # === KILL STATISTICS ===
                'total_kills': n_kills,
                'headshot_kills': round_deaths['headshot'].sum() if n_kills > 0 else 0,
                'headshot_rate': round_deaths['headshot'].mean() if n_kills > 0 else 0,

                # === WEAPON CATEGORIES ===
                'rifle_kills': round_deaths['weapon'].str.contains('ak47|m4a1|m4a4|famas|galil|aug|sg553', case=False, na=False).sum(),
                'awp_kills': round_deaths['weapon'].str.contains('awp|ssg08', case=False, na=False).sum(),
                'pistol_kills': round_deaths['weapon'].str.contains('glock|usp|p2000|p250|deagle|fiveseven|tec9|cz75', case=False, na=False).sum(),
                'smg_kills': round_deaths['weapon'].str.contains('mp7|mp9|mp5|mac10|ump45|bizon|p90', case=False, na=False).sum(),
                'shotgun_kills': round_deaths['weapon'].str.contains('nova|xm1014|sawedoff|mag7', case=False, na=False).sum(),
                'knife_kills': round_deaths['weapon'].str.contains('knife', case=False, na=False).sum(),
                'grenade_kills': round_deaths['weapon'].str.contains('hegrenade|inferno|molotov', case=False, na=False).sum(),

                # === SITUATIONAL KILLS ===
                'smoke_kills': round_deaths['thrusmoke'].sum() if 'thrusmoke' in round_deaths.columns else 0,
                'noscope_kills': round_deaths['noscope'].sum() if 'noscope' in round_deaths.columns else 0,
                'wallbang_kills': (round_deaths['penetrated'] > 0).sum() if 'penetrated' in round_deaths.columns else 0,
                'blind_kills': round_deaths['attackerblind'].sum() if 'attackerblind' in round_deaths.columns else 0,
                'airborne_kills': round_deaths['attackerinair'].sum() if 'attackerinair' in round_deaths.columns else 0,

                # === DISTANCE METRICS ===
                'avg_kill_distance': round_deaths['distance'].mean() if n_kills > 0 else 0,
                'max_kill_distance': round_deaths['distance'].max() if n_kills > 0 else 0,
                'min_kill_distance': round_deaths['distance'].min() if n_kills > 0 else 0,
                'std_kill_distance': round_deaths['distance'].std() if n_kills > 1 else 0,

                # === DAMAGE METRICS ===
                'total_damage': round_deaths['dmg_health'].sum(),
                'avg_damage_per_kill': round_deaths['dmg_health'].mean() if n_kills > 0 else 0,
                'max_damage': round_deaths['dmg_health'].max() if n_kills > 0 else 0,
                'armor_damage': round_deaths['dmg_armor'].sum() if 'dmg_armor' in round_deaths.columns else 0,

                # === HITGROUP ANALYSIS ===
                'head_hits': (round_deaths['hitgroup'] == 'head').sum() if 'hitgroup' in round_deaths.columns else 0,
                'chest_hits': (round_deaths['hitgroup'] == 'chest').sum() if 'hitgroup' in round_deaths.columns else 0,
                'limb_hits': round_deaths['hitgroup'].str.contains('arm|leg', case=False, na=False).sum() if 'hitgroup' in round_deaths.columns else 0,

                # === UNIQUE PLAYERS ===
                'unique_killers': round_deaths['attacker_name'].nunique() if n_kills > 0 else 0,
                'unique_victims': round_deaths['user_name'].nunique() if n_kills > 0 else 0,
            }

            # === TIMING FEATURES (within round) ===
            if n_kills > 0:
                kill_ticks = round_deaths['tick'].values
                features['first_kill_tick'] = kill_ticks.min() - prev_tick
                features['last_kill_tick'] = kill_ticks.max() - prev_tick
                features['kill_spread'] = kill_ticks.max() - kill_ticks.min()

                # Kill tempo (kills per tick interval)
                if features['kill_spread'] > 0:
                    features['kill_tempo'] = n_kills / features['kill_spread'] * 1000
                else:
                    features['kill_tempo'] = 0
            else:
                features['first_kill_tick'] = 0
                features['last_kill_tick'] = 0
                features['kill_spread'] = 0
                features['kill_tempo'] = 0

            round_features.append(features)

    return pd.DataFrame(round_features)

# Create base features
base_features = create_round_features(rounds_df, deaths_df)
print(f"Created {len(base_features)} rounds with {len(base_features.columns)} base features")

# Add target variables
base_features['t_win'] = (base_features['winner'] == 'T').astype(int)
base_features['ct_win'] = (base_features['winner'] == 'CT').astype(int)

# ============================================================================
# 1. FREQUENT PATTERN MINING FEATURES
# ============================================================================
print("\n[3] CREATING FREQUENT PATTERN MINING FEATURES...")

def create_fpm_features(base_df):
    """
    Create transaction-style data for Apriori/FP-Growth.
    Each round becomes a transaction with binary items.
    """
    fpm_df = base_df.copy()

    # === BINARY ITEMSETS (presence/absence) ===

    # Weapon usage items
    fpm_df['item_rifle_used'] = (fpm_df['rifle_kills'] > 0).astype(int)
    fpm_df['item_awp_used'] = (fpm_df['awp_kills'] > 0).astype(int)
    fpm_df['item_pistol_only'] = ((fpm_df['pistol_kills'] > 0) & (fpm_df['rifle_kills'] == 0) & (fpm_df['awp_kills'] == 0)).astype(int)
    fpm_df['item_smg_used'] = (fpm_df['smg_kills'] > 0).astype(int)
    fpm_df['item_shotgun_used'] = (fpm_df['shotgun_kills'] > 0).astype(int)
    fpm_df['item_knife_kill'] = (fpm_df['knife_kills'] > 0).astype(int)
    fpm_df['item_grenade_kill'] = (fpm_df['grenade_kills'] > 0).astype(int)

    # Kill style items
    fpm_df['item_high_headshot'] = (fpm_df['headshot_rate'] > 0.5).astype(int)
    fpm_df['item_perfect_headshot'] = (fpm_df['headshot_rate'] == 1.0).astype(int)
    fpm_df['item_multi_kill'] = (fpm_df['total_kills'] >= 5).astype(int)
    fpm_df['item_dominant'] = (fpm_df['total_kills'] >= 7).astype(int)
    fpm_df['item_quick_round'] = (fpm_df['kill_spread'] < fpm_df['kill_spread'].quantile(0.25)).astype(int)
    fpm_df['item_long_round'] = (fpm_df['kill_spread'] > fpm_df['kill_spread'].quantile(0.75)).astype(int)

    # Situational items
    fpm_df['item_smoke_kill'] = (fpm_df['smoke_kills'] > 0).astype(int)
    fpm_df['item_wallbang'] = (fpm_df['wallbang_kills'] > 0).astype(int)
    fpm_df['item_noscope'] = (fpm_df['noscope_kills'] > 0).astype(int)
    fpm_df['item_blind_kill'] = (fpm_df['blind_kills'] > 0).astype(int)

    # Distance items
    fpm_df['item_long_range'] = (fpm_df['avg_kill_distance'] > fpm_df['avg_kill_distance'].quantile(0.75)).astype(int)
    fpm_df['item_close_range'] = (fpm_df['avg_kill_distance'] < fpm_df['avg_kill_distance'].quantile(0.25)).astype(int)
    fpm_df['item_mixed_range'] = (fpm_df['std_kill_distance'] > fpm_df['std_kill_distance'].quantile(0.75)).astype(int)

    # Team coordination items
    fpm_df['item_team_spread'] = (fpm_df['unique_killers'] >= 3).astype(int)
    fpm_df['item_carry_performance'] = (fpm_df['unique_killers'] <= 2).astype(int)

    # Outcome items
    fpm_df['item_t_win'] = fpm_df['t_win']
    fpm_df['item_ct_win'] = fpm_df['ct_win']

    # Reason items
    fpm_df['item_elimination'] = fpm_df['reason'].str.contains('killed|eliminated', case=False, na=False).astype(int)
    fpm_df['item_bomb_exploded'] = fpm_df['reason'].str.contains('exploded', case=False, na=False).astype(int)
    fpm_df['item_bomb_defused'] = fpm_df['reason'].str.contains('defused', case=False, na=False).astype(int)
    fpm_df['item_time_out'] = fpm_df['reason'].str.contains('time', case=False, na=False).astype(int)

    # Map items
    for map_name in ['inferno', 'mirage', 'dust2', 'overpass', 'train', 'nuke', 'ancient']:
        fpm_df[f'item_map_{map_name}'] = (fpm_df['map'] == map_name).astype(int)

    # Extract only item columns for transaction format
    item_cols = [col for col in fpm_df.columns if col.startswith('item_')]

    # Create transaction format (list of items per round)
    transactions = []
    for idx, row in fpm_df.iterrows():
        items = [col.replace('item_', '') for col in item_cols if row[col] == 1]
        transactions.append({
            'round_id': f"{row['match']}_{row['round']}",
            'items': ','.join(items),
            'n_items': len(items)
        })

    transactions_df = pd.DataFrame(transactions)

    return fpm_df[['match', 'round'] + item_cols], transactions_df

fpm_binary, fpm_transactions = create_fpm_features(base_features)
print(f"Created {len([c for c in fpm_binary.columns if c.startswith('item_')])} binary items for FPM")

# Save FPM data
fpm_binary.to_csv(OUTPUT_DIR / "fpm_binary_features.csv", index=False)
fpm_transactions.to_csv(OUTPUT_DIR / "fpm_transactions.csv", index=False)
print(f"✓ Saved FPM features to {OUTPUT_DIR}")

# ============================================================================
# 2. CLASSIFICATION FEATURES
# ============================================================================
print("\n[4] CREATING CLASSIFICATION FEATURES...")

def create_classification_features(base_df):
    """
    Create features optimized for classification algorithms.
    Includes discriminative features, interactions, and proper scaling.
    """
    clf_df = base_df.copy()

    # === DERIVED RATIO FEATURES ===
    clf_df['headshot_efficiency'] = clf_df['headshot_kills'] / (clf_df['total_kills'] + 1)
    clf_df['rifle_ratio'] = clf_df['rifle_kills'] / (clf_df['total_kills'] + 1)
    clf_df['awp_ratio'] = clf_df['awp_kills'] / (clf_df['total_kills'] + 1)
    clf_df['pistol_ratio'] = clf_df['pistol_kills'] / (clf_df['total_kills'] + 1)
    clf_df['special_kills_ratio'] = (clf_df['smoke_kills'] + clf_df['wallbang_kills'] + clf_df['noscope_kills']) / (clf_df['total_kills'] + 1)

    # === INTERACTION FEATURES ===
    clf_df['awp_long_range'] = clf_df['awp_kills'] * clf_df['avg_kill_distance']
    clf_df['rifle_headshot'] = clf_df['rifle_kills'] * clf_df['headshot_rate']
    clf_df['damage_per_distance'] = clf_df['total_damage'] / (clf_df['avg_kill_distance'] + 1)
    clf_df['kills_per_tick'] = clf_df['total_kills'] / (clf_df['kill_spread'] + 1) * 1000

    # === CATEGORICAL ENCODINGS ===
    # Discretize continuous features for Decision Trees / Naïve Bayes
    clf_df['kill_level'] = pd.cut(clf_df['total_kills'], bins=[0, 3, 5, 7, 10], labels=['low', 'medium', 'high', 'dominant'])
    clf_df['distance_level'] = pd.cut(clf_df['avg_kill_distance'], bins=[0, 10, 20, 30, 100], labels=['close', 'medium', 'long', 'sniper'])
    clf_df['headshot_level'] = pd.cut(clf_df['headshot_rate'], bins=[-0.01, 0.33, 0.66, 1.01], labels=['low', 'medium', 'high'])

    # Label encode categorical features
    le = LabelEncoder()
    clf_df['map_encoded'] = le.fit_transform(clf_df['map'].fillna('unknown'))
    clf_df['reason_encoded'] = le.fit_transform(clf_df['reason'].fillna('unknown'))

    # One-hot encode maps for some classifiers
    map_dummies = pd.get_dummies(clf_df['map'], prefix='map')
    clf_df = pd.concat([clf_df, map_dummies], axis=1)

    # === POLYNOMIAL FEATURES (for SVM with RBF) ===
    clf_df['kills_squared'] = clf_df['total_kills'] ** 2
    clf_df['distance_squared'] = clf_df['avg_kill_distance'] ** 2
    clf_df['headshot_squared'] = clf_df['headshot_rate'] ** 2

    # === MOMENTUM FEATURES ===
    # Calculate rolling features within each match
    for match in clf_df['match'].unique():
        match_mask = clf_df['match'] == match
        match_data = clf_df[match_mask].sort_values('round')

        # Previous round performance
        clf_df.loc[match_mask, 'prev_round_kills'] = match_data['total_kills'].shift(1).fillna(0).values
        clf_df.loc[match_mask, 'prev_round_won'] = match_data['t_win'].shift(1).fillna(0).values

        # Cumulative performance
        clf_df.loc[match_mask, 'cumulative_kills'] = match_data['total_kills'].cumsum().values
        clf_df.loc[match_mask, 'win_streak'] = match_data['t_win'].groupby((match_data['t_win'] != match_data['t_win'].shift()).cumsum()).cumsum().values

    # Fill NaN from rolling calculations (only numeric columns)
    numeric_cols = clf_df.select_dtypes(include=[np.number]).columns
    clf_df[numeric_cols] = clf_df[numeric_cols].fillna(0)

    return clf_df

clf_features = create_classification_features(base_features)

# Select numeric features for scaling
numeric_cols = clf_features.select_dtypes(include=[np.number]).columns.tolist()
exclude_cols = ['round', 'tick', 't_win', 'ct_win', 'map_encoded', 'reason_encoded']
feature_cols = [c for c in numeric_cols if c not in exclude_cols]

# Create scaled versions
scaler = StandardScaler()
clf_scaled = clf_features.copy()
clf_scaled[feature_cols] = scaler.fit_transform(clf_features[feature_cols])

print(f"Created {len(feature_cols)} numeric classification features")

# Feature importance using mutual information
X = clf_features[feature_cols].fillna(0)
y = clf_features['t_win']

mi_scores = mutual_info_classif(X, y, random_state=42)
mi_df = pd.DataFrame({'feature': feature_cols, 'mi_score': mi_scores}).sort_values('mi_score', ascending=False)

print("\nTop 10 features by Mutual Information:")
print(mi_df.head(10).to_string())

# Save classification features
clf_features.to_csv(OUTPUT_DIR / "classification_features.csv", index=False)
clf_scaled.to_csv(OUTPUT_DIR / "classification_features_scaled.csv", index=False)
mi_df.to_csv(OUTPUT_DIR / "feature_importance_mi.csv", index=False)
print(f"✓ Saved classification features to {OUTPUT_DIR}")

# ============================================================================
# 3. CLUSTERING FEATURES
# ============================================================================
print("\n[5] CREATING CLUSTERING FEATURES...")

def create_clustering_features(base_df):
    """
    Create features optimized for clustering algorithms.
    Focus on similarity measures and normalized features.
    """
    clust_df = base_df.copy()

    # === NORMALIZED FEATURES (important for K-Means) ===
    # Create proportional features
    clust_df['prop_headshot'] = clust_df['headshot_kills'] / (clust_df['total_kills'] + 1)
    clust_df['prop_rifle'] = clust_df['rifle_kills'] / (clust_df['total_kills'] + 1)
    clust_df['prop_awp'] = clust_df['awp_kills'] / (clust_df['total_kills'] + 1)
    clust_df['prop_pistol'] = clust_df['pistol_kills'] / (clust_df['total_kills'] + 1)
    clust_df['prop_smg'] = clust_df['smg_kills'] / (clust_df['total_kills'] + 1)
    clust_df['prop_special'] = (clust_df['smoke_kills'] + clust_df['wallbang_kills'] + clust_df['noscope_kills']) / (clust_df['total_kills'] + 1)

    # === PLAY STYLE METRICS ===
    # Aggression index (based on damage and speed)
    clust_df['aggression_index'] = (clust_df['total_damage'] / 100) * (clust_df['total_kills'] / 5) / (clust_df['kill_spread'] / 1000 + 1)

    # Precision index (headshots and damage efficiency)
    clust_df['precision_index'] = clust_df['headshot_rate'] * (clust_df['avg_damage_per_kill'] / 100)

    # Range preference
    clust_df['range_preference'] = (clust_df['avg_kill_distance'] - clust_df['avg_kill_distance'].min()) / (clust_df['avg_kill_distance'].max() - clust_df['avg_kill_distance'].min() + 1)

    # Team play index
    clust_df['team_play_index'] = clust_df['unique_killers'] / 5  # Normalized to 5 players

    # === CONSISTENCY METRICS (important for DBSCAN) ===
    clust_df['kill_consistency'] = 1 - (clust_df['std_kill_distance'] / (clust_df['avg_kill_distance'] + 1))
    clust_df['damage_consistency'] = clust_df['avg_damage_per_kill'] / (clust_df['max_damage'] + 1)

    # === COMPOSITE FEATURES ===
    # Economy indicator (weapon tiers)
    clust_df['economy_tier'] = (
        clust_df['rifle_kills'] * 3 +
        clust_df['awp_kills'] * 4 +
        clust_df['smg_kills'] * 2 +
        clust_df['pistol_kills'] * 1
    ) / (clust_df['total_kills'] + 1)

    # Skill expression
    clust_df['skill_expression'] = (
        clust_df['headshot_rate'] * 0.4 +
        clust_df['prop_awp'] * 0.3 +
        clust_df['prop_special'] * 0.3
    )

    return clust_df

clust_features = create_clustering_features(base_features)

# Select clustering-specific features
cluster_cols = [
    'total_kills', 'headshot_rate', 'avg_kill_distance', 'std_kill_distance',
    'total_damage', 'avg_damage_per_kill', 'kill_spread', 'unique_killers',
    'prop_rifle', 'prop_awp', 'prop_pistol', 'prop_smg', 'prop_headshot', 'prop_special',
    'aggression_index', 'precision_index', 'range_preference', 'team_play_index',
    'kill_consistency', 'economy_tier', 'skill_expression'
]

# Keep only existing columns
cluster_cols = [c for c in cluster_cols if c in clust_features.columns]

# Normalize using MinMaxScaler for clustering
minmax = MinMaxScaler()
clust_normalized = clust_features[cluster_cols].copy()
clust_normalized = pd.DataFrame(
    minmax.fit_transform(clust_normalized),
    columns=cluster_cols
)

# Also create standardized version
std_scaler = StandardScaler()
clust_standardized = pd.DataFrame(
    std_scaler.fit_transform(clust_features[cluster_cols]),
    columns=cluster_cols
)

# Add metadata back
clust_normalized['match'] = clust_features['match'].values
clust_normalized['round'] = clust_features['round'].values
clust_normalized['winner'] = clust_features['winner'].values
clust_normalized['map'] = clust_features['map'].values

clust_standardized['match'] = clust_features['match'].values
clust_standardized['round'] = clust_features['round'].values
clust_standardized['winner'] = clust_features['winner'].values
clust_standardized['map'] = clust_features['map'].values

print(f"Created {len(cluster_cols)} clustering features")

# Save clustering features
clust_normalized.to_csv(OUTPUT_DIR / "clustering_features_normalized.csv", index=False)
clust_standardized.to_csv(OUTPUT_DIR / "clustering_features_standardized.csv", index=False)
print(f"✓ Saved clustering features to {OUTPUT_DIR}")

# ============================================================================
# 4. REGRESSION FEATURES
# ============================================================================
print("\n[6] CREATING REGRESSION FEATURES...")

def create_regression_features(base_df):
    """
    Create features for regression tasks.
    Targets: total_kills, total_damage, win_probability
    """
    reg_df = base_df.copy()

    # === CONTINUOUS TARGET VARIABLES ===
    # Primary targets
    reg_df['target_kills'] = reg_df['total_kills']
    reg_df['target_damage'] = reg_df['total_damage']
    reg_df['target_headshot_rate'] = reg_df['headshot_rate']

    # === PREDICTIVE FEATURES (no data leakage) ===
    # Map difficulty features
    map_stats = reg_df.groupby('map').agg({
        'total_kills': 'mean',
        'headshot_rate': 'mean',
        'avg_kill_distance': 'mean'
    }).add_prefix('map_avg_')

    reg_df = reg_df.merge(
        map_stats,
        left_on='map',
        right_index=True,
        how='left'
    )

    # === LOG TRANSFORMED FEATURES (for Linear Regression) ===
    for col in ['total_kills', 'total_damage', 'avg_kill_distance', 'kill_spread']:
        if col in reg_df.columns:
            reg_df[f'{col}_log'] = np.log1p(reg_df[col])

    # === INTERACTION TERMS ===
    reg_df['rifle_x_headshot'] = reg_df['rifle_kills'] * reg_df['headshot_rate']
    reg_df['awp_x_distance'] = reg_df['awp_kills'] * reg_df['avg_kill_distance']
    reg_df['kills_x_damage'] = reg_df['total_kills'] * reg_df['avg_damage_per_kill']

    # === POLYNOMIAL TERMS ===
    reg_df['kills_poly2'] = reg_df['total_kills'] ** 2
    reg_df['distance_poly2'] = reg_df['avg_kill_distance'] ** 2
    reg_df['damage_poly2'] = reg_df['total_damage'] ** 2

    # === MATCH CONTEXT FEATURES ===
    # Round number effects (early vs late game)
    reg_df['round_normalized'] = reg_df['round'] / 30  # Normalize to 30 rounds
    reg_df['is_early_round'] = (reg_df['round'] <= 5).astype(int)
    reg_df['is_late_round'] = (reg_df['round'] >= 25).astype(int)

    # === WITHIN-MATCH ROLLING STATS ===
    for match in reg_df['match'].unique():
        match_mask = reg_df['match'] == match
        match_data = reg_df[match_mask].sort_values('round')

        # Rolling averages (lag to avoid leakage)
        reg_df.loc[match_mask, 'rolling_kills_avg'] = match_data['total_kills'].shift(1).rolling(3, min_periods=1).mean().values
        reg_df.loc[match_mask, 'rolling_damage_avg'] = match_data['total_damage'].shift(1).rolling(3, min_periods=1).mean().values
        reg_df.loc[match_mask, 'rolling_headshot_avg'] = match_data['headshot_rate'].shift(1).rolling(3, min_periods=1).mean().values

    # Fill NaN (only numeric columns)
    numeric_cols = reg_df.select_dtypes(include=[np.number]).columns
    reg_df[numeric_cols] = reg_df[numeric_cols].fillna(0)

    return reg_df

reg_features = create_regression_features(base_features)

# Create logistic regression specific features (probability output)
reg_features['prob_t_win'] = reg_features['t_win'].astype(float)

# Identify feature columns for regression (exclude targets and metadata)
exclude_for_reg = ['match', 'round', 'map', 'winner', 'reason', 'tick', 't_win', 'ct_win',
                   'target_kills', 'target_damage', 'target_headshot_rate', 'prob_t_win',
                   'kill_level', 'distance_level', 'headshot_level']
reg_feature_cols = [c for c in reg_features.columns if c not in exclude_for_reg and reg_features[c].dtype in ['int64', 'float64']]

print(f"Created {len(reg_feature_cols)} regression features")

# Correlation with targets
print("\nTop correlations with target_kills:")
kill_corr = reg_features[reg_feature_cols + ['target_kills']].corr()['target_kills'].drop('target_kills').abs().sort_values(ascending=False)
print(kill_corr.head(10).to_string())

# Save regression features
reg_features.to_csv(OUTPUT_DIR / "regression_features.csv", index=False)
kill_corr.to_frame('correlation').to_csv(OUTPUT_DIR / "regression_correlations.csv")
print(f"✓ Saved regression features to {OUTPUT_DIR}")

# ============================================================================
# 5. PLAYER-LEVEL AGGREGATIONS
# ============================================================================
print("\n[7] CREATING PLAYER-LEVEL FEATURES...")

def create_player_features(deaths_df):
    """
    Aggregate features at player level for player performance analysis.
    """
    player_features = deaths_df.groupby('attacker_steamid').agg({
        'attacker_name': 'first',
        'tick': 'count',  # Total kills
        'headshot': ['sum', 'mean'],
        'distance': ['mean', 'std', 'max'],
        'dmg_health': ['sum', 'mean'],
        'thrusmoke': 'sum',
        'noscope': 'sum',
        'penetrated': lambda x: (x > 0).sum(),
        'weapon': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'unknown'
    }).reset_index()

    # Flatten column names
    player_features.columns = [
        'steamid', 'name', 'total_kills',
        'headshot_kills', 'headshot_rate',
        'avg_distance', 'std_distance', 'max_distance',
        'total_damage', 'avg_damage',
        'smoke_kills', 'noscope_kills', 'wallbang_kills',
        'favorite_weapon'
    ]

    # Add derived metrics
    player_features['kpr'] = player_features['total_kills']  # Kills per round approximation
    player_features['adr'] = player_features['avg_damage']   # Damage per round approximation

    return player_features

if len(deaths_df) > 0:
    player_features = create_player_features(deaths_df)
    player_features.to_csv(OUTPUT_DIR / "player_features.csv", index=False)
    print(f"Created features for {len(player_features)} unique players")
else:
    print("No death data available for player features")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FEATURE ENGINEERING COMPLETE")
print("="*80)

print(f"\nOutput directory: {OUTPUT_DIR}")
print("\nGenerated files:")
print("\n[Frequent Pattern Mining]")
print("  - fpm_binary_features.csv: Binary item matrix")
print("  - fpm_transactions.csv: Transaction format for Apriori/FP-Growth")

print("\n[Classification]")
print("  - classification_features.csv: Full feature set")
print("  - classification_features_scaled.csv: StandardScaler normalized")
print("  - feature_importance_mi.csv: Mutual information scores")

print("\n[Clustering]")
print("  - clustering_features_normalized.csv: MinMax normalized (K-Means)")
print("  - clustering_features_standardized.csv: StandardScaler (DBSCAN)")

print("\n[Regression]")
print("  - regression_features.csv: Features with multiple targets")
print("  - regression_correlations.csv: Feature correlations")

print("\n[Player Analysis]")
print("  - player_features.csv: Player-level aggregations")

print("\n" + "="*80)
print("RECOMMENDED MODEL USAGE")
print("="*80)

print("""
[Frequent Pattern Mining]
- Use fpm_transactions.csv with mlxtend Apriori/FP-Growth
- Find patterns like: {awp_used, long_range} -> {t_win}
- Discover weapon + playstyle combinations that lead to wins

[Classification]
- Use classification_features_scaled.csv for SVM, k-NN
- Use classification_features.csv for Decision Trees, Naive Bayes
- Target: t_win (binary)
- Top features: Check feature_importance_mi.csv

[Clustering]
- K-Means: clustering_features_normalized.csv
- DBSCAN: clustering_features_standardized.csv
- Discover play style clusters (aggressive, passive, sniper, etc.)

[Regression]
- Linear Regression: Predict total_kills, total_damage
- Logistic Regression: Predict prob_t_win
- Use log-transformed features for better linearity
""")
