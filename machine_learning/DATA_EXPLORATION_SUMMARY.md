# ESL Pro League CS2 Data Exploration & Preprocessing
## Focus: Factors Contributing to Round Wins

---

## Executive Summary

This comprehensive data exploration analyzed **71 competitive CS2 rounds** from **10 ESL Pro League Season 22 matches**, examining **1,838 death events** to identify key factors that contribute to round wins. The analysis revealed that **T-side wins 63.4%** of rounds, with critical factors including CT eliminations, bomb explosions, and tactical positioning.

---

## 1. Data Collection

### Data Sources
- **Website**: HLTV.org (professional CS:GO/CS2 statistics)
- **Matches**: 10 ESL Pro League Season 22 matches
- **Time Period**: October 2025
- **Data Types**: Demo files (.dem format) and match metadata

### Collection Method
- **Automated scraping** using Python (requests, BeautifulSoup)
- **Demo file parsing** using demoparser2 library
- **Rate limiting** to respect server resources
- **Archive extraction** from RAR files

### Datasets Created
1. **Match Metadata CSV** (hltv_matches.csv): 102 rows with team names, scores, player rosters
2. **Death Events CSVs** (13 files): 1,838 death events with player names, weapons, positions
3. **Round Data CSVs** (29 files): 71 rounds with outcomes and timing

---

## 2. Data Quality Assessment

### Initial Assessment

**Deaths Dataset:**
- Shape: 1,848 rows × 27 columns
- Memory: 0.90 MB
- Missing Values:
  - `assister_name`: 65% (expected - not all kills have assists)
  - `weapon_itemid`: 3.4%
  - `weapon_originalowner_xuid`: 100% (not tracked by parser)
  - `attacker_name`: 0.5% (data quality issue)

**Rounds Dataset:**
- Shape: 99 rows × 12 columns
- Memory: 0.03 MB
- Missing Values:
  - Parse metadata: 73.7% (expected - only applies to failed parses)
  - `winner`: 28% (incomplete round data)
  - `reason`: 28% (incomplete round data)

### Data Quality Issues Identified

1. **Missing Critical Data**: 28% of rounds missing winner information
2. **Parsing Failures**: Some demo files failed to parse due to corruption
3. **Duplicate Extractions**: Multiple copies of extracted files
4. **Inconsistent Naming**: Varied column names across files

---

## 3. Data Cleaning & Preprocessing

### Handling Missing Values

**Deaths Data:**
- **Removal**: Dropped 10 rows (0.5%) with missing attacker/victim (critical fields)
- **Imputation**: Filled numeric columns (distance, damage) with 0
- **Imputation**: Filled boolean columns (headshot, thrusmoke) with False
- **Imputation**: Filled weapon column with 'unknown'

**Rounds Data:**
- **Removal**: Dropped 28 rows (28%) with missing winner (unusable for analysis)
- **Imputation**: Filled missing reason with 'unknown'
- **Result**: 71 complete rounds retained

### Handling Duplicates

- **Deaths**: 0 duplicates found
- **Rounds**: 0 duplicates found
- **Extracted Files**: Removed 50 duplicate directories (saved 12.2 GB)

### Handling Outliers

- **Distance outliers**: Filtered extreme values (>50 units) for visualizations
- **Damage outliers**: Kept all values (valid gameplay data)
- **Kill counts**: All values valid (2-9 kills per round)

### Data Transformations Applied

1. **Log Transformation** (for 10 highly skewed features):
   - awp_kills, pistol_kills, smg_kills
   - smoke_kills, wallbang_kills, assisted_kills
   - avg_kill_distance, min_kill_distance
   - bomb_defused, t_eliminated

2. **Standardization** (Z-score normalization):
   - Applied to all 20 numeric features
   - Mean = 0, Standard Deviation = 1
   - Purpose: Prepare for PCA and machine learning

3. **Min-Max Normalization**:
   - Scaled all features to [0, 1] range
   - Purpose: Alternative scaling for algorithms sensitive to magnitude

