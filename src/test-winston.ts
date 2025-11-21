import winston from 'winston';

// Test if we can modify silent property dynamically
const consoleTransport = new winston.transports.Console();
const logger = winston.createLogger({
  level: 'info',
  transports: [consoleTransport],
});

console.log('=== Test 1: Normal logging ===');
logger.info('This should appear');

console.log('\n=== Test 2: After setting silent=true ===');
consoleTransport.silent = true;
logger.info('This should NOT appear');

console.log('\n=== Test 3: After setting silent=false ===');
consoleTransport.silent = false;
logger.info('This should appear again');

console.log('\n=== Test complete ===');
