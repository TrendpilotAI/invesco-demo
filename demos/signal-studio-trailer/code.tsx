// Signal Studio Trailer - Remotion Code
import { AbsoluteFill, Img, Series, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { interpolate } from 'remotion';

export const Trailer = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const progress = spring({
    frame,
    fps,
    config: { damping: 200 },
  });

  // Scenes
  const scene1 = interpolate(progress, [0, 100], [0, 1], { extrapolateRight: 'clamp' });
  const scene2 = interpolate(progress, [100, 200], [0, 1], { extrapolateRight: 'clamp' });
  // ... more scenes

  return (
    <AbsoluteFill style={{ backgroundColor: '#1a1a2e' }}>
      {/* Hook */}
      {scene1 > 0 && (
        <h1 style={{ opacity: scene1, color: '#f7931e' }}>Unlock Real-Time Insights</h1>
      )}
      {/* Features */}
      {/* ... */}
    </AbsoluteFill>
  );
};