---

## 4. Feature Engineering

### Round-Level Aggregations

Created **24 features** from death events for each round:

#### Kill Statistics
- `total_kills`: Number of eliminations in round
- `headshot_kills`: Headshot eliminations
- `headshot_rate`: Percentage of kills that were headshots

#### Weapon Categories
- `rifle_kills`: AK47, M4A1, M4A4, FAMAS, Galil
- `awp_kills`: AWP sniper rifle
- `pistol_kills`: Glock, USP, P2000, P250, Deagle, Five-Seven
- `smg_kills`: MP5, MP7, MP9, MAC-10, UMP-45

#### Situational Kills
- `smoke_kills`: Kills through smoke
- `noscope_kills`: AWP kills without scoping
- `wallbang_kills`: Kills through walls
- `assisted_kills`: Flash-assisted eliminations

#### Distance Metrics
- `avg_kill_distance`: Average engagement distance
- `max_kill_distance`: Longest kill distance
- `min_kill_distance`: Shortest kill distance

#### Damage Statistics
- `total_damage`: Total damage dealt in round
- `avg_damage_per_kill`: Damage efficiency

#### Round Outcomes
- `bomb_exploded`: Bomb detonated (1/0)
- `bomb_defused`: Bomb defused (1/0)
- `ct_eliminated`: All CTs eliminated (1/0)
- `t_eliminated`: All Ts eliminated (1/0)
- `t_win`: T-side won round (1/0) - **TARGET VARIABLE**

---

## 5. Statistical Analysis

### Summary Statistics

| Metric | Mean | Median | Std Dev | Skewness | Kurtosis |
|--------|------|--------|---------|----------|----------|
| Total Kills | 6.38 | 7.0 | 1.71 | -0.71 | -0.02 |
| Headshot Rate | 50.8% | 50.0% | 26.7% | 0.17 | -0.59 |
| Rifle Kills | 4.18 | 4.0 | 2.29 | -0.29 | -0.75 |
| AWP Kills | 0.80 | 0.0 | 1.14 | 1.76 | 3.55 |
| Avg Kill Distance | 17.49 | 16.24 | 5.20 | 1.14 | 2.08 |

### Key Findings

1. **Rounds are relatively short**: Average of 6.4 kills per round
2. **Headshots are common**: 50.8% headshot rate
3. **Rifles dominate**: 65.5% of kills are with rifles
4. **AWP usage varies**: Highly skewed distribution (many rounds with 0 AWP kills)
5. **Most engagements are mid-range**: Average 17.5 units

### Correlation Analysis

**Top 5 Features Correlated with T-Side Wins:**

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| CT Eliminated | +0.543 | Strong positive - eliminating all CTs leads to T wins |
| Bomb Exploded | +0.493 | Strong positive - successful plants lead to T wins |
| Max Kill Distance | +0.087 | Weak positive - longer range fights favor T-side |
| Avg Kill Distance | +0.082 | Weak positive - T-side prefers distance |
| Wallbang Kills | +0.076 | Weak positive - aggressive play |

**Features Negatively Correlated with T-Side Wins:**

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| Bomb Defused | -0.441 | Strong negative - defuses mean CT wins |
| T Eliminated | -0.441 | Strong negative - T elimination means CT wins |
| Headshot Kills | -0.054 | Weak negative - CT-side slightly better at headshots |

### Normality Tests (Shapiro-Wilk)

| Feature | P-Value | Normal? | Action Taken |
|---------|---------|---------|--------------|
| Total Kills | 0.0003 | ❌ No | Log transformation |
| Headshot Rate | 0.0715 | ✅ Yes | No transformation needed |
| Avg Kill Distance | 0.0007 | ❌ No | Log transformation |
| Rifle Kills | 0.0043 | ❌ No | Log transformation |

---

## 6. Dimensionality Reduction (PCA)

### Results

- **Total Components**: 20 (number of numeric features)
- **Components for 90% Variance**: 10
- **Components for 95% Variance**: 12
- **Recommendation**: Use 10 components for modeling

