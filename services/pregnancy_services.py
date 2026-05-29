from db.models import PregnancyRecord


def get_user_pregnancy_data(db, user_id, content=None):
    # Fetch user record
    record = (
        db.query(PregnancyRecord)
        .filter(PregnancyRecord.user_id == user_id)
        .first()
    )

    # 2. If no record exists
    if not record:
        return {
            "user_id": user_id,
            "current_week": None,
            "trimester": None,
            "symptoms": [],
            "description": "No pregnancy data available."
        }

    # 3. Build response
    return {
        "user_id": user_id,
        "current_week": record.current_week,
        "trimester": get_trimester(record.current_week),
        "symptoms": get_symptoms(record),
        "description": build_description(record)
    }
    
def get_trimester(week):
    if week <= 12:
        return "First Trimester"
    elif 13 <= week <= 26:
        return "Second Trimester"
    else:
        return "Third Trimester"
    
def build_description(record):
    description = f"User is currently in week {record.current_week} of pregnancy, which is in the {get_trimester(record.current_week)}. "
    symptoms = get_symptoms(record)
    if symptoms:
        description += f"User is experiencing the following symptoms: {', '.join(symptoms)}. "
    else:
        description += "No data available."
    return description


def get_symptoms(record):
    if not record.symptoms:
        return []
    return [
        symptom.strip()
        for symptom in record.symptoms.split(",")
        if symptom.strip()
    ]
