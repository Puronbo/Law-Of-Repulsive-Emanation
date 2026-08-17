const http = require('http');
const https = require('https');
const fs = require('fs');
const { WebSocketServer } = require('ws');

// --- Configuration ---
const PORT = parseInt(process.env.PORT || '8080', 10);
const HOST = process.env.HOST || '0.0.0.0';
const SSL_KEY = process.env.SSL_KEY || '';
const SSL_CERT = process.env.SSL_CERT || '';
const MAX_ROOMS = parseInt(process.env.MAX_ROOMS || '1000', 10);
const ROOM_TTL_MS = parseInt(process.env.ROOM_TTL_MS || '3600000', 10); // 1 hour

// --- Server ---
let server;
if (SSL_KEY && SSL_CERT && fs.existsSync(SSL_KEY) && fs.existsSync(SSL_CERT)) {
  server = https.createServer({
    key: fs.readFileSync(SSL_KEY),
    cert: fs.readFileSync(SSL_CERT),
  }, handler);
  console.log('HTTPS enabled');
} else {
  server = http.createServer(handler);
}

function handler(req, res) {
  const url = req.url.split('?')[0];

  // Health check
  if (url === '/health') {
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    });
    res.end(JSON.stringify({
      status: 'ok',
      rooms: rooms.size,
      connections: connections,
      uptime: Math.floor(process.uptime()),
    }));
    return;
  }

  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end();
    return;
  }

  // Default: status page
  res.writeHead(200, {
    'Content-Type': 'text/plain',
    'Access-Control-Allow-Origin': '*',
  });
  res.end(`Bazaar signaling server\nRooms: ${rooms.size}\nConnections: ${connections}\nUptime: ${Math.floor(process.uptime())}s\n`);
}

// --- WebSocket ---
const wss = new WebSocketServer({ server, perMessageDeflate: false });

const rooms = new Map();
let connections = 0;

function makeId() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let id = '';
  for (let i = 0; i < 6; i++) id += chars[Math.floor(Math.random() * chars.length)];
  return rooms.has(id) ? makeId() : id;
}

wss.on('connection', (ws, req) => {
  connections++;
  const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
  let myRoom = null;
  let isHost = false;

  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch(e) { return; }
    if (ws.readyState !== 1) return;

    if (msg.type === 'create') {
      if (rooms.size >= MAX_ROOMS) {
        ws.send(JSON.stringify({ type: 'error', msg: 'Server full' }));
        return;
      }
      const id = makeId();
      rooms.set(id, { host: ws, guests: [], created: Date.now() });
      myRoom = id;
      isHost = true;
      ws.send(JSON.stringify({ type: 'created', roomId: id }));

    } else if (msg.type === 'join') {
      const room = rooms.get(msg.roomId);
      if (!room) {
        ws.send(JSON.stringify({ type: 'error', msg: 'Room not found' }));
        return;
      }
      myRoom = msg.roomId;
      room.guests.push(ws);
      ws.send(JSON.stringify({ type: 'joined', roomId: msg.roomId }));
      if (room.host && room.host.readyState === 1) {
        room.host.send(JSON.stringify({ type: 'peerJoined' }));
      }

    } else if (msg.type === 'offer') {
      const room = rooms.get(msg.roomId);
      if (room && room.host && room.host.readyState === 1) {
        room.host.send(JSON.stringify({ type: 'offer', sdp: msg.sdp, roomId: msg.roomId }));
      }

    } else if (msg.type === 'answer') {
      const room = rooms.get(msg.roomId);
      if (room) {
        for (const g of room.guests) {
          if (g.readyState === 1 && g !== ws) {
            g.send(JSON.stringify({ type: 'answer', sdp: msg.sdp }));
          }
        }
        if (room.host && room.host.readyState === 1 && room.host !== ws) {
          room.host.send(JSON.stringify({ type: 'answer', sdp: msg.sdp }));
        }
      }
    }
  });

  ws.on('close', () => {
    connections--;
    if (isHost && myRoom) {
      const room = rooms.get(myRoom);
      if (room) {
        for (const g of room.guests) {
          if (g.readyState === 1) g.close();
        }
        rooms.delete(myRoom);
      }
    } else if (myRoom) {
      const room = rooms.get(myRoom);
      if (room) {
        room.guests = room.guests.filter(g => g !== ws);
        if (room.guests.length === 0 && room.host.readyState !== 1) {
          rooms.delete(myRoom);
        }
      }
    }
  });

  ws.on('error', () => {});
});

// --- Cleanup stale rooms ---
setInterval(() => {
  const now = Date.now();
  for (const [id, room] of rooms) {
    if (now - room.created > ROOM_TTL_MS) {
      for (const g of room.guests) { if (g.readyState === 1) g.close(); }
      if (room.host && room.host.readyState === 1) room.host.close();
      rooms.delete(id);
    }
  }
}, 60000);

// --- Start ---
server.listen(PORT, HOST, () => {
  const proto = SSL_KEY ? 'wss' : 'ws';
  console.log(`Bazaar signaling: ${proto}://${HOST}:${PORT}`);
  console.log(`Health: http://${HOST}:${PORT}/health`);
  console.log(`Max rooms: ${MAX_ROOMS}, TTL: ${ROOM_TTL_MS/1000}s`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down...');
  wss.clients.forEach(ws => ws.close());
  server.close(() => process.exit(0));
});
