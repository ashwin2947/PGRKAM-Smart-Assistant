# Simple keyword-based intent classifier
from typing import Optional, List, Dict

def predict_intent(text: str, history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Predicts intent using keyword matching with conversation history context.
    """
    text_lower = text.lower()
    
    # Job search keywords
    job_keywords = ["job", "jobs", "employment", "work", "career", "position", "vacancy", "hiring", "recruitment"]
    
    # Scheme keywords  
    scheme_keywords = ["scheme", "program", "benefit", "subsidy", "training", "skill", "course", "rozgar", "yojana"]
    
    # Application keywords (for both jobs and schemes)
    application_keywords = ["apply", "application", "how to apply", "register", "registration", "enroll", "enrollment"]
    
    # Status keywords
    status_keywords = ["status", "applied", "submitted", "pending", "approved", "rejected"]
    
    # Greeting keywords
    greeting_keywords = ["hello", "hi", "hey", "good morning", "good evening", "namaste"]
    
    # Off-topic keywords (things not related to PGRKAM)
    off_topic_keywords = ["weather", "movie", "music", "food", "recipe", "sports", "cricket", "football", 
                         "politics", "news", "entertainment", "joke", "story", "game", "play", "shopping", 
                         "travel", "hotel", "restaurant", "medicine", "doctor", "health", "love", "relationship"]
    
    try:
        # Check for off-topic queries first
        if any(keyword in text_lower for keyword in off_topic_keywords):
            print(f"🧠 Intent: 'off_topic' for input: '{text}'")
            return "off_topic"
        
        # Check for application-related queries (context-sensitive)
        if any(keyword in text_lower for keyword in application_keywords):
            # Check conversation history for context
            recent_context = ""
            if history:
                # Get last 2 assistant messages to understand context
                for msg in history[-4:]:
                    if msg.get('role') == 'assistant' and msg.get('content'):
                        recent_context += msg['content'].lower() + " "
            
            # If recent context or current query mentions schemes/training, classify as scheme application
            scheme_indicators = ["scheme", "program", "training", "skill", "course", "these", "this"]
            if (any(word in recent_context for word in scheme_indicators) or 
                any(word in text_lower for word in scheme_indicators)):
                print(f"🧠 Intent: 'scheme_application' for input: '{text}' (context: schemes/training)")
                return "scheme_application"
            # Otherwise, could be job application
            print(f"🧠 Intent: 'job_application' for input: '{text}'")
            return "job_application"
        
        # Check for scheme queries
        if any(keyword in text_lower for keyword in scheme_keywords):
            print(f"🧠 Intent: 'search_scheme' for input: '{text}'")
            return "search_scheme"
        
        # Check for job-related queries
        if any(keyword in text_lower for keyword in job_keywords):
            print(f"🧠 Intent: 'search_job' for input: '{text}'")
            return "search_job"
            
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