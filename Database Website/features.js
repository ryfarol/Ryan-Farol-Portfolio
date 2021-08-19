module.exports = function(){
    var express = require('express');
    var router = express.Router();
	
	
	// -- Retrieves features from database --
	
 function get_features(res, mysql, context, complete){
        mysql.pool.query("SELECT * FROM features", function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.features = results;
            complete();
        });
    }
	
	// -- Displays features on the page --
	
	router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deletefeatures.js"];
        var mysql = req.app.get('mysql');
        get_features(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 1)
			{
                res.render('features', context);
            }

        }
    });
	
	// -- Adds additional features to the database --
	
	router.post('/', function(req, res){
        console.log(req.body)
        var mysql = req.app.get('mysql');
        var sql = "INSERT INTO features (feat_name) VALUES (?)";
        var inserts = [req.body.feature_name];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(JSON.stringify(error))
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.redirect('/features');
            }
        });
    });

    // -- Delete features --

    router.delete('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        var sql = "DELETE FROM features WHERE feat_id = ?";
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