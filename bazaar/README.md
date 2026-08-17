# Bazaar — Decentralized Social Platform

A peer-to-peer social app. Reddit + 4chan in the browser. No server stores your data.

## Quick Start

### Option 1: Local (no server)
1. Open `index.html` in your browser
2. Click "Create Room" → copy the room code
3. Send the code to a friend → they paste it and send back an answer
4. Connected — no server needed

### Option 2: With signaling server (better UX)
```bash
npm install ws          # one-time
node server.js          # starts on port 8080
```
Open `index.html` on two devices. Click "Create Room" — the relay handles signaling automatically.

### Option 3: Deploy to the internet

#### Step 1: Deploy the relay server
Deploy `server.js` to any VPS (DigitalOcean, Linode, Railway, etc.):
```bash
npm install ws
PORT=8080 node server.js
```

For HTTPS (required for mic/camera access on some browsers):
```bash
SSL_KEY=/path/to/key.pem SSL_CERT=/path/to/cert.pem PORT=8080 node server.js
```

#### Step 2: Deploy the web app (GitHub Pages)
```bash
# From the repo root:
bash bazaar/deploy.sh
```
Then go to your repo Settings > Pages > Source: `gh-pages` branch.

Your app is now at `https://yourusername.github.io/repo-name/`

#### Step 3: Connect them
In the Bazaar app, go to **Settings** and set the relay URL to your VPS:
```
wss://your-vps-domain.com:8080
```

Or use the manual SDP mode (no relay needed, but copy-paste required).

## How It Works

### P2P Mesh
- Browser-to-browser via WebRTC DataChannels
- Star topology: host relays for small rooms (<20 peers)
- Content-addressed: every post gets a SHA-256 hash (CID)
- All data stored locally in IndexedDB

### 0/0 Quality Scoring
Every post starts at `score=0, count=0` — a `0/0` indeterminate state.
As peers vote, the quality converges to a removable value:
- Score moves from 0 to a running total
- Quality = `score / count` (the removable value of the 0/0 singularity)
- Posts sorted by quality
- Flagged posts auto-deleted when enough peers flag them

### Identity
- ECDSA P-256 keypair generated in browser
- Stored in localStorage (survives page reloads)
- Posts signed with your private key
- Display name optional (defaults to "Anonymous")

### Features
- Create/join rooms with codes
- Text posts and image uploads
- Threaded comments
- Upvote/downvote (no karma accumulation)
- Flag and moderate (quorum-based deletion)
- Content addressing (SHA-256 CIDs)
- Full sync on peer join

## Architecture

```
bazaar/
  index.html   — Self-contained web app (no build step)
  server.js    — WebSocket signaling relay (~150 lines, production-ready)
  deploy.sh    — GitHub Pages deploy script
  deploy.bat   — Windows deploy script
  README.md    — This file
```

### Server Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Listening port |
| `HOST` | 0.0.0.0 | Bind address |
| `SSL_KEY` | (none) | Path to TLS key file |
| `SSL_CERT` | (none) | Path to TLS cert file |
| `MAX_ROOMS` | 1000 | Maximum concurrent rooms |
| `ROOM_TTL_MS` | 3600000 | Room timeout (1 hour) |

### Health Check
```
GET /health
→ {"status":"ok","rooms":3,"connections":7,"uptime":42}
```

## The 0/0 Connection

This is an implementation of the 0/0 framework from L.O.R.E.:

- **Indeterminate state**: Post quality is `0/0` — neither up nor down
- **Community votes**: Each vote shifts the numerator or denominator
- **Removable value**: The running average is the unique removable value
- **Convergence**: As votes accumulate, the removable value stabilizes

The quality score IS a removable singularity. The community's collective judgment is what gives it meaning.

## License

Part of the L.O.R.E. (Law of Repulsive Emanation) project.
