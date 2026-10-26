# =============================================================================
# train_model.py — ML Training Pipeline
# Machine Learning-Based Disease Risk Prediction System
# =============================================================================

import os
import sys
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve
)

from preprocess import DataPreprocessor

warnings.filterwarnings('ignore')

# ─────────────────────────── Paths ───────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODELS_DIR  = os.path.join(BASE_DIR, 'models')
EVAL_DIR    = os.path.join(BASE_DIR, 'evaluation')

for d in [DATASET_DIR, MODELS_DIR, EVAL_DIR]:
    os.makedirs(d, exist_ok=True)


# =============================================================================
# 1. Synthetic Dataset Generator
# =============================================================================
def generate_dataset(n_samples: int = 1000, seed: int = 42) -> str:
    """
    Generate a realistic synthetic diabetes-like healthcare dataset and save to CSV.
    Returns the filepath.
    """
    filepath = os.path.join(DATASET_DIR, 'diabetes.csv')
    if os.path.exists(filepath):
        print(f"[INFO] Dataset already exists at {filepath}")
        return filepath

    rng = np.random.default_rng(seed)

    age            = rng.integers(18, 80, n_samples)
    bmi            = rng.uniform(17.0, 45.0, n_samples).round(1)
    glucose        = rng.integers(60, 200, n_samples)
    blood_pressure = rng.integers(60, 140, n_samples)
    insulin        = rng.uniform(10.0, 300.0, n_samples).round(1)
    heart_rate     = rng.integers(55, 105, n_samples)
    cholesterol    = rng.integers(120, 320, n_samples)
    gender         = rng.choice(['Male', 'Female'], n_samples)
    smoking        = rng.choice(['Never', 'Former', 'Current'], n_samples,
                                p=[0.55, 0.25, 0.20])
    family_history = rng.choice(['Yes', 'No'], n_samples, p=[0.35, 0.65])
    exercise       = rng.choice(['Low', 'Moderate', 'High'], n_samples,
                                p=[0.40, 0.35, 0.25])

    # Outcome driven by risk factors
    risk_score = (
        (glucose > 140).astype(int) * 3
        + (bmi > 30).astype(int) * 2
        + (age > 50).astype(int) * 2
        + (blood_pressure > 100).astype(int)
        + (family_history == 'Yes').astype(int) * 2
        + (smoking == 'Current').astype(int) * 2
        + (exercise == 'Low').astype(int)
        + rng.integers(0, 3, n_samples)          # noise
    )
    outcome = (risk_score >= 6).astype(int)

    df = pd.DataFrame({
        'Age':           age,
        'Gender':        gender,
        'BMI':           bmi,
        'BloodPressure': blood_pressure,
        'Glucose':       glucose,
        'Insulin':       insulin,
        'HeartRate':     heart_rate,
        'Cholesterol':   cholesterol,
        'SmokingStatus': smoking,
        'FamilyHistory': family_history,
        'ExerciseLevel': exercise,
        'Outcome':       outcome,
    })

    # Inject ~3% missing values realistically
    for col in ['Insulin', 'BMI', 'Cholesterol']:
        mask = rng.random(n_samples) < 0.03
        df.loc[mask, col] = np.nan

    df.to_csv(filepath, index=False)
    print(f"[INFO] Dataset generated: {n_samples} records -> {filepath}")
    return filepath


# =============================================================================
# 2. Model Definitions
# =============================================================================
def get_models() -> dict:
    return {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree':       DecisionTreeClassifier(max_depth=6, random_state=42),
        'Random Forest':       RandomForestClassifier(n_estimators=150, random_state=42),
        'SVM':                 SVC(probability=True, kernel='rbf', random_state=42),
        'KNN':                 KNeighborsClassifier(n_neighbors=7),
    }


# =============================================================================
# 3. Model Evaluation
# =============================================================================
def evaluate_model(model, X_test, y_test) -> dict:
    """Return a dict of all evaluation metrics."""
    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        'accuracy':  round(accuracy_score(y_test, y_pred),  4),
        'precision': round(precision_score(y_test, y_pred, zero_division=0), 4),
        'recall':    round(recall_score(y_test, y_pred,    zero_division=0), 4),
        'f1':        round(f1_score(y_test, y_pred,        zero_division=0), 4),
        'roc_auc':   round(roc_auc_score(y_test, y_proba),  4),
        'confusion_matrix':        confusion_matrix(y_test, y_pred).tolist(),
        'classification_report':   classification_report(y_test, y_pred),
        'y_pred':   y_pred.tolist(),
        'y_proba':  y_proba.tolist(),
    }


