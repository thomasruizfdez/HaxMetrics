'use strict';

class ScoreTracker {
  constructor() {
    this._prevRed = 0;
    this._prevBlue = 0;
    this._simRed = 0;
    this._simBlue = 0;
    this._initialized = false;
    this._initialRed = 0;
    this._initialBlue = 0;
  }

  get initialized() { return this._initialized; }
  get initial() { return { red: this._initialRed, blue: this._initialBlue }; }

  init(redScore, blueScore) {
    this._initialRed = redScore;
    this._initialBlue = blueScore;
    this._prevRed = redScore;
    this._prevBlue = blueScore;
    this._initialized = true;
  }

  feed(redScore, blueScore) {
    if (redScore > this._prevRed) this._simRed += redScore - this._prevRed;
    if (blueScore > this._prevBlue) this._simBlue += blueScore - this._prevBlue;
    this._prevRed = redScore;
    this._prevBlue = blueScore;
  }

  get total() {
    return { red: this._simRed, blue: this._simBlue };
  }
}

module.exports = ScoreTracker;
