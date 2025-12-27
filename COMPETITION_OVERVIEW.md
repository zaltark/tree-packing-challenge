# 2025 Kaggle Playground Series: Tree Packing Challenge

## Overview
The goal of this competition is to predict the probability that a patient will be diagnosed with diabetes using a synthetically generated dataset based on real-world data.

## Goal
Predict the probability for the `diagnosed_diabetes` variable for each `id` in the test set.

## Evaluation
Submissions are evaluated on **Area Under the ROC Curve (AUC)** between the predicted probability and the observed target.

### Submission Format
The submission file should be a CSV with a header and the following format:
```csv
id,diagnosed_diabetes
700000,0.2
700001,0.4
700002,0.5
```

## Timeline
- **Start Date:** December 1, 2025
- **Final Submission Deadline:** December 31, 2025 (11:59 PM UTC)

## About the Dataset
This is a tabular dataset synthetically generated from real-world data. It is designed to be lightweight, allowing for quick iteration on feature engineering and modeling.
