const http = require('http');
const { WebSocketServer } = require('ws');

const PORT = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type':'text/plain'});
  res.end('Bazaar signaling server — ' + rooms.size + ' rooms active\n');
});

const wss = new WebSocketServer({ server });

const rooms = new Map();

function makeId() {
  return Math.random().toString(36).slice(2, 8).toUpperCase();
}

wss.on('connection', (ws) => {
  let myRoom = null;
  let isHost = false;

  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch(e) { return; }

    if (msg.type === 'create') {
      const id = makeId();
      rooms.set(id, { host: ws, guests: [] });
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
      }
    }
  });

  ws.on('close', () => {
    if (isHost && myRoom) {
      const room = rooms.get(myRoom);
      if (room) {
        for (const g of room.guests) {
          if (g.readyState === 1) g.close();
        }
        rooms.delete(myRoom);
      }
    }
    if (myRoom && !isHost) {
      const room = rooms.get(myRoom);
      if (room) {
        room.guests = room.guests.filter(g => g !== ws);
      }
    }
  });
});

server.listen(PORT, () => {
  console.log('Bazaar signaling server on ws://localhost:' + PORT);
});
