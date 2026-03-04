# TODO 573 — Voice Provider Abstraction

**Priority:** MEDIUM  
**Repo:** Ultrafone  
**Effort:** 1 day  
**Status:** pending

## Description
Three overlapping TTS implementations: `fish_tts.py`, `elevenlabs_tts.py`, `voice_service.py`. Consolidate behind a `VoiceProvider` ABC.

## Coding Prompt
```python
# backend/services/voice/base.py
from abc import ABC, abstractmethod

class VoiceProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice_id: str) -> bytes: ...
    
    @abstractmethod
    async def list_voices(self) -> list[dict]: ...
    
    @property
    @abstractmethod
    def provider_name(self) -> str: ...

# backend/services/voice/elevenlabs.py — wraps existing elevenlabs_tts.py
# backend/services/voice/fish.py — wraps existing fish_tts.py  
# backend/services/voice/deepgram.py — Deepgram TTS

# backend/services/voice/factory.py
def get_voice_provider(settings) -> VoiceProvider:
    match settings.VOICE_PROVIDER:
        case "elevenlabs": return ElevenLabsProvider(settings.ELEVENLABS_API_KEY)
        case "fish": return FishProvider(settings.FISH_API_KEY)
        case "deepgram": return DeepgramProvider(settings.DEEPGRAM_API_KEY)
        case _: raise ValueError(f"Unknown provider: {settings.VOICE_PROVIDER}")

# Delete: fish_tts.py, elevenlabs_tts.py (after migration)
# Update: voice_service.py to use factory
```

## Acceptance Criteria
- [ ] `VoiceProvider` ABC with synthesize + list_voices
- [ ] All three providers implement the interface
- [ ] Factory function selects provider from settings
- [ ] Old standalone files deleted
- [ ] Unit tests for each provider (mocked)

## Dependencies
None
