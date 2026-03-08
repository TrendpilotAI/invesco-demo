'use client';

import { useEffect, useCallback, useState } from 'react';
import { resetDemo, checkResetParam } from '@/lib/demo-reset';

interface ToastState {
  visible: boolean;
  message: string;
}

/** Full-screen confirmation dialog shown before reset */
function ResetConfirmDialog({
  onConfirm,
  onCancel,
}: {
  onConfirm: () => void;
  onCancel: () => void;
}) {
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.55)',
        zIndex: 99999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      onClick={onCancel}
    >
      <div
        onClick={e => e.stopPropagation()}
        style={{
          background: '#fff',
          borderRadius: '12px',
          padding: '32px 36px',
          maxWidth: '420px',
          width: '90%',
          boxShadow: '0 20px 60px rgba(0,0,0,0.25)',
          textAlign: 'center',
          fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        }}
      >
        {/* Invesco-style icon */}
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: '50%',
            background: '#fef3c7',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 20px',
            fontSize: 28,
          }}
        >
          🔄
        </div>

        <h2
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: '#111827',
            margin: '0 0 8px',
          }}
        >
          Reset Demo?
        </h2>
        <p
          style={{
            fontSize: 14,
            color: '#6b7280',
            margin: '0 0 28px',
            lineHeight: '1.5',
          }}
        >
          This will clear all demo state, filters, and selections and return to the home screen.
          Use this before each new presentation.
        </p>

        <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
          <button
            onClick={onCancel}
            style={{
              padding: '10px 24px',
              borderRadius: 8,
              border: '1.5px solid #d1d5db',
              background: '#fff',
              color: '#374151',
              fontSize: 14,
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            style={{
              padding: '10px 24px',
              borderRadius: 8,
              border: 'none',
              background: '#003087', // Invesco navy
              color: '#fff',
              fontSize: 14,
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Reset Demo
          </button>
        </div>

        <p
          style={{
            marginTop: 16,
            fontSize: 11,
            color: '#9ca3af',
          }}
        >
          Shortcut: ⌘⇧R (Mac) · Ctrl+⇧R (Win)
        </p>
      </div>
    </div>
  );
}

/** Toast notification shown briefly after reset (if page doesn't reload) */
function Toast({ toast }: { toast: ToastState }) {
  if (!toast.visible) return null;
  return (
    <div
      style={{
        position: 'fixed',
        bottom: 60,
        left: '50%',
        transform: 'translateX(-50%)',
        background: '#111827',
        color: '#fff',
        padding: '10px 20px',
        borderRadius: 8,
        fontSize: 13,
        fontWeight: 500,
        zIndex: 99998,
        boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
        pointerEvents: 'none',
      }}
    >
      ✓ {toast.message}
    </div>
  );
}

export default function DemoResetOverlay() {
  const [showConfirm, setShowConfirm] = useState(false);
  const [toast, setToast] = useState<ToastState>({ visible: false, message: '' });

  const triggerReset = useCallback(() => {
    setShowConfirm(false);
    setToast({ visible: true, message: 'Demo reset — returning to home screen…' });
    setTimeout(() => {
      resetDemo({ navigateTo: '/' });
    }, 800);
  }, []);

  useEffect(() => {
    // Check ?reset=true on mount
    checkResetParam();

    // Keyboard shortcut: Ctrl+Shift+R or Cmd+Shift+R
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.shiftKey && e.key === 'R' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        setShowConfirm(prev => !prev); // toggle dialog
      }
      // Escape closes dialog
      if (e.key === 'Escape') {
        setShowConfirm(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      {showConfirm && (
        <ResetConfirmDialog
          onConfirm={triggerReset}
          onCancel={() => setShowConfirm(false)}
        />
      )}

      <Toast toast={toast} />

      {/* Subtle floating button */}
      <button
        onClick={() => setShowConfirm(true)}
        title="Reset Demo (⌘⇧R)"
        style={{
          position: 'fixed',
          bottom: '36px',
          right: '12px',
          fontSize: '10px',
          color: '#9ca3af',
          background: 'transparent',
          border: 'none',
          cursor: 'pointer',
          opacity: 0.5,
          zIndex: 10000,
          padding: '4px 6px',
          letterSpacing: '0.02em',
          transition: 'opacity 0.15s',
        }}
        onMouseEnter={e => (e.currentTarget.style.opacity = '1')}
        onMouseLeave={e => (e.currentTarget.style.opacity = '0.5')}
      >
        Reset Demo
      </button>
    </>
  );
}
