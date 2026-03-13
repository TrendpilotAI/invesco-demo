'use client'

interface SeparatorProps {
  orientation?: 'horizontal' | 'vertical'
  className?: string
  style?: React.CSSProperties
}

export function Separator({ orientation = 'horizontal', className = '', style }: SeparatorProps) {
  return (
    <div
      role="separator"
      data-orientation={orientation}
      className={className}
      style={{
        background: '#e5e5e5',
        ...(orientation === 'horizontal'
          ? { width: '100%', height: 1 }
          : { width: 1, height: '100%' }),
        ...style,
      }}
    />
  )
}
