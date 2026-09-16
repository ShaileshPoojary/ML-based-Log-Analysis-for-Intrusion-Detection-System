# ML-Based System Log Analysis for Intrusion Detection

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange?logo=scikit-learn&logoColor=white" alt="Machine Learning">
  <img src="https://img.shields.io/badge/XGBoost-ML-blue?logo=xgboost&logoColor=white" alt="XGBoost">
</p>

## 📌 Overview

This project is a Machine Learning-based Intrusion Detection System that analyzes system call traces and classifies system activity as **Normal** or **Attack**.

The project uses the **ADFA-WD dataset** and compares multiple Machine Learning algorithms for detecting malicious system behavior.

## 🎯 Objectives

- Detect malicious activity by analyzing system call traces.
- Train and compare multiple Machine Learning algorithms.
- Evaluate model performance using standard classification metrics.

## 🔍 Scope

The project focuses on preprocessing system call traces, extracting useful features, training Machine Learning models, and classifying system activity as normal or malicious.

## 📊 Dataset

This project uses the **ADFA-WD (ADFA Windows Dataset)** for intrusion detection research.

**Official Dataset:**  
https://research.unsw.edu.au/projects/adfa-ids-datasets

The dataset contains normal and attack system-call traces.

> The original dataset is not included in this repository. Please obtain it from the official source and follow its usage terms.

## 🤖 Machine Learning Algorithms

The project includes:

- Random Forest
- Logistic Regression
- XGBoost
- Gradient Boosting
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

## 🔄 Workflow

```text
ADFA-WD Dataset
       ↓
Data Preprocessing
       ↓
System Call Encoding
       ↓
Feature Extraction
       ↓
Train ML Models
       ↓
Model Evaluation
       ↓
Normal / Attack Prediction
```

## 📈 Evaluation

The models are evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

The results are compared to understand the performance of different algorithms for intrusion detection.

## 🛠️ Technologies Used

- Python
- Scikit-learn
- XGBoost
- NumPy
- Pandas
- Joblib
- Streamlit
- Altair
- Jupyter Notebook

## 🚀 Run the Application

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Log_Analysis
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install application dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application uses the trained `.pkl` models and preprocessing files included in the repository.

## 📁 Project Structure

```text
Log_Analysis/
│
├── .venv/                         # Local virtual environment (ignored)
│
├── Models/
│   ├── random_forest.pkl
│   ├── logistic_regression.pkl
│   ├── xgboost.pkl
│   ├── gradient_boosting.pkl
│   └── knn.pkl
│
├── Random_test_files/             # Test system-call trace files
│
├── .gitignore
├── app.py                         # Streamlit application
├── call_to_int.pkl                # System-call encoding mapping
├── log_Analysis.ipynb             # Training and experimentation notebook
├── README.md
├── requirements.txt               # Application dependencies
├── requirements-for-training-models.txt
└── vectorizer.pkl                 # Saved feature vectorizer
```

## 💡 Applications

This project can be used as a foundation for:

- Host-Based Intrusion Detection
- System-call anomaly detection
- Malware and suspicious activity analysis
- Cybersecurity research and education

## 🔮 Future Improvements

- Real-time system-call monitoring
- Improved sequence-based detection
- Deep Learning models
- Real-time security alerts
- Enhanced security dashboard

## 🎓 Disclaimer

This project was developed as a **student academic project** for learning and research purposes in the field of Machine Learning and Cybersecurity.

It is intended for educational and experimental use and is **not a production-ready intrusion detection system**. 
