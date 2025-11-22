#!/usr/bin/env python3
"""
Redesigned Feature Engineering for CS2 Match Analysis

Focus on:
1. Player-level features (performance, consistency, weapon preference)
2. Round-level features (tempo, economy, first kills)
3. Match-level aggregations (team dynamics, map control)

Uses properly parsed data with round_num correctly mapped.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR = BASE_DIR / "ml_features"
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("CS2 FEATURE ENGINEERING - REDESIGNED")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1] LOADING DATA...")

# Load all data files
rounds_files = sorted(DATA_DIR.glob("*_rounds.csv"))
deaths_files = sorted(DATA_DIR.glob("*_deaths.csv"))
players_files = sorted(DATA_DIR.glob("*_players.csv"))

print(f"Found {len(rounds_files)} matches")

# Combine all data
all_rounds = pd.concat([pd.read_csv(f) for f in rounds_files], ignore_index=True)
all_deaths = pd.concat([pd.read_csv(f) for f in deaths_files], ignore_index=True)
all_players = pd.concat([pd.read_csv(f) for f in players_files], ignore_index=True)

print(f"Loaded:")
print(f"  - {len(all_rounds)} rounds")
print(f"  - {len(all_deaths)} deaths")
print(f"  - {len(all_players)} player records")
print(f"  - {all_deaths['round_num'].nunique()} rounds with deaths")

# ============================================================================
# 2. PLAYER-LEVEL FEATURES
# ============================================================================
print("\n[2] CREATING PLAYER-LEVEL FEATURES...")

# Aggregate across all matches for each player
player_features = all_players.groupby('attacker_steamid').agg({
    'player_name': 'first',
    'kills': 'sum',
    'deaths': 'sum',
    'headshot_kills': 'sum',
    'total_damage': 'sum',
    'avg_kill_distance': 'mean',
    'kd_ratio': 'mean',
    'headshot_pct': 'mean',
    'match_id': 'count'  # matches played
}).rename(columns={'match_id': 'matches_played'}).reset_index()

# Add derived features
player_features['total_kills'] = player_features['kills']
player_features['total_deaths'] = player_features['deaths']
player_features['overall_kd'] = player_features['total_kills'] / player_features['total_deaths'].replace(0, 1)
player_features['kills_per_match'] = player_features['total_kills'] / player_features['matches_played']
player_features['deaths_per_match'] = player_features['total_deaths'] / player_features['matches_played']
player_features['damage_per_match'] = player_features['total_damage'] / player_features['matches_played']

# Weapon usage from deaths
weapon_usage = all_deaths.groupby('attacker_steamid')['weapon'].value_counts().unstack(fill_value=0)
weapon_usage['total'] = weapon_usage.sum(axis=1)
weapon_usage = weapon_usage.div(weapon_usage['total'], axis=0) * 100  # Percentages

# Merge top weapons
for weapon in ['ak47', 'awp', 'm4a1_silencer', 'deagle', 'glock']:
    if weapon in weapon_usage.columns:
        player_features = player_features.merge(
            weapon_usage[[weapon]].rename(columns={weapon: f'{weapon}_usage_pct'}),
            left_on='attacker_steamid',
            right_index=True,
            how='left'
        ).fillna(0)

# Consistency metrics (variation across matches)
player_consistency = all_players.groupby('attacker_steamid').agg({
    'kd_ratio': ['std', 'min', 'max'],
    'headshot_pct': 'std',
    'kills': 'std'
}).round(2)
player_consistency.columns = ['_'.join(col).strip() for col in player_consistency.columns.values]
player_features = player_features.merge(player_consistency, left_on='attacker_steamid', right_index=True, how='left').fillna(0)

print(f"Created {len(player_features)} player profiles with {len(player_features.columns)} features")

# Save
player_features.to_csv(OUTPUT_DIR / "player_features.csv", index=False)
print(f"✓ Saved player_features.csv")

# ============================================================================
# 3. ROUND-LEVEL FEATURES
# ============================================================================
print("\n[3] CREATING ROUND-LEVEL FEATURES...")

# Merge deaths with rounds
round_features = all_rounds.copy()

# Aggregate deaths per round
deaths_by_round = all_deaths.groupby(['match_id', 'round_num']).agg({
    'victim_name': 'count',  # total kills
    'headshot': 'sum',
    'distance': ['mean', 'std', 'max'],
    'dmg_health': 'sum',
    'weapon': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'unknown',
    'thrusmoke': 'sum',
    'penetrated': lambda x: (x > 0).sum(),
    'noscope': 'sum',
    'tick': ['min', 'max']  # first and last kill
}).reset_index()

deaths_by_round.columns = ['_'.join(col).strip('_') for col in deaths_by_round.columns.values]
deaths_by_round = deaths_by_round.rename(columns={
    'victim_name_count': 'total_kills',
    'headshot_sum': 'headshot_kills',
    'distance_mean': 'avg_kill_distance',
    'distance_std': 'kill_distance_std',
    'distance_max': 'max_kill_distance',
    'dmg_health_sum': 'total_damage',
    'weapon_<lambda>': 'most_common_weapon',
    'thrusmoke_sum': 'smoke_kills',
    'penetrated_<lambda>': 'wallbang_kills',
    'noscope_sum': 'noscope_kills',
    'tick_min': 'first_kill_tick',
    'tick_max': 'last_kill_tick'
})

# Merge with rounds
round_features = round_features.merge(
    deaths_by_round,
    on=['match_id', 'round_num'],
    how='left'
).fillna(0)

# Add derived features
round_features['headshot_rate'] = round_features['headshot_kills'] / round_features['total_kills'].replace(0, 1)
round_features['kill_duration'] = round_features['last_kill_tick'] - round_features['first_kill_tick']
round_features['kill_tempo'] = round_features['total_kills'] / round_features['kill_duration'].replace(0, 1) * 1000

# First kill analysis
first_kills = all_deaths.sort_values(['match_id', 'round_num', 'tick']).groupby(['match_id', 'round_num']).first()
round_features = round_features.merge(
    first_kills[['attacker_name', 'weapon', 'headshot']].add_prefix('first_kill_'),
    left_on=['match_id', 'round_num'],
    right_index=True,
    how='left'
)

# Economy indicators (weapon types)
weapon_counts = all_deaths.groupby(['match_id', 'round_num', 'weapon']).size().unstack(fill_value=0)
for weapon_type in ['rifle', 'awp', 'pistol', 'smg']:
    if weapon_type in str(weapon_counts.columns):
        cols = [c for c in weapon_counts.columns if weapon_type in str(c).lower()]
        if cols:
            round_features = round_features.merge(
                weapon_counts[cols].sum(axis=1).rename(f'{weapon_type}_kills'),
                left_on=['match_id', 'round_num'],
                right_index=True,
                how='left'
            ).fillna(0)

# Target variables
round_features['t_win'] = (round_features['winning_team'] == 'T').astype(int)
round_features['ct_win'] = (round_features['winning_team'] == 'CT').astype(int)

# Momentum features (within match)
for match_id in round_features['match_id'].unique():
    mask = round_features['match_id'] == match_id
    match_data = round_features[mask].sort_values('round_num')

    # Previous round outcome
    round_features.loc[mask, 'prev_t_win'] = match_data['t_win'].shift(1).fillna(0).values
    round_features.loc[mask, 'prev_ct_win'] = match_data['ct_win'].shift(1).fillna(0).values

    # Win streaks
    round_features.loc[mask, 't_win_streak'] = match_data['t_win'].groupby(
        (match_data['t_win'] != match_data['t_win'].shift()).cumsum()
    ).cumsum().values

    # Score
    round_features.loc[mask, 't_score'] = match_data['t_win'].cumsum().values
    round_features.loc[mask, 'ct_score'] = match_data['ct_win'].cumsum().values
    round_features.loc[mask, 'score_diff'] = (match_data['t_win'].cumsum() - match_data['ct_win'].cumsum()).values

print(f"Created {len(round_features)} rounds with {len(round_features.columns)} features")

# Save
round_features.to_csv(OUTPUT_DIR / "round_features.csv", index=False)
print(f"✓ Saved round_features.csv")

# ============================================================================
# 4. MATCH-LEVEL FEATURES
# ============================================================================
print("\n[4] CREATING MATCH-LEVEL FEATURES...")

match_features = all_rounds.groupby('match_id').agg({
    'round_num': 'max',  # total rounds
    'winning_team': lambda x: (x == 'T').sum(),  # T wins
    'bomb_planted': 'sum',
    'bomb_defused': 'sum',
    'bomb_exploded': 'sum',
    'map_name': 'first'
}).rename(columns={
    'round_num': 'total_rounds',
    'winning_team': 't_rounds_won'
}).reset_index()

match_features['ct_rounds_won'] = match_features['total_rounds'] - match_features['t_rounds_won']
match_features['t_win_pct'] = match_features['t_rounds_won'] / match_features['total_rounds'] * 100
match_features['overtime'] = (match_features['total_rounds'] > 30).astype(int)

# Add match-level death stats
match_deaths = all_deaths.groupby('match_id').agg({
    'victim_name': 'count',
    'headshot': ['sum', 'mean'],
    'distance': 'mean',
    'dmg_health': 'sum',
    'attacker_steamid': 'nunique'  # unique players
}).round(2)
match_deaths.columns = ['_'.join(col).strip('_') for col in match_deaths.columns.values]
match_deaths = match_deaths.rename(columns={
    'victim_name_count': 'total_kills',
    'headshot_sum': 'total_headshots',
    'headshot_mean': 'headshot_rate',
    'distance_mean': 'avg_kill_distance',
    'dmg_health_sum': 'total_damage',
    'attacker_steamid_nunique': 'unique_players'
})

match_features = match_features.merge(match_deaths, left_on='match_id', right_index=True, how='left')

print(f"Created {len(match_features)} match records with {len(match_features.columns)} features")

# Save
match_features.to_csv(OUTPUT_DIR / "match_features.csv", index=False)
print(f"✓ Saved match_features.csv")

# ============================================================================
# 5. CLASSIFICATION DATASET (Round Winner Prediction)
# ============================================================================
print("\n[5] CREATING CLASSIFICATION DATASET...")

# Select features for classification (no data leakage)
clf_features = round_features[[
    'match_id', 'round_num', 'map_name',
    # Round context
    'round_num', 'bomb_planted', 'bomb_defused', 'bomb_exploded',
    # Kill stats (aggregate, no winner info)
    'total_kills', 'headshot_kills', 'headshot_rate',
    'avg_kill_distance', 'kill_distance_std', 'max_kill_distance',
    'total_damage', 'kill_duration', 'kill_tempo',
    # Special kills
    'smoke_kills', 'wallbang_kills', 'noscope_kills',
    # First kill
    'first_kill_headshot',
    # Momentum
    'prev_t_win', 'prev_ct_win', 't_win_streak',
    't_score', 'ct_score', 'score_diff',
    # Target
    't_win', 'ct_win'
]].copy()

# Remove rows with missing winner (round 1 often has no kills)
clf_features = clf_features[clf_features['total_kills'] > 0].reset_index(drop=True)

# Encode map
clf_features['map_encoded'] = pd.factorize(clf_features['map_name'])[0]

# Scale numeric features
numeric_cols = clf_features.select_dtypes(include=[np.number]).columns.tolist()
exclude = ['match_id', 'round_num', 't_win', 'ct_win', 'map_encoded']
scale_cols = [c for c in numeric_cols if c not in exclude]

clf_scaled = clf_features.copy()
scaler = StandardScaler()
clf_scaled[scale_cols] = scaler.fit_transform(clf_features[scale_cols])

print(f"Created classification dataset: {len(clf_features)} samples, {len(scale_cols)} features")

# Save
clf_features.to_csv(OUTPUT_DIR / "classification_features.csv", index=False)
clf_scaled.to_csv(OUTPUT_DIR / "classification_features_scaled.csv", index=False)
print(f"✓ Saved classification_features.csv")
print(f"✓ Saved classification_features_scaled.csv")

# ============================================================================
# 6. REGRESSION DATASET (Kills/Damage Prediction)
# ============================================================================
print("\n[6] CREATING REGRESSION DATASET...")

# Predict total_kills and total_damage
reg_features = round_features[[
    'match_id', 'round_num', 'map_name',
    # Context
    'bomb_planted', 'prev_t_win', 'prev_ct_win',
    't_score', 'ct_score', 'score_diff',
    # Targets
    'total_kills', 'total_damage', 'headshot_rate',
    # Other features (for predicting above)
    'kill_duration', 'smoke_kills', 'wallbang_kills'
]].copy()

reg_features = reg_features[reg_features['total_kills'] > 0].reset_index(drop=True)
reg_features['map_encoded'] = pd.factorize(reg_features['map_name'])[0]

print(f"Created regression dataset: {len(reg_features)} samples")

# Save
reg_features.to_csv(OUTPUT_DIR / "regression_features.csv", index=False)
print(f"✓ Saved regression_features.csv")

# ============================================================================
# 7. CLUSTERING DATASET (Player/Round Patterns)
# ============================================================================
print("\n[7] CREATING CLUSTERING DATASET...")

# Player clustering (play styles)
player_cluster = player_features[[
    'attacker_steamid', 'player_name',
    'overall_kd', 'headshot_pct', 'avg_kill_distance',
    'kills_per_match', 'deaths_per_match',
    'kd_ratio_std',  # consistency
    'matches_played'
]].copy()

player_cluster = player_cluster[player_cluster['matches_played'] >= 2]  # At least 2 matches

# Normalize for clustering
numeric_cols = player_cluster.select_dtypes(include=[np.number]).columns.tolist()
exclude = ['attacker_steamid']
cluster_cols = [c for c in numeric_cols if c not in exclude]

player_cluster_norm = player_cluster.copy()
normalizer = MinMaxScaler()
player_cluster_norm[cluster_cols] = normalizer.fit_transform(player_cluster[cluster_cols])

print(f"Created player clustering dataset: {len(player_cluster)} players, {len(cluster_cols)} features")

# Save
player_cluster.to_csv(OUTPUT_DIR / "clustering_players.csv", index=False)
player_cluster_norm.to_csv(OUTPUT_DIR / "clustering_players_normalized.csv", index=False)
print(f"✓ Saved clustering_players.csv")
print(f"✓ Saved clustering_players_normalized.csv")

# Round clustering (round patterns)
round_cluster = round_features[[
    'match_id', 'round_num',
    'total_kills', 'headshot_rate', 'kill_tempo',
    'avg_kill_distance', 'total_damage',
    'smoke_kills', 'wallbang_kills',
    't_win'
]].copy()

round_cluster = round_cluster[round_cluster['total_kills'] > 0].reset_index(drop=True)

cluster_round_cols = ['total_kills', 'headshot_rate', 'kill_tempo', 'avg_kill_distance', 'total_damage']
round_cluster_norm = round_cluster.copy()
round_cluster_norm[cluster_round_cols] = normalizer.fit_transform(round_cluster[cluster_round_cols])

print(f"Created round clustering dataset: {len(round_cluster)} rounds")

# Save
round_cluster.to_csv(OUTPUT_DIR / "clustering_rounds.csv", index=False)
round_cluster_norm.to_csv(OUTPUT_DIR / "clustering_rounds_normalized.csv", index=False)
print(f"✓ Saved clustering_rounds.csv")
print(f"✓ Saved clustering_rounds_normalized.csv")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FEATURE ENGINEERING COMPLETE")
print("="*80)

print(f"\nGenerated files in {OUTPUT_DIR}:")
print("\n[Player-Level]")
print(f"  - player_features.csv: {len(player_features)} players × {len(player_features.columns)} features")

print("\n[Round-Level]")
print(f"  - round_features.csv: {len(round_features)} rounds × {len(round_features.columns)} features")

print("\n[Match-Level]")
print(f"  - match_features.csv: {len(match_features)} matches × {len(match_features.columns)} features")

print("\n[Classification (Round Winner)]")
print(f"  - classification_features.csv: {len(clf_features)} samples")
print(f"  - classification_features_scaled.csv: {len(clf_scaled)} samples (normalized)")
print(f"  Target: t_win (binary)")
print(f"  Class balance: T={clf_features['t_win'].sum()}, CT={clf_features['ct_win'].sum()}")

print("\n[Regression (Kills/Damage)]")
print(f"  - regression_features.csv: {len(reg_features)} samples")
print(f"  Targets: total_kills, total_damage, headshot_rate")

print("\n[Clustering]")
print(f"  - clustering_players.csv: {len(player_cluster)} players")
print(f"  - clustering_players_normalized.csv (MinMax scaled)")
print(f"  - clustering_rounds.csv: {len(round_cluster)} rounds")
print(f"  - clustering_rounds_normalized.csv (MinMax scaled)")

print("\n" + "="*80)
print("READY FOR ML TRAINING")
print("="*80)
