# Machine Learning-Based Disease Risk Prediction System

> **MCA (AI & ML) Minor Project** — Production-quality Flask web application for disease risk prediction using 5 Machine Learning algorithms.

---

## 📋 Project Overview

This system predicts whether a patient is at risk of **diabetes** using advanced machine learning algorithms. It preprocesses clinical data, trains and compares 5 ML models, automatically selects the best, and deploys it via a Flask web application with a modern Bootstrap 5 UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **5 ML Models** | Logistic Regression, Decision Tree, Random Forest, SVM, KNN |
| 📊 **Model Comparison** | Accuracy, Precision, Recall, F1, ROC-AUC with charts |
| 🎯 **Risk Stratification** | Low / Medium / High risk with probability % |
| 💡 **Recommendations** | Personalised health advice per risk level |
| 📄 **PDF Reports** | Downloadable professional health report |
| 📁 **Batch Prediction** | CSV upload for bulk patient processing |
| 🔐 **Auth System** | Login / Register with role-based access |
| 📈 **Patient Dashboard** | Full prediction history |
| 🛡️ **Admin Panel** | System stats, all users, all predictions |
| 🌙 **Dark Mode** | Toggle dark/light with persistence |
| 📱 **Responsive** | Mobile-first Bootstrap 5 design |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip

### 1. Clone / Open Project
```bash
cd Disease_Risk_Prediction
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the ML Models *(run once)*
```bash
python train_model.py
```
This will:
- Generate the synthetic diabetes dataset (1,000 patients)
- Train all 5 ML models
- Evaluate and compare performance
- Save the best model to `models/`
- Generate 5 evaluation charts to `evaluation/`

### 5. Run the Flask Application
```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## 📁 Project Structure

```
Disease_Risk_Prediction/
├── app.py              # Flask application (15+ routes)
├── train_model.py      # ML training pipeline
├── predict.py          # Prediction & recommendation engine
├── preprocess.py       # Data preprocessing module
├── utils.py            # DB, PDF, auth utilities
├── requirements.txt    # Python dependencies
├── README.md
│
├── dataset/
│   └── diabetes.csv    # Auto-generated on first train
│
├── models/
│   ├── best_model.pkl         # Best trained model
│   ├── best_model_name.pkl    # Name of best model
│   ├── scaler.pkl             # StandardScaler
│   ├── label_encoders.pkl     # Label encoders
│   ├── feature_columns.pkl    # Feature list
│   └── results.json           # All model metrics
│
├── evaluation/
│   ├── model_comparison.png
│   ├── roc_curves.png
│   ├── confusion_matrices.png
│   ├── feature_importance.png
│   └── correlation_heatmap.png
│
├── reports/            # Generated PDF reports
├── preprocessing/      # Package __init__
│
├── static/
│   ├── css/style.css   # Full custom CSS + dark mode
│   └── js/main.js      # Interactive JavaScript
│
└── templates/
    ├── base.html       # Base layout
    ├── index.html      # Home page
    ├── predict.html    # Prediction form
    ├── result.html     # Prediction result
    ├── comparison.html # Model comparison
    ├── about.html      # About / documentation
    ├── contact.html    # Contact form
    ├── login.html      # Login
    ├── register.html   # Register
    ├── dashboard.html  # Patient dashboard
    ├── admin.html      # Admin dashboard
    ├── batch_predict.html  # CSV batch prediction
    ├── 404.html / 403.html / 500.html
```

---

## 🧬 Dataset

A **synthetic but medically realistic** dataset is auto-generated with:
- **1,000 patient records**
- **11 clinical features**: Age, Gender, BMI, Blood Pressure, Glucose, Insulin, Heart Rate, Cholesterol, Smoking Status, Family History, Exercise Level
- **Binary outcome**: Diabetic risk (0 = No Risk, 1 = At Risk)
- Risk driven by medically sound factors (high glucose, high BMI, family history, etc.)

---

## 🤖 Machine Learning Pipeline

### Preprocessing
1. Missing value imputation (median/mode)
2. Duplicate removal
3. Outlier capping (IQR method)
4. Label Encoding (categorical features)
5. Standard Scaling (Z-score normalisation)
6. Stratified Train/Test Split (80/20)

### Models Trained
| Model | Key Parameters |
|---|---|
| Logistic Regression | `max_iter=1000` |
| Decision Tree | `max_depth=6` |
| Random Forest | `n_estimators=150` |
| SVM | `kernel='rbf', probability=True` |
| KNN | `n_neighbors=7` |

### Evaluation Metrics
- Accuracy, Precision, Recall, F1 Score, ROC-AUC
- Confusion Matrix, Classification Report

---

## 🌐 Web Application Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page |
| `/predict` | GET/POST | Prediction form |
| `/comparison` | GET | Model comparison & charts |
| `/about` | GET | Project documentation |
| `/contact` | GET/POST | Contact form |
| `/login` | GET/POST | User login |
| `/register` | GET/POST | User registration |
| `/logout` | GET | Logout |
| `/dashboard` | GET | Patient prediction history |
| `/admin` | GET | Admin analytics panel |
| `/batch_predict` | GET/POST | CSV batch prediction |
| `/download_report/<id>` | GET | PDF report download |
| `/evaluation/<file>` | GET | Serve chart images |
| `/api/history` | GET | JSON prediction history |
| `/api/stats` | GET | JSON admin stats |

---

## 👤 User Roles

- **First registered user** → automatically becomes **Admin**
- Subsequent registrations → **Patient** role
- Admin can see all users and all predictions

---

## 📊 Visualisations Generated

1. **Model Performance Comparison** — grouped bar chart (5 metrics × 5 models)
2. **ROC Curves** — all 5 models with AUC scores
3. **Confusion Matrices** — all 5 models side-by-side
4. **Feature Importance** — horizontal bar chart (best model only)
5. **Correlation Heatmap** — feature correlation matrix

---

## 💻 Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Web Framework | Flask 3.1 |
| ML Library | Scikit-learn 1.6 |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| PDF Generation | ReportLab |
| Model Persistence | Joblib |
| Database | SQLite (via stdlib) |
| Frontend | Bootstrap 5, Bootstrap Icons |
| Fonts | Google Fonts (Inter, Outfit) |
| Charts (Admin) | Chart.js |

---

## ⚠️ Disclaimer

> This system is for **educational and research purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## 📝 License

This project is developed as an **MCA Minor Project** for academic submission.
