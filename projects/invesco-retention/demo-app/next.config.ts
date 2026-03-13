import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
  basePath: '/invesco-demo',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
}

export default nextConfig
