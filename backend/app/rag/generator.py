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
    
    # 1. Format the Retrieved Context (expanded for better context)
    grounding_text = "\n".join([d['content'][:300] for d in context_docs[:3]])
    
    # 2. Define the System Persona with language support
    if language == "pa":
        system_instruction = (
            "ਤੁਸੀਂ PGRKAM ਸਮਾਰਟ ਸਹਾਇਕ ਹੋ (ਪੰਜਾਬ ਘਰ ਘਰ ਰੋਜ਼ਗਾਰ)। "
            "ਤੁਹਾਡਾ ਟੀਚਾ ਪੰਜਾਬ ਵਿੱਚ ਨੌਕਰੀਆਂ ਅਤੇ ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਲੱਭਣ ਵਿੱਚ ਮਦਦ ਕਰਨਾ ਹੈ। "
            "ਪਿਛਲੀ ਗੱਲਬਾਤ ਨੂੰ ਯਾਦ ਰੱਖੋ ਅਤੇ ਸੰਦਰਭ ਅਨੁਸਾਰ ਜਵਾਬ ਦਿਓ। "
            "ਜੇ ਤੁਹਾਨੂੰ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ, ਤਾਂ ਸਿੱਧਾ ਕਹੋ 'ਮੈਨੂੰ ਇਸ ਬਾਰੇ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ'। "
            "ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ। ਸਾਦਾ ਟੈਕਸਟ ਵਰਤੋ, ਕੋਈ ਮਾਰਕਡਾਊਨ ਨਹੀਂ।"
        )
    else:
        system_instruction = (
            "You are the PGRKAM Smart Assistant (Punjab Ghar Ghar Rozgar). "
            "Help users find jobs and government schemes in Punjab. "
            "Remember previous conversation context and provide relevant follow-up responses. "
            "Give direct answers. If you don't know something, simply say 'I don't have that information'. "
            "Never mention 'context' or 'provided information'. Respond naturally in English. "
            "Use plain text only, no markdown formatting like ### or ** or quotes."
        )
    
    # Handle greetings and off-topic queries early
    if intent == "general_query":
        if language == "pa":
            return "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ PGRKAM ਸਮਾਰਟ ਸਹਾਇਕ ਹਾਂ। ਮੈਂ ਤੁਹਾਨੂੰ ਪੰਜਾਬ ਵਿੱਚ ਨੌਕਰੀਆਂ, ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਅਤੇ ਹੁਨਰ ਵਿਕਾਸ ਪ੍ਰੋਗਰਾਮਾਂ ਬਾਰੇ ਜਾਣਕਾਰੀ ਦੇ ਸਕਦਾ ਹਾਂ। ਤੁਸੀਂ ਕੀ ਜਾਣਨਾ ਚਾਹੁੰਦੇ ਹੋ?"
        else:
            return "Hello! I'm the PGRKAM Smart Assistant. I can help you find government and private jobs, skill development programs, and employment schemes in Punjab. What would you like to know about?"
    
    if intent == "off_topic":
        if language == "pa":
            return "ਮਾਫ਼ ਕਰਨਾ, ਮੈਂ ਸਿਰਫ ਪੰਜਾਬ ਵਿੱਚ ਨੌਕਰੀਆਂ, ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ ਅਤੇ ਹੁਨਰ ਵਿਕਾਸ ਬਾਰੇ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ। ਕਿਰਪਾ ਕਰਕੇ ਮੈਨੂੰ ਰੋਜ਼ਗਾਰ ਸੰਬੰਧੀ ਸਵਾਲ ਪੁੱਛੋ।"
        else:
            return "I'm sorry, I can only help with employment opportunities, government schemes, and skill development programs in Punjab. Please ask me about jobs, training, or career-related queries."
    
    if intent == "search_job":
        if language == "pa":
            system_instruction += " ਅਰਜ਼ੀ ਦੀ ਆਖਰੀ ਮਿਤੀ, ਯੋਗਤਾ (ਉਮਰ/ਸਿੱਖਿਆ), ਅਤੇ ਤਨਖਾਹ 'ਤੇ ਧਿਆਨ ਦਿਓ।"
        else:
            system_instruction += " Focus on Application Deadlines, Eligibility (Age/Qualification), and Salary."
    elif intent == "search_scheme":
        if language == "pa":
            system_instruction += " ਫਾਇਦੇ ਅਤੇ ਲਾਭਪਾਤਰੀ ਦੇ ਮਾਪਦੰਡ ਸਪੱਸ਼ਟ ਰੂਪ ਵਿੱਚ ਸੂਚੀਬੱਧ ਕਰੋ।"
        else:
            system_instruction += " Clearly list the Benefits and Beneficiary criteria."
    elif intent == "scheme_application":
        if language == "pa":
            system_instruction += " ਯੋਜਨਾ ਲਈ ਅਰਜ਼ੀ ਦੇਣ ਦੇ ਤਰੀਕੇ, ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ ਅਤੇ ਅਰਜ਼ੀ ਦੀ ਪ੍ਰਕਿਰਿਆ ਬਾਰੇ ਜਾਣਕਾਰੀ ਦਿਓ।"
        else:
            system_instruction += " Provide information about how to apply for schemes, required documents, and application process."
    elif intent == "job_application":
        if language == "pa":
            system_instruction += " ਨੌਕਰੀ ਲਈ ਅਰਜ਼ੀ ਦੇਣ ਦੇ ਤਰੀਕੇ, ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ ਅਤੇ ਅਰਜ਼ੀ ਦੀ ਪ੍ਰਕਿਰਿਆ ਬਾਰੇ ਜਾਣਕਾਰੀ ਦਿਓ।"
        else:
            system_instruction += " Provide information about how to apply for jobs, required documents, and application process."

    # 3. Handle simple queries early (skip AI call for efficiency)
    if intent in ["off_topic", "general_query"]:
        # Return early without calling Sarvam AI
        pass  # Response already returned above
    
    # 4. Create simple alternating conversation for Sarvam AI
    messages = []
    
    # Start with system instruction as first user message
    messages.append({"role": "user", "content": system_instruction})
    messages.append({"role": "assistant", "content": "I understand. I'm ready to help with PGRKAM services."})
    
    # Add recent conversation history with proper alternation
    if history and len(history) > 0:
        # Get last few messages and ensure alternation
        recent_history = history[-4:]  # Last 4 messages only
        for i, msg in enumerate(recent_history):
            if msg.get('role') in ['user', 'assistant'] and msg.get('content'):
                # Ensure alternation by checking expected role
                expected_role = 'user' if len(messages) % 2 == 0 else 'assistant'
                if msg['role'] == expected_role:
                    messages.append({
                        "role": msg['role'],
                        "content": msg['content'][:150]  # Truncate for token limit
                    })
    
    # Add current query as final user message
    current_query = f"""Available Information:
{grounding_text}

Current Question: {query}"""
    
    # Ensure we end with user message
    if messages[-1]['role'] == 'user':
        messages.append({"role": "assistant", "content": "I'm ready to help."})
    
    messages.append({"role": "user", "content": current_query})

    # 4. Call Sarvam AI API with increased token limit
    try:
        response = client.chat.completions(
            messages=messages,
            temperature=0.1,
            max_tokens=400  # Increased to prevent response breaking
        )
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Sarvam AI API Error: {e}")
        if language == "pa":
            return "ਮਾਫ਼ ਕਰਨਾ, ਮੈਂ ਇਸ ਸਮੇਂ ਸਰਵਰ ਕਨੈਕਸ਼ਨ ਦੀ ਸਮੱਸਿਆ ਕਾਰਨ ਜਵਾਬ ਨਹੀਂ ਦੇ ਸਕਦਾ।"
        else:
            return "I apologize, but I am currently unable to generate a response due to a server connection issue."