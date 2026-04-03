# LEE - Command Layer Agent

LEE is the Command Layer Agent for MyDataGPT, providing voice-based executive oversight of the entire agent workforce.

## Architecture

LEE operates as a **command interface over a live multi-agent system**:

- **Real-time database integration** - connects to PostgreSQL databases for live system state
- **Does not generate reports** - reads actual system metrics and agent status
- **Announces, routes, approves, escalates** - never processes data directly
- **Mission control + theater announcer** - authoritative with cinematic presentation

## Database Integration

LEE connects to two PostgreSQL databases:

- **Cloud Database**: VM instances, container events, session management
- **Payments Database**: Transaction sessions, refunds, payment processing

### Database Schema

- `cloud-schema.prisma` - Cloud database schema (VM instances, events)
- `payments-schema.prisma` - Payments database schema (transactions, sessions, refunds)

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Add your database URLs and VAPI_API_KEY
   ```

3. **Setup databases:**
   ```bash
   # Generate Prisma clients
   npx prisma generate --schema=cloud-schema.prisma
   npx prisma generate --schema=payments-schema.prisma

   # Run migrations (if needed)
   npx prisma db push --schema=cloud-schema.prisma
   npx prisma db push --schema=payments-schema.prisma
   ```

4. **Test database connections:**
   ```bash
   npm test
   ```

5. **Start webhook server:**
   ```bash
   npm run webhook
   ```

6. **Setup Vapi assistant:**
   ```bash
   npm run setup-lee
   ```

## Environment Variables

```env
# Database URLs
CLOUD_DATABASE_URL="postgresql://user:pass@localhost:5432/mydatagpt_cloud"
PAYMENTS_DATABASE_URL="postgresql://user:pass@localhost:5432/mydatagpt_payments"

# Vapi Configuration
VAPI_API_KEY="your-vapi-api-key-here"
PORT=3000
```

## Voice Call Flow

### Call Opens
> "Welcome to the LEE Marquee. Retrieving current system status."

*(Tool call: getSystemMarquee with mode: "marquee")*

### LEE Announces Status
> "System status: GREEN. Eight agents operational. One degraded. No failures.
>
> 🎬 NOW SHOWING: LEE — Workforce aligned. Health report compiled.
> 🎬 NOW SHOWING: AXEL — One service under review.
> 🎬 NOW SHOWING: SAGE — No active threats.
>
> Special announcements: One high-severity incident. Two pending consent requests. One payment awaiting confirmation."

### Interactive Options
> "Say: 'details on AXEL', 'read incidents', 'handle consent', 'finance status', or 'repeat marquee'."

## Testing

### Database Connection Test
```bash
npm test
```

This will test connections to both cloud and payments databases and display current system metrics.

### Webhook Test
```bash
# Start the webhook server
npm run webhook

# Test with curl
curl -X POST http://localhost:3000/api/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": {"role": "user", "content": "system status"}}'
```

### Voice Call Test
1. Use Vapi dashboard to initiate a call to your LEE assistant
2. Say "system status" or "marquee" to trigger the system overview
3. Try agent-specific commands like "details on AXEL"

## Tool Schema

### getSystemMarquee

Retrieves current system status and agent marquee lines.

**Inputs:**
```json
{
  "mode": "marquee | normal | detailed",
  "include_extended": false
}
```

**Outputs:**
- `marquee`: Cinematic status lines only
- `normal`: Status summary + marquee lines
- `detailed`: Full agent details + metrics

### getAgentDetails

Get detailed information about a specific agent.

**Inputs:**
```json
{
  "agentName": "LEE | ALEX | NOVA | SAGE | ECHO | AXEL | RHEA | ZENO | IVY"
}
```

## Agent Marquee Lines

Each core agent has a fixed cinematic announcement:

- **LEE**: "Workforce aligned. Health report compiled. Approvals queued."
- **ALEX**: "Tasks orchestrated. Escalations handled. Compliance enforced."
- **NOVA**: "Encryption verified. Vault integrity intact. Zero-knowledge operations normal."
- **SAGE**: "Intrusion scans complete. Signatures validated. No active threats."
- **ECHO**: "Consent protocols enforced. Privacy boundaries intact. Inbox active."
- **AXEL**: "Uptime steady. Logs monitored. One service under review."
- **RHEA**: "Prompt optimization logged. Retrieval experiments progressing."
- **ZENO**: "Transactions processed. One payment awaiting confirmation."
- **IVY**: "Audit trails current. No regulatory violations detected."

## Extended Workforce

The 30+ specialized agents (developers, researchers, sales agents, etc.) are summarized as aggregates unless specifically requested:

> "Extended workforce: thirty-two specialized agents active across development, research, and operations. No escalations reported."

## Weekly Health Reports

When available, LEE announces and offers to summarize:

> "A weekly health report is available. Would you like the executive summary or full breakdown?"

## Security & Compliance

- All communications logged in Consent Ledger
- Zero-knowledge architecture maintained
- Constitutional violations trigger immediate escalation
- User consent required for any data operations

## Development

The webhook server provides mock data. Replace `getMockSystemState()` with actual database/API calls to:

- PostgreSQL for agent status
- Internal APIs for metrics
- Encrypted audit logs for compliance data

## Docker Deployment

Build and run with Docker:

```bash
# Build image
docker build -t lee-agent .

# Run container
docker run -d \
  --name lee \
  -p 3000:3000 \
  --env-file .env \
  lee-agent
```

## API Endpoints

- `GET /` - Agent information
- `GET /health` - Health check
- `POST /api/webhook` - Vapi webhook endpoint

## Core Agent Roster

1. **LEE** - Command Layer Agent (this agent)
2. **ALEX** - Task Orchestration Agent
3. **NOVA** - Security & Encryption Agent
4. **SAGE** - Threat Detection Agent
5. **ECHO** - Consent & Privacy Agent
6. **AXEL** - Infrastructure Monitoring Agent
7. **RHEA** - AI Research & Optimization Agent
8. **ZENO** - Payment Processing Agent
9. **IVY** - Compliance & Audit Agent

## License

GPL-3.0 - Part of the C-A-D-E (Community Application Development Environment) project.

---

*LEE - Your voice-activated command center for autonomous agent workforce management.*
