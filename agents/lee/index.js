require('dotenv').config();
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Agent marquee lines
const AGENT_MARQUEE = {
  LEE: "Workforce aligned. Health report compiled. Approvals queued.",
  ALEX: "Tasks orchestrated. Escalations handled. Compliance enforced.",
  NOVA: "Encryption verified. Vault integrity intact. Zero-knowledge operations normal.",
  SAGE: "Intrusion scans complete. Signatures validated. No active threats.",
  ECHO: "Consent protocols enforced. Privacy boundaries intact. Inbox active.",
  AXEL: "Uptime steady. Logs monitored. One service under review.",
  RHEA: "Prompt optimization logged. Retrieval experiments progressing.",
  ZENO: "Transactions processed. One payment awaiting confirmation.",
  IVY: "Audit trails current. No regulatory violations detected."
};

// Middleware
app.use(express.json());

// Mock system state (replace with actual database queries in production)
function getMockSystemState() {
  return {
    systemStatus: 'GREEN',
    agents: {
      operational: 8,
      degraded: 1,
      failed: 0
    },
    coreAgents: [
      { name: 'LEE', status: 'operational', marquee: AGENT_MARQUEE.LEE },
      { name: 'ALEX', status: 'operational', marquee: AGENT_MARQUEE.ALEX },
      { name: 'NOVA', status: 'operational', marquee: AGENT_MARQUEE.NOVA },
      { name: 'SAGE', status: 'operational', marquee: AGENT_MARQUEE.SAGE },
      { name: 'ECHO', status: 'operational', marquee: AGENT_MARQUEE.ECHO },
      { name: 'AXEL', status: 'degraded', marquee: AGENT_MARQUEE.AXEL },
      { name: 'RHEA', status: 'operational', marquee: AGENT_MARQUEE.RHEA },
      { name: 'ZENO', status: 'operational', marquee: AGENT_MARQUEE.ZENO },
      { name: 'IVY', status: 'operational', marquee: AGENT_MARQUEE.IVY }
    ],
    extendedWorkforce: {
      total: 32,
      active: 32,
      escalations: 0
    },
    alerts: {
      incidents: { high: 1, total: 3 },
      consentRequests: 2,
      pendingPayments: 1
    }
  };
}

// Tool: getSystemMarquee
function getSystemMarquee(mode = 'normal', includeExtended = false) {
  const state = getMockSystemState();
  const result = {
    systemStatus: state.systemStatus,
    timestamp: new Date().toISOString()
  };

  if (mode === 'marquee') {
    // Marquee-only mode: just the cinematic lines
    result.marqueeLines = state.coreAgents.map(agent =>
      `🎬 NOW SHOWING: ${agent.name} — ${agent.marquee}`
    );
  } else if (mode === 'detailed') {
    // Detailed mode: full agent info
    result.summary = {
      operational: state.agents.operational,
      degraded: state.agents.degraded,
      failed: state.agents.failed
    };
    result.coreAgents = state.coreAgents;
    result.alerts = state.alerts;
    if (includeExtended) {
      result.extendedWorkforce = state.extendedWorkforce;
    }
  } else {
    // Normal mode: summary + marquee
    result.summary = `System status: ${state.systemStatus}. ${state.agents.operational} agents operational. ${state.agents.degraded} degraded. ${state.agents.failed} failures.`;
    result.marqueeLines = state.coreAgents.map(agent =>
      `🎬 NOW SHOWING: ${agent.name} — ${agent.marquee}`
    );
    result.specialAnnouncements = [
      `${state.alerts.incidents.high} high-severity incident${state.alerts.incidents.high !== 1 ? 's' : ''}.`,
      `${state.alerts.consentRequests} pending consent request${state.alerts.consentRequests !== 1 ? 's' : ''}.`,
      `${state.alerts.pendingPayments} payment${state.alerts.pendingPayments !== 1 ? 's' : ''} awaiting confirmation.`
    ];
  }

  return result;
}

// Tool: getAgentDetails
function getAgentDetails(agentName) {
  const state = getMockSystemState();
  const agent = state.coreAgents.find(a => a.name.toLowerCase() === agentName.toLowerCase());

  if (!agent) {
    return { error: `Agent ${agentName} not found` };
  }

  return {
    name: agent.name,
    status: agent.status,
    marquee: agent.marquee,
    lastHealthCheck: new Date().toISOString(),
    metrics: {
      uptime: '99.8%',
      responseTime: '120ms',
      tasksCompleted: 1247
    }
  };
}

// Webhook endpoint for Vapi
app.post('/api/webhook', (req, res) => {
  console.log('📞 Webhook received:', JSON.stringify(req.body, null, 2));

  const { message, call, tool } = req.body;

  // Handle tool calls
  if (tool && tool.name === 'getSystemMarquee') {
    const { mode, include_extended } = tool.parameters || {};
    const result = getSystemMarquee(mode, include_extended);

    return res.json({
      results: [result]
    });
  }

  if (tool && tool.name === 'getAgentDetails') {
    const { agentName } = tool.parameters || {};
    const result = getAgentDetails(agentName);

    return res.json({
      results: [result]
    });
  }

  // Default response
  res.json({
    message: "LEE Command Layer Agent ready. Say 'system status' or 'marquee' for overview."
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    agent: 'LEE',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'LEE - Command Layer Agent',
    version: '1.0.0',
    status: 'operational',
    description: 'Voice-based executive oversight of MyDataGPT agent workforce'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🎬  LEE - COMMAND LAYER AGENT                          ║
║                                                           ║
║   Webhook server running on port ${PORT}                    ║
║   Voice-based executive oversight active                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
  console.log(`📡 Webhook endpoint: http://localhost:${PORT}/api/webhook`);
  console.log(`💚 Health check: http://localhost:${PORT}/health\n`);
});

module.exports = app;
