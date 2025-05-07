var createError = require('http-errors');
var express = require('express');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var session = require('express-session');
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var AnonymousStrategy = require('passport-anonymous').Strategy;
var cors = require('cors')
require ('dotenv/config');
var stripeRoutes = require('./routes/stripe');

var apiRouter = require('./routes/index');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(session({
  secret: process.env.SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: { 
    secure: false,
    maxAge: 24 * 60 * 60 * 1000
  } //Test true after implementation //Session expiring after 24 hours
}));

// Passport configuration
var User = require('./models/user');
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());
passport.use(new AnonymousStrategy(User.authenticate()));

app.use(passport.initialize());
app.use(passport.session());

app.use(cors({
  origin: (origin, callback) => {
    // Allow all origins
    callback(null, origin || '*');  // Respond with the request's origin or * for no-origin requests
  },
  credentials: true,  // Allow credentials (cookies, headers, etc.)
}));

var mongoose = require("mongoose");
var mongoDB = process.env.MONGO_URI;
mongoose.connect(mongoDB, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  serverSelectionTimeoutMS: 5000
});

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'Erro de conexão ao MongoDB'));
db.once('open', () => {
  console.log("Conexão ao MongoDb realizada com sucesso");
});

app.use('/api', apiRouter);
app.use('/api', stripeRoutes);

app.use(function(req, res, next) {
  next(createError(404));
});

// Use the Stripe routes


app.use(function (err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  res.status(err.status || 500);
  res.json({
    message: err.message,
    error: req.app.get('env') === 'development' ? err : {}
  });
});

module.exports = app;
