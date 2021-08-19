var mysql = require('mysql');
var process = require('process');
var pool = mysql.createPool({
  connectionLimit : 10,
  host            : process.env.DB_HOST,
  user            : process.env.DB_USER,
  password        : process.env.DB_PW,
  database        : process.env.DB_SCHEMA
});
module.exports.pool = pool;
