# Simple keyword-based intent classifier

def predict_intent(text: str) -> str:
    """
    Predicts intent using keyword matching for reliability.
    """
    text_lower = text.lower()
    
    # Job search keywords
    job_keywords = ["job", "jobs", "employment", "work", "career", "position", "vacancy", "hiring", "recruitment", "show", "find", "search"]
    
    # Scheme keywords  
    scheme_keywords = ["scheme", "program", "benefit", "subsidy", "training", "skill", "course", "rozgar"]
    
    # Status keywords
    status_keywords = ["status", "application", "applied", "submitted", "pending", "approved", "rejected"]
    
    # Greeting keywords
    greeting_keywords = ["hello", "hi", "hey", "good morning", "good evening", "namaste"]
    
    try:
        # Check for job-related queries first
        if any(keyword in text_lower for keyword in job_keywords):
            print(f"🧠 Intent: 'search_job' for input: '{text}'")
            return "search_job"
        
        # Check for scheme queries
        if any(keyword in text_lower for keyword in scheme_keywords):
            print(f"🧠 Intent: 'search_scheme' for input: '{text}'")
            return "search_scheme"
            
        # Check for status queries
        if any(keyword in text_lower for keyword in status_keywords):
            print(f"🧠 Intent: 'check_status' for input: '{text}'")
            return "check_status"
            
        # Check for greetings
        if any(keyword in text_lower for keyword in greeting_keywords):
            print(f"🧠 Intent: 'general_query' for input: '{text}'")
            return "general_query"
        
        # Default to general query
        print(f"🧠 Intent: 'general_query' (default) for input: '{text}'")
        return "general_query"
        
    except Exception as e:
        print(f"⚠️ NLU Error: {e}")
        return "general_query"