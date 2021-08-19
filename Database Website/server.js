var path = require('path');
var express = require('express');
var exphbs = require('express-handlebars');
var bodyParser = require('body-parser');
PORT = 9652;

var mysql = require('./dbcon.js');

var app = express();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');
app.set('mysql', mysql);
app.use(bodyParser.urlencoded({extended:true}));

var port = process.env.PORT || 9652;

app.use(express.static(path.join(__dirname, '/public')));

app.get('/', function (req, res, next) {
  res.status(200).render('index', {});
});

app.get('/index',function(req,res,next){
  res.status(200).render('index', {});
});

app.use('/customers', require('./customers.js'));
app.use('/cars', require('./cars.js'));
app.use('/orders', require('./orders.js'));
app.use('/features', require('./features.js'));
app.use('/tires', require('./tires.js'));
app.use('/cars-features', require('./cars-features.js'));


app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});


app.listen(port, function () {
  console.log('Express started on http://flip1.engr.oregonstate.edu' + port + '; press Ctrl-C to terminate.');
});