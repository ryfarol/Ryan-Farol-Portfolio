module.exports = function(){
    var express = require('express');
    var router = express.Router();
	
	// -- Function for getting customers from database --
	
    function get_customers(res, mysql, context, complete){
        mysql.pool.query("SELECT * FROM customers", function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.customers = results;
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

	// -- Function for getting orders from database --
	
    function get_orders(res, mysql, context, complete){
        mysql.pool.query("SELECT * FROM orders", function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.orders = results;
            complete();
        });
    }

    function getorder(res, mysql, context, id, complete){
        var sql = "SELECT order_id as id, customer_num, car_num, order_date, credit_card_num, credit_card_exp_date FROM orders WHERE order_id = ?";
        var inserts = [id];
        mysql.pool.query(sql, inserts, function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.order = results[0];
            complete();
        });
    }
	
	
	// -- Displays orders on page --
	
	router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deleteorders.js"];
        var mysql = req.app.get('mysql');
        get_orders(res, mysql, context, complete);
		get_customers(res, mysql, context, complete);
		get_cars(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 3)
			{
                res.render('orders', context);
            }

        }
    });

    // -- Displays one order for updating --

    router.get('/:id', function(req, res){
        callbackCount = 0;
        var context = {};
        context.jsscripts = ["selectcustomer.js", "selectcar.js", "updateorder.js"];
        var mysql = req.app.get('mysql');
        getorder(res, mysql, context, req.params.id, complete);
        get_customers(res, mysql, context,complete)
        get_cars(res, mysql, context, complete)
        function complete(){
            callbackCount++;
            if(callbackCount >= 3){
                res.render('update-order', context);
            }

        }
    });
	
	// -- Adds additional orders --
	
	router.post('/', function(req, res){
        console.log(req.body.customer_num)
        console.log(req.body.car_num)
        console.log(req.body)
        var mysql = req.app.get('mysql');
        var sql = "INSERT INTO orders (customer_num, car_num, order_date, credit_card_num, credit_card_exp_date) VALUES (?,?,?,?,?)";
        var inserts = [req.body.customer, req.body.car, req.body.order_date, req.body.card_num, req.body.card_exp];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(JSON.stringify(error))
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.redirect('/orders');
            }
        });
    });

    // -- URI that is sent to update an order --
    router.put('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        console.log(req.body)
        console.log(req.params.id)
        var sql = "UPDATE orders SET customer_num =?, car_num =?, order_date =?, credit_card_num =?, credit_card_exp_date =? WHERE order_id =?";
        var inserts = [req.body.customer, req.body.car, req.body.order_date, req.body.card_num, req.body.card_exp, req.params.id];
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
        var sql = "DELETE FROM orders WHERE order_id = ?";
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