# TODO 420: Consolidate Voice Providers into Abstraction

**Repo:** Ultrafone  
**Priority:** Medium  
**Effort:** S (3-4 hours)  
**Dependencies:** None

## Description
Three TTS implementations exist: `fish_tts.py`, `elevenlabs_tts.py`, and `voice_service.py`. This creates DRY violations and makes it hard to switch providers. Create a unified `VoiceProvider` abstract interface.

## Coding Prompt
```
1. Create services/voice/base.py:
   class VoiceProvider(ABC):
     @abstractmethod
     async def synthesize(self, text: str, voice_id: str) -> bytes: ...
     @abstractmethod
     async def list_voices(self) -> list[Voice]: ...
     @abstractmethod  
     async def clone_voice(self, name: str, samples: list[bytes]) -> str: ...

2. Create services/voice/fish_provider.py - wrap fish_tts.py
3. Create services/voice/elevenlabs_provider.py - wrap elevenlabs_tts.py  
4. Create services/voice/deepgram_provider.py - Deepgram TTS
5. Create services/voice/factory.py:
   def get_voice_provider(settings) -> VoiceProvider based on VOICE_PROVIDER env var

6. Update receptionist.py, agent_service.py to use factory
7. Delete old fish_tts.py, elevenlabs_tts.py (keep voice_service.py as facade)
8. Add VOICE_PROVIDER=fish|elevenlabs|deepgram to .env.example
```

## Acceptance Criteria
- Single interface for all TTS providers
- Switch providers via env var with no code changes
- All existing functionality preserved
- Dead code removed
