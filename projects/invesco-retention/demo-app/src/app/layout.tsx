import './globals.css'
import DemoResetOverlay from '@/components/DemoResetOverlay'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <title>Signal Studio — Invesco</title>
        <meta name="description" content="AI-powered intelligence for Invesco wholesalers" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body
        className="antialiased"
        style={{
          fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
          paddingBottom: '32px',
        }}
      >
        {children}
        <DemoResetOverlay />
        <div
          style={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            right: 0,
            backgroundColor: '#f3f4f6',
            borderTop: '1px solid #e5e7eb',
            padding: '6px 16px',
            textAlign: 'center',
            fontSize: '11px',
            color: '#9ca3af',
            zIndex: 9999,
          }}
        >
          Demo data is synthetic — all advisors, AUM figures, and fund data are fictional for demonstration purposes only.
        </div>
      </body>
    </html>
  )
}
