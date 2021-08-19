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

    function getcustomer(res, mysql, context, id, complete){
        var sql = "SELECT customer_id as id, customer_first_name, customer_last_name, customer_email, customer_phone, customer_street, customer_city, customer_state, customer_zip FROM customers WHERE customer_id = ?";
        var inserts = [id];
        mysql.pool.query(sql, inserts, function(error, results, fields){
            if(error){
                res.write(JSON.stringify(error));
                res.end();
            }
            context.customer = results[0];
            complete();
        });
    }
	
	// -- Displays customers on page --
	
	router.get('/', function(req, res){
        var callbackCount = 0;
        var context = {};
        context.jsscripts = ["deletecustomers.js"];
        var mysql = req.app.get('mysql');
        get_customers(res, mysql, context, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 1)
			{
                res.render('customers', context);
            }

        }
    });

       // -- Displays one customer for updating --

    router.get('/:id', function(req, res){
        callbackCount = 0;
        var context = {};
        context.jsscripts = ["updatecustomer.js"];
        var mysql = req.app.get('mysql');
        getcustomer(res, mysql, context, req.params.id, complete);
        function complete(){
            callbackCount++;
            if(callbackCount >= 1){
                res.render('update-customer', context);
            }

        }
    });
	
	// -- Adds additional customers --
	
	router.post('/', function(req, res){
        console.log(req.body)
        var mysql = req.app.get('mysql');
        var sql = "INSERT INTO customers (customer_first_name, customer_last_name, customer_email, customer_phone, customer_street, customer_city, customer_state, customer_zip) VALUES (?,?,?,?,?,?,?,?)";
        var inserts = [req.body.fname, req.body.lname, req.body.email, req.body.phone,req.body.street, req.body.city, req.body.state, req.body.zip];
        sql = mysql.pool.query(sql,inserts,function(error, results, fields){
            if(error){
                console.log(JSON.stringify(error))
                res.write(JSON.stringify(error));
                res.end();
            }else{
                res.redirect('/customers');
            }
        });
    });


     // -- URI that is sent to update a person --
    router.put('/:id', function(req, res){
        var mysql = req.app.get('mysql');
        console.log(req.body)
        console.log(req.params.id)
        var sql = "UPDATE customers SET customer_first_name =?, customer_last_name =?, customer_email =?, customer_phone =?, customer_street =?, customer_city =?, customer_state =?, customer_zip =? WHERE customer_id =?";
        var inserts = [req.body.fname, req.body.lname, req.body.email, req.body.phone,req.body.street, req.body.city, req.body.state, req.body.zip, req.params.id];
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
        var sql = "DELETE FROM customers WHERE customer_id = ?";
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