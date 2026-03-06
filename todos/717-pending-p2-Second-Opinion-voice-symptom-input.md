# TODO 717: Voice Symptom Input for Second-Opinion

**Repo**: Second-Opinion  
**Priority**: P2  
**Effort**: 6 hours  
**Status**: pending

## Description
Add Web Speech API voice input to the patient intake/chat flow. Users speak symptoms → transcribed → fills PatientChat intake form. Massive accessibility win + differentiator.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/components/PatientChat.tsx:
1. Add a microphone button using Web Speech API (SpeechRecognition)
2. On click: start recognition, show animated mic indicator
3. On result: append transcript to the text input
4. Add fallback message if browser doesn't support (Safari issues)
5. Add types/speech-recognition.d.ts for TypeScript compatibility
6. Style with Tailwind — mic button should be subtle, not intrusive
7. Test: Chrome desktop + Chrome mobile
```

## Acceptance Criteria
- [ ] Mic button appears in PatientChat intake
- [ ] Clicking starts voice recognition
- [ ] Transcript fills input field
- [ ] Works on Chrome desktop and mobile
- [ ] Graceful fallback for unsupported browsers

## Dependencies
- None

## Notes
Web Speech API is free (browser-native). No external service needed for MVP.
