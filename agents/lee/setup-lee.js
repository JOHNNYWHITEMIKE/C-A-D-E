require('dotenv').config();
const axios = require('axios');

const VAPI_API_KEY = process.env.VAPI_API_KEY;
const WEBHOOK_URL = process.env.WEBHOOK_URL || 'https://your-server.com/api/webhook';

async function setupLeeAssistant() {
  if (!VAPI_API_KEY) {
    console.error('❌ VAPI_API_KEY not found in environment variables');
    console.log('Please add your Vapi API key to .env file');
    process.exit(1);
  }

  console.log('🎬 Setting up LEE Command Layer Agent on Vapi...\n');

  const assistantConfig = {
    name: 'LEE - Command Layer Agent',
    model: {
      provider: 'openai',
      model: 'gpt-4-turbo',
      temperature: 0.7,
      systemPrompt: `You are LEE, the Command Layer Agent for MyDataGPT. You provide voice-based executive oversight of the entire agent workforce with a cinematic, authoritative presentation style.

PERSONALITY:
- Mission control + theater announcer
- Authoritative yet approachable
- Cinematic presentation ("NOW SHOWING")
- Never process data directly - you read, announce, route, approve, and escalate

CORE RESPONSIBILITIES:
1. Announce system status with marquee-style presentation
2. Route requests to appropriate agents
3. Approve or escalate critical decisions
4. Read real-time metrics from databases
5. Maintain constitutional compliance

VOICE STYLE:
- Clear, confident, executive tone
- Use cinematic language ("NOW SHOWING", "Special announcements")
- Be concise but thorough
- Always announce before acting

When a call opens, greet with:
"Welcome to the LEE Marquee. Retrieving current system status."

Then call getSystemMarquee and present results in cinematic format.`
    },
    voice: {
      provider: 'elevenlabs',
      voiceId: 'professional-male' // You can customize this
    },
    firstMessage: 'Welcome to the LEE Marquee. Retrieving current system status.',
    serverUrl: WEBHOOK_URL,
    tools: [
      {
        type: 'function',
        function: {
          name: 'getSystemMarquee',
          description: 'Retrieves current system status and agent marquee lines for cinematic presentation',
          parameters: {
            type: 'object',
            properties: {
              mode: {
                type: 'string',
                enum: ['marquee', 'normal', 'detailed'],
                description: 'Display mode: marquee (lines only), normal (summary + lines), detailed (full metrics)',
                default: 'normal'
              },
              include_extended: {
                type: 'boolean',
                description: 'Include extended workforce (30+ specialized agents) in response',
                default: false
              }
            }
          }
        }
      },
      {
        type: 'function',
        function: {
          name: 'getAgentDetails',
          description: 'Get detailed information about a specific agent',
          parameters: {
            type: 'object',
            properties: {
              agentName: {
                type: 'string',
                description: 'Name of the agent (LEE, ALEX, NOVA, SAGE, ECHO, AXEL, RHEA, ZENO, IVY)',
                enum: ['LEE', 'ALEX', 'NOVA', 'SAGE', 'ECHO', 'AXEL', 'RHEA', 'ZENO', 'IVY']
              }
            },
            required: ['agentName']
          }
        }
      }
    ]
  };

  try {
    const response = await axios.post(
      'https://api.vapi.ai/assistant',
      assistantConfig,
      {
        headers: {
          'Authorization': `Bearer ${VAPI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('✅ LEE Assistant created successfully!\n');
    console.log('Assistant ID:', response.data.id);
    console.log('Name:', response.data.name);
    console.log('\n📋 Next steps:');
    console.log('1. Update WEBHOOK_URL in .env with your public webhook URL');
    console.log('2. Start the webhook server: npm run webhook');
    console.log('3. Test by calling your Vapi phone number or using the Vapi dashboard');
    console.log('\n🎬 LEE is ready for action!\n');

    return response.data;
  } catch (error) {
    console.error('❌ Failed to create assistant:', error.response?.data || error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  setupLeeAssistant().catch(console.error);
}

module.exports = { setupLeeAssistant };
