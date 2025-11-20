/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Allow body parser for API routes to handle JSON
  api: {
    bodyParser: {
      sizeLimit: '1mb',
    },
  },
}

module.exports = nextConfig
