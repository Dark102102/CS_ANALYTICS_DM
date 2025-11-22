#!/usr/bin/env python3
"""
CS2 Machine Learning Models - Examples and Training

This script demonstrates how to train all four types of ML models:
1. Frequent Pattern Mining (Apriori, FP-Growth)
2. Classification (Decision Trees, SVM, k-NN, Naïve Bayes)
3. Clustering (K-Means, DBSCAN, Hierarchical)
4. Regression (Linear Regression, Logistic Regression)

Author: Data Science Pipeline
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                            confusion_matrix, classification_report, silhouette_score,
                            davies_bouldin_score, mean_squared_error, r2_score, mean_absolute_error)

# Classification models
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# Clustering models
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA

# Regression models
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.metrics import roc_auc_score, roc_curve

# Frequent pattern mining
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
BASE_DIR = Path(__file__).parent
FEATURES_DIR = BASE_DIR / "ml_features"
OUTPUT_DIR = BASE_DIR / "ml_results"
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*80)
print("CS2 MACHINE LEARNING MODELS - TRAINING & EVALUATION")
print("="*80)

# ============================================================================
# 1. FREQUENT PATTERN MINING
# ============================================================================
print("\n" + "="*80)
print("1. FREQUENT PATTERN MINING (Apriori & FP-Growth)")
print("="*80)

# Load binary features
fpm_binary = pd.read_csv(FEATURES_DIR / "fpm_binary_features.csv")
fpm_transactions = pd.read_csv(FEATURES_DIR / "fpm_transactions.csv")

print(f"\nLoaded {len(fpm_binary)} rounds with {len([c for c in fpm_binary.columns if c.startswith('item_')])} items")

# Get item columns
item_cols = [c for c in fpm_binary.columns if c.startswith('item_')]
items_df = fpm_binary[item_cols].astype(bool)

print("\n[1.1] Running Apriori Algorithm...")
try:
    # Run Apriori with low support threshold
    frequent_itemsets_apriori = apriori(items_df, min_support=0.1, use_colnames=True)

    if len(frequent_itemsets_apriori) > 0:
        print(f"Found {len(frequent_itemsets_apriori)} frequent itemsets")

        # Generate association rules
        rules_apriori = association_rules(frequent_itemsets_apriori, metric="confidence", min_threshold=0.5)

        print(f"Generated {len(rules_apriori)} association rules")

        # Sort by lift
        rules_apriori = rules_apriori.sort_values('lift', ascending=False)

        print("\nTop 10 Association Rules (by lift):")
        print(rules_apriori[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10).to_string())

        # Save results
        frequent_itemsets_apriori.to_csv(OUTPUT_DIR / "apriori_frequent_itemsets.csv", index=False)
        rules_apriori.to_csv(OUTPUT_DIR / "apriori_rules.csv", index=False)
        print(f"\n✓ Saved Apriori results to {OUTPUT_DIR}")
    else:
        print("No frequent itemsets found with min_support=0.1")
except Exception as e:
    print(f"Error running Apriori: {e}")

print("\n[1.2] Running FP-Growth Algorithm...")
try:
    # Run FP-Growth
    frequent_itemsets_fpgrowth = fpgrowth(items_df, min_support=0.1, use_colnames=True)

    if len(frequent_itemsets_fpgrowth) > 0:
        print(f"Found {len(frequent_itemsets_fpgrowth)} frequent itemsets")

        # Generate association rules
        rules_fpgrowth = association_rules(frequent_itemsets_fpgrowth, metric="confidence", min_threshold=0.5)

        print(f"Generated {len(rules_fpgrowth)} association rules")

        # Find rules predicting wins
        win_rules = rules_fpgrowth[
            rules_fpgrowth['consequents'].apply(lambda x: 'item_t_win' in str(x) or 'item_ct_win' in str(x))
        ].sort_values('lift', ascending=False)

        print(f"\nFound {len(win_rules)} rules predicting round wins")
        print("\nTop 10 Win-Predicting Rules:")
        print(win_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10).to_string())

        # Save results
        frequent_itemsets_fpgrowth.to_csv(OUTPUT_DIR / "fpgrowth_frequent_itemsets.csv", index=False)
        rules_fpgrowth.to_csv(OUTPUT_DIR / "fpgrowth_rules.csv", index=False)
        win_rules.to_csv(OUTPUT_DIR / "fpgrowth_win_rules.csv", index=False)
        print(f"\n✓ Saved FP-Growth results to {OUTPUT_DIR}")
    else:
        print("No frequent itemsets found with min_support=0.1")
except Exception as e:
    print(f"Error running FP-Growth: {e}")

# ============================================================================
# 2. CLASSIFICATION MODELS
# ============================================================================
print("\n" + "="*80)
print("2. CLASSIFICATION MODELS")
print("="*80)

# Load classification features
clf_features = pd.read_csv(FEATURES_DIR / "classification_features.csv")
clf_scaled = pd.read_csv(FEATURES_DIR / "classification_features_scaled.csv")

print(f"\nLoaded {len(clf_features)} samples")

# Prepare data
# For scaled models (SVM, k-NN)
exclude_cols = ['match', 'round', 'map', 'winner', 'reason', 'tick', 't_win', 'ct_win',
                'kill_level', 'distance_level', 'headshot_level']
feature_cols_scaled = [c for c in clf_scaled.columns if c not in exclude_cols and clf_scaled[c].dtype in ['int64', 'float64']]
X_scaled = clf_scaled[feature_cols_scaled].fillna(0)
y = clf_features['t_win']

# For tree-based models (Decision Tree, Naive Bayes) - use unscaled
feature_cols_unscaled = [c for c in clf_features.columns if c not in exclude_cols and clf_features[c].dtype in ['int64', 'float64']]
X_unscaled = clf_features[feature_cols_unscaled].fillna(0)

# Train-test split
X_train_s, X_test_s, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)
X_train_u, X_test_u, _, _ = train_test_split(X_unscaled, y, test_size=0.3, random_state=42, stratify=y)

print(f"Training set: {len(X_train_s)} samples")
print(f"Test set: {len(X_test_s)} samples")
print(f"Class distribution: {y.value_counts().to_dict()}")

# Store results
clf_results = []

print("\n[2.1] Decision Tree Classifier...")
dt_clf = DecisionTreeClassifier(max_depth=10, min_samples_split=5, random_state=42)
dt_clf.fit(X_train_u, y_train)
dt_pred = dt_clf.predict(X_test_u)
dt_acc = accuracy_score(y_test, dt_pred)
dt_f1 = f1_score(y_test, dt_pred)

print(f"  Accuracy: {dt_acc:.4f}")
print(f"  F1-Score: {dt_f1:.4f}")
print(f"\n  Classification Report:")
print(classification_report(y_test, dt_pred))

clf_results.append({
    'model': 'Decision Tree',
    'accuracy': dt_acc,
    'f1_score': dt_f1,
    'precision': precision_score(y_test, dt_pred),
    'recall': recall_score(y_test, dt_pred)
})

# Feature importance
dt_importance = pd.DataFrame({
    'feature': X_train_u.columns,
    'importance': dt_clf.feature_importances_
}).sort_values('importance', ascending=False)
dt_importance.to_csv(OUTPUT_DIR / "dt_feature_importance.csv", index=False)
print(f"\n  Top 10 Important Features:")
print(dt_importance.head(10).to_string())

print("\n[2.2] Support Vector Machine (SVM)...")
svm_clf = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_clf.fit(X_train_s, y_train)
svm_pred = svm_clf.predict(X_test_s)
svm_acc = accuracy_score(y_test, svm_pred)
svm_f1 = f1_score(y_test, svm_pred)

print(f"  Accuracy: {svm_acc:.4f}")
print(f"  F1-Score: {svm_f1:.4f}")

clf_results.append({
    'model': 'SVM (RBF)',
    'accuracy': svm_acc,
    'f1_score': svm_f1,
    'precision': precision_score(y_test, svm_pred),
    'recall': recall_score(y_test, svm_pred)
})

print("\n[2.3] k-Nearest Neighbors (k-NN)...")
# Find optimal k using cross-validation
best_k = 5
best_score = 0
for k in [3, 5, 7, 9, 11]:
    knn_temp = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn_temp, X_train_s, y_train, cv=5)
    if scores.mean() > best_score:
        best_score = scores.mean()
        best_k = k

print(f"  Optimal k: {best_k} (CV score: {best_score:.4f})")

knn_clf = KNeighborsClassifier(n_neighbors=best_k)
knn_clf.fit(X_train_s, y_train)
knn_pred = knn_clf.predict(X_test_s)
knn_acc = accuracy_score(y_test, knn_pred)
knn_f1 = f1_score(y_test, knn_pred)

print(f"  Accuracy: {knn_acc:.4f}")
print(f"  F1-Score: {knn_f1:.4f}")

clf_results.append({
    'model': f'k-NN (k={best_k})',
    'accuracy': knn_acc,
    'f1_score': knn_f1,
    'precision': precision_score(y_test, knn_pred),
    'recall': recall_score(y_test, knn_pred)
})

print("\n[2.4] Naïve Bayes (Gaussian)...")
nb_clf = GaussianNB()
nb_clf.fit(X_train_s, y_train)
nb_pred = nb_clf.predict(X_test_s)
nb_acc = accuracy_score(y_test, nb_pred)
nb_f1 = f1_score(y_test, nb_pred)

print(f"  Accuracy: {nb_acc:.4f}")
print(f"  F1-Score: {nb_f1:.4f}")

clf_results.append({
    'model': 'Naïve Bayes',
    'accuracy': nb_acc,
    'f1_score': nb_f1,
    'precision': precision_score(y_test, nb_pred),
    'recall': recall_score(y_test, nb_pred)
})

# Summary
clf_results_df = pd.DataFrame(clf_results).sort_values('f1_score', ascending=False)
print("\n" + "="*80)
print("CLASSIFICATION RESULTS SUMMARY")
print("="*80)
print(clf_results_df.to_string(index=False))
clf_results_df.to_csv(OUTPUT_DIR / "classification_results.csv", index=False)
print(f"\n✓ Saved classification results to {OUTPUT_DIR}")

# ============================================================================
# 3. CLUSTERING MODELS
# ============================================================================
print("\n" + "="*80)
print("3. CLUSTERING MODELS")
print("="*80)

# Load clustering features
clust_norm = pd.read_csv(FEATURES_DIR / "clustering_features_normalized.csv")
clust_std = pd.read_csv(FEATURES_DIR / "clustering_features_standardized.csv")

print(f"\nLoaded {len(clust_norm)} samples")

# Prepare data
cluster_cols = [c for c in clust_norm.columns if c not in ['match', 'round', 'winner', 'map']]
X_clust_norm = clust_norm[cluster_cols].fillna(0)
X_clust_std = clust_std[cluster_cols].fillna(0)

print(f"Features: {len(cluster_cols)}")

# Store results
clust_results = []

print("\n[3.1] K-Means Clustering...")
# Find optimal k using elbow method and silhouette score
inertias = []
silhouettes = []
K_range = range(2, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_clust_norm)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_clust_norm, labels))

# Choose k with best silhouette score
optimal_k = K_range[np.argmax(silhouettes)]
print(f"  Optimal k: {optimal_k} (Silhouette: {max(silhouettes):.4f})")

# Train final model
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_clust_norm)

kmeans_silhouette = silhouette_score(X_clust_norm, kmeans_labels)
kmeans_db = davies_bouldin_score(X_clust_norm, kmeans_labels)

print(f"  Silhouette Score: {kmeans_silhouette:.4f}")
print(f"  Davies-Bouldin Index: {kmeans_db:.4f}")

clust_results.append({
    'model': f'K-Means (k={optimal_k})',
    'silhouette': kmeans_silhouette,
    'davies_bouldin': kmeans_db,
    'n_clusters': optimal_k
})

# Analyze clusters
clust_analysis = clust_norm.copy()
clust_analysis['cluster'] = kmeans_labels
cluster_summary = clust_analysis.groupby('cluster').agg({
    'winner': lambda x: (x == 'T').mean(),
    'map': lambda x: x.mode().iloc[0] if len(x) > 0 else 'unknown'
}).rename(columns={'winner': 't_win_rate', 'map': 'dominant_map'})

print(f"\n  Cluster Summary:")
print(cluster_summary.to_string())
cluster_summary.to_csv(OUTPUT_DIR / "kmeans_cluster_summary.csv")

print("\n[3.2] DBSCAN Clustering...")
# Try different epsilon values
best_eps = 0.5
best_labels = None
best_score = -1

for eps in [0.3, 0.5, 0.7, 1.0]:
    dbscan = DBSCAN(eps=eps, min_samples=5)
    labels = dbscan.fit_predict(X_clust_std)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    if n_clusters > 1:
        # Only calculate silhouette if we have at least 2 clusters
        score = silhouette_score(X_clust_std[labels != -1], labels[labels != -1]) if len(set(labels)) > 1 else -1
        if score > best_score:
            best_score = score
            best_eps = eps
            best_labels = labels

print(f"  Optimal eps: {best_eps}")
n_clusters_dbscan = len(set(best_labels)) - (1 if -1 in best_labels else 0)
n_noise = list(best_labels).count(-1)

print(f"  Number of clusters: {n_clusters_dbscan}")
print(f"  Number of noise points: {n_noise}")

if n_clusters_dbscan > 1:
    dbscan_silhouette = silhouette_score(X_clust_std[best_labels != -1], best_labels[best_labels != -1])
    dbscan_db = davies_bouldin_score(X_clust_std[best_labels != -1], best_labels[best_labels != -1])
    print(f"  Silhouette Score: {dbscan_silhouette:.4f}")
    print(f"  Davies-Bouldin Index: {dbscan_db:.4f}")

    clust_results.append({
        'model': f'DBSCAN (eps={best_eps})',
        'silhouette': dbscan_silhouette,
        'davies_bouldin': dbscan_db,
        'n_clusters': n_clusters_dbscan
    })

print("\n[3.3] Hierarchical Clustering (Agglomerative)...")
# Use same k as K-Means for comparison
agg_clust = AgglomerativeClustering(n_clusters=optimal_k, linkage='ward')
agg_labels = agg_clust.fit_predict(X_clust_std)

agg_silhouette = silhouette_score(X_clust_std, agg_labels)
agg_db = davies_bouldin_score(X_clust_std, agg_labels)

print(f"  Number of clusters: {optimal_k}")
print(f"  Silhouette Score: {agg_silhouette:.4f}")
print(f"  Davies-Bouldin Index: {agg_db:.4f}")

clust_results.append({
    'model': f'Hierarchical (k={optimal_k})',
    'silhouette': agg_silhouette,
    'davies_bouldin': agg_db,
    'n_clusters': optimal_k
})

# Summary
clust_results_df = pd.DataFrame(clust_results).sort_values('silhouette', ascending=False)
print("\n" + "="*80)
print("CLUSTERING RESULTS SUMMARY")
print("="*80)
print(clust_results_df.to_string(index=False))
clust_results_df.to_csv(OUTPUT_DIR / "clustering_results.csv", index=False)
print(f"\n✓ Saved clustering results to {OUTPUT_DIR}")

# ============================================================================
# 4. REGRESSION MODELS
# ============================================================================
print("\n" + "="*80)
print("4. REGRESSION MODELS")
print("="*80)

# Load regression features
reg_features = pd.read_csv(FEATURES_DIR / "regression_features.csv")

print(f"\nLoaded {len(reg_features)} samples")

# Prepare data
exclude_reg = ['match', 'round', 'map', 'winner', 'reason', 'tick', 't_win', 'ct_win',
               'target_kills', 'target_damage', 'target_headshot_rate', 'prob_t_win',
               'kill_level', 'distance_level', 'headshot_level']
reg_feature_cols = [c for c in reg_features.columns if c not in exclude_reg and reg_features[c].dtype in ['int64', 'float64']]
X_reg = reg_features[reg_feature_cols].fillna(0)

# Store results
reg_results = []

# Linear Regression - Predict total kills
print("\n[4.1] Linear Regression - Predicting Total Kills...")
y_kills = reg_features['target_kills']
X_train_r, X_test_r, y_train_k, y_test_k = train_test_split(X_reg, y_kills, test_size=0.3, random_state=42)

lr_kills = LinearRegression()
lr_kills.fit(X_train_r, y_train_k)
lr_kills_pred = lr_kills.predict(X_test_r)

lr_kills_r2 = r2_score(y_test_k, lr_kills_pred)
lr_kills_mse = mean_squared_error(y_test_k, lr_kills_pred)
lr_kills_mae = mean_absolute_error(y_test_k, lr_kills_pred)

print(f"  R² Score: {lr_kills_r2:.4f}")
print(f"  MSE: {lr_kills_mse:.4f}")
print(f"  MAE: {lr_kills_mae:.4f}")

reg_results.append({
    'model': 'Linear Regression (Kills)',
    'target': 'total_kills',
    'r2_score': lr_kills_r2,
    'mse': lr_kills_mse,
    'mae': lr_kills_mae
})

# Ridge Regression - Predict total damage
print("\n[4.2] Ridge Regression - Predicting Total Damage...")
y_damage = reg_features['target_damage']
X_train_r, X_test_r, y_train_d, y_test_d = train_test_split(X_reg, y_damage, test_size=0.3, random_state=42)

ridge_damage = Ridge(alpha=1.0)
ridge_damage.fit(X_train_r, y_train_d)
ridge_damage_pred = ridge_damage.predict(X_test_r)

ridge_r2 = r2_score(y_test_d, ridge_damage_pred)
ridge_mse = mean_squared_error(y_test_d, ridge_damage_pred)
ridge_mae = mean_absolute_error(y_test_d, ridge_damage_pred)

print(f"  R² Score: {ridge_r2:.4f}")
print(f"  MSE: {ridge_mse:.4f}")
print(f"  MAE: {ridge_mae:.4f}")

reg_results.append({
    'model': 'Ridge Regression (Damage)',
    'target': 'total_damage',
    'r2_score': ridge_r2,
    'mse': ridge_mse,
    'mae': ridge_mae
})

# Logistic Regression - Predict T-side win
print("\n[4.3] Logistic Regression - Predicting T-side Win...")
y_twin = reg_features['t_win']
X_train_r, X_test_r, y_train_w, y_test_w = train_test_split(X_reg, y_twin, test_size=0.3, random_state=42, stratify=y_twin)

log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_r, y_train_w)
log_pred = log_reg.predict(X_test_r)
log_proba = log_reg.predict_proba(X_test_r)[:, 1]

log_acc = accuracy_score(y_test_w, log_pred)
log_f1 = f1_score(y_test_w, log_pred)
log_auc = roc_auc_score(y_test_w, log_proba)

print(f"  Accuracy: {log_acc:.4f}")
print(f"  F1-Score: {log_f1:.4f}")
print(f"  ROC-AUC: {log_auc:.4f}")

reg_results.append({
    'model': 'Logistic Regression (Win)',
    'target': 't_win',
    'r2_score': log_acc,  # Using accuracy for classification
    'mse': log_f1,        # Using F1 for classification
    'mae': log_auc        # Using AUC for classification
})

# Summary
reg_results_df = pd.DataFrame(reg_results)
print("\n" + "="*80)
print("REGRESSION RESULTS SUMMARY")
print("="*80)
print(reg_results_df.to_string(index=False))
reg_results_df.to_csv(OUTPUT_DIR / "regression_results.csv", index=False)
print(f"\n✓ Saved regression results to {OUTPUT_DIR}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ALL MODELS TRAINED SUCCESSFULLY")
print("="*80)

print(f"\nResults saved to: {OUTPUT_DIR}")
print("\nGenerated files:")
print("  [Frequent Pattern Mining]")
print("    - apriori_frequent_itemsets.csv")
print("    - apriori_rules.csv")
print("    - fpgrowth_frequent_itemsets.csv")
print("    - fpgrowth_rules.csv")
print("    - fpgrowth_win_rules.csv")
print("\n  [Classification]")
print("    - classification_results.csv")
print("    - dt_feature_importance.csv")
print("\n  [Clustering]")
print("    - clustering_results.csv")
print("    - kmeans_cluster_summary.csv")
print("\n  [Regression]")
print("    - regression_results.csv")

print("\n" + "="*80)
print("MODEL PERFORMANCE HIGHLIGHTS")
print("="*80)

print(f"\n[Best Classification Model]")
best_clf = clf_results_df.iloc[0]
print(f"  Model: {best_clf['model']}")
print(f"  F1-Score: {best_clf['f1_score']:.4f}")
print(f"  Accuracy: {best_clf['accuracy']:.4f}")

print(f"\n[Best Clustering Model]")
best_clust = clust_results_df.iloc[0]
print(f"  Model: {best_clust['model']}")
print(f"  Silhouette: {best_clust['silhouette']:.4f}")
print(f"  Clusters: {int(best_clust['n_clusters'])}")

print(f"\n[Best Regression Model]")
best_reg = reg_results_df.iloc[0]
print(f"  Model: {best_reg['model']}")
print(f"  Target: {best_reg['target']}")
print(f"  R²/Accuracy: {best_reg['r2_score']:.4f}")

print("\n" + "="*80)
