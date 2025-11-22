#!/usr/bin/env python3
"""
Comprehensive CS2 Player Role Clustering with Class Balance Handling

Consolidates feature extraction, clustering, and visualization into a single pipeline.
Addresses class imbalance issues and provides better role identification.

Author: Data Mining Expert
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend
import matplotlib
matplotlib.use('Agg')

# ML Libraries
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
BASE_DIR = Path(__file__).parent
HLTV_DATA_DIR = BASE_DIR.parent / "hltv_data"
FEATURES_DIR = BASE_DIR / "enhanced_clustering_features"
OUTPUT_DIR = BASE_DIR / "final_results"
OUTPUT_DIR.mkdir(exist_ok=True)
FEATURES_DIR.mkdir(exist_ok=True)

sns.set_style("whitegrid")

print("="*80)
print("COMPREHENSIVE CS2 PLAYER ROLE CLUSTERING")
print("="*80)


# ============================================================================
# PART 1: FEATURE EXTRACTION
# ============================================================================

class PlayerFeatureExtractor:
    """Extract comprehensive player features from parsed demo data"""
    
    def __init__(self, deaths_file, rounds_file):
        self.match_id = deaths_file.stem.replace('_deaths', '')
        self.deaths_df = pd.read_csv(deaths_file)
        self.rounds_df = pd.read_csv(rounds_file)
        self.map_name = self.deaths_df['map_name'].iloc[0] if not self.deaths_df.empty else 'unknown'
    
    def extract_player_features(self, player):
        """Extract features for a single player"""
        kills_df = self.deaths_df[self.deaths_df['attacker_name'] == player]
        deaths_df = self.deaths_df[self.deaths_df['victim_name'] == player]
        
        num_kills = len(kills_df)
        num_deaths = len(deaths_df)
        num_rounds = len(self.rounds_df)
        
        if num_kills == 0 and num_deaths == 0:
            return None
        
        features = {
            'player_name': player,
            'match_id': self.match_id,
            'map_name': self.map_name,
            'kills': num_kills,
            'deaths': num_deaths,
            'kd_ratio': num_kills / max(num_deaths, 1),
            'kills_per_round': num_kills / max(num_rounds, 1),
            'headshot_percentage': (kills_df['headshot'].sum() / max(num_kills, 1)) * 100 if not kills_df.empty else 0,
            'avg_kill_distance': kills_df['distance'].mean() if not kills_df.empty and 'distance' in kills_df.columns else 0,
        }
        
        # Tactical features
        if not kills_df.empty and 'round_num' in kills_df.columns:
            # Opening kills
            opening_kills = 0
            for round_num in kills_df['round_num'].unique():
                all_round_kills = self.deaths_df[self.deaths_df['round_num'] == round_num].sort_values('tick')
                if not all_round_kills.empty:
                    first_kill_tick = all_round_kills['tick'].iloc[0]
                    player_kills = kills_df[kills_df['round_num'] == round_num]
                    if not player_kills.empty and player_kills['tick'].min() == first_kill_tick:
                        opening_kills += 1
            
            features['opening_kills'] = opening_kills
            features['opening_kill_rate'] = opening_kills / max(num_rounds, 1)
            
            # Multi-kills
            kills_per_round = kills_df.groupby('round_num').size()
            features['rounds_with_2k'] = (kills_per_round >= 2).sum()
            features['rounds_with_3k'] = (kills_per_round >= 3).sum()
            features['multi_kill_rate'] = features['rounds_with_2k'] / max(num_rounds, 1)
        else:
            features['opening_kills'] = 0
            features['opening_kill_rate'] = 0
            features['rounds_with_2k'] = 0
            features['rounds_with_3k'] = 0
            features['multi_kill_rate'] = 0
        
        # Weapon preferences
        if not kills_df.empty and 'weapon' in kills_df.columns:
            weapons = kills_df['weapon'].fillna('unknown')
            features['awp_kills'] = weapons.str.contains('awp', case=False).sum()
            features['rifle_kills'] = weapons.str.contains('ak47|m4a1|m4a4|galilar|famas', case=False).sum()
        else:
            features['awp_kills'] = 0
            features['rifle_kills'] = 0
        
        # Assist features
        assists_df = self.deaths_df[self.deaths_df['assister_name'] == player]
        features['assists'] = len(assists_df)
        features['assist_per_round'] = len(assists_df) / max(num_rounds, 1)
        
        return features
    
    def extract_all_features(self):
        """Extract features for all players in the match"""
        all_players = set()
        all_players.update(self.deaths_df['attacker_name'].dropna().unique())
        all_players.update(self.deaths_df['victim_name'].dropna().unique())
        
        player_features = []
        for player in all_players:
            if pd.isna(player):
                continue
            features = self.extract_player_features(player)
            if features:
                player_features.append(features)
        
        return pd.DataFrame(player_features)


def extract_features_from_all_matches():
    """Extract features from all parsed matches"""
    print("\n[1/4] EXTRACTING PLAYER FEATURES")
    print("="*80)
    
    all_features = []
    deaths_files = sorted(HLTV_DATA_DIR.glob('*_deaths.csv'))
    
    print(f"Found {len(deaths_files)} matches to process\n")
    
    for deaths_file in deaths_files:
        match_id = deaths_file.stem.replace('_deaths', '')
        rounds_file = HLTV_DATA_DIR / f"{match_id}_rounds.csv"
        
        if not rounds_file.exists():
            continue
        
        try:
            extractor = PlayerFeatureExtractor(deaths_file, rounds_file)
            match_features = extractor.extract_all_features()
            
            if not match_features.empty:
                all_features.append(match_features)
                print(f"  ✓ {match_id}: {len(match_features)} players")
        except Exception as e:
            print(f"  ✗ {match_id}: {e}")
    
    if all_features:
        combined = pd.concat(all_features, ignore_index=True)
        output_file = FEATURES_DIR / "player_features.csv"
        combined.to_csv(output_file, index=False)
        print(f"\n✓ Extracted features for {len(combined)} performances")
        print(f"✓ Saved to: {output_file}")
        return combined
    else:
        print("\n✗ No features extracted!")
        return pd.DataFrame()


# ============================================================================
# PART 2: PLAYER AGGREGATION WITH SMARTER CLUSTERING
# ============================================================================

def aggregate_player_features(features_df):
    """Aggregate features per player across all matches"""
    print("\n[2/4] AGGREGATING PLAYER STATISTICS")
    print("="*80)
    
    grouped = features_df.groupby('player_name')
    
    agg_features = []
    for player in grouped.groups.keys():
        player_data = features_df[features_df['player_name'] == player]
        
        agg_feature = {
            'player_name': player,
            'num_matches': len(player_data),
            'kd_ratio': player_data['kd_ratio'].mean(),
            'kills_per_round': player_data['kills_per_round'].mean(),
            'headshot_percentage': player_data['headshot_percentage'].mean(),
            'opening_kill_rate': player_data['opening_kill_rate'].mean(),
            'multi_kill_rate': player_data['multi_kill_rate'].mean(),
            'avg_kill_distance': player_data['avg_kill_distance'].mean(),
            'awp_kills_avg': player_data['awp_kills'].mean(),
            'assist_rate': player_data['assist_per_round'].mean(),
            'total_kills': player_data['kills'].sum(),
            'total_rounds': player_data['kills_per_round'].sum() * len(player_data),
        }
        
        agg_features.append(agg_feature)
    
    agg_df = pd.DataFrame(agg_features)
    print(f"✓ Aggregated features for {len(agg_df)} unique players")
    print(f"  Average matches per player: {agg_df['num_matches'].mean():.1f}")
    
    return agg_df


# ============================================================================
# PART 3: IMPROVED CLUSTERING WITH BETTER K SELECTION
# ============================================================================

def perform_improved_clustering(agg_df):
    """Perform clustering with better k selection to avoid class imbalance"""
    print("\n[3/4] PERFORMING IMPROVED CLUSTERING")
    print("="*80)
    
    # Select clustering features
    feature_cols = ['kd_ratio', 'kills_per_round', 'headshot_percentage', 
                    'opening_kill_rate', 'multi_kill_rate', 'avg_kill_distance',
                    'awp_kills_avg', 'assist_rate']
    
    X = agg_df[feature_cols].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"\nPCA: First 2 components explain {pca.explained_variance_ratio_.sum()*100:.1f}% variance")
    
    # Find optimal k with focus on silhouette AND cluster balance
    print("\nFinding optimal k (prioritizing balanced clusters)...")
    
    best_k = 2
    best_score = -1
    best_balance = 0
    
    for k in range(2, min(8, len(agg_df) // 3)):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = kmeans.fit_predict(X_scaled)
        
        # Calculate metrics
        silhouette = silhouette_score(X_scaled, labels)
        
        # Calculate cluster balance (how evenly distributed are clusters)
        cluster_sizes = pd.Series(labels).value_counts().values
        balance = cluster_sizes.min() / cluster_sizes.max()  # 1.0 is perfect balance
        
        # Combined score: prioritize silhouette but penalize severe imbalance
        combined_score = silhouette * (0.5 + 0.5 * balance)
        
        print(f"  k={k}: silhouette={silhouette:.3f}, balance={balance:.3f}, score={combined_score:.3f}")
        
        # Prefer this k if it has better combined score
        if combined_score > best_score:
            best_score = combined_score
            best_k = k
            best_balance = balance
    
    print(f"\n✓ Selected k={best_k} (silhouette={best_score:.3f}, balance={best_balance:.3f})")
    
    # Final clustering with best k
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    labels = kmeans.fit_predict(X_scaled)
    
    agg_df['cluster'] = labels
    
    # Analyze clusters
    print("\n" + "="*80)
    print("CLUSTER ANALYSIS")
    print("="*80)
    
    role_names = identify_roles(agg_df, X_scaled, feature_cols, best_k)
    agg_df['role'] = agg_df['cluster'].map(role_names)
    
    # Print cluster statistics
    for cluster_id in range(best_k):
        cluster_data = agg_df[agg_df['cluster'] == cluster_id]
        role_name = role_names.get(cluster_id, f'Role {cluster_id}')
        
        print(f"\n{role_name.upper()} ({len(cluster_data)} players, {len(cluster_data)/len(agg_df)*100:.1f}%)")
        print(f"  Avg K/D: {cluster_data['kd_ratio'].mean():.2f}")
        print(f"  Avg KPR: {cluster_data['kills_per_round'].mean():.2f}")
        print(f"  Avg HS%: {cluster_data['headshot_percentage'].mean():.1f}%")
        print(f"  Opening Kill Rate: {cluster_data['opening_kill_rate'].mean():.3f}")
        print(f"  Multi-kill Rate: {cluster_data['multi_kill_rate'].mean():.3f}")
        print(f"  Top players: {', '.join(cluster_data.nlargest(3, 'kd_ratio')['player_name'].tolist())}")
    
    return agg_df, X_pca, labels, role_names, best_k


def identify_roles(agg_df, X_scaled, feature_names, n_clusters):
    """Intelligently identify role names based on cluster characteristics"""
    
    role_names = {}
    
    for cluster_id in range(n_clusters):
        cluster_data = agg_df[agg_df['cluster'] == cluster_id]
        
        # Calculate z-scores for key metrics
        overall_means = agg_df[feature_names].mean()
        overall_stds = agg_df[feature_names].std()
        cluster_means = cluster_data[feature_names].mean()
        
        z_scores = (cluster_means - overall_means) / (overall_stds + 1e-6)
        
        # Decision tree for role classification
        if z_scores['opening_kill_rate'] > 0.5:
            role_names[cluster_id] = "Entry Fragger"
        elif z_scores['awp_kills_avg'] > 0.8:
            role_names[cluster_id] = "AWPer/Sniper"
        elif z_scores['assist_rate'] > 0.5:
            role_names[cluster_id] = "Support"
        elif z_scores['multi_kill_rate'] > 0.5:
            role_names[cluster_id] = "Star Player"
        elif z_scores['kills_per_round'] > 0.3:
            role_names[cluster_id] = "Rifler"
        elif z_scores['kills_per_round'] < -0.3:
            role_names[cluster_id] = "IGL/Anchor"
        else:
            role_names[cluster_id] = "Balanced Player"
    
    return role_names


# ============================================================================
# PART 4: VISUALIZATION
# ============================================================================

def create_visualizations(agg_df, X_pca, role_names, n_clusters):
    """Create comprehensive visualizations"""
    print("\n[4/4] CREATING VISUALIZATIONS")
    print("="*80)
    
    # 1. PCA Scatter Plot with Better Colors
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.Set2(np.linspace(0, 1, n_clusters))
    
    for cluster_id in range(n_clusters):
        mask = agg_df['cluster'] == cluster_id
        role_name = role_names.get(cluster_id, f'Cluster {cluster_id}')
        cluster_size = mask.sum()
        
        ax.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            c=[colors[cluster_id]],
            label=f'{role_name} (n={cluster_size})',
            s=150,
            alpha=0.7,
            edgecolors='black',
            linewidths=1
        )
    
    ax.set_xlabel('First Principal Component', fontsize=14, fontweight='bold')
    ax.set_ylabel('Second Principal Component', fontsize=14, fontweight='bold')
    ax.set_title('CS2 Player Role Clustering (Balanced)', fontsize=16, fontweight='bold')
    ax.legend(loc='best', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'player_roles_balanced.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: player_roles_balanced.png")
    plt.close()
    
    # 2. Role Distribution Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    role_counts = agg_df['role'].value_counts()
    bars = ax.bar(role_counts.index, role_counts.values, color=colors[:len(role_counts)])
    
    # Add count labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('Player Role', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Players', fontsize=14, fontweight='bold')
    ax.set_title('Player Role Distribution', fontsize=16, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'role_distribution_balanced.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: role_distribution_balanced.png")
    plt.close()
    
    # 3. Feature Comparison Heatmap
    key_features = ['kd_ratio', 'kills_per_round', 'headshot_percentage',
                    'opening_kill_rate', 'multi_kill_rate', 'assist_rate']
    
    role_means = agg_df.groupby('role')[key_features].mean()
    role_means_norm = (role_means - role_means.min()) / (role_means.max() - role_means.min())
    
    role_means_norm.columns = [c.replace('_', ' ').title() for c in role_means_norm.columns]
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(role_means)*1.5)))
    sns.heatmap(role_means_norm.T, annot=True, fmt='.2f', cmap='RdYlGn',
                linewidths=0.5, cbar_kws={'label': 'Normalized Value'}, ax=ax,
                vmin=0, vmax=1)
    ax.set_title('Role Characteristics (Normalized)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Player Role', fontsize=14, fontweight='bold')
    ax.set_ylabel('Feature', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'role_heatmap_balanced.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: role_heatmap_balanced.png")
    plt.close()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution pipeline"""
    
    # Step 1: Extract features
    features_df = extract_features_from_all_matches()
    
    if features_df.empty:
        print("\n✗ No features extracted! Check that demo files are parsed.")
        return
    
    # Step 2: Aggregate by player
    agg_df = aggregate_player_features(features_df)
    
    # Step 3: Perform improved clustering
    agg_df, X_pca, labels, role_names, n_clusters = perform_improved_clustering(agg_df)
    
    # Step 4: Create visualizations
    create_visualizations(agg_df, X_pca, role_names, n_clusters)
    
    # Save results
    output_file = OUTPUT_DIR / "player_roles_final.csv"
    agg_df[['player_name', 'cluster', 'role', 'num_matches', 'kd_ratio', 
            'kills_per_round', 'opening_kill_rate', 'multi_kill_rate']].to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print("CLUSTERING COMPLETE")
    print("="*80)
    print(f"\n✓ Results saved to: {OUTPUT_DIR}")
    print(f"✓ Player roles: {output_file}")
    print(f"\nIdentified {n_clusters} player roles with better balance")
    print("\nGenerated files:")
    for file in sorted(OUTPUT_DIR.glob('*')):
        print(f"  - {file.name}")


if __name__ == "__main__":
    main()

