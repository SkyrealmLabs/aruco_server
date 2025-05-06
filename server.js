const express = require('express');
const http = require('http');

const app = express();
const port = 5006;

app.use(express.json());

app.post('/detect-aruco', (req, res) => {
  const { image } = req.body;

  if (!image) {
    return res.status(400).json({ error: 'Image data is required' });
  }

  const postData = JSON.stringify({ image });

  const options = {
    hostname: '0.0.0.0',
    port: 5001,
    path: '/detect',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    },
  };

  const request = http.request(options, (response) => {
    let data = '';

    response.on('data', (chunk) => {
      data += chunk;
    });

    response.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        res.status(response.statusCode).json(parsed);
      } catch (e) {
        res.status(500).json({ error: 'Failed to parse response from Python API' });
      }
    });
  });

  request.on('error', (e) => {
    console.error(`Request error: ${e.message}`);
    res.status(500).json({ error: 'Could not connect to detection server' });
  });

  request.write(postData);
  request.end();
});

app.listen(port, () => {
  console.log(`Node.js server running at http://localhost:${port}`);
});
