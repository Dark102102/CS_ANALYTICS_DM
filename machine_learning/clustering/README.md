# CS2 Player Role Clustering - Final Version

## 🎯 Quick Start

```bash
cd /Users/lukerobinson/Dropbox/school/csci_5502/CS_ANALYTICS_DM/machine_learning/clustering
python3 comprehensive_player_clustering.py
```

## 📁 Directory Structure

```
clustering/
├── comprehensive_player_clustering.py    ⭐ PRIMARY SCRIPT (use this)
│
├── final_results/                        ✅ CURRENT RESULTS (best balance)
│   ├── player_roles_balanced.png         - PCA visualization (23% vs 77%)
│   ├── role_distribution_balanced.png    - Role distribution chart
│   ├── role_heatmap_balanced.png        - Feature comparison
│   └── player_roles_final.csv           - Role assignments
│
├── enhanced_clustering_features/         ✅ EXTRACTED FEATURES
│   └── player_features.csv              - All player features
│
├── archive_old_results/                  ⚠️  OLD RESULTS (imbalanced)
│   ├── clustering_results/              - Performance clustering (3% vs 97%)
│   └── player_role_clustering/          - Old player roles (13% vs 87%)
│
└── README.md                             📖 THIS FILE
```

## 📊 Results Summary

### Improved Clustering (Current)
- **Entry Fragger**: 21 players (23.3%) ✓ Better balance
- **Balanced Player**: 69 players (76.7%) ✓ More reasonable
- **Silhouette Score**: 0.309 (moderate)
- **Balance Score**: 0.304 (much better than 0.15 in old version)

### Why This is Better Than Previous
1. **Less Class Imbalance**: 23% vs 77% (was 13% vs 87%)
2. **Combined Scoring**: Considers both silhouette AND cluster balance
3. **Consolidated Code**: Single script instead of 3 separate files
4. **Cleaner Features**: Streamlined to essential metrics

## 🔬 How It Works

### 1. Feature Extraction
Extracts 11 key features per player:
- K/D ratio, kills per round, headshot %
- Opening kill rate, multi-kill rate
- Avg kill distance, AWP kills
- Assist rate, total kills/rounds

### 2. Player Aggregation
Aggregates statistics across all matches per player

### 3. Balanced Clustering
Uses modified K-Means that considers:
```python
combined_score = silhouette * (0.5 + 0.5 * balance)
```
Where balance = min_cluster_size / max_cluster_size

### 4. Visualization
Generates 3 plots showing cluster distribution and characteristics

## 📈 Comparison with Previous Results

| Metric | Old Method | New Method | Improvement |
|--------|-----------|-----------|-------------|
| Entry Fragger % | 13.3% | 23.3% | +10% (less extreme) |
| Support % | 86.7% | 76.7% | -10% (more balanced) |
| Balance Ratio | 0.15 | 0.30 | +100% better |
| K-Means Score | 0.35 | 0.31 | Slightly lower (expected) |

**Note**: Slight decrease in silhouette is EXPECTED and ACCEPTABLE because we're prioritizing balanced clusters over maximum separation.

## ⚠️ Current Limitation: Data Scarcity

**Problem**: Only 1.2 matches per player on average

**Impact**:
- Can only identify 2 broad roles (need 4-6 specific roles)
- Limited statistical significance
- Roles are "Entry Fragger" and "Balanced Player" (too general)

**Solution**: Download 40+ more professional demos

**Expected with More Data**:
- 4-6 distinct roles: Entry, Support, AWPer, IGL, Lurker, Rifler
- Better separation (silhouette > 0.4)
- More nuanced role characteristics

## 🚀 Next Steps

### Immediate
1. ✅ Use `comprehensive_player_clustering.py` for all future clustering
2. ✅ Reference `final_results/` for current best results
3. ⏳ Download more demos (see parent directory's `manual_demo_helper.py`)

### After Getting More Data
```bash
# Re-run clustering with expanded dataset
python3 comprehensive_player_clustering.py

# Expected improvements:
# - 4-6 clusters instead of 2
# - Clearer role boundaries
# - Better silhouette scores (0.4-0.6)
```

## 📚 Technical Details

### Algorithm: Balanced K-Means
- Standard K-Means with modified k-selection
- Considers both cluster quality (silhouette) and balance
- Prevents degenerate solutions (1 vs 99 player splits)

### Feature Scaling
- StandardScaler (zero mean, unit variance)
- PCA for 2D visualization (explains 56.7% variance)

### Role Classification
Uses z-score based decision tree:
1. High opening kill rate → Entry Fragger
2. High AWP kills → AWPer
3. High assist rate → Support
4. High multi-kills → Star Player
5. Balanced stats → Balanced Player/Rifler

## 🎓 For Your Report

**Key Points to Mention**:
1. Addressed severe class imbalance from initial clustering
2. Implemented combined scoring (quality + balance)
3. Consolidated 3 separate scripts into 1 comprehensive pipeline
4. Achieved 2x better cluster balance (0.30 vs 0.15)
5. Identified that more data needed for granular role detection

**Limitations to Discuss**:
1. Only 11 professional matches parsed (need 50+)
2. 1.2 matches per player (need 5+)
3. Currently identifies 2 broad roles (need 4-6 specific)
4. Moderate silhouette score due to data scarcity

**Strengths to Highlight**:
1. Production-ready pipeline
2. Addresses class imbalance
3. Comprehensive feature engineering
4. Professional visualizations
5. Clear path forward (get more data)

---

**Last Updated**: November 22, 2025  
**Status**: Ready for use, awaiting more demo data  
**Contact**: See parent directory for demo acquisition tools

