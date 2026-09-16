# ML-Based System Log Analysis for Intrusion Detection

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Machine%20Learning-scikit--learn-orange?logo=scikit-learn&logoColor=white" alt="Machine Learning">
  <img src="https://img.shields.io/badge/XGBoost-ML-blue?logo=xgboost&logoColor=white" alt="XGBoost">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## 📌 Overview

**ML-Based System Log Analysis for Intrusion Detection** is a machine-learning project that analyzes system-call traces from the **ADFA-WD (ADFA Windows Dataset)** to distinguish between normal and malicious system activity.

The project converts system-call/function-call sequences into numerical/text-based features and trains multiple machine-learning classifiers. Their performance is evaluated using standard classification metrics such as accuracy, precision, recall, and F1-score.

The project is intended as an academic/research-oriented Host-Based Intrusion Detection System (HIDS) prototype.

---

## 🎯 Objectives

- Analyze system-call traces for intrusion detection.
- Preprocess and transform raw traces into machine-learning features.
- Train multiple classification algorithms for normal/attack classification.
- Compare model performance using standard evaluation metrics.
- Provide a reusable trained-model pipeline for testing new traces.

---

## 🔍 Scope

The project focuses on host-based intrusion detection using system-call/function-call traces. It covers data preprocessing, feature extraction, machine-learning model training, evaluation, model serialization, and prediction on new trace files.

The current implementation focuses on the **ADFA-WD Windows dataset** and its system-call/DLL-call traces.

---

## 🧠 Machine Learning Models

The project includes trained models based on:

- Random Forest
- Logistic Regression
- XGBoost
- Gradient Boosting
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM/LinearSVC) during model experimentation

The models are evaluated using the same feature representation and train/test methodology where applicable to provide a consistent comparison.

---

## 🔄 Project Pipeline

```text
ADFA-WD Dataset
       │
       ▼
Raw System/Function Call Traces
       │
       ▼
Preprocessing
       │
       ▼
Call-to-Integer Mapping
       │
       ▼
CountVectorizer / TF-IDF
       │
       ▼
Train / Test Split
       │
       ▼
Machine Learning Models
       │
       ├── Random Forest
       ├── Logistic Regression
       ├── XGBoost
       ├── Gradient Boosting
       └── KNN
       │
       ▼
Performance Evaluation
       │
       ▼
Normal / Attack Classification
```

---

## 📊 Dataset

This project uses the **ADFA-WD (ADFA Windows Dataset)** from the Australian Defence Force Academy / UNSW.

The official dataset page provides the ADFA intrusion-detection datasets, including ADFA-WD and the ADFA-WD Stealth Attacks Addendum.

**Official dataset source:**

https://research.unsw.edu.au/projects/adfa-ids-datasets

### ADFA-WD

ADFA-WD is a Windows host-based intrusion-detection dataset designed for evaluating system-call-based HIDS approaches.

The dataset contains normal and attack traces and includes Windows DLL/system-call related activity. The commonly reported ADFA-WD structure contains:

- Training traces — normal activity
- Validation traces — normal activity
- Attack traces — malicious activity

The dataset and its associated material are provided under terms specified by the dataset creators. Please review the official dataset page and license before redistributing dataset files.

> **Important:** The raw ADFA-WD dataset is not included in this repository. Users should obtain it from the official source and comply with its usage terms.

---

## 📁 Repository Structure

```text
Log_Analysis/
│
├── Models/
│   ├── random_forest.pkl
│   ├── logistic_regression.pkl
│   ├── xgboost.pkl
│   ├── gradient_boosting.pkl
│   └── knn.pkl
│
├── Random_test_files/
│   └── *.GHC
│
├── app.py
├── log_Analysis.ipynb
├── call_to_int.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
└── .gitignore
```

### Important files

| File | Purpose |
|---|---|
| `app.py` | Application/prediction entry point |
| `log_Analysis.ipynb` | Data preprocessing, training and experimentation |
| `Models/` | Saved trained ML models |
| `vectorizer.pkl` | Saved feature vectorizer |
| `call_to_int.pkl` | Mapping used to encode system/function calls |
| `Random_test_files/` | Small test traces used for experimentation |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from version control |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Log_Analysis
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Training

Open:

```text
log_Analysis.ipynb
```

Run the preprocessing, feature extraction, training, and evaluation cells.

The trained models can be saved using `joblib`.

### Prediction

The saved models and preprocessing artifacts can be loaded by the application:

```python
import joblib

model = joblib.load("Models/random_forest.pkl")
vectorizer = joblib.load("vectorizer.pkl")
call_to_int = joblib.load("call_to_int.pkl")
```

New system/function-call traces can then be processed using the same preprocessing and vectorization pipeline before prediction.

---

## 📈 Evaluation

The project evaluates the classifiers using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

A comparison chart can be generated to compare the accuracy and F1-score of the different algorithms.

For intrusion detection, accuracy should not be considered in isolation because the distribution between normal and attack traces can affect the interpretation of performance. Precision, recall and F1-score should also be examined.

---

## 🛡️ Applications

This type of system can be used as a foundation for:

- Host-Based Intrusion Detection Systems (HIDS)
- Malware behavior analysis
- System-call anomaly detection
- Security monitoring research
- Suspicious process/activity classification
- Academic cybersecurity experiments
- Machine-learning-based security analytics

This project is a research/academic prototype and should not be treated as a production security system without additional validation.

---

## ⚠️ Important Dataset/Platform Note

The project uses **ADFA-WD**, which is a Windows system-call/function-call trace dataset.

Windows Event Viewer logs such as:

```text
Index
Time
EntryType
Source
InstanceID
Message
```

are a different type of data and should **not** be directly passed to the ADFA-WD-trained models.

Similarly, traces containing entries such as:

```text
kernel32.dll+0xace4
ntdll.dll+0x1cd1b
```

represent Windows DLL/module-based call traces used in the ADFA-WD context. They should be processed using the same representation and preprocessing assumptions used during training.

---

## 🔬 Future Improvements

- Add real-time system-call monitoring.
- Add a dedicated prediction API/UI.
- Improve sequence-based feature extraction.
- Experiment with TF-IDF and n-gram representations.
- Add deep-learning sequence models such as LSTM/GRU/Transformers.
- Add explainable-AI techniques for prediction analysis.
- Evaluate the system on additional Windows security datasets.
- Add automated performance reports and visualization.

---

## 📚 References

1. G. Creech and J. Hu, *A Semantic Approach to Host-based Intrusion Detection Systems Using Contiguous and Discontiguous System Call Patterns*, IEEE Transactions on Information Forensics and Security.
2. G. Creech, *Developing a high-accuracy cross platform Host-Based Intrusion Detection System capable of reliably detecting zero-day attacks*, PhD thesis, Australian Defence Force Academy.
3. Australian Defence Force Academy / UNSW, **ADFA Intrusion Detection Datasets**.

Official dataset information:

https://research.unsw.edu.au/projects/adfa-ids-datasets

---

## 📄 License

This repository's source code can be released under the **MIT License** if that is the license you choose for your own code.

The ADFA-WD dataset is subject to its own terms and licensing conditions. The dataset is not relicensed by this repository.

---

## 👨‍💻 Project Status

**Status:** Academic/Research Project

The project is under active development, with ongoing experimentation and comparison of machine-learning algorithms for system-call-based intrusion detection.