# =============================================================================
# 4. Visualisations
# =============================================================================
PALETTE = ['#6C63FF', '#FF6584', '#43C6AC', '#F7B731', '#FC5C7D']

def _save(fig, filename: str):
    path = os.path.join(EVAL_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"[INFO] Chart saved -> {path}")


def plot_accuracy_comparison(results: dict):
    names   = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    labels  = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC-AUC']

    x   = np.arange(len(names))
    w   = 0.15
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')

    for i, (m, lbl) in enumerate(zip(metrics, labels)):
        vals = [results[n][m] for n in names]
        bars = ax.bar(x + i * w, vals, w, label=lbl, color=PALETTE[i], alpha=0.88, edgecolor='white', linewidth=0.4)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                    f'{v:.2f}', ha='center', va='bottom', fontsize=7, color='white')

    ax.set_xticks(x + w * 2)
    ax.set_xticklabels(names, rotation=15, ha='right', color='white', fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel('Score', color='white')
    ax.set_title('Model Performance Comparison', color='white', fontsize=14, pad=12)
    ax.tick_params(colors='white')
    ax.spines[['top', 'right']].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color('#475569')
    ax.yaxis.grid(True, color='#334155', linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)
    legend = ax.legend(facecolor='#1E293B', edgecolor='#475569', labelcolor='white', fontsize=9)
    _save(fig, 'model_comparison.png')


def plot_roc_curves(models: dict, X_test, y_test):
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')

    for (name, model), color in zip(models.items(), PALETTE):
        y_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        ax.plot(fpr, tpr, color=color, lw=2, label=f'{name} (AUC={auc:.3f})')

    ax.plot([0, 1], [0, 1], 'w--', lw=1, alpha=0.5)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1.02])
    ax.set_xlabel('False Positive Rate', color='white')
    ax.set_ylabel('True Positive Rate', color='white')
    ax.set_title('ROC Curves — All Models', color='white', fontsize=14, pad=10)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#475569')
    ax.grid(color='#334155', linestyle='--', alpha=0.4)
    ax.legend(facecolor='#1E293B', edgecolor='#475569', labelcolor='white', fontsize=9)
    _save(fig, 'roc_curves.png')


def plot_confusion_matrices(models: dict, X_test, y_test):
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    fig.patch.set_facecolor('#0F172A')

    for ax, (name, model), color in zip(axes, models.items(), PALETTE):
        cm = confusion_matrix(y_test, model.predict(X_test))
        ax.set_facecolor('#1E293B')
        im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
        ax.set_title(name, color='white', fontsize=9, pad=6)
        ax.set_xlabel('Predicted', color='white', fontsize=8)
        ax.set_ylabel('Actual', color='white', fontsize=8)
        ax.tick_params(colors='white', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#475569')
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, str(cm[i, j]),
                        ha='center', va='center',
                        color='white' if cm[i, j] < thresh else 'black',
                        fontsize=14, fontweight='bold')
        ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
        ax.set_xticklabels(['No Risk', 'At Risk'], color='white', fontsize=8)
        ax.set_yticklabels(['No Risk', 'At Risk'], color='white', fontsize=8)

    fig.suptitle('Confusion Matrices', color='white', fontsize=14, y=1.02)
    plt.tight_layout()
    _save(fig, 'confusion_matrices.png')


