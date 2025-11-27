import React, { useEffect, useRef, useState, useCallback } from "react";
import type { ReactNode } from "react";

import {
  Bot,
  User,
  Mic,
  Square,
  Send,
  RotateCcw,
  Loader2,
  Languages,
  AlertCircle,
} from "lucide-react";

// Type definitions for translation structure
type LanguageCode = "en" | "pa";

interface TranslationStrings {
  title: string;
  subtitle: string;
  reset: string;
  speak: string;
  stop: string;
  send: string;
  thinking: string;
  placeholder: string;
  tip: string;
  example1: string;
  example2: string;
  example3: string;
  voiceError: string;
  micError: string;
  greeting: string;
}

const translations: Record<LanguageCode, TranslationStrings> = {
  en: {
    title: "PGRKAM Assistant",
    subtitle: "Employment & Skill Development",
    reset: "Reset",
    speak: "Speak",
    stop: "Stop",
    send: "Send",
    thinking: "Searching...",
    placeholder: "Ask about jobs, training, or schemes...",
    tip: "💡 Examples:",
    example1: "Government jobs in Punjab",
    example2: "Skill development courses",
    example3: "Self-employment schemes",
    voiceError: "🎤 Voice input requires Chrome browser",
    micError: "⚠️ Microphone error:",
    greeting:
      "Welcome to PGRKAM! 🙏\n\nI can help you with:\n• Government & Private Job Listings\n• Skill Development Programs\n• Self-Employment Schemes\n• Job Fair Information\n• Career Counseling\n\nHow can I assist you today?",
  },
  pa: {
    title: "PGRKAM ਸਹਾਇਕ",
    subtitle: "ਰੋਜ਼ਗਾਰ ਅਤੇ ਹੁਨਰ ਵਿਕਾਸ",
    reset: "ਰੀਸੈੱਟ",
    speak: "ਬੋਲੋ",
    stop: "ਰੁਕੋ",
    send: "ਭੇਜੋ",
    thinking: "ਖੋਜ ਰਿਹਾ ਹੈ...",
    placeholder: "ਨੌਕਰੀਆਂ, ਸਿਖਲਾਈ ਜਾਂ ਯੋਜਨਾਵਾਂ ਬਾਰੇ ਪੁੱਛੋ...",
    tip: "💡 ਉਦਾਹਰਣਾਂ:",
    example1: "ਪੰਜਾਬ ਵਿੱਚ ਸਰਕਾਰੀ ਨੌਕਰੀਆਂ",
    example2: "ਹੁਨਰ ਵਿਕਾਸ ਕੋਰਸ",
    example3: "ਸਵੈ-ਰੁਜ਼ਗਾਰ ਯੋਜਨਾਵਾਂ",
    voiceError: "🎤 ਵੌਇਸ ਇਨਪੁਟ ਲਈ ਕ੍ਰੋਮ ਬ੍ਰਾਊਜ਼ਰ ਦੀ ਲੋੜ ਹੈ",
    micError: "⚠️ ਮਾਈਕ੍ਰੋਫੋਨ ਗਲਤੀ:",
    greeting:
      "ਪੀ.ਜੀ.ਆਰ.ਕੇ.ਏ.ਐਮ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ! 🙏\n\nਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ:\n• ਸਰਕਾਰੀ ਅਤੇ ਪ੍ਰਾਈਵੇਟ ਨੌਕਰੀਆਂ\n• ਹੁਨਰ ਵਿਕਾਸ ਪ੍ਰੋਗਰਾਮ\n• ਸਵੈ-ਰੁਜ਼ਗਾਰ ਯੋਜਨਾਵਾਂ\n• ਰੋਜ਼ਗਾਰ ਮੇਲੇ ਦੀ ਜਾਣਕਾਰੀ\n• ਕੈਰੀਅਰ ਸਲਾਹ\n\nਮੈਂ ਅੱਜ ਤੁਹਾਡੀ ਕਿਵੇਂ ਸਹਾਇਤਾ ਕਰ ਸਕਦਾ ਹਾਂ?",
  },
};

// Props types for TitleBar
interface TitleBarProps {
  onReset: () => void;
  language: LanguageCode;
  setLanguage: (lang: LanguageCode) => void;
  t: TranslationStrings;
}

