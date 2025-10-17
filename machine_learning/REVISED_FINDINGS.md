# REVISED ANALYSIS: Predictive Features for Round Wins

## Important Correction

**Previous analysis incorrectly included outcome variables** (ct_eliminated, bomb_exploded, bomb_defused, t_eliminated) which are **deterministic with the winner** and cannot be used as predictive features.

**This revision focuses only on gameplay metrics that occur DURING the round and can actually predict the outcome.**

---

## Key Finding: Weak Correlations Are Expected!

**All correlations are now < 20%**, which is actually **realistic** for CS2:
- Round outcomes depend on **hundreds of micro-decisions**
- Team coordination, economy, and map position aren't captured
- Individual player skill varies significantly
- Small sample size (71 rounds) limits statistical power

---

## Actual Predictive Features (Ranked by Correlation with T-Side Wins)

### ✅ Features Favoring T-Side Wins (Positive Correlation)

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| **Max Kill Distance** | +8.7% | T-side wins when kills happen at longer ranges (map control) |
| **Avg Kill Distance** | +8.2% | Longer engagement distances favor T-side |
| **Wallbang Kills** | +7.6% | Aggressive wallbangs favor T-side |
| **Min Kill Distance** | +7.0% | T-side controls engagement distances |
| **Assisted Kills** | +3.4% | Flash assists slightly favor T-side |
| **Smoke Kills** | +1.0% | Very weak - both sides use smokes |

**Insight**: T-side wins when they **control engagement distances** and play more **tactically** (wallbangs, assists, long-range fights).

---

### ❌ Features Favoring CT-Side Wins (Negative Correlation)

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| **Total Damage** | -17.4% | **Strongest predictor** - CT wins with high damage output |
| **Total Kills** | -17.4% | **Strongest predictor** - CT wins with more total eliminations |
| **Headshot Kills** | -13.3% | CT-side better at headshots (defensive angles) |
| **Avg Damage Per Kill** | -12.6% | CT-side has higher damage efficiency |
| **Headshot Rate** | -10.3% | CT-side has better accuracy overall |
| **Rifle Kills** | -4.2% | Weak - both sides use rifles |
| **AWP Kills** | -2.9% | Very weak - both sides use AWP similarly |

**Insight**: CT-side wins when they have **higher damage output** and **better accuracy** (headshots). This makes sense - CTs defend from advantageous positions.

---

## What This Means for Prediction

### For Decision Tree Modeling:

1. **Top Predictive Features** (use these first):
   - `total_damage` (-17.4%)
   - `total_kills` (-17.4%)
   - `headshot_kills` (-13.3%)
   - `avg_damage_per_kill` (-12.6%)
   - `headshot_rate` (-10.3%)
   - `max_kill_distance` (+8.7%)
   - `avg_kill_distance` (+8.2%)

2. **Expected Model Performance**:
   - **Baseline Accuracy**: 63.4% (always predict T-side wins)
   - **Expected ML Accuracy**: 65-75% (modest improvement)
   - **Cross-validation critical** due to weak correlations

3. **Why Accuracy Won't Be Very High**:
   - Weak correlations (all < 20%)
   - Small sample (71 rounds)
   - Missing critical features:
     - Economic state (money, equipment)
     - Map-specific positions
     - Utility usage (grenades, flashes)
     - Player identities/roles
     - Round number (early vs late game)
     - Score state (momentum)

---

## Realistic Interpretation

### The Data Tells Us:

1. **CT-Side wins through superior firepower**
   - More kills, more damage, better accuracy
   - Defensive positions provide advantages
   - When CTs get many kills, they win (obviously)

2. **T-Side wins through tactical play**
   - Controlling engagement distances
   - Using utility effectively (wallbangs, flashes)
   - Avoiding direct confrontations

3. **Round outcomes are COMPLEX**
   - No single feature is a strong predictor
   - Many unmeasured factors matter more
   - Team coordination >>> individual metrics

---

## Updated Correlation Heatmap

The **revised heatmap** now shows:
- ✅ Only gameplay metrics (no outcome variables)
- ✅ Realistic weak correlations
- ✅ No false hot spots
- ✅ Interpretable relationships

**Key patterns visible:**
- `total_kills` and `total_damage` highly correlated (0.93) - expected
- `headshot_kills` and `headshot_rate` correlated (0.78) - expected
- `avg_kill_distance` features cluster together - expected
- Most features have low inter-correlation - good for decision trees

---

## Updated Feature Importance Plot

The **revised plot** shows:
1. `total_damage` and `total_kills` as top predictors
2. Accuracy/headshot metrics as secondary predictors
3. Distance metrics as tertiary predictors
4. All other features have minimal predictive power

---

## Recommendations for Decision Tree

### 1. Feature Selection Strategy

**Start Simple** (3-5 features):
```python
features = [
    'total_kills',        # Strongest predictor
    'headshot_rate',      # Accuracy metric
    'max_kill_distance'   # Tactical metric
]
```

**Expand if Needed** (7-10 features):
```python
features = [
    'total_kills', 'total_damage',
    'headshot_kills', 'headshot_rate',
    'max_kill_distance', 'avg_kill_distance',
    'wallbang_kills', 'assisted_kills'
]
```

### 2. Model Configuration

```python
from sklearn.tree import DecisionTreeClassifier

# Prevent overfitting with weak features
dt = DecisionTreeClassifier(
    max_depth=4,              # Shallow tree (weak correlations)
    min_samples_split=10,     # Require 10 samples to split
    min_samples_leaf=5,       # At least 5 samples per leaf
    random_state=42
)
```

### 3. Evaluation Strategy

```python
from sklearn.model_selection import cross_val_score

# Use stratified k-fold (preserve class distribution)
cv_scores = cross_val_score(
    dt, X, y, 
    cv=5,                    # 5-fold cross-validation
    scoring='accuracy'
)

print(f"CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

### 4. Expected Results

**Realistic Expectations:**
- **Training Accuracy**: 70-80% (may overfit)
- **Cross-Validation Accuracy**: 65-72% (more realistic)
- **Test Accuracy**: 65-75% (if lucky)

**If accuracy is < 65%:**
- The features don't predict well (expected with weak correlations)
- Consider Random Forest or ensemble methods
- Accept that outcomes depend on unmeasured factors

---

## Honest Assessment

### What We Can Learn:

✅ **General patterns exist**: CT-side wins with firepower, T-side wins with tactics
✅ **Some prediction is possible**: Better than random guessing
✅ **Distance matters**: Engagement ranges affect outcomes

### What We Cannot Do:

❌ **High accuracy prediction**: Too many unmeasured factors
❌ **Causal inference**: Correlation ≠ causation
❌ **Generalization**: Small sample from specific tournament

### What's Missing:

- **Economic data**: Weapon values, money remaining
- **Map context**: Specific positions, bomb sites
- **Utility usage**: Grenades thrown, flashes landed
- **Team composition**: Player roles, strategies
- **Game state**: Round number, score, momentum

---

## Conclusion

The **revised analysis** is now:
- ✅ **Methodologically sound** (no outcome variables)
- ✅ **Honestly interpreted** (weak correlations acknowledged)
- ✅ **Realistically framed** (modest expectations set)

**For the decision tree project**, this provides:
- Clean predictive features
- Reasonable baseline
- Interpretable results
- Honest limitations discussion

**The model will likely achieve 65-75% accuracy**, which is:
- Better than baseline (63.4%)
- Reasonable given data limitations
- Honest and defensible

---

*Revised Analysis: October 17, 2025*
*Correction: Removed deterministic outcome variables from predictive features*

