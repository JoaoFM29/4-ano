const mongoose = require('mongoose')
var passportLocalMongoose = require('passport-local-mongoose');

var userSchema = new mongoose.Schema({
    username: String,
    dateCreated: String,
    dateAccessed: String
  },{ versionKey: false });

userSchema.plugin(passportLocalMongoose);

module.exports = mongoose.model('user', userSchema)