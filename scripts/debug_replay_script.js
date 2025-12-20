#!/usr/bin/env node
/**
 * Debug Script for Haxball Replay Decoder
 * 
 * This script loads replay-min.js and lists all available functions/classes
 * to help identify the correct class names when the minified code changes.
 * 
 * Usage:
 *   node scripts/debug_replay_script.js
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

console.log('='.repeat(60));
console.log('Haxball Replay Script Debug Tool');
console.log('='.repeat(60));

// Create a minimal sandbox
const sandbox = {
  console: console,
  Buffer: Buffer,
  Uint8Array: Uint8Array,
  DataView: DataView,
  ArrayBuffer: ArrayBuffer,
  window: {},
  document: {
    createElement: () => ({
      getContext: () => null,
      addEventListener: () => {}
    }),
    addEventListener: () => {}
  },
  performance: { now: () => Date.now() },
  requestAnimationFrame: () => {},
  setTimeout: setTimeout,
  setInterval: setInterval
};

sandbox.window.document = sandbox.document;
sandbox.window.window = sandbox.window;
sandbox.document.defaultView = sandbox.window;
sandbox.global = sandbox.window;
sandbox.self = sandbox.window;

// Load pako
try {
  sandbox.pako = require('pako');
} catch (error) {
  console.error('Warning: pako not found. Some features may not work.');
}

console.log('\n1. Loading replay-min.js...');

// Load the replay-min.js file
const replayScriptPath = path.join(__dirname, '..', 'original_script', 'replay-min.js');
if (!fs.existsSync(replayScriptPath)) {
  console.error(`Error: replay-min.js not found at: ${replayScriptPath}`);
  process.exit(1);
}

const replayScript = fs.readFileSync(replayScriptPath, 'utf8');
console.log(`   File size: ${(replayScript.length / 1024).toFixed(1)} KB`);

// Try to find IIFE patterns
console.log('\n2. Analyzing script structure...');
const patterns = [
  { name: 'C.cj();', regex: /C\.cj\(\);/ },
  { name: 'X.fj();', regex: /X\.fj\(\);/ },
  { name: '})(window);', regex: /\}\)\(window\);/ },
  { name: '})(this);', regex: /\}\)\(this\);/ },
  { name: '})(self);', regex: /\}\)\(self\);/ },
  { name: '})(global);', regex: /\}\)\(global\);/ }
];

console.log('   IIFE patterns found:');
patterns.forEach(p => {
  if (p.regex.test(replayScript)) {
    console.log(`   ✓ ${p.name}`);
  }
});

// Patch code to expose internal classes
const exposePatchCode = `
; try {
  // Try to expose everything to the passed parameter (ub)
  if (typeof ub !== 'undefined') {
    for (var key in this) {
      if (this.hasOwnProperty(key) && typeof this[key] === 'function') {
        ub[key] = this[key];
      }
    }
  }
} catch(e) {}
`;

// Add a patch to expose all top-level variables
const patchedScript = replayScript.replace(
  /(function\s*\([^)]*\)\s*\{)/,
  '$1\nvar __exposed = {}; (function() { var _vars = []; '
) + exposePatchCode;

console.log('\n3. Executing script in sandbox...');

// Execute the script
try {
  vm.createContext(sandbox);
  vm.runInContext(patchedScript, sandbox);
  console.log('   ✓ Script executed successfully');
} catch (error) {
  console.error('   ✗ Error executing script:', error.message);
  // Continue anyway to list what we can
}

console.log('\n4. Analyzing exposed objects...');

// List all properties in window
const windowProps = Object.keys(sandbox.window);
console.log(`   Total properties in window: ${windowProps.length}`);

// Filter and categorize
const functions = [];
const classes = [];
const objects = [];
const primitives = [];

windowProps.forEach(key => {
  if (key.startsWith('_')) return; // Skip private
  
  const val = sandbox.window[key];
  const type = typeof val;
  
  if (type === 'function') {
    // Check if it's a class (constructor)
    const isClass = /^[A-Z]/.test(key) || val.toString().includes('function ' + key);
    if (isClass || val.prototype) {
      classes.push(key);
    } else {
      functions.push(key);
    }
  } else if (type === 'object' && val !== null) {
    objects.push(key);
  } else if (type !== 'undefined') {
    primitives.push(key);
  }
});

console.log('\n5. Potential Decoder/Room classes (uppercase, 2-3 chars):');
const potentialClasses = classes.filter(c => {
  return c.length >= 1 && c.length <= 3 && /^[A-Z]/.test(c);
}).sort();

if (potentialClasses.length > 0) {
  potentialClasses.forEach(c => {
    const fn = sandbox.window[c];
    const proto = fn.prototype;
    const methods = proto ? Object.getOwnPropertyNames(proto).filter(m => m !== 'constructor') : [];
    console.log(`   ${c}: ${methods.length} methods ${methods.length > 0 ? `(${methods.slice(0, 5).join(', ')}${methods.length > 5 ? '...' : ''})` : ''}`);
  });
} else {
  console.log('   (none found with standard pattern)');
}

console.log('\n6. Looking for known patterns...');

// Look for specific patterns we know
const knownPatterns = {
  'Decoder (ab/Jb)': ['ab', 'Jb'],
  'Room (ca/fa)': ['ca', 'fa'],
  'Messages (rb)': ['rb'],
  'Replay player (Vb)': ['Vb'],
  'Reader helpers (F/O)': ['F', 'O']
};

Object.entries(knownPatterns).forEach(([desc, names]) => {
  const found = names.filter(n => sandbox.window[n]);
  if (found.length > 0) {
    console.log(`   ✓ ${desc}: ${found.join(', ')}`);
  } else {
    console.log(`   ✗ ${desc}: not found`);
  }
});

console.log('\n7. All classes/constructors found:');
if (classes.length > 0) {
  console.log('   ' + classes.sort().join(', '));
} else {
  console.log('   (none found)');
}

console.log('\n8. All standalone functions:');
if (functions.length > 0) {
  console.log('   ' + functions.sort().slice(0, 30).join(', '));
  if (functions.length > 30) {
    console.log(`   ... and ${functions.length - 30} more`);
  }
} else {
  console.log('   (none found)');
}

console.log('\n9. Recommendations:');
console.log('   - Look for classes with methods like: yk() for stadium export');
console.log('   - Decoder class typically has: ad (duration), le (start time), eg (events)');
console.log('   - Room class typically has: Fb (name), L (players), D (game state), I (stadium)');
console.log('   - Try testing different 2-letter uppercase combinations');

console.log('\n' + '='.repeat(60));
console.log('Debug complete!');
console.log('='.repeat(60));
