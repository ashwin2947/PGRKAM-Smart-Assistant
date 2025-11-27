# backend/app/nlu/entity_extractor.py
from gliner import GLiNER

# Load model once when server starts (lightweight model)
model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")

LABELS = ["job_role", "city", "scheme_name", "age_limit", "qualification"]

def extract_entities(text: str):
    """
    Extracts structured data from text using GLiNER.
    Input: "I want a plumber job in Ludhiana"
    Output: [{'text': 'plumber', 'label': 'job_role'}, {'text': 'Ludhiana', 'label': 'city'}]
    """
    entities = model.predict_entities(text, LABELS)
    return [{"text": e["text"], "label": e["label"]} for e in entities]