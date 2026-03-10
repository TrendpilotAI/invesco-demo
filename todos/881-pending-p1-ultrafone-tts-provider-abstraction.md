# 881 · Consolidate 3 TTS Services into Unified Provider Interface

**Project:** Ultrafone  
**Priority:** P1 (Code Quality)  
**Status:** pending  
**Effort:** 4h  
**Created:** 2026-03-10

---

## Problem

Three separate TTS implementations exist with no unified interface:
- `backend/services/fish_tts.py` — Fish Audio
- `backend/services/elevenlabs_tts.py` — ElevenLabs  
- `backend/services/voice_service.py` — Wraps ElevenLabs directly

`requirements.txt` has duplicate `elevenlabs>=1.0.0` entry.
TTS selection logic is scattered — unclear which service is used at runtime.

## Task

Create `backend/services/tts_provider.py` with abstract provider interface, make all three providers conform to it, remove duplication.

## Implementation

```python
# backend/services/tts_provider.py
from abc import ABC, abstractmethod
from enum import Enum

class TTSEmotion(str, Enum):
    NEUTRAL = "neutral"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"

class TTSProvider(ABC):
    """Abstract TTS provider interface."""
    
    @abstractmethod
    async def synthesize(
        self, 
        text: str, 
        emotion: TTSEmotion = TTSEmotion.NEUTRAL,
        voice_id: str | None = None
    ) -> bytes:
        """Returns raw audio bytes (mulaw 8kHz for Twilio compatibility)."""
        ...
    
    @abstractmethod
    async def list_voices(self) -> list[dict]:
        """Returns available voice options."""
        ...


class FishAudioProvider(TTSProvider):
    """Wraps fish_tts.py logic."""
    ...

class ElevenLabsProvider(TTSProvider):
    """Wraps elevenlabs_tts.py logic."""
    ...


def get_tts_provider(provider_name: str = None) -> TTSProvider:
    """Factory: returns configured TTS provider."""
    name = provider_name or settings.tts_provider  # "fish" | "elevenlabs"
    if name == "fish":
        return FishAudioProvider(api_key=settings.fish_api_key, voice_id=settings.fish_voice_id)
    elif name == "elevenlabs":
        return ElevenLabsProvider(api_key=settings.elevenlabs_api_key)
    raise ValueError(f"Unknown TTS provider: {name}")
```

### Config Addition

```python
# backend/config/settings.py
class Settings(BaseSettings):
    tts_provider: str = "fish"  # "fish" | "elevenlabs"
    fish_api_key: SecretStr = ""
    fish_voice_id: str = ""
    elevenlabs_api_key: SecretStr = ""
```

### Cleanup

```python
# requirements.txt — remove duplicate:
# elevenlabs>=1.0.0  ← remove one
elevenlabs>=1.0.0   # keep one
```

## Acceptance Criteria
- [ ] `TTSProvider` abstract base class created
- [ ] `FishAudioProvider` and `ElevenLabsProvider` conform to interface
- [ ] `voice_service.py` refactored to use provider pattern
- [ ] Config-driven provider selection (`TTS_PROVIDER=fish`)
- [ ] Duplicate `elevenlabs` removed from `requirements.txt`
- [ ] Unit tests: `test_tts_provider.py` tests both providers with mocks
- [ ] `voice_service.py` can be deleted or kept as thin adapter

## Dependencies
- Blocks: Android app TTS, voice persona features
