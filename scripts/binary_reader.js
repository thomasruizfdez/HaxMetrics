/**
 * Binary reader for HBR2 replay files
 * Implements the same reading methods as the Python BinaryReader
 */

class BinaryReader {
  constructor(buffer) {
    this.buffer = buffer;
    this.pos = 0;
  }
  
  /**
   * Read a single byte (uint8)
   */
  readByte() {
    if (this.pos >= this.buffer.length) {
      throw new Error('EOF reached');
    }
    return this.buffer[this.pos++];
  }
  
  /**
   * Read uint8
   */
  readUInt8() {
    return this.readByte();
  }
  
  /**
   * Read uint16 big-endian
   */
  readUInt16BE() {
    const val = this.buffer.readUInt16BE(this.pos);
    this.pos += 2;
    return val;
  }
  
  /**
   * Read uint32 big-endian
   */
  readUInt32BE() {
    const val = this.buffer.readUInt32BE(this.pos);
    this.pos += 4;
    return val;
  }
  
  /**
   * Read int32 little-endian
   */
  readInt32LE() {
    const val = this.buffer.readInt32LE(this.pos);
    this.pos += 4;
    return val;
  }
  
  /**
   * Read varint (variable-length integer)
   */
  readVarint() {
    let result = 0;
    let shift = 0;
    let byte;
    do {
      byte = this.readByte();
      result |= (byte & 0x7F) << shift;
      shift += 7;
    } while (byte & 0x80);
    return result;
  }
  
  /**
   * Read string (length-prefixed with varint)
   */
  readString() {
    const length = this.readVarint();
    if (length === 0) return '';
    const str = this.buffer.toString('utf8', this.pos, this.pos + length);
    this.pos += length;
    return str;
  }
  
  /**
   * Check if we've reached end of file
   */
  eof() {
    return this.pos >= this.buffer.length;
  }
  
  /**
   * Skip n bytes
   */
  skip(n) {
    this.pos += n;
  }
  
  /**
   * Get remaining bytes
   */
  remaining() {
    return this.buffer.length - this.pos;
  }
  
  /**
   * Peek at next n bytes without advancing position
   */
  peekBytes(n) {
    return this.buffer.slice(this.pos, this.pos + n);
  }
  
  /**
   * Get current position
   */
  getPosition() {
    return this.pos;
  }
  
  /**
   * Set position
   */
  setPosition(pos) {
    this.pos = pos;
  }
}

module.exports = BinaryReader;
