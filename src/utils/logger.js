/**
 * Logger - Simple logging utility for C.A.D.E.
 */

export class Logger {
  constructor(context = 'CADE') {
    this.context = context;
    this.colors = {
      reset: '\x1b[0m',
      red: '\x1b[31m',
      green: '\x1b[32m',
      yellow: '\x1b[33m',
      blue: '\x1b[34m',
      magenta: '\x1b[35m',
      cyan: '\x1b[36m'
    };
  }

  /**
   * Format a log message with context
   * @param {string} level - Log level
   * @param {string} message - Message to log
   * @returns {string} Formatted message
   */
  format(level, message) {
    const timestamp = new Date().toISOString();
    return `[${timestamp}] [${this.context}] ${level}: ${message}`;
  }

  /**
   * Log an info message
   * @param {string} message - Message to log
   * @param {...any} args - Additional arguments
   */
  info(message, ...args) {
    console.log(
      this.colors.cyan + this.format('INFO', message) + this.colors.reset,
      ...args
    );
  }

  /**
   * Log a success message
   * @param {string} message - Message to log
   * @param {...any} args - Additional arguments
   */
  success(message, ...args) {
    console.log(
      this.colors.green + this.format('SUCCESS', message) + this.colors.reset,
      ...args
    );
  }

  /**
   * Log a warning message
   * @param {string} message - Message to log
   * @param {...any} args - Additional arguments
   */
  warn(message, ...args) {
    console.warn(
      this.colors.yellow + this.format('WARN', message) + this.colors.reset,
      ...args
    );
  }

  /**
   * Log an error message
   * @param {string} message - Message to log
   * @param {...any} args - Additional arguments
   */
  error(message, ...args) {
    console.error(
      this.colors.red + this.format('ERROR', message) + this.colors.reset,
      ...args
    );
  }

  /**
   * Log a debug message
   * @param {string} message - Message to log
   * @param {...any} args - Additional arguments
   */
  debug(message, ...args) {
    if (process.env.DEBUG) {
      console.log(
        this.colors.magenta + this.format('DEBUG', message) + this.colors.reset,
        ...args
      );
    }
  }
}
