from __future__ import annotations

TM_STRUCTURED_A_HEADERS = [
    "CHEVAL", "MUSIQUE", "CORDE", "POIDS", "ENTRAINEUR", "JOCKEY", "GAINS"
]
TM_STRUCTURED_B_KEYS = [
    "PRONOSTIC DE TURFOMANIA", "LE PRONOSTIC DE TURFOMANIA"
]
TM_STRUCTURED_C_KEYS = [
    "LE SCAN PREMIUM", "SCAN PREMIUM"
]

MAX_HORSE_NUMBER = 60

CSV_COLUMNS = [
    "Reunion","Hippodrome","Course","Nom_Prix","Caracteristiques","Partants","Montant",
    "Turfomania_P","Turfomania_P_Rouges","Turfomania_B","Turfomania_T","Turfomania_Scan","Turfomania_Scan_Rouges",
    "Veinard_JeChoisis","Veinard_Outsiders","Veinard_DM","Veinard_RP",
    "ParisT_JeChoisis","ParisT_Outsiders",
    "Resultat","Non_Partants"
]

DIAG_COLUMNS = ["Reunion","Course","Nom_Prix","Etape","Statut","Detail"]

OCR_DPI = 350
