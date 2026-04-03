require('dotenv').config();
const { PrismaClient: CloudPrismaClient } = require('./generated/cloud-client');
const { PrismaClient: PaymentsPrismaClient } = require('./generated/payments-client');

async function testConnections() {
  console.log('🔍 Testing database connections...\n');

  // Test Cloud Database
  console.log('📊 Cloud Database:');
  console.log('URL:', process.env.CLOUD_DATABASE_URL?.replace(/:[^:@]+@/, ':****@') || 'NOT SET');

  try {
    const cloudDb = new CloudPrismaClient();
    await cloudDb.$connect();

    // Test queries
    const vmCount = await cloudDb.vMInstance.count();
    const agentCount = await cloudDb.agentStatus.count();
    const incidentCount = await cloudDb.incident.count();

    console.log('✅ Connected successfully');
    console.log(`   - VM Instances: ${vmCount}`);
    console.log(`   - Agent Status Records: ${agentCount}`);
    console.log(`   - Incidents: ${incidentCount}`);

    await cloudDb.$disconnect();
  } catch (error) {
    console.log('❌ Connection failed:', error.message);
  }

  console.log('\n💳 Payments Database:');
  console.log('URL:', process.env.PAYMENTS_DATABASE_URL?.replace(/:[^:@]+@/, ':****@') || 'NOT SET');

  try {
    const paymentsDb = new PaymentsPrismaClient();
    await paymentsDb.$connect();

    // Test queries
    const transactionCount = await paymentsDb.transaction.count();
    const sessionCount = await paymentsDb.transactionSession.count();
    const refundCount = await paymentsDb.refund.count();
    const consentCount = await paymentsDb.paymentConsent.count();

    console.log('✅ Connected successfully');
    console.log(`   - Transactions: ${transactionCount}`);
    console.log(`   - Sessions: ${sessionCount}`);
    console.log(`   - Refunds: ${refundCount}`);
    console.log(`   - Consent Requests: ${consentCount}`);

    await paymentsDb.$disconnect();
  } catch (error) {
    console.log('❌ Connection failed:', error.message);
  }

  console.log('\n✨ Test complete!\n');
}

// Run if called directly
if (require.main === module) {
  testConnections().catch(console.error);
}

module.exports = { testConnections };