### Variance Explained

| Components | Cumulative Variance |
|------------|---------------------|
| PC1-PC2 | 31.4% |
| PC1-PC5 | 64.2% |
| PC1-PC10 | 90.0% |
| PC1-PC12 | 95.0% |

### Interpretation

- **First two components** explain only 31% of variance - data is complex
- **High dimensionality needed** - 10 components required for 90% variance
- **Many factors contribute to wins** - no single dominant pattern

---

## 7. Key Insights & Patterns

### 1. T-Side Advantage (63.4% Win Rate)

**Possible Explanations:**
- Sample bias (selected matches may favor aggressive T-side play)
- Map pool favoring T-side (certain maps are T-sided)
- Meta shift in professional CS2
- High skill ceiling for executing T-side strategies

### 2. Round Win Factors

**Most Important Factors for T-Side Victory:**
1. **Eliminating all CTs** (54.3% correlation)
2. **Planting and detonating bomb** (49.3% correlation)
3. **Maintaining distance** (8.2% correlation)

**Most Important Factors for CT-Side Victory:**
1. **Eliminating all Ts** (44.1% correlation with CT win)
2. **Defusing bomb** (44.1% correlation with CT win)
3. **Close-range engagements** (weak correlation)

### 3. Weapon Meta

**T-Side Winning Rounds:**
- Rifles: 66.8%
- AWP: 12.8%
- Pistols: 12.1%
- SMGs: 5.4%

**CT-Side Winning Rounds:**
- Rifles: 63.1%
- AWP: 13.2%
- Pistols: 11.8%
- SMGs: 8.8%

**Insight**: Both sides rely heavily on rifles, with AWP providing strategic advantages

### 4. Tactical Patterns

**Smoke Kills:**
- Present in 70.4% of rounds
- Higher in T-side wins (suggests aggressive T-side utility usage)

**Wallbangs:**
- Rare (19.7% of rounds have wallbang kills)
- Slightly favors T-side (7.6% correlation)

**Flash Assists:**
- Present in 33.8% of rounds
- Weak correlation with outcome (3.4%)

### 5. Match-Specific Variance

- **High variance** in win rates across matches (20% to 80% T-win rate)
- **Map-dependent** outcomes
- **Team-specific** playstyles affect patterns

---

## 8. Data Quality After Cleaning

### Completeness
- ✅ **100%** of retained rounds have complete feature data
- ✅ **100%** of death events have attacker and victim information
- ✅ **96.5%** of death events have weapon information

### Consistency
- ✅ All numeric values within expected ranges
- ✅ All categorical values properly encoded
- ✅ All timestamps (ticks) properly ordered

### Usability
- ✅ Data ready for machine learning (standardized, normalized)
- ✅ Multiple formats available (raw, transformed, PCA)
- ✅ Clear documentation of all transformations

---

## 9. Ethical Considerations & Limitations

### Data Ethics

✅ **Public Data**: All data from public competitive matches
✅ **No Personal Information**: Player handles only (public personas)
✅ **Fair Use**: Educational and research purposes
✅ **Attribution**: Data sourced from HLTV.org

### Potential Biases

⚠️ **Sample Bias**: Only 10 matches from one tournament
⚠️ **Temporal Bias**: Data from single time period (October 2025)
⚠️ **Survival Bias**: Only matches with available demos included
⚠️ **Skill Bias**: Only top-tier professional teams represented

### Limitations

1. **Small Sample Size**: 71 rounds may not generalize to all CS2 gameplay
2. **Missing Context**: Economic state, utility usage not captured
3. **Parsing Failures**: 26 rounds couldn't be parsed (26% data loss)
4. **Map Imbalance**: Not all maps equally represented
5. **No Player Tracking**: Can't analyze individual player contributions across rounds

### Recommendations for Future Work

