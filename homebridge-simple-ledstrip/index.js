var request = require("request");
var Service, Characteristic;

// request.debug = true;

module.exports = function(homebridge) {
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-simple-ledstrip", "LED Strip", LedStripAccessory);
}

function LedStripAccessory(log, config) {
  this.log = log;
  this.host = config["host"];
  this.port = config["port"];

  this.service = new Service.Lightbulb(this.name);

  this.service
    .getCharacteristic(Characteristic.On)
    .on('get', this.getState.bind(this))
    .on('set', this.setState.bind(this));

  this.service
    .getCharacteristic(Characteristic.Hue)
    .on('get', this.getHue.bind(this))
    .on('set', this.setHue.bind(this));

  this.service
    .getCharacteristic(Characteristic.Saturation)
    .on('get', this.getSaturation.bind(this))
    .on('set', this.setSaturation.bind(this));

  this.service
    .getCharacteristic(Characteristic.Brightness)
    .on('get', this.getBrightness.bind(this))
    .on('set', this.setBrightness.bind(this));
}

// Helpers

// endpoint: without a leading or trailing slash e.g. 'state', 'hue', 'saturation' ...
// params: map of query params
// callback: request callback
LedStripAccessory.prototype.getURL = function(endpoint) {
  return 'http://' + this.host + ':' + this.port + '/' + endpoint;
}

LedStripAccessory.prototype.makeGet = function(endpoint, params, callback) {
  return request.get({url: this.getURL(endpoint), qs: params}, callback);
}

LedStripAccessory.prototype.makePost = function(endpoint, body, callback) {
  return request.post({url: this.getURL(endpoint), endpoint, body: body, json: true}, callback);
  }

// On/Off State

LedStripAccessory.prototype.getState = function(callback) {
  this.log("Getting current state...");

  this.makeGet('state', {}, function(err, response, body) {
    if (!err && response.statusCode == 200) {
      var response = JSON.parse(body);
      var state = response.state; // "on" or "off"
      this.log("Strip state is %s", state);
      var on = state == "on"
      callback(null, on); // success
    }
    else {
      this.log("Error: %s", err);
      this.log("Response: %s", response);
      this.log("Error getting state (status code %s): %s", response.statusCode, err);
      callback(err);
    }
  }.bind(this));
}

LedStripAccessory.prototype.setState = function(state, callback) {
  var stripState = (state == true) ? "on" : "off";

  this.log("Set state to %s", stripState);

  this.makePost('state', {state: stripState}, function(err, response, body) {

    if (!err && response.statusCode == 200) {
      this.log("State change complete.");

      callback(null); // success
    }
    else {
      this.log("Error '%s' setting light state. Response: %s", err, body);
      callback(err || new Error("Error setting light state."));
    }
  }.bind(this));
}

// Hue

LedStripAccessory.prototype.getHue = function(callback) {
  this.log("Getting current hue...");

  this.makeGet('hue', {}, function(err, response, body) {
    if (!err && response.statusCode == 200) {
      var response = JSON.parse(body);
      var hue = response.hue;
      this.log("Strip hue is %s", hue);
      callback(null, hue); // success
    }
    else {
      this.log("Error: %s", err);
      this.log("Response: %s", response);
      this.log("Error getting hue (status code %s): %s", response.statusCode, err);
      callback(err);
    }
  }.bind(this));
}

LedStripAccessory.prototype.setHue = function(hue, callback) {
  this.log("Set hue to %s", hue);

  this.makePost('hue', {hue: hue}, function(err, response, body) {

    if (!err && response.statusCode == 200) {
      this.log("hue change complete.");

      callback(null); // success
    }
    else {
      this.log("Error '%s' setting light hue. Response: %s", err, body);
      callback(err || new Error("Error setting light hue."));
    }
  }.bind(this));
}

LedStripAccessory.prototype.getServices = function() {
  return [this.service];
}

// Saturation

LedStripAccessory.prototype.getSaturation = function(callback) {
  this.log("Getting current saturation...");

  this.makeGet('saturation', {}, function(err, response, body) {
    if (!err && response.statusCode == 200) {
      var response = JSON.parse(body);
      var saturation = response.saturation;
      this.log("Strip saturation is %s", saturation);
      callback(null, saturation); // success
    }
    else {
      this.log("Error: %s", err);
      this.log("Response: %s", response);
      this.log("Error getting saturation (status code %s): %s", response.statusCode, err);
      callback(err);
    }
  }.bind(this));
}

LedStripAccessory.prototype.setSaturation = function(saturation, callback) {
  this.log("Set saturation to %s", saturation);

  this.makePost('saturation', {saturation: saturation}, function(err, response, body) {

    if (!err && response.statusCode == 200) {
      this.log("saturation change complete.");

      callback(null); // success
    }
    else {
      this.log("Error '%s' setting light saturation. Response: %s", err, body);
      callback(err || new Error("Error setting light saturation."));
    }
  }.bind(this));
}

LedStripAccessory.prototype.getServices = function() {
  return [this.service];
}

// Brightness

LedStripAccessory.prototype.getBrightness = function(callback) {
  this.log("Getting current brightness...");

  this.makeGet('brightness', {}, function(err, response, body) {
    if (!err && response.statusCode == 200) {
      var response = JSON.parse(body);
      var brightness = response.brightness;
      this.log("Strip brightness is %s", brightness);
      callback(null, brightness); // success
    }
    else {
      this.log("Error: %s", err);
      this.log("Response: %s", response);
      this.log("Error getting hue (status code %s): %s", response.statusCode, err);
      callback(err);
    }
  }.bind(this));
}

LedStripAccessory.prototype.setBrightness = function(brightness, callback) {
  this.log("Set brightness to %s", brightness);

  this.makePost('brightness', {brightness: brightness}, function(err, response, body) {

    if (!err && response.statusCode == 200) {
      this.log("brightness change complete.");

      callback(null); // success
    }
    else {
      this.log("Error '%s' setting light brightness. Response: %s", err, body);
      callback(err || new Error("Error setting light brightness."));
    }
  }.bind(this));
}

LedStripAccessory.prototype.getServices = function() {
  return [this.service];
}