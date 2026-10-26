# =============================================================================
# utils.py — Utility Functions
# Machine Learning-Based Disease Risk Prediction System
# =============================================================================

import os
import sqlite3
import json
import hashlib
import secrets
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DB_PATH     = os.path.join(BASE_DIR, 'disease_risk.db')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)


# =============================================================================
# Database Helpers
# =============================================================================

def get_db():
    """Return a SQLite connection with row_factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    cur  = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt          TEXT NOT NULL,
            role          TEXT NOT NULL DEFAULT 'patient',
            created_at    TEXT NOT NULL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER,
            age           INTEGER,
            gender        TEXT,
            bmi           REAL,
            blood_pressure INTEGER,
            glucose       INTEGER,
            insulin       REAL,
            heart_rate    INTEGER,
            cholesterol   INTEGER,
            smoking       TEXT,
            family_history TEXT,
            exercise      TEXT,
            prediction    INTEGER,
            probability   REAL,
            risk_level    TEXT,
            model_name    TEXT,
            created_at    TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT,
            email      TEXT,
            subject    TEXT,
            message    TEXT,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("[INFO] Database initialised.")


# =============================================================================
# Password Utilities
# =============================================================================

def hash_password(password: str) -> tuple[str, str]:
    """Return (hashed_password, salt)."""
    salt = secrets.token_hex(16)
    pw_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return pw_hash, salt


def verify_password(password: str, pw_hash: str, salt: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return hashlib.sha256((salt + password).encode()).hexdigest() == pw_hash


# =============================================================================
# User CRUD
# =============================================================================

def create_user(username: str, email: str, password: str, role: str = 'patient') -> bool:
    """Create a new user. Returns True on success, False if duplicate."""
    pw_hash, salt = hash_password(password)
    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO users (username, email, password_hash, salt, role, created_at) VALUES (?,?,?,?,?,?)',
            (username, email, pw_hash, salt, role, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_username(username: str):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    return user


def get_all_users():
    conn = get_db()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return users


# =============================================================================
# Prediction History CRUD
# =============================================================================

def save_prediction(user_id, form_data: dict, result: dict) -> int:
    """Persist a prediction record and return its ID."""
    conn = get_db()
    cur  = conn.cursor()
    cur.execute('''
        INSERT INTO predictions
        (user_id, age, gender, bmi, blood_pressure, glucose, insulin,
         heart_rate, cholesterol, smoking, family_history, exercise,
         prediction, probability, risk_level, model_name, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        user_id,
        form_data.get('Age'),
        form_data.get('Gender'),
        form_data.get('BMI'),
        form_data.get('BloodPressure'),
        form_data.get('Glucose'),
        form_data.get('Insulin'),
        form_data.get('HeartRate'),
        form_data.get('Cholesterol'),
        form_data.get('SmokingStatus'),
        form_data.get('FamilyHistory'),
        form_data.get('ExerciseLevel'),
        result.get('prediction'),
        result.get('probability'),
        result.get('risk_level'),
        result.get('model_name'),
        datetime.now().isoformat(),
    ))
    pred_id = cur.lastrowid
    conn.commit()
    conn.close()
    return pred_id


def get_user_predictions(user_id: int):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM predictions WHERE user_id=? ORDER BY created_at DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_predictions():
    conn = get_db()
    rows = conn.execute(
        '''SELECT p.*, u.username FROM predictions p
           LEFT JOIN users u ON p.user_id=u.id
           ORDER BY p.created_at DESC'''
    ).fetchall()
    conn.close()
    return rows


def get_prediction_by_id(pred_id: int):
    conn = get_db()
    row  = conn.execute('SELECT * FROM predictions WHERE id=?', (pred_id,)).fetchone()
    conn.close()
    return row


# =============================================================================
# Contact Form
# =============================================================================

def save_contact(name: str, email: str, subject: str, message: str):
    conn = get_db()
    conn.execute(
        'INSERT INTO contacts (name, email, subject, message, created_at) VALUES (?,?,?,?,?)',
        (name, email, subject, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


# =============================================================================
# PDF Report Generator
# =============================================================================

def generate_pdf_report(pred_id: int, patient_data: dict, result: dict) -> str:
    """
    Generate a PDF prediction report.
    Returns the file path of the saved PDF.
    """
    filename  = f"report_{pred_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath  = os.path.join(REPORTS_DIR, filename)

    doc    = SimpleDocTemplate(filepath, pagesize=A4,
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    # --- Colour palette ---
    dark_blue   = colors.HexColor('#1E3A5F')
    accent      = colors.HexColor('#6C63FF')
    light_gray  = colors.HexColor('#F8F9FA')
    danger_red  = colors.HexColor('#DC3545')
    warn_orange = colors.HexColor('#FFC107')
    ok_green    = colors.HexColor('#28A745')

    risk_color = {'Low': ok_green, 'Medium': warn_orange, 'High': danger_red}

    # --- Title ---
    title_style = ParagraphStyle('Title', fontSize=22, textColor=dark_blue,
                                 alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold')
    sub_style   = ParagraphStyle('Sub', fontSize=11, textColor=colors.grey,
                                 alignment=TA_CENTER, spaceAfter=12)
    story.append(Paragraph('ML Disease Risk Prediction Report', title_style))
    story.append(Paragraph(f'Generated on {datetime.now().strftime("%d %B %Y, %H:%M")}', sub_style))
    story.append(HRFlowable(width='100%', thickness=2, color=accent, spaceAfter=14))

    # --- Risk Banner ---
    risk_level = result.get('risk_level', 'Unknown')
    probability = result.get('probability', 0)
    rl_color = risk_color.get(risk_level, colors.black)

    banner_data = [[
        Paragraph(f'<b>Risk Level: {risk_level.upper()}</b>', ParagraphStyle(
            'Banner', fontSize=16, textColor=colors.white, alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )),
        Paragraph(f'<b>Probability: {probability}%</b>', ParagraphStyle(
            'BannerSub', fontSize=14, textColor=colors.white, alignment=TA_CENTER
        )),
    ]]
    banner_table = Table(banner_data, colWidths=[9*cm, 8*cm])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), rl_color),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [rl_color]),
        ('BOX', (0,0), (-1,-1), 1, colors.white),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 16))

    # --- Patient Info ---
    section_style = ParagraphStyle('Section', fontSize=13, textColor=dark_blue,
                                   fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=12)
    story.append(Paragraph('Patient Information', section_style))

    info_rows = [
        ['Field', 'Value'],
        ['Age',           str(patient_data.get('Age', '—'))],
        ['Gender',        str(patient_data.get('Gender', '—'))],
        ['BMI',           str(patient_data.get('BMI', '—'))],
        ['Blood Pressure',str(patient_data.get('BloodPressure', '—')) + ' mmHg'],
        ['Glucose',       str(patient_data.get('Glucose', '—')) + ' mg/dL'],
        ['Insulin',       str(patient_data.get('Insulin', '—')) + ' μU/mL'],
        ['Heart Rate',    str(patient_data.get('HeartRate', '—')) + ' bpm'],
        ['Cholesterol',   str(patient_data.get('Cholesterol', '—')) + ' mg/dL'],
        ['Smoking Status',str(patient_data.get('SmokingStatus', '—'))],
        ['Family History',str(patient_data.get('FamilyHistory', '—'))],
        ['Exercise Level',str(patient_data.get('ExerciseLevel', '—'))],
    ]

    info_table = Table(info_rows, colWidths=[8*cm, 9*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), accent),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [light_gray, colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    # --- ML Results ---
    story.append(Paragraph('ML Model Results', section_style))
    ml_rows = [
        ['Metric', 'Value'],
        ['Model Used',       result.get('model_name', '—')],
        ['Prediction',       'At Risk' if result.get('prediction') == 1 else 'No Risk'],
        ['Risk Probability', f"{probability}%"],
        ['Risk Level',       risk_level],
    ]
    ml_table = Table(ml_rows, colWidths=[8*cm, 9*cm])
    ml_table.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0), dark_blue),
        ('TEXTCOLOR',     (0,0), (-1,0), colors.white),
        ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [light_gray, colors.white]),
        ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    story.append(ml_table)
    story.append(Spacer(1, 12))

    # --- Recommendations ---
    recs = result.get('recommendation', {})
    story.append(Paragraph('Health Recommendations', section_style))
    story.append(Paragraph(recs.get('title', ''), ParagraphStyle(
        'RecTitle', fontSize=12, textColor=rl_color, fontName='Helvetica-Bold', spaceAfter=6
    )))

    tip_style = ParagraphStyle('Tip', fontSize=10, leftIndent=12, spaceAfter=4)
    for tip in recs.get('tips', []):
        story.append(Paragraph(f'• {tip}', tip_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f"<b>Action Required:</b> {recs.get('action', '')}",
        ParagraphStyle('Action', fontSize=11, textColor=dark_blue, spaceAfter=6)
    ))

    # --- Footer ---
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#DEE2E6')))
    story.append(Paragraph(
        '<i>This report is generated by an AI/ML system and is NOT a substitute for professional medical advice. '
        'Always consult a qualified healthcare provider for diagnosis and treatment.</i>',
        ParagraphStyle('Disclaimer', fontSize=8, textColor=colors.grey,
                       alignment=TA_CENTER, spaceBefore=8)
    ))

    doc.build(story)
    return filepath


# =============================================================================
# Admin Statistics
# =============================================================================

def get_admin_stats() -> dict:
    conn = get_db()
    total_users       = conn.execute('SELECT COUNT(*) FROM users WHERE role="patient"').fetchone()[0]
    total_predictions = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    high_risk         = conn.execute('SELECT COUNT(*) FROM predictions WHERE risk_level="High"').fetchone()[0]
    low_risk          = conn.execute('SELECT COUNT(*) FROM predictions WHERE risk_level="Low"').fetchone()[0]
    med_risk          = conn.execute('SELECT COUNT(*) FROM predictions WHERE risk_level="Medium"').fetchone()[0]
    conn.close()
    return {
        'total_users':       total_users,
        'total_predictions': total_predictions,
        'high_risk':         high_risk,
        'medium_risk':       med_risk,
        'low_risk':          low_risk,
    }
