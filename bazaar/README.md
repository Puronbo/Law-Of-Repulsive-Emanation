# Bazaar — Decentralized Social Platform

A peer-to-peer social app. Reddit + 4chan in the browser. No server stores your data.

## Quick Start

**With signaling server** (recommended):
```bash
# Start the relay (optional, improves UX)
node bazaar/server.js

# Open the app
open bazaar/index.html
```

**Without any server**:
1. Open `bazaar/index.html` on two devices
2. One person clicks "Create Room"
3. Copy the room code, send it to the other person
4. The other person pastes it and sends back an answer
5. Connected — no server needed

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
  server.js    — Optional WebSocket signaling relay (~70 lines)
  README.md    — This file
```

### Protocol
1. Host creates room → gets room code
2. Joiner enters code → WebRTC signaling exchange
3. DataChannel opens → peers exchange identity + sync posts
4. All subsequent messages: posts, votes, flags, comments
5. Content is hash-addressed (CID = SHA-256 of content)

## No Server = No Problem

The app works in two modes:

| Mode | Requires | UX |
|------|----------|-----|
| Relay | Node.js server | One-click room creation |
| Manual | Nothing | Copy-paste SDP exchange |

Both modes are fully peer-to-peer. The relay only helps with signaling (SDP exchange) — no content is stored or relayed.

## The 0/0 Connection

This is an implementation of the 0/0 framework from L.O.R.E.:

- **Indeterminate state**: Post quality is `0/0` — neither up nor down
- **Community votes**: Each vote shifts the numerator or denominator
- **Removable value**: The running average is the unique removable value
- **Convergence**: As votes accumulate, the removable value stabilizes

The quality score IS a removable singularity. The community's collective judgment is what gives it meaning.

## License

Part of the L.O.R.E. (Law of Repulsive Emanation) project.