function TitleBar({ onReset, language, setLanguage, t }: TitleBarProps) {
  return (
    <div className="flex items-center justify-between px-6 py-4 border-b border-orange-200/20 bg-gradient-to-r from-orange-50/5 to-amber-50/5">
      <div className="flex items-center gap-3">
        <div className="h-12 w-12 rounded-lg grid place-items-center bg-gradient-to-br from-orange-500 to-amber-600 shadow-lg">
          <Bot className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="text-base font-bold text-orange-900">{t.title}</div>
          <div className="text-xs text-orange-700/80">{t.subtitle}</div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {/* Language Toggle */}
        <button
          onClick={() => setLanguage(language === "en" ? "pa" : "en")}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium border-2 border-orange-500/30 text-orange-700 hover:bg-orange-50 hover:border-orange-500/50 transition-all"
        >
          <Languages className="w-4 h-4" />
          <span className="font-semibold">
            {language === "en" ? "ਪੰਜਾਬੀ" : "English"}
          </span>
        </button>

        <button
          onClick={onReset}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium border-2 border-orange-500/30 text-orange-700 hover:bg-orange-50 hover:border-orange-500/50 transition-all"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          {t.reset}
        </button>
      </div>
    </div>
  );
}

interface BubbleProps {
  role: "assistant" | "user";
  children: ReactNode;
  isNew?: boolean;
}

