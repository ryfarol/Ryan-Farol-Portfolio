module.exports = function(){
    var express = require('express');
    var router = express.Router();
	
	// -- Function for getting cars from database --

function get_cars(res, mysql, context, complete){
	mysql.pool.query("SELECT * FROM cars", function(error, results, fields){
		if(error){
			res.write(JSON.stringify(error));
			res.end();
		}
		context.cars = results;
		complete();
	});
}

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
	
	//-- Function for getting cars-features from database --
	
 function get_cars_features(res, mysql, context, complete){
        mysql.pool.query("SELECT * FROM cars_features_relations", function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.cars_features_relations = results;
            complete();
        });
    }
	
	// -- Displays cars-features on page --
	
	router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deletecarsfeatures.js"];
        var mysql = req.app.get('mysql');
        get_cars_features(res, mysql, context, complete);
		get_cars(res, mysql, context, complete);
		get_features(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 3)
			{
                res.render('cars-features', context);
            }

        }
    });

	
	// -- Adds additional cars-features to the database --
	
	router.post('/', function(req, res){
        console.log(req.body)
        var mysql = req.app.get('mysql');
        var sql = "INSERT INTO cars_features_relations (car_id, feat_id, notes) VALUES (?,?,?)";
        var inserts = [req.body.car, req.body.feature, req.body.notes];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(JSON.stringify(error))
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.redirect('/cars-features');
            }
        });
    });
	
    // -- Delete customers --

    router.delete('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        var sql = "DELETE FROM cars_features_relations WHERE car_feat_id =?";
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