const fs = require('fs');
const vm = require('vm');
const pako = require('pako');

const replayData = fs.readFileSync('src/replays/test_all_teams.hbr2');

function createSandbox() {
  const sandbox = {
    console: console,
    pako: pako,
    Math: Math,
    Date: Date,
    Object: Object,
    Array: Array,
    Uint8Array: Uint8Array,
    DataView: DataView,
    ArrayBuffer: ArrayBuffer,
    performance: { now: () => Date.now() },
    window: {},
    document: {
      createElement: () => ({ 
        getContext: () => ({ 
          fillRect: () => {}, clearRect: () => {}, save: () => {}, restore: () => {},
          beginPath: () => {}, closePath: () => {}, moveTo: () => {}, lineTo: () => {},
          arc: () => {}, fill: () => {}, stroke: () => {}
        }),
        toDataURL: () => '',
        width: 800, height: 600, style: {}
      })
    }
  };
  sandbox.window.performance = sandbox.performance;
  sandbox.window.document = sandbox.document;
  sandbox.window.localStorage = { getItem: () => null, setItem: () => {} };
  sandbox.window.AudioContext = function() {};
  sandbox.window.Image = function() {};
  sandbox.ub = sandbox.window;
  return sandbox;
}

const sandbox = createSandbox();
let replayScript = fs.readFileSync('original_script/replay-min.js', 'utf8');

const patchCode = `
  if (typeof ab !== 'undefined') ub.ab = ab;
  if (typeof ca !== 'undefined') ub.ca = ca;
  if (typeof rb !== 'undefined') ub.rb = rb;
`;
replayScript = replayScript.replace(/(\s+C\.cj\(\);)/, patchCode + '$1');

vm.createContext(sandbox);
vm.runInContext(replayScript, sandbox);

const DecoderClass = sandbox.window.ab;
const RoomClass = sandbox.window.ca;
const MessageClass = sandbox.window.rb;

if (MessageClass && typeof MessageClass.Xe === 'function') {
  MessageClass.Xe();
}

const room = new RoomClass();
const decoder = new DecoderClass(new Uint8Array(replayData), room, 3);

console.log('=== Game State ===');
console.log('Has game state (D):', room.D ? 'yes' : 'no');

if (room.D) {
  console.log('\nGame properties:');
  console.log('  Time (za):', room.D.za);
  console.log('  Red score (Ta):', room.D.Ta);
  console.log('  Blue score ($a):', room.D.$a);
  console.log('  State:', room.D.state);
  
  // Look for other properties
  const gameKeys = Object.keys(room.D).filter(k => !k.startsWith('_'));
  console.log('\nAll game keys:', gameKeys.slice(0, 30).join(', '));
}

console.log('\n=== Room State ===');
const roomKeys = Object.keys(room).filter(k => !k.startsWith('_') && typeof room[k] !== 'function');
console.log('Room keys:', roomKeys.slice(0, 30).join(', '));

