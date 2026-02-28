const http = require('http');
const https = require('https');

const TARGET_HOST = 'signal-studio-production.up.railway.app';
const PORT = process.env.PORT || 3001;

const server = http.createServer((req, res) => {
  const options = {
    hostname: TARGET_HOST,
    port: 443,
    path: req.url,
    method: req.method,
    headers: {
      ...req.headers,
      'Host': TARGET_HOST
    }
  };

  const proxyReq = https.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  proxyReq.on('error', (e) => {
    console.error('Proxy error:', e.message);
    res.writeHead(502);
    res.end('Bad gateway');
  });

  req.pipe(proxyReq, { end: true });
});

server.listen(PORT, () => {
  console.log(`Proxy running on port ${PORT} -> https://${TARGET_HOST}`);
});