1. **Expand Dataset**: Include more matches, tournaments, time periods
2. **Add Economic Data**: Track money, equipment purchases
3. **Include Utility Data**: Grenades thrown, flashes, smokes
4. **Player Tracking**: Link kills to specific players across rounds
5. **Positional Data**: Extract player positions throughout round
6. **Team Compositions**: Analyze roster impact on outcomes

---

## 10. Visualizations Created (13 Unique Plots)

1. **Round Wins Distribution**: T vs CT win balance
2. **Round End Reasons**: How rounds are concluded
3. **Headshot Rate Impact**: Relationship between HS% and wins
4. **Weapon Usage Comparison**: Weapon distribution by winner
5. **Kill Distance Distribution**: Engagement distances by side
6. **Feature Correlation Heatmap**: Inter-feature relationships
7. **Kills vs Outcome Scatter**: Kill patterns by winner
8. **QQ Plots**: Normality assessment for key features
9. **PCA Variance Explained**: Scree plot and cumulative variance
10. **PCA Biplot**: First two principal components
11. **Situational Kills Impact**: Effect of special kill types
12. **Feature Importance**: Top features for predicting wins
13. **Match-Specific Trends**: Win rate variation across matches

---

## 11. Files Generated

### CSV Files (11)
- `before_cleaning_deaths.csv` - Raw death events sample
- `before_cleaning_rounds.csv` - Raw rounds sample
- `after_cleaning_deaths.csv` - Cleaned death events
- `after_cleaning_rounds.csv` - Cleaned rounds
- `rounds_with_features.csv` - Engineered features (ready for ML)
- `rounds_transformed.csv` - With log, standardized, normalized features
- `rounds_pca.csv` - Dimensionality reduced (10 components)
- `summary_statistics.csv` - Descriptive statistics
- `feature_correlations.csv` - Correlations with target
- `normality_tests.csv` - Shapiro-Wilk test results
- `pca_results.csv` - PCA variance explained

### Visualization Files (13 PNG)
- All plots saved at 300 DPI for publication quality
- Stored in `analysis_output/plots/` directory

### Code Files (3)
- `data_exploration.py` - Main preprocessing script
- `create_visualizations.py` - Visualization generation
- `scraping.py` - Data collection script
- `parse_demo_demoparser2.py` - Demo file parser

---

## 12. Next Steps: Decision Tree Modeling

The data is now prepared for decision tree analysis:

### Ready-to-Use Datasets

1. **For Basic Decision Tree**: `rounds_with_features.csv`
   - 71 samples × 24 features
   - Target: `t_win` (binary: 0/1)
   - All features meaningful and interpretable

2. **For Complex Models**: `rounds_transformed.csv`
   - Includes log-transformed features for skewed distributions
   - Standardized features for algorithms requiring normalization

3. **For High-Dimensional Models**: `rounds_pca.csv`
   - 10 principal components (90% variance)
   - Reduces overfitting risk with small sample size

### Recommended Approach

1. **Start with interpretable features** from `rounds_with_features.csv`
2. **Use cross-validation** (small sample size)
3. **Limit tree depth** to prevent overfitting (max_depth=4-6)
4. **Feature selection**: Focus on top 10 correlated features
5. **Ensemble methods**: Consider Random Forest for robustness

### Expected Performance

With 71 samples:
- **Training set**: 50 samples (70%)
- **Test set**: 21 samples (30%)
- **Cross-validation**: 5-fold recommended
- **Expected accuracy**: 70-80% (based on correlation analysis)

---

## Conclusion

This comprehensive data exploration has successfully:

✅ Collected and processed professional CS2 match data
✅ Cleaned and transformed data with rigorous quality checks
✅ Identified key factors contributing to round wins
✅ Created 13 meaningful visualizations
✅ Prepared multiple dataset versions for modeling
✅ Documented all transformations and decisions

**The data is now ready for decision tree modeling and further machine learning analysis.**

---

*Analysis completed: October 17, 2025*
*Analyst: CS Analytics Team*
*Course: CSCI 5502 - Data Mining*

