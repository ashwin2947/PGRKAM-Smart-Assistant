# backend/app/nlu/entity_extractor.py
import re
from typing import List, Dict

# Fast rule-based entity extraction
def extract_entities_fast(text: str) -> List[Dict[str, str]]:
    """
    Fast rule-based entity extraction using regex patterns.
    """
    text_lower = text.lower()
    entities = []
    
    # Punjab cities
    cities = ["ludhiana", "amritsar", "jalandhar", "patiala", "bathinda", "mohali", "chandigarh", 
              "ferozepur", "hoshiarpur", "moga", "pathankot", "sangrur", "fazilka"]
    
    # Job roles
    job_roles = ["engineer", "teacher", "doctor", "nurse", "clerk", "officer", "manager", 
                "driver", "mechanic", "electrician", "plumber", "accountant", "programmer"]
    
    # Qualifications
    qualifications = ["b.tech", "btech", "mba", "bca", "mca", "ba", "bsc", "ma", "msc", 
                     "12th", "10th", "graduate", "diploma", "phd"]
    
    # Extract cities
    for city in cities:
        if city in text_lower:
            entities.append({"text": city.title(), "label": "city"})
    
    # Extract job roles
    for role in job_roles:
        if role in text_lower:
            entities.append({"text": role.title(), "label": "job_role"})
    
    # Extract qualifications
    for qual in qualifications:
        if qual in text_lower:
            entities.append({"text": qual.upper(), "label": "qualification"})
    
    # Extract age using regex
    age_pattern = r'\b(\d{1,2})\s*(?:years?|yrs?)\b'
    age_matches = re.findall(age_pattern, text_lower)
    for age in age_matches:
        if 18 <= int(age) <= 65:
            entities.append({"text": age, "label": "age"})
    
    return entities

# Fallback to GLiNER for complex cases (optional)
try:
    from gliner import GLiNER
    model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
    LABELS = ["job_role", "city", "scheme_name", "age_limit", "qualification"]
    
    def extract_entities_gliner(text: str):
        entities = model.predict_entities(text, LABELS)
    
except ImportError:
    def extract_entities_gliner(text: str):
        return []

def extract_entities(text: str, use_fast=True) -> List[Dict[str, str]]:
    """
    Main entity extraction function with fast/accurate modes.
    """
    if use_fast:
        return extract_entities_fast(text)
    else:
        return extract_entities_gliner(text)