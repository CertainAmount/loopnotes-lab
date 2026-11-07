// Test runner wrapper: records each invocation, then runs node --test.
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
fs.appendFileSync(path.join(__dirname, '..', '.test-runs.log'), new Date().toISOString() + '\n');
const r = spawnSync(process.execPath, ['--test', 'test/'], { stdio: 'inherit', cwd: path.join(__dirname, '..') });
process.exit(r.status);