function Bubble({ role, children, isNew }: BubbleProps) {
  const isAssistant = role === "assistant";
  return (
    <div
      className={`flex items-start gap-3 max-w-[85%] ${
        isNew ? "animate-fadeIn" : ""
      }`}
    >
      {isAssistant && (
        <div className="flex-shrink-0 w-9 h-9 rounded-full bg-gradient-to-br from-orange-500 to-amber-600 grid place-items-center shadow-md border-2 border-orange-300/50">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      <div
        className={`flex-1 rounded-2xl px-5 py-3.5 shadow-sm ${
          isAssistant
            ? "bg-white border-2 border-orange-200/40 text-gray-800"
            : "bg-gradient-to-br from-orange-500 to-amber-600 text-white ml-auto border-2 border-orange-400/30"
        }`}
      >
        <div className="text-[15px] leading-relaxed whitespace-pre-wrap">
          {children}
        </div>
      </div>

      {!isAssistant && (
        <div className="flex-shrink-0 w-9 h-9 rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 grid place-items-center shadow-md border-2 border-blue-400/50">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
}

function useSpeechRecognition(language: LanguageCode) {
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const [supported, setSupported] = useState<boolean>(false);
  const [listening, setListening] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const R =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;
    if (!R) {
      setSupported(false);
      return;
    }
    const rec: SpeechRecognition = new R();
    rec.lang = language === "pa" ? "pa-IN" : "en-IN";
    rec.interimResults = true;
    rec.maxAlternatives = 1;
    recognitionRef.current = rec;
    setSupported(true);
  }, [language]);

  const start = ({
    onResult,
    onEnd,
  }: {
    onResult?: (text: string, isFinal: boolean) => void;
    onEnd?: () => void;
  } = {}) => {
    const rec = recognitionRef.current;
    if (!rec) return;
    setError(null);

    try {
      let interimTranscript = "";
      rec.onresult = (e: SpeechRecognitionEvent) => {
        const res = e.results[e.results.length - 1];
        interimTranscript = res[0].transcript;
        onResult && onResult(interimTranscript, res.isFinal);
      };
      rec.onerror = (e: SpeechRecognitionErrorEvent) => {
        setError(e.error || "speech-error");
        setListening(false);
      };
      rec.onend = () => {
        setListening(false);
        onEnd && onEnd();
      };
      rec.start();
      setListening(true);
    } catch (err: any) {
      setError(err?.message ?? "Unable to start mic");
      setListening(false);
    }
  };

  const stop = () => {
    const rec = recognitionRef.current;
    if (rec) {
      try {
        rec.stop();
      } catch (e) {
        // Ignore errors when stopping
      }
    }
  };

  return { supported, listening, start, stop, error };
}

interface Message {
  role: "assistant" | "user";
  content: string;
  timestamp?: string;
  meta?: Record<string, any>;
  response_id?: string;
}

interface ApiResponse {
  text: string;
  session_id: string;
  response_id: string;
  original_language: string;
  meta?: Record<string, any>;
  timestamp: string;
}

interface ErrorState {
  hasError: boolean;
  message: string;
  type: 'network' | 'server' | 'validation' | null;
}

export default function PGRKAMChatbot() {
  const [language, setLanguage] = useState<LanguageCode>("en");
  const [value, setValue] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<ErrorState>({ hasError: false, message: "", type: null });
  const [sessionId, setSessionId] = useState<string>("");
  
  const { supported, listening, start, stop, error: speechError } =
    useSpeechRecognition(language);

  const t = translations[language];

  // Initialize with greeting in current language and store language preference
  useEffect(() => {
    setMessages([{ role: "assistant", content: t.greeting }]);
    // Store language preference in session storage
    sessionStorage.setItem('pgrkam_language', language);
  }, [language]);

  // Load language preference on component mount
  useEffect(() => {
    const savedLanguage = sessionStorage.getItem('pgrkam_language') as LanguageCode;
    if (savedLanguage && savedLanguage !== language) {
      setLanguage(savedLanguage);
    }
  }, []);

  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const onSend = useCallback(async () => {
    const text = value.trim();
    if (!text || loading) return;
    
    // Clear any previous errors
    setError({ hasError: false, message: "", type: null });
    
    // Add user message
    const userMessage: Message = {
      role: "user",
      content: text,
      timestamp: new Date().toISOString()
    };
    setMessages((m) => [...m, userMessage]);
    setValue("");
    setLoading(true);

    try {
      const requestBody = {
        message: text,
        language: language,
        session_id: sessionId || sessionStorage.getItem('pgrkam_session_id') || undefined,
        history: messages.slice(-4).map(m => ({
          role: m.role === "assistant" ? "assistant" : "user",
          content: m.content
        }))
      };
      
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }
      
      const data: ApiResponse = await response.json();

      // Store session ID for continuity
      if (data.session_id) {
        setSessionId(data.session_id);
        sessionStorage.setItem('pgrkam_session_id', data.session_id);
      }
      
      // Update language if backend detected a different preference
      if (data.meta?.preferred_language && data.meta.preferred_language !== language) {
        setLanguage(data.meta.preferred_language as LanguageCode);
        sessionStorage.setItem('pgrkam_language', data.meta.preferred_language);
      }
      
      // Add assistant response
      const assistantMessage: Message = {
        role: "assistant",
        content: data.text || "No response received",
        timestamp: data.timestamp,
        meta: data.meta,
        response_id: data.response_id
      };
      setMessages((m) => [...m, assistantMessage]);
    } catch (err: any) {
      console.error('Chat error:', err);
      
      // Determine error type
      let errorType: ErrorState['type'] = 'server';
      let errorMessage = err.message || 'Unknown error occurred';
      
      if (err.name === 'TypeError' || errorMessage.includes('fetch')) {
        errorType = 'network';
        errorMessage = 'Network connection failed. Please check your internet connection.';
      }
      
      setError({ hasError: true, message: errorMessage, type: errorType });
      
      // Add error message to chat
      const errorMessages = {
        en: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        pa: "ਮਾਫ਼ ਕਰਨਾ, ਮੈਨੂੰ ਹੁਣ ਜੁੜਨ ਵਿੱਚ ਸਮੱਸਿਆ ਹੋ ਰਹੀ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਥੋੜ੍ਹੀ ਦੇਰ ਬਾਅਦ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
        hi: "क्षमा करें, मुझे अभी कनेक्ट करने में समस्या हो रही है। कृपया थोड़ी देर बाद प्रयास करें।"
      };
      
      const errorMessage_localized = errorMessages[language] || errorMessages.en;
      
      setMessages((m) => [...m, {
        role: "assistant",
        content: errorMessage_localized,
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  }, [value, loading, language, sessionId]);

  const onReset = useCallback(() => {
    setMessages([{ role: "assistant", content: t.greeting, timestamp: new Date().toISOString() }]);
    setValue("");
    setError({ hasError: false, message: "", type: null });
    if (listening) stop();
    // Clear session but keep language preference
    setSessionId("");
    sessionStorage.removeItem('pgrkam_session_id');
  }, [t.greeting, listening, stop]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-amber-50 to-yellow-50 flex items-center justify-center p-6">
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(12px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .custom-scroll::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scroll::-webkit-scrollbar-track {
          background: rgba(251, 146, 60, 0.1);
          border-radius: 4px;
        }
        .custom-scroll::-webkit-scrollbar-thumb {
          background: rgba(249, 115, 22, 0.3);
          border-radius: 4px;
        }
        .custom-scroll::-webkit-scrollbar-thumb:hover {
          background: rgba(249, 115, 22, 0.5);
        }
      `}</style>

      <div className="w-full max-w-4xl rounded-2xl border-2 border-orange-300/50 bg-white shadow-2xl overflow-hidden">
        <TitleBar
          onReset={onReset}
          language={language}
          setLanguage={setLanguage}
          t={t}
        />

        <div
          ref={scrollRef}
          className="h-[65vh] p-6 overflow-y-auto custom-scroll space-y-4 bg-gradient-to-b from-orange-50/30 to-white"
        >
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "assistant" ? "justify-start" : "justify-end"
              }`}
            >
              <Bubble
                role={m.role}
                isNew={i === messages.length - 1 && !loading}
              >
                {m.content}
              </Bubble>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="flex items-start gap-3 max-w-[85%]">
                <div className="flex-shrink-0 w-9 h-9 rounded-full bg-gradient-to-br from-orange-500 to-amber-600 grid place-items-center shadow-md border-2 border-orange-300/50">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1 rounded-2xl px-5 py-3.5 bg-white border-2 border-orange-200/40">
                  <div className="flex items-center gap-2 text-orange-700">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-sm font-medium">{t.thinking}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="border-t-3 border-orange-200/40 p-5 bg-gradient-to-r from-orange-50/50 to-amber-50/50">
          <div className="flex items-end gap-3">
            {/* Speak button */}
            <button
              onClick={() => {
                if (listening) {
                  stop();
                  return;
                }
                start({
                  onResult: (text, isFinal) => {
                    setValue(text);
                  },
                });
              }}
              disabled={!supported || loading}
              className={`flex-shrink-0 flex items-center justify-center gap-2 px-4 py-3 rounded-xl text-sm font-semibold transition-all ${
                !supported || loading
                  ? "opacity-40 cursor-not-allowed bg-gray-200 border-2 border-gray-300"
                  : listening
                  ? "bg-orange-100 border-2 border-orange-500 text-orange-700 hover:bg-orange-200 shadow-md"
                  : "bg-white border-2 border-orange-400/50 text-orange-700 hover:bg-orange-50 hover:border-orange-500"
              }`}
            >
              {listening ? (
                <>
                  <Square className="w-4 h-4 fill-current" />
                  <span>{t.stop}</span>
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4" />
                  <span>{t.speak}</span>
                </>
              )}
            </button>

            {/* Input area */}
            <div className="flex-1 relative">
              <input
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    onSend();
                  }
                }}
                placeholder={t.placeholder}
                className="w-full rounded-xl px-5 py-3 pr-14 bg-white border-2 border-orange-300/50 text-gray-800 placeholder-gray-500 focus:outline-none focus:border-orange-500 focus:ring-2 focus:ring-orange-200 transition-all text-[15px] font-medium"
                disabled={loading}
              />
              <button
                onClick={onSend}
                disabled={loading || !value.trim()}
                className="absolute right-1.25 bottom-1.25 h-10 w-10 rounded-lg grid place-items-center transition-all disabled:opacity-40 disabled:cursor-not-allowed bg-gradient-to-br from-orange-500 to-amber-600 hover:shadow-lg hover:scale-105 active:scale-95 border-2 border-orange-400/50"
                aria-label={t.send}
              >
                <Send className="w-4 h-4 text-white" />
              </button>
            </div>
          </div>

          <div className="mt-3 text-center text-xs text-orange-800/80 font-medium">
            {t.tip}{" "}
            <span className="text-orange-700 italic">"{t.example1}"</span>,{" "}
            <span className="text-orange-700 italic">"{t.example2}"</span>,{" "}
            <span className="text-orange-700 italic">"{t.example3}"</span>
          </div>

          {/* Test Query Buttons */}
          <div className="mt-3 flex flex-wrap gap-2 justify-center">
            {[
              "I have B.Tech, show government jobs in Chhattisgarh",
              "Find private jobs for 12th pass in Punjab", 
              "I have MBA, looking for management jobs",
              "Show engineering jobs in Raipur"
            ].map((query, idx) => (
              <button
                key={idx}
                onClick={() => setValue(query)}
                className="px-3 py-1 text-xs bg-orange-100 hover:bg-orange-200 text-orange-700 rounded-full border border-orange-300 transition-colors"
              >
                {query.length > 30 ? query.substring(0, 30) + '...' : query}
              </button>
            ))}
          </div>

          {/* Error Display */}
          {error.hasError && (
            <div className="mt-2 text-xs text-red-700 text-center bg-red-100 border-2 border-red-300 rounded-lg py-2 px-3 font-medium flex items-center justify-center gap-2">
              <AlertCircle className="w-4 h-4" />
              <span>{error.message}</span>
            </div>
          )}
          
          {/* Voice Input Warnings */}
          {!supported && (
            <div className="mt-2 text-xs text-amber-700 text-center bg-amber-100 border-2 border-amber-300 rounded-lg py-2 px-3 font-medium">
              {t.voiceError}
            </div>
          )}
          {speechError && (
            <div className="mt-2 text-xs text-red-700 text-center bg-red-100 border-2 border-red-300 rounded-lg py-2 px-3 font-medium">
              {t.micError} {speechError}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
