import os
import logging
from typing import List, Dict, Optional
from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Load and validate API Key
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if not SARVAM_API_KEY:
    logger.error("SARVAM_API_KEY environment variable is not set")
    raise ValueError("SARVAM_API_KEY is required but not found in environment variables")

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

def generate_response(query: str, context_docs: List[dict], intent: str, language: str = "en", history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Generates a response using Sarvam AI (Llama-3/Sarvam models) with RAG context and Chat History.
    
    :param query: The current user question.
    :param context_docs: Retrieved documents from Hybrid Search.
    :param intent: The detected intent (e.g., 'search_job').
    :param history: List of previous messages [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    
    # 1. Format the Retrieved Context (simplified)
    grounding_text = "\n".join([d['content'][:200] for d in context_docs[:2]])
    
    # 2. Define the System Persona with language support
    if language == "pa":
        system_instruction = (
            "ਤੁਸੀਂ PGRKAM ਸਮਾਰਟ ਸਹਾਇਕ ਹੋ (ਪੰਜਾਬ ਘਰ ਘਰ ਰੋਜ਼ਗਾਰ)। "
            "ਤੁਹਾਡਾ ਟੀਚਾ ਪੰਜਾਬ ਵਿੱਚ ਨੌਕਰੀਆਂ ਅਤੇ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰਨਾ ਹੈ। "
            "ਜੇ ਤੁਹਾਨੂੰ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ, ਤਾਂ ਸਿੱਧਾ ਕਹੋ 'ਮੈਨੂੰ ਇਸ ਬਾਰੇ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ'। "
            "ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।"
        )
    else:
        system_instruction = (
            "You are the PGRKAM Smart Assistant (Punjab Ghar Ghar Rozgar). "
            "Help users find jobs and government schemes in Punjab. "
            "Give direct answers. If you don't know something, simply say 'I don't have that information'. "
            "Never mention 'context' or 'provided information'. Respond naturally in English."
        )
    
    if intent == "search_job":
        if language == "pa":
            system_instruction += " ਅਰਜ਼ੀ ਦੀ ਆਖਰੀ ਮਿਤੀ, ਯੋਗਤਾ (ਉਮਰ/ਸਿੱਖਿਆ), ਅਤੇ ਤਨਖਾਹ 'ਤੇ ਧਿਆਨ ਦਿਓ।"
        else:
            system_instruction += " Focus on Application Deadlines, Eligibility (Age/Qualification), and Salary."
    elif intent == "scheme_info":
        if language == "pa":
            system_instruction += " ਫਾਇਦੇ ਅਤੇ ਲਾਭਪਾਤਰੀ ਦੇ ਮਾਪਦੰਡ ਸਪੱਸ਼ਟ ਰੂਪ ਵਿੱਚ ਸੂਚੀਬੱਧ ਕਰੋ।"
        else:
            system_instruction += " Clearly list the Benefits and Beneficiary criteria."

    # 3. Simple message structure for Sarvam AI
    final_user_content = f"""
    You are PGRKAM Smart Assistant. Help with jobs and schemes in Punjab.
    
    Available Information:
    {grounding_text}

    Question: {query}
    """
    
    messages = [
        {"role": "user", "content": final_user_content}
    ]

    # 5. Call Sarvam AI API
    try:
        response = client.chat.completions(
            messages=messages,
            temperature=0.1,
            max_tokens=200
        )
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Sarvam AI API Error: {e}")
        if language == "pa":
            return "ਮਾਫ਼ ਕਰਨਾ, ਮੈਂ ਇਸ ਸਮੇਂ ਸਰਵਰ ਕਨੈਕਸ਼ਨ ਦੀ ਸਮੱਸਿਆ ਕਾਰਨ ਜਵਾਬ ਨਹੀਂ ਦੇ ਸਕਦਾ।"
        else:
            return "I apologize, but I am currently unable to generate a response due to a server connection issue."