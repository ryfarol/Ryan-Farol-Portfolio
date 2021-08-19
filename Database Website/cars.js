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

    function getcar(res, mysql, context, id, complete){
        var sql = "SELECT car_id as id, car_manufacturer, car_model, car_model_year, car_type, car_color, car_mileage, car_price, tires_num FROM cars WHERE car_id = ?";
        var inserts = [id];
        mysql.pool.query(sql, inserts, function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.car = results[0];
            complete();
        });
    }

        // -- Displays cars on page --
        
    router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deletecars.js"];
        var mysql = req.app.get('mysql');
        get_tires(res, mysql, context, complete);
        get_cars(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 2)
            {
                res.render('cars', context);
            }

        }
    });

   // -- Displays one car for updating --

   router.get('/:id', function(req, res){
        callbackCount = 0;
        var context = {};
        context.jsscripts = ["selecttire.js", "updatecar.js"];
        var mysql = req.app.get('mysql');
        getcar(res, mysql, context, req.params.id, complete);
        get_tires(res, mysql, context, complete)
        function complete(){
            callbackCount++;
            if(callbackCount >= 2){
                res.render('update-car', context);
            }

        }
    });
        
        // -- Adds additional cars to database --
        
    router.post('/', function(req, res){
            console.log(req.body.tire_num)
            console.log(req.body)
            var mysql = req.app.get('mysql');
            var sql = "INSERT INTO cars (car_manufacturer, car_model, car_model_year, car_type, car_color, car_mileage, car_price, tires_num) VALUES (?,?,?,?,?,?,?,?)";
            var inserts = [req.body.car_manufacturer, req.body.car_model, req.body.car_model_year, req.body.car_type, req.body.car_color, req.body.car_mileage, req.body.car_price, req.body.tire];
            sql = mysql.pool.query(sql,inserts,function(error, results, fields){
                if(error){
                    console.log(JSON.stringify(error))
                    res.write(JSON.stringify(error));
                    res.end();
                }else{
                    res.redirect('/cars');
                }
            });
        });
    
    // -- URI that is sent to update an car --
    router.put('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        console.log(req.body)
        console.log(req.params.id)
        var sql = "UPDATE cars SET car_manufacturer =?, car_model =?, car_model_year =?, car_type =?, car_color =?, car_mileage =?, car_price =?, tires_num =? WHERE car_id =?";
        var inserts = [req.body.car_manufacturer, req.body.car_model, req.body.car_model_year, req.body.car_type, req.body.car_color, req.body.car_mileage, req.body.car_price, req.body.tire, req.params.id];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(error)
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.status(200);
                res.end();
            }
        });
    });

    // -- Delete customers --

    router.delete('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        var sql = "DELETE FROM cars WHERE car_id = ?";
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