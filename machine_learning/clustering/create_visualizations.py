#!/usr/bin/env python3
"""
ESL Pro League CS2 Data Visualizations
Creating 10+ unique visualizations focused on round wins
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 100

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "analysis_output"
PLOTS_DIR = OUTPUT_DIR / "plots"
PLOTS_DIR.mkdir(exist_ok=True, parents=True)

print("="*80)
print("CREATING VISUALIZATIONS FOR ESL PRO LEAGUE CS2 DATA")
print("="*80)

# Load data
print("\nLoading processed data...")
rounds_df = pd.read_csv(OUTPUT_DIR / "rounds_with_features.csv")
rounds_trans = pd.read_csv(OUTPUT_DIR / "rounds_transformed.csv")
pca_df = pd.read_csv(OUTPUT_DIR / "rounds_pca.csv")

print(f"Loaded {len(rounds_df)} rounds")

# ============================================================================
# VISUALIZATION 1: Round Win Distribution by Side
# ============================================================================
print("\n[1] Creating round win distribution plot...")
plt.figure(figsize=(10, 6))
win_counts = rounds_df['winner'].value_counts()
colors = ['#E74C3C', '#3498DB']  # Red for T, Blue for CT
plt.bar(win_counts.index, win_counts.values, color=colors, alpha=0.8, edgecolor='black')
plt.title('Round Wins by Side (T-Side vs CT-Side)', fontsize=16, fontweight='bold')
plt.xlabel('Winning Side', fontsize=12)
plt.ylabel('Number of Rounds Won', fontsize=12)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(win_counts.values):
    plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
t_pct = (win_counts['T'] / win_counts.sum()) * 100
ct_pct = (win_counts['CT'] / win_counts.sum()) * 100
plt.text(0, win_counts['T']/2, f'{t_pct:.1f}%', ha='center', fontsize=14, color='white', fontweight='bold')
plt.text(1, win_counts['CT']/2, f'{ct_pct:.1f}%', ha='center', fontsize=14, color='white', fontweight='bold')
plt.tight_layout()
plt.savefig(PLOTS_DIR / "01_round_wins_distribution.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 01_round_wins_distribution.png")

# ============================================================================
# VISUALIZATION 2: Round End Reasons Distribution
# ============================================================================
print("\n[2] Creating round end reasons plot...")
plt.figure(figsize=(12, 6))
reason_counts = rounds_df['reason'].value_counts()
colors_palette = sns.color_palette("Set2", len(reason_counts))
plt.barh(reason_counts.index, reason_counts.values, color=colors_palette, alpha=0.8, edgecolor='black')
plt.title('Distribution of Round End Reasons', fontsize=16, fontweight='bold')
plt.xlabel('Number of Rounds', fontsize=12)
plt.ylabel('Round End Reason', fontsize=12)
plt.grid(axis='x', alpha=0.3)
for i, v in enumerate(reason_counts.values):
    plt.text(v + 0.5, i, str(v), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(PLOTS_DIR / "02_round_end_reasons.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 02_round_end_reasons.png")

# ============================================================================
# VISUALIZATION 3: Headshot Rate Impact on Win Rate
# ============================================================================
print("\n[3] Creating headshot rate vs win rate plot...")
plt.figure(figsize=(12, 6))

# Create bins for headshot rate
rounds_df['hs_rate_bin'] = pd.cut(rounds_df['headshot_rate'], bins=5)
hs_win_rate = rounds_df.groupby('hs_rate_bin')['t_win'].agg(['mean', 'count'])
hs_win_rate = hs_win_rate[hs_win_rate['count'] > 5]  # Only bins with sufficient data

# Plot
x_labels = [f'{interval.left:.2f}-{interval.right:.2f}' for interval in hs_win_rate.index]
plt.bar(range(len(hs_win_rate)), hs_win_rate['mean'], color='#9B59B6', alpha=0.8, edgecolor='black')
plt.title('T-Side Win Rate by Headshot Rate', fontsize=16, fontweight='bold')
plt.xlabel('Headshot Rate Range', fontsize=12)
plt.ylabel('T-Side Win Rate', fontsize=12)
plt.xticks(range(len(hs_win_rate)), x_labels, rotation=45)
plt.axhline(y=0.5, color='red', linestyle='--', label='50% Win Rate', linewidth=2)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "03_headshot_rate_vs_wins.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 03_headshot_rate_vs_wins.png")

# ============================================================================
# VISUALIZATION 4: Weapon Type Distribution in Winning Rounds
# ============================================================================
print("\n[4] Creating weapon usage comparison...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

weapon_types = ['rifle_kills', 'awp_kills', 'pistol_kills', 'smg_kills']
t_wins = rounds_df[rounds_df['winner'] == 'T'][weapon_types].sum()
ct_wins = rounds_df[rounds_df['winner'] == 'CT'][weapon_types].sum()

# T-side wins
axes[0].pie(t_wins.values, labels=['Rifle', 'AWP', 'Pistol', 'SMG'], autopct='%1.1f%%',
            colors=sns.color_palette("Reds", 4), startangle=90)
axes[0].set_title('T-Side Winning Rounds: Weapon Distribution', fontweight='bold', fontsize=14)

# CT-side wins
axes[1].pie(ct_wins.values, labels=['Rifle', 'AWP', 'Pistol', 'SMG'], autopct='%1.1f%%',
            colors=sns.color_palette("Blues", 4), startangle=90)
axes[1].set_title('CT-Side Winning Rounds: Weapon Distribution', fontweight='bold', fontsize=14)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "04_weapon_usage_by_winner.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 04_weapon_usage_by_winner.png")

# ============================================================================
# VISUALIZATION 5: Kill Distance Distribution by Round Outcome
# ============================================================================
print("\n[5] Creating kill distance distribution...")
plt.figure(figsize=(12, 6))

# Filter out extreme outliers
valid_distances = rounds_df[rounds_df['avg_kill_distance'] < 50]

sns.violinplot(data=valid_distances, x='winner', y='avg_kill_distance', palette={'T': '#E74C3C', 'CT': '#3498DB'})
plt.title('Average Kill Distance by Winning Side', fontsize=16, fontweight='bold')
plt.xlabel('Winning Side', fontsize=12)
plt.ylabel('Average Kill Distance (units)', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "05_kill_distance_distribution.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 05_kill_distance_distribution.png")

# ============================================================================
# VISUALIZATION 6: Feature Correlation Heatmap (Top Features)
# ============================================================================
print("\n[6] Creating correlation heatmap...")
plt.figure(figsize=(14, 10))

# Select ONLY predictive features (no outcome variables)
feature_cols = ['total_kills', 'headshot_rate', 'rifle_kills', 'awp_kills', 'pistol_kills',
                'smg_kills', 'smoke_kills', 'wallbang_kills', 'assisted_kills',
                'avg_kill_distance', 'max_kill_distance', 'min_kill_distance',
                'total_damage', 'avg_damage_per_kill', 't_win']

correlation_matrix = rounds_df[feature_cols].corr()

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Feature Correlation Matrix (Focused on Round Wins)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(PLOTS_DIR / "06_correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 06_correlation_heatmap.png")

# ============================================================================
# VISUALIZATION 7: Total Kills vs Round Outcome
# ============================================================================
print("\n[7] Creating kills vs outcome scatter plot...")
plt.figure(figsize=(12, 6))

t_rounds = rounds_df[rounds_df['winner'] == 'T']
ct_rounds = rounds_df[rounds_df['winner'] == 'CT']

plt.scatter(t_rounds.index, t_rounds['total_kills'], alpha=0.6, s=50,
            label='T Wins', color='#E74C3C', edgecolors='black', linewidth=0.5)
plt.scatter(ct_rounds.index, ct_rounds['total_kills'], alpha=0.6, s=50,
            label='CT Wins', color='#3498DB', edgecolors='black', linewidth=0.5)

plt.title('Total Kills per Round by Winning Side', fontsize=16, fontweight='bold')
plt.xlabel('Round Index', fontsize=12)
plt.ylabel('Total Kills in Round', fontsize=12)
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "07_kills_by_outcome.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 07_kills_by_outcome.png")

# ============================================================================
# VISUALIZATION 8: QQ Plot for Normality Assessment
# ============================================================================
print("\n[8] Creating QQ plots for normality assessment...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('QQ Plots for Key Features (Normality Assessment)', fontsize=16, fontweight='bold')

features_to_test = ['total_kills', 'headshot_rate', 'avg_kill_distance', 'rifle_kills']

for idx, feature in enumerate(features_to_test):
    row = idx // 2
    col = idx % 2
    
    data = rounds_df[feature].dropna()
    stats.probplot(data, dist="norm", plot=axes[row, col])
    axes[row, col].set_title(f'{feature.replace("_", " ").title()}', fontweight='bold')
    axes[row, col].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "08_qq_plots_normality.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 08_qq_plots_normality.png")

# ============================================================================
# VISUALIZATION 9: PCA Variance Explained
# ============================================================================
print("\n[9] Creating PCA variance plot...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

pca_results = pd.read_csv(OUTPUT_DIR / "pca_results.csv")

# Scree plot
axes[0].plot(pca_results['component'], pca_results['explained_variance'],
             marker='o', linewidth=2, markersize=8, color='#E74C3C')
axes[0].set_title('PCA Scree Plot', fontweight='bold', fontsize=14)
axes[0].set_xlabel('Principal Component', fontsize=12)
axes[0].set_ylabel('Explained Variance Ratio', fontsize=12)
axes[0].grid(alpha=0.3)

# Cumulative variance
axes[1].plot(pca_results['component'], pca_results['cumulative_variance'],
             marker='s', linewidth=2, markersize=8, color='#3498DB')
axes[1].axhline(y=0.90, color='red', linestyle='--', label='90% Variance', linewidth=2)
axes[1].axhline(y=0.95, color='orange', linestyle='--', label='95% Variance', linewidth=2)
axes[1].set_title('Cumulative Explained Variance', fontweight='bold', fontsize=14)
axes[1].set_xlabel('Number of Components', fontsize=12)
axes[1].set_ylabel('Cumulative Variance Ratio', fontsize=12)
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "09_pca_variance.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 09_pca_variance.png")

# ============================================================================
# VISUALIZATION 10: PCA Biplot (First Two Components)
# ============================================================================
print("\n[10] Creating PCA biplot...")
plt.figure(figsize=(12, 8))

# Plot points colored by winner
t_pca = pca_df[pca_df['winner'] == 'T']
ct_pca = pca_df[pca_df['winner'] == 'CT']

plt.scatter(t_pca['PC1'], t_pca['PC2'], alpha=0.6, s=50,
            label='T Wins', color='#E74C3C', edgecolors='black', linewidth=0.5)
plt.scatter(ct_pca['PC1'], ct_pca['PC2'], alpha=0.6, s=50,
            label='CT Wins', color='#3498DB', edgecolors='black', linewidth=0.5)

plt.title('PCA Biplot: First Two Principal Components', fontsize=16, fontweight='bold')
plt.xlabel(f'PC1 ({pca_results.iloc[0]["explained_variance"]*100:.1f}% variance)', fontsize=12)
plt.ylabel(f'PC2 ({pca_results.iloc[1]["explained_variance"]*100:.1f}% variance)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', linewidth=0.5, alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "10_pca_biplot.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 10_pca_biplot.png")

# ============================================================================
# VISUALIZATION 11: Situational Kills Impact
# ============================================================================
print("\n[11] Creating situational kills analysis...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Impact of Situational Kills on Round Outcome', fontsize=16, fontweight='bold')

situational_kills = ['smoke_kills', 'noscope_kills', 'wallbang_kills', 'assisted_kills']

for idx, kill_type in enumerate(situational_kills):
    row = idx // 2
    col = idx % 2
    
    # Create bins
    rounds_df[f'{kill_type}_present'] = (rounds_df[kill_type] > 0).astype(int)
    win_rate = rounds_df.groupby(f'{kill_type}_present')['t_win'].agg(['mean', 'count'])
    
    if len(win_rate) > 1:
        labels = ['No ' + kill_type.replace('_', ' ').title(), 'With ' + kill_type.replace('_', ' ').title()]
        axes[row, col].bar(range(len(win_rate)), win_rate['mean'],
                          color=['#95A5A6', '#2ECC71'], alpha=0.8, edgecolor='black')
        axes[row, col].set_title(kill_type.replace('_', ' ').title(), fontweight='bold')
        axes[row, col].set_ylabel('T-Side Win Rate', fontsize=10)
        axes[row, col].set_xticks(range(len(win_rate)))
        axes[row, col].set_xticklabels(labels, rotation=15)
        axes[row, col].axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
        axes[row, col].grid(axis='y', alpha=0.3)
        
        # Add counts
        for i, count in enumerate(win_rate['count']):
            axes[row, col].text(i, win_rate['mean'].iloc[i] + 0.02,
                              f'n={count}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(PLOTS_DIR / "11_situational_kills_impact.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 11_situational_kills_impact.png")

# ============================================================================
# VISUALIZATION 12: Feature Importance for Round Wins (Top 15)
# ============================================================================
print("\n[12] Creating feature importance plot...")
plt.figure(figsize=(12, 8))

# Calculate absolute correlations with T wins (EXCLUDE outcome variables)
exclude_vars = ['t_win', 'ct_win', 'bomb_exploded', 'bomb_defused', 'ct_eliminated', 't_eliminated']
all_correlations = rounds_df.select_dtypes(include=[np.number]).corr()['t_win'].abs()
correlations = all_correlations[[col for col in all_correlations.index if col not in exclude_vars]]
correlations = correlations.sort_values(ascending=False).head(15)

colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(correlations)))
plt.barh(range(len(correlations)), correlations.values, color=colors, alpha=0.8, edgecolor='black')
plt.yticks(range(len(correlations)), [c.replace('_', ' ').title() for c in correlations.index])
plt.xlabel('Absolute Correlation with T-Side Win', fontsize=12)
plt.title('Top 15 Features by Correlation with Round Outcome', fontsize=16, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "12_feature_importance.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 12_feature_importance.png")

# ============================================================================
# VISUALIZATION 13: Round Win Trends Across Matches
# ============================================================================
print("\n[13] Creating round win trends across matches...")
plt.figure(figsize=(14, 6))

match_win_rates = rounds_df.groupby('match')['t_win'].mean().sort_values()
colors = plt.cm.coolwarm(match_win_rates.values)

plt.bar(range(len(match_win_rates)), match_win_rates.values, color=colors, alpha=0.8, edgecolor='black')
plt.axhline(y=0.5, color='black', linestyle='--', label='50% (Balanced)', linewidth=2)
plt.title('T-Side Win Rate by Match', fontsize=16, fontweight='bold')
plt.xlabel('Match', fontsize=12)
plt.ylabel('T-Side Win Rate', fontsize=12)
plt.xticks(range(len(match_win_rates)), [m[:20] + '...' if len(m) > 20 else m for m in match_win_rates.index],
           rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(PLOTS_DIR / "13_win_rate_by_match.png", dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved: 13_win_rate_by_match.png")

print("\n" + "="*80)
print("VISUALIZATIONS COMPLETE")
print("="*80)
print(f"\nAll 13 visualizations saved to: {PLOTS_DIR}")
print("\nVisualization descriptions:")
print("  1. Round Wins Distribution - Shows T vs CT side win balance")
print("  2. Round End Reasons - How rounds are being won")
print("  3. Headshot Rate Impact - Relationship between HS% and wins")
print("  4. Weapon Usage - Weapon type distribution in winning rounds")
print("  5. Kill Distance - Average engagement distances by winner")
print("  6. Correlation Heatmap - Feature relationships")
print("  7. Kills vs Outcome - Kill patterns by round winner")
print("  8. QQ Plots - Normality assessment for key features")
print("  9. PCA Variance - Dimensionality reduction analysis")
print(" 10. PCA Biplot - First two principal components visualization")
print(" 11. Situational Kills - Impact of special kill types")
print(" 12. Feature Importance - Top features correlated with wins")
print(" 13. Match Trends - Win rate variation across different matches")

