"""
Configuration and environment validation.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # LLM Settings
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.TAVILY_API_KEY:
            errors.append("TAVILY_API_KEY not set in .env file")
        
        if errors:
            raise ValueError(
                "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            )
    
    @classmethod
    def check_ollama(cls):
        """Check if Ollama is running"""
        try:
            import ollama
            # Try to list models
            ollama.list()
            return True
        except Exception:
            return False


def validate_environment():
    """
    Validate environment before running agent.
    Raises helpful errors if something is missing.
    """
    print("🔍 Validating environment...")
    
    # Check config
    try:
        Config.validate()
        print("   ✅ Environment variables OK")
    except ValueError as e:
        print(f"\n❌ Configuration Error:\n{e}\n")
        print("Please create a .env file with required keys.")
        print("See .env.example for template.\n")
        raise
    
    # Check Ollama
    if not Config.check_ollama():
        print("\n❌ Ollama Error:")
        print("   Ollama is not running or Mistral is not installed\n")
        print("Please run:")
        print("   ollama pull mistral")
        print("   ollama serve  (if not running)\n")
        raise RuntimeError("Ollama not available")
    
    print("   ✅ Ollama is running")
    print("   ✅ All checks passed!\n")