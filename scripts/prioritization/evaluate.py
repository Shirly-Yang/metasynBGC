# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score


truth = pd.read_csv('results/split/test.csv')
pred = pd.read_csv('results/predictions/test_predictions.csv')
merged = pd.merge(truth, pred[['smiles', 'pred_0']], on='smiles', how='inner')


y_true = merged['label'].astype(int)
y_pred_proba = merged['pred_0'].values
y_pred_class = (y_pred_proba >= 0.5).astype(int)


auc = roc_auc_score(y_true, y_pred_proba)
acc = accuracy_score(y_true, y_pred_class)
prec = precision_score(y_true, y_pred_class)
rec = recall_score(y_true, y_pred_class)
f1 = f1_score(y_true, y_pred_class)
tn, fp, fn, tp = confusion_matrix(y_true, y_pred_class).ravel()


print("\n" + "="*50)
print("EVALUATION METRICS")
print("="*50)
print(f"AUC-ROC:        {auc:.4f}")
print(f"Accuracy:       {acc:.4f}")
print(f"Precision:      {prec:.4f}")
print(f"Recall:         {rec:.4f}")
print(f"F1-Score:       {f1:.4f}")
print(f"\nConfusion Matrix:")
print(f"  True Negatives:  {tn}")
print(f"  False Positives: {fp}")
print(f"  False Negatives: {fn}")
print(f"  True Positives:  {tp}")
print(f"\nSample size: {len(y_true)}")
print("="*50)

import os
os.makedirs('results/metrics', exist_ok=True)
with open('results/metrics/evaluation_results.txt', 'w') as f:
    f.write("="*50 + "\n")
    f.write("EVALUATION METRICS\n")
    f.write("="*50 + "\n")
    f.write(f"AUC-ROC:        {auc:.4f}\n")
    f.write(f"Accuracy:       {acc:.4f}\n")
    f.write(f"Precision:      {prec:.4f}\n")
    f.write(f"Recall:         {rec:.4f}\n")
    f.write(f"F1-Score:       {f1:.4f}\n")
    f.write(f"\nConfusion Matrix:\n")
    f.write(f"  True Negatives:  {tn}\n")
    f.write(f"  False Positives: {fp}\n")
    f.write(f"  False Negatives: {fn}\n")
    f.write(f"  True Positives:  {tp}\n")
    f.write(f"\nSample size: {len(y_true)}\n")
    f.write("="*50 + "\n")

print("\nResults saved to: results/metrics/evaluation_results.txt")
EOF

# 运行脚本
#python evaluate_new.py
