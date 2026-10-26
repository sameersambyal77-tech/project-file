# =============================================================================
# predict.py — Prediction & Recommendation Engine
# Machine Learning-Based Disease Risk Prediction System
# =============================================================================

import os
import numpy as np
import joblib
from preprocess import DataPreprocessor

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')


class DiseasePredictor:
    """
    Loads the best-trained model and runs inference on patient data.
    Returns prediction, probability, risk level, and health recommendations.
    """

    # Risk thresholds
    LOW_THRESHOLD    = 0.35
    MEDIUM_THRESHOLD = 0.65

    # ─────────────────────────────────────────────────────────────
    # Recommendations by risk level
    # ─────────────────────────────────────────────────────────────
    RECOMMENDATIONS = {
        'Low': {
            'title':   '✅ Low Risk — Keep it Up!',
            'color':   'success',
            'icon':    'bi-shield-check',
            'tips': [
                '🥗 Maintain a balanced diet rich in vegetables and whole grains.',
                '🏃 Exercise at least 150 minutes per week (brisk walking, cycling, swimming).',
                '💧 Stay well-hydrated — aim for 8 glasses of water daily.',
                '😴 Get 7–9 hours of quality sleep each night.',
                '🚭 Avoid smoking and limit alcohol consumption.',
                '🩺 Schedule routine health check-ups every 12 months.',
                '🧘 Manage stress through meditation, yoga, or hobbies.',
                '⚖️ Maintain a healthy weight (BMI 18.5–24.9).',
            ],
            'action': 'Continue your healthy lifestyle and monitor your health annually.'
        },
        'Medium': {
            'title':   '⚠️ Moderate Risk — Take Action',
            'color':   'warning',
            'icon':    'bi-exclamation-triangle',
            'tips': [
                '🩺 Consult your doctor within the next 2–4 weeks for a thorough evaluation.',
                '🍽️ Reduce intake of sugar, saturated fats, and processed foods.',
                '🏋️ Increase physical activity — aim for 30 minutes of exercise 5×/week.',
                '📊 Monitor blood glucose, blood pressure, and cholesterol regularly.',
                '⚖️ Work towards a healthy BMI if currently overweight.',
                '🚭 Quit smoking immediately; seek help if needed.',
                '💊 Discuss preventive medications or supplements with your physician.',
                '👨‍👩‍👧 Inform close family members — hereditary conditions may affect them too.',
            ],
            'action': 'Schedule a medical appointment soon and adopt healthier habits.'
        },
        'High': {
            'title':   '🚨 High Risk — Seek Immediate Care',
            'color':   'danger',
            'icon':    'bi-heart-pulse-fill',
            'tips': [
                '🏥 URGENT: Consult a doctor or specialist IMMEDIATELY.',
                '📋 Get a comprehensive health screening (blood panel, ECG, imaging).',
                '💊 Follow prescribed medications strictly and without interruption.',
                '🚨 If experiencing chest pain, dizziness, or breathlessness — call emergency services.',
                '🍎 Adopt a strict low-sugar, low-sodium, high-fibre diet under dietitian guidance.',
                '🛑 Stop all tobacco and alcohol use immediately.',
                '📱 Use health-monitoring devices (glucometer, BP monitor) daily.',
                '👨‍⚕️ Consider referral to an endocrinologist or cardiologist.',
                '🏋️ Begin a medically supervised exercise programme.',
                '🧬 Genetic counselling recommended if strong family history.',
            ],
            'action': 'Do NOT delay — book an emergency medical appointment today.'
        }
    }

    def __init__(self):
        self.model              = None
        self.model_name         = None
        self.preprocessor       = DataPreprocessor()
        self._loaded            = False

    # ─────────────────────────────────────────────────────────────
    def load_model(self):
        """Load the trained model and preprocessing artefacts from disk."""
        model_path = os.path.join(MODELS_DIR, 'best_model.pkl')
        name_path  = os.path.join(MODELS_DIR, 'best_model_name.pkl')

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "Trained model not found. Please run train_model.py first."
            )

        self.model      = joblib.load(model_path)
        self.model_name = joblib.load(name_path)
        self.preprocessor.load_artifacts(MODELS_DIR)
        self._loaded = True
        print(f"[INFO] Model loaded: {self.model_name}")

    # ─────────────────────────────────────────────────────────────
    def _ensure_loaded(self):
        if not self._loaded:
            self.load_model()

    # ─────────────────────────────────────────────────────────────
    def predict(self, patient_data: dict) -> dict:
        """
        Run prediction on a single patient record.

        Parameters
        ----------
        patient_data : dict
            Keys matching the training feature columns.

        Returns
        -------
        dict with keys: prediction, probability, risk_level, recommendations, model_name
        """
        self._ensure_loaded()

        try:
            X = self.preprocessor.preprocess_single(patient_data)
        except Exception as e:
            raise ValueError(f"Preprocessing error: {e}")

        prediction  = int(self.model.predict(X)[0])
        probability = float(self.model.predict_proba(X)[0][1])

        risk_level  = self._determine_risk_level(probability)
        recs        = self.RECOMMENDATIONS[risk_level]

        return {
            'prediction':      prediction,
            'probability':     round(probability * 100, 2),
            'risk_level':      risk_level,
            'model_name':      self.model_name,
            'recommendation':  recs,
        }

    # ─────────────────────────────────────────────────────────────
    def predict_batch(self, records: list) -> list:
        """Run prediction on a list of patient records (CSV batch)."""
        self._ensure_loaded()
        return [self.predict(rec) for rec in records]

    # ─────────────────────────────────────────────────────────────
    def _determine_risk_level(self, probability: float) -> str:
        if probability < self.LOW_THRESHOLD:
            return 'Low'
        elif probability < self.MEDIUM_THRESHOLD:
            return 'Medium'
        else:
            return 'High'


# ─────────────────────────────────────────────────────────────────
# Quick test
# ─────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    predictor = DiseasePredictor()
    test_patient = {
        'Age':           55,
        'Gender':        'Male',
        'BMI':           32.4,
        'BloodPressure': 110,
        'Glucose':       160,
        'Insulin':       85.0,
        'HeartRate':     78,
        'Cholesterol':   240,
        'SmokingStatus': 'Current',
        'FamilyHistory': 'Yes',
        'ExerciseLevel': 'Low',
    }
    result = predictor.predict(test_patient)
    print("\n[PREDICTION RESULT]")
    print(f"  Prediction  : {'At Risk' if result['prediction'] == 1 else 'No Risk'}")
    print(f"  Probability : {result['probability']}%")
    print(f"  Risk Level  : {result['risk_level']}")
    print(f"  Model Used  : {result['model_name']}")
