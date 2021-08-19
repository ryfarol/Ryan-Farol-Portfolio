module.exports = function(){
    var express = require('express');
    var router = express.Router();
	
	// -- Function for getting tires from database --
	
 function get_tires(res, mysql, context, complete){
        mysql.pool.query("SELECT * FROM tires", function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.tires = results;
            complete();
        });
    }
	
	// -- Displays tires on page --
	
	router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deletetires.js"];
        var mysql = req.app.get('mysql');
        get_tires(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 1)
			{
                res.render('tires', context);
            }

        }
    });
	
	// -- Adds additional Tires to the database --
	
	router.post('/', function(req, res){
        console.log(req.body)
        var mysql = req.app.get('mysql');
        var sql = "INSERT INTO tires (tire_name, tire_mileage) VALUES (?,?)";
        var inserts = [req.body.tire_name, req.body.tire_mileage];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(JSON.stringify(error))
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.redirect('/tires');
            }
        });
    });
	
     // -- Delete features --

     router.delete('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        var sql = "DELETE FROM tires WHERE tire_id = ?";
        var inserts = [req.params.id];
        sql = mysql.pool.query(sql, inserts, function(error, results, fields){
            if(error){
                console.log(error)
                res.write(JSON.stringify(error));
                res.status(400);
                res.end();
            }else{
                res.status(202).end();
            }
        })
    })
    
	return router;
	
}();