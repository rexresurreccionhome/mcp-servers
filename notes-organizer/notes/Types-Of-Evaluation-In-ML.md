# Types Of Evaluation Metrics in ML

## Overview
Evaluation metrics are quantitative measures used to assess the performance of machine learning models. Different metrics are appropriate for different types of problems.

## Quick Reference Guide

### When to Use Each Metric

**Classification Problems:**
- **Accuracy**: Use when classes are balanced and all errors are equally important
- **Precision**: Use when false positives are costly (e.g., spam detection - don't want important emails marked as spam)
- **Recall**: Use when false negatives are costly (e.g., disease detection - don't want to miss sick patients)
- **F1 Score**: Use when you need balance between precision and recall, especially with imbalanced datasets
- **ROC-AUC**: Use when you want to evaluate performance across different classification thresholds

**Regression Problems:**
- **MAE**: Use when you want easy-to-interpret average error in original units
- **MSE**: Use when you want to heavily penalize large errors
- **RMSE**: Use when you want interpretability (same units) while penalizing large errors
- **R² Score**: Use when you want to understand how much variance your model explains

**Clustering Problems:**
- **Silhouette Score**: Use to validate cluster quality and optimal number of clusters
- **Davies-Bouldin Index**: Use to compare different clustering algorithms

## Classification Metrics

### Accuracy
- Proportion of correct predictions out of total predictions
- Formula: `(TP + TN) / (TP + TN + FP + FN)`
- Best for: Balanced datasets
- Limitation: Misleading for imbalanced datasets

### Precision
- Proportion of true positive predictions among all positive predictions
- Formula: `TP / (TP + FP)`
- Answers: "Of all predicted positives, how many are actually positive?"
- Important when: False positives are costly

### Recall (Sensitivity)
- Proportion of actual positives correctly identified
- Formula: `TP / (TP + FN)`
- Answers: "Of all actual positives, how many did we identify?"
- Important when: False negatives are costly

### F1 Score
- Harmonic mean of precision and recall
- Formula: `2 * (Precision * Recall) / (Precision + Recall)`
- Best for: Imbalanced datasets where you need balance between precision and recall

### ROC-AUC
- Area Under the Receiver Operating Characteristic curve
- Measures trade-off between true positive rate and false positive rate
- Range: 0 to 1 (higher is better)
- Best for: Binary classification, understanding model performance across thresholds

## Regression Metrics

### Mean Absolute Error (MAE)
- Average of absolute differences between predicted and actual values
- Formula: `Σ|y_actual - y_predicted| / n`
- Interpretation: Easy to understand, same units as target variable

### Mean Squared Error (MSE)
- Average of squared differences between predicted and actual values
- Formula: `Σ(y_actual - y_predicted)² / n`
- Property: Penalizes larger errors more heavily

### Root Mean Squared Error (RMSE)
- Square root of MSE
- Formula: `√(MSE)`
- Advantage: Same units as target variable, penalizes large errors

### R² Score (Coefficient of Determination)
- Proportion of variance in the dependent variable explained by the model
- Range: -∞ to 1 (1 is perfect fit)
- Formula: `1 - (SS_residual / SS_total)`

## Clustering Metrics

### Silhouette Score
- Measures how similar an object is to its own cluster vs other clusters
- Range: -1 to 1 (higher is better)

### Davies-Bouldin Index
- Average similarity ratio of each cluster with its most similar cluster
- Lower values indicate better clustering

## Key Considerations

1. **Problem Type**: Choose metrics appropriate for classification, regression, or clustering
2. **Business Context**: Align metrics with business objectives
3. **Data Balance**: Consider class imbalance when selecting classification metrics
4. **Multiple Metrics**: Use several metrics to get a comprehensive view of model performance
5. **Baseline Comparison**: Compare against baseline models to gauge improvement

## Confusion Matrix Components

- **True Positives (TP)**: Correctly predicted positive cases
- **True Negatives (TN)**: Correctly predicted negative cases
- **False Positives (FP)**: Incorrectly predicted as positive (Type I error)
- **False Negatives (FN)**: Incorrectly predicted as negative (Type II error)
