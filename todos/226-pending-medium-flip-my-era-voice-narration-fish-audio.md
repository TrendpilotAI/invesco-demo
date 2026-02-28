## Task: Voice Narration via Fish Audio TTS
## Priority: medium
## Effort: 8 hours
## Description:
Add voice narration to FlipMyEra stories using Fish Audio TTS API. When a story/ebook is generated, offer users a "Listen" button that streams audio narration. This adds premium value and differentiates from competitors. Nathan has a Fish Audio API key available.

## Coding Prompt:
You are implementing voice narration for FlipMyEra at /data/workspace/projects/flip-my-era/.

Fish Audio API key: 3b27c316ae734415b81e72db715cce61
API endpoint: POST https://api.fish.audio/v1/tts
Recommended voice: `b545c585f631496c914815291da4e893` (Friendly Women - warm female)
Format: mp3

Steps:
1. Create a new Supabase Edge Function at supabase/functions/text-to-speech/ (already exists - check and extend it)
   - Accept `{ text: string, voice_id?: string }` 
   - Call Fish Audio TTS API with Authorization: Bearer 3b27c316ae734415b81e72db715cce61
   - Stream the MP3 response back to client
   - Limit text to 5000 chars max per request (cost control)

2. Create React hook `src/modules/story/hooks/useVoiceNarration.ts`:
   - `useVoiceNarration(storyText: string)` 
   - Returns: `{ isLoading, isPlaying, play, pause, stop, audioUrl }`
   - Uses HTML5 Audio API for playback
   - Cache audio URL in state to avoid re-fetching

3. Create component `src/modules/story/components/VoiceNarrationPlayer.tsx`:
   - Play/Pause/Stop buttons with loading state
   - Progress bar
   - Voice selector (optional: let user pick from 3 voices)
   - Gate behind Premium feature flag

4. Wire into ebook/story view page - add narration button next to download

5. Cost control: 1 narration = ~1 credit deducted from user account

## Acceptance Criteria:
- [ ] Edge function returns MP3 audio for given text
- [ ] Play button appears on story view page (behind premium_features flag)
- [ ] Audio plays, pauses, stops correctly
- [ ] Loading state shown while generating
- [ ] Error handling if API fails
- [ ] Credit deduction on use

## Dependencies: 016-pending-P1-flip-my-era-move-secrets-to-edge-functions.md