def plot_feature_importance(model, feature_names: list):
    if not hasattr(model, 'feature_importances_'):
        print("[INFO] Best model has no feature_importances_; skipping chart.")
        return

    importances = model.feature_importances_
    indices     = np.argsort(importances)[::-1]
    sorted_feats = [feature_names[i] for i in indices]
    sorted_vals  = importances[indices]

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')

    colors = plt.cm.plasma(np.linspace(0.2, 0.85, len(sorted_feats)))
    bars = ax.barh(sorted_feats[::-1], sorted_vals[::-1], color=colors[::-1],
                   edgecolor='white', linewidth=0.3)
    for bar, v in zip(bars, sorted_vals[::-1]):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                f'{v:.3f}', va='center', color='white', fontsize=9)

    ax.set_xlabel('Importance Score', color='white')
    ax.set_title('Feature Importance (Best Model)', color='white', fontsize=14, pad=10)
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#475569')
    ax.xaxis.grid(True, color='#334155', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    _save(fig, 'feature_importance.png')


def plot_correlation_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(11, 9))
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#1E293B')

    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(
        corr, mask=mask, annot=True, fmt='.2f',
        cmap='coolwarm', center=0, linewidths=0.5,
        linecolor='#0F172A', ax=ax,
        annot_kws={'size': 9, 'color': 'white'},
        cbar_kws={'shrink': 0.8}
    )
    ax.set_title('Feature Correlation Heatmap', color='white', fontsize=14, pad=12)
    ax.tick_params(colors='white', labelsize=9)
    for spine in ax.spines.values():
        spine.set_color('#475569')
    _save(fig, 'correlation_heatmap.png')


# =============================================================================
# 5. Main Training Pipeline
# =============================================================================
def train_and_evaluate():
    print("\n" + "=" * 60)
    print("  ML Disease Risk Prediction — Training Pipeline")
    print("=" * 60 + "\n")

    # 5.1 Generate / load dataset
    filepath = generate_dataset(n_samples=1000, seed=42)
    preprocessor = DataPreprocessor()
    df_raw = preprocessor.load_data(filepath)

    # 5.2 Preprocess
    X_train, X_test, y_train, y_test, X_full, y_full = preprocessor.preprocess(df_raw.copy())

    # 5.3 Correlation heatmap (uses raw encoded df)
    df_encoded = df_raw.copy()
    df_encoded = preprocessor.handle_missing_values(df_encoded)
    df_encoded = preprocessor.remove_duplicates(df_encoded)
    df_encoded = preprocessor.handle_outliers(df_encoded)
    df_encoded = preprocessor.encode_categorical(df_encoded, fit=False)
    plot_correlation_heatmap(df_encoded)

    # 5.4 Train models
    models = get_models()
    results = {}
    trained_models = {}

    print("\n[TRAINING] Fitting all models ...")
    for name, model in models.items():
        print(f"  >> {name} ...", end=' ', flush=True)
        model.fit(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        results[name]        = metrics
        trained_models[name] = model
        print(f"Acc={metrics['accuracy']:.4f}  ROC-AUC={metrics['roc_auc']:.4f}")

    # 5.5 Select best model
    best_name  = max(results, key=lambda n: results[n]['accuracy'])
    best_model = trained_models[best_name]
    best_acc   = results[best_name]['accuracy']
    print(f"\n[BEST MODEL] {best_name}  (Accuracy={best_acc:.4f})")

    # 5.6 Save artefacts
    joblib.dump(best_model, os.path.join(MODELS_DIR, 'best_model.pkl'))
    joblib.dump(best_name,  os.path.join(MODELS_DIR, 'best_model_name.pkl'))
    preprocessor.save_artifacts(MODELS_DIR)

    # Save all results as JSON for Flask
    results_serialisable = {
        name: {k: v for k, v in m.items() if k not in ('y_pred', 'y_proba')}
        for name, m in results.items()
    }
    with open(os.path.join(MODELS_DIR, 'results.json'), 'w') as f:
        json.dump({'results': results_serialisable, 'best_model': best_name}, f, indent=2)
    print("[INFO] results.json saved.")

    # 5.7 Generate visualisations
    print("\n[CHARTS] Generating evaluation charts ...")
    plot_accuracy_comparison(results)
    plot_roc_curves(trained_models, X_test, y_test)
    plot_confusion_matrices(trained_models, X_test, y_test)
    plot_feature_importance(best_model, preprocessor.feature_columns)

    print("\n" + "=" * 60)
    print("  Training Complete! All artefacts saved.")
    print("=" * 60 + "\n")
    return results, best_name


if __name__ == '__main__':
    train_and_evaluate()
