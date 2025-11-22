#!/usr/bin/env python3
"""
ESL Pro League CS2 Data Exploration and Preprocessing
Focus: Understanding factors that contribute to round wins
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "hltv_data"
OUTPUT_DIR = BASE_DIR / "analysis_output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("ESL PRO LEAGUE CS2 DATA EXPLORATION")
print("Focus: Factors Contributing to Round Wins")
print("="*80)

# ============================================================================
# 1. DATA LOADING
# ============================================================================
print("\n[1] LOADING DATA...")

# Load all deaths data
death_files = list(DATA_DIR.glob("*_deaths.csv"))
rounds_files = list(DATA_DIR.glob("*_rounds.csv"))

print(f"Found {len(death_files)} death event files")
print(f"Found {len(rounds_files)} round files")

# Combine all deaths data
all_deaths = []
for f in death_files:
    try:
        df = pd.read_csv(f)
        # Extract match info from filename
        match_name = f.stem.replace("_deaths", "")
        df['match'] = match_name
        all_deaths.append(df)
        print(f"  ✓ Loaded {f.name}: {len(df)} death events")
    except Exception as e:
        print(f"  ✗ Error loading {f.name}: {e}")

deaths_df = pd.concat(all_deaths, ignore_index=True)
print(f"\nTotal death events: {len(deaths_df)}")

# Combine all rounds data
all_rounds = []
for f in rounds_files:
    try:
        df = pd.read_csv(f)
        match_name = f.stem.replace("_rounds", "")
        df['match'] = match_name
        all_rounds.append(df)
        print(f"  ✓ Loaded {f.name}: {len(df)} rounds")
    except Exception as e:
        print(f"  ✗ Error loading {f.name}: {e}")

rounds_df = pd.concat(all_rounds, ignore_index=True)
print(f"\nTotal rounds: {len(rounds_df)}")

# Save raw data snapshot
print("\n[BEFORE CLEANING] Saving snapshot of raw data...")
deaths_df.head(20).to_csv(OUTPUT_DIR / "before_cleaning_deaths.csv", index=False)
rounds_df.head(20).to_csv(OUTPUT_DIR / "before_cleaning_rounds.csv", index=False)

# ============================================================================
# 2. DATA QUALITY ASSESSMENT
# ============================================================================
print("\n[2] DATA QUALITY ASSESSMENT...")

def assess_data_quality(df, name):
    print(f"\n{name}:")
    print(f"  Shape: {df.shape}")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\n  Missing values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({'Count': missing, 'Percentage': missing_pct})
    print(missing_df[missing_df['Count'] > 0].to_string())
    
    print(f"\n  Data types:")
    print(df.dtypes.value_counts().to_string())
    
    print(f"\n  Duplicates: {df.duplicated().sum()}")
    
    return missing_df

deaths_quality = assess_data_quality(deaths_df, "DEATHS DATASET")
rounds_quality = assess_data_quality(rounds_df, "ROUNDS DATASET")

# ============================================================================
# 3. DATA CLEANING
# ============================================================================
print("\n[3] DATA CLEANING...")

# DEATHS DATA CLEANING
print("\nCleaning deaths data...")

# Remove rows where critical info is missing
deaths_clean = deaths_df.copy()
initial_count = len(deaths_clean)

# Handle missing values
print(f"  Initial records: {initial_count}")

# Remove rows with missing attacker or victim
deaths_clean = deaths_clean.dropna(subset=['attacker_name', 'user_name'])
print(f"  After removing missing attacker/victim: {len(deaths_clean)} (removed {initial_count - len(deaths_clean)})")

# Fill missing numeric values with 0
numeric_cols = ['dmg_armor', 'dmg_health', 'distance']
for col in numeric_cols:
    if col in deaths_clean.columns:
        deaths_clean[col] = deaths_clean[col].fillna(0)

# Fill missing boolean values with False
bool_cols = ['headshot', 'attackerblind', 'attackerinair', 'noscope', 'thrusmoke']
for col in bool_cols:
    if col in deaths_clean.columns:
        deaths_clean[col] = deaths_clean[col].fillna(False)

# Handle weapon missing values
deaths_clean['weapon'] = deaths_clean['weapon'].fillna('unknown')

# Remove duplicates
deaths_clean = deaths_clean.drop_duplicates()
print(f"  After removing duplicates: {len(deaths_clean)}")

# ROUNDS DATA CLEANING
print("\nCleaning rounds data...")

rounds_clean = rounds_df.copy()
initial_rounds = len(rounds_clean)

# Remove rows with missing winner
rounds_clean = rounds_clean.dropna(subset=['winner'])
print(f"  Initial records: {initial_rounds}")
print(f"  After removing missing winner: {len(rounds_clean)} (removed {initial_rounds - len(rounds_clean)})")

# Fill missing reason with 'unknown'
rounds_clean['reason'] = rounds_clean['reason'].fillna('unknown')

# Remove duplicates
rounds_clean = rounds_clean.drop_duplicates()
print(f"  After removing duplicates: {len(rounds_clean)}")

# ============================================================================
# 4. FEATURE ENGINEERING FOR ROUND WINS
# ============================================================================
print("\n[4] FEATURE ENGINEERING FOR ROUND WINS...")

# Create round-level aggregations from death events
print("\nAggregating death events by round and match...")

# We need to map deaths to rounds using tick information
# Group deaths by match and create features per round

round_features = []

for match in rounds_clean['match'].unique():
    match_rounds = rounds_clean[rounds_clean['match'] == match].copy()
    match_deaths = deaths_clean[deaths_clean['match'] == match].copy()
    
    if len(match_deaths) == 0:
        continue
    
    # Sort rounds by tick
    match_rounds = match_rounds.sort_values('tick')
    match_rounds['round_num'] = range(1, len(match_rounds) + 1)
    
    # For each round, aggregate death events that occurred before that round's end tick
    for idx, round_row in match_rounds.iterrows():
        round_tick = round_row['tick']
        round_num = round_row['round_num']
        
        # Get deaths in this round (between previous round and current round tick)
        if round_num == 1:
            prev_tick = 0
        else:
            prev_round = match_rounds[match_rounds['round_num'] == round_num - 1]
            prev_tick = prev_round['tick'].values[0] if len(prev_round) > 0 else 0
        
        round_deaths = match_deaths[(match_deaths['tick'] > prev_tick) & 
                                    (match_deaths['tick'] <= round_tick)]
        
        # Calculate features
        features = {
            'match': match,
            'round': round_num,
            'winner': round_row['winner'],
            'reason': round_row['reason'],
            'tick': round_tick,
            
            # Kill statistics
            'total_kills': len(round_deaths),
            'headshot_kills': round_deaths['headshot'].sum(),
            'headshot_rate': round_deaths['headshot'].mean() if len(round_deaths) > 0 else 0,
            
            # Weapon usage
            'rifle_kills': round_deaths['weapon'].str.contains('ak47|m4a1|m4a4|famas|galil', case=False, na=False).sum(),
            'awp_kills': round_deaths['weapon'].str.contains('awp', case=False, na=False).sum(),
            'pistol_kills': round_deaths['weapon'].str.contains('glock|usp|p2000|p250|deagle|fiveseven', case=False, na=False).sum(),
            'smg_kills': round_deaths['weapon'].str.contains('mp|mac|ump', case=False, na=False).sum(),
            
            # Situational kills
            'smoke_kills': round_deaths['thrusmoke'].sum(),
            'noscope_kills': round_deaths['noscope'].sum(),
            'wallbang_kills': (round_deaths['penetrated'] > 0).sum() if 'penetrated' in round_deaths.columns else 0,
            'assisted_kills': round_deaths['assistedflash'].sum() if 'assistedflash' in round_deaths.columns else 0,
            
            # Distance statistics
            'avg_kill_distance': round_deaths['distance'].mean() if len(round_deaths) > 0 else 0,
            'max_kill_distance': round_deaths['distance'].max() if len(round_deaths) > 0 else 0,
            'min_kill_distance': round_deaths['distance'].min() if len(round_deaths) > 0 else 0,
            
            # Damage statistics
            'total_damage': round_deaths['dmg_health'].sum(),
            'avg_damage_per_kill': round_deaths['dmg_health'].mean() if len(round_deaths) > 0 else 0,
        }
        
        round_features.append(features)

rounds_with_features = pd.DataFrame(round_features)
print(f"Created features for {len(rounds_with_features)} rounds")

# Add binary target variable
rounds_with_features['t_win'] = (rounds_with_features['winner'] == 'T').astype(int)
rounds_with_features['ct_win'] = (rounds_with_features['winner'] == 'CT').astype(int)

# NOTE: Do NOT add outcome variables (bomb_exploded, bomb_defused, ct_eliminated, t_eliminated)
# These are deterministic with the winner and cannot be used as predictive features

print(f"\nRound win distribution:")
print(rounds_with_features['winner'].value_counts())

# Save processed data
print("\n[AFTER CLEANING] Saving processed data...")
deaths_clean.to_csv(OUTPUT_DIR / "after_cleaning_deaths.csv", index=False)
rounds_clean.to_csv(OUTPUT_DIR / "after_cleaning_rounds.csv", index=False)
rounds_with_features.to_csv(OUTPUT_DIR / "rounds_with_features.csv", index=False)

print(f"\n✓ Saved processed datasets to {OUTPUT_DIR}")

# ============================================================================
# 5. STATISTICAL ANALYSIS
# ============================================================================
print("\n[5] STATISTICAL ANALYSIS...")

# Select numeric columns for analysis (ONLY predictive features, not outcomes)
numeric_features = rounds_with_features.select_dtypes(include=[np.number]).columns.tolist()
# Remove target variables, IDs, and any outcome variables
exclude_cols = ['t_win', 'ct_win', 'tick', 'round', 
                'bomb_exploded', 'bomb_defused', 'ct_eliminated', 't_eliminated']
numeric_features = [col for col in numeric_features if col not in exclude_cols]

print(f"\nPredictive features being analyzed:")
for feat in numeric_features:
    print(f"  - {feat}")

print(f"\nAnalyzing {len(numeric_features)} numeric features")

# Summary statistics
summary_stats = rounds_with_features[numeric_features].describe()
summary_stats.loc['skewness'] = rounds_with_features[numeric_features].skew()
summary_stats.loc['kurtosis'] = rounds_with_features[numeric_features].kurtosis()

print("\nSummary Statistics:")
print(summary_stats.to_string())

# Save summary stats
summary_stats.to_csv(OUTPUT_DIR / "summary_statistics.csv")

# Correlation analysis
print("\nComputing correlations with round outcome...")
correlations = rounds_with_features[numeric_features + ['t_win']].corr()['t_win'].sort_values(ascending=False)
print("\nTop 10 features correlated with T-side wins:")
print(correlations.head(10).to_string())

# Save correlations
correlations.to_csv(OUTPUT_DIR / "feature_correlations.csv")

# Test for normality on key features
print("\nNormality tests (Shapiro-Wilk) for key features:")
key_features = ['total_kills', 'headshot_rate', 'avg_kill_distance', 'rifle_kills']
normality_results = []

for feature in key_features:
    if feature in rounds_with_features.columns:
        stat, p_value = stats.shapiro(rounds_with_features[feature].dropna())
        is_normal = p_value > 0.05
        normality_results.append({
            'feature': feature,
            'statistic': stat,
            'p_value': p_value,
            'is_normal': is_normal
        })
        print(f"  {feature}: p={p_value:.4f} ({'Normal' if is_normal else 'Not Normal'})")

normality_df = pd.DataFrame(normality_results)
normality_df.to_csv(OUTPUT_DIR / "normality_tests.csv", index=False)

# ============================================================================
# 6. DATA TRANSFORMATIONS
# ============================================================================
print("\n[6] DATA TRANSFORMATIONS...")

# Create a copy for transformations
rounds_transformed = rounds_with_features.copy()

# Log transformation for skewed features
skewed_features = rounds_with_features[numeric_features].skew()
highly_skewed = skewed_features[abs(skewed_features) > 1].index.tolist()

print(f"\nApplying log transformation to {len(highly_skewed)} highly skewed features:")
for col in highly_skewed:
    if (rounds_transformed[col] >= 0).all():
        rounds_transformed[f'{col}_log'] = np.log1p(rounds_transformed[col])
        print(f"  ✓ {col}")

# Standardization
print("\nApplying standardization...")
scaler = StandardScaler()
scaled_features = scaler.fit_transform(rounds_transformed[numeric_features])
scaled_df = pd.DataFrame(scaled_features, columns=[f'{col}_scaled' for col in numeric_features])

# Normalization (Min-Max)
print("Applying normalization...")
normalizer = MinMaxScaler()
normalized_features = normalizer.fit_transform(rounds_transformed[numeric_features])
normalized_df = pd.DataFrame(normalized_features, columns=[f'{col}_norm' for col in numeric_features])

# Combine transformed features
rounds_final = pd.concat([rounds_transformed, scaled_df, normalized_df], axis=1)

# Save transformed data
rounds_final.to_csv(OUTPUT_DIR / "rounds_transformed.csv", index=False)
print(f"✓ Saved transformed data with {rounds_final.shape[1]} features")

# ============================================================================
# 7. DIMENSIONALITY REDUCTION (PCA)
# ============================================================================
print("\n[7] DIMENSIONALITY REDUCTION (PCA)...")

# Prepare data for PCA
pca_features = rounds_transformed[numeric_features].fillna(0)
pca = PCA()
pca_result = pca.fit_transform(StandardScaler().fit_transform(pca_features))

# Explained variance
explained_var = pca.explained_variance_ratio_
cumsum_var = np.cumsum(explained_var)

print(f"\nPCA Results:")
print(f"  Components needed for 90% variance: {np.argmax(cumsum_var >= 0.90) + 1}")
print(f"  Components needed for 95% variance: {np.argmax(cumsum_var >= 0.95) + 1}")

# Save PCA results
pca_df = pd.DataFrame({
    'component': range(1, len(explained_var) + 1),
    'explained_variance': explained_var,
    'cumulative_variance': cumsum_var
})
pca_df.to_csv(OUTPUT_DIR / "pca_results.csv", index=False)

# Apply PCA with 90% variance
n_components_90 = np.argmax(cumsum_var >= 0.90) + 1
pca_90 = PCA(n_components=n_components_90)
pca_features_90 = pca_90.fit_transform(StandardScaler().fit_transform(pca_features))

pca_90_df = pd.DataFrame(pca_features_90, columns=[f'PC{i+1}' for i in range(n_components_90)])
pca_90_df['winner'] = rounds_transformed['winner'].values
pca_90_df['t_win'] = rounds_transformed['t_win'].values
pca_90_df.to_csv(OUTPUT_DIR / "rounds_pca.csv", index=False)

print(f"✓ Applied PCA with {n_components_90} components")

print("\n" + "="*80)
print("DATA EXPLORATION COMPLETE")
print("="*80)
print(f"\nAll results saved to: {OUTPUT_DIR}")
print(f"\nGenerated files:")
print(f"  - before_cleaning_*.csv (raw data samples)")
print(f"  - after_cleaning_*.csv (cleaned data)")
print(f"  - rounds_with_features.csv (engineered features)")
print(f"  - rounds_transformed.csv (with transformations)")
print(f"  - rounds_pca.csv (dimensionality reduced)")
print(f"  - summary_statistics.csv")
print(f"  - feature_correlations.csv")
print(f"  - normality_tests.csv")
print(f"  - pca_results.csv")

print("\nNext: Run visualization script to generate plots")

