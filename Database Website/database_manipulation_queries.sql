-- Customers Page 

-- get all Customer info to populate from the Customers table
SELECT * FROM customers;

-- add a new customer with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO customers (customer_first_name, customer_last_name, customer_email, customer_phone, customer_street, customer_city, customer_state, customer_zip) VALUES (:customer_first_nameINPUT, :customer_last_nameINPUT, :customer_emailINPUT, :customer_phoneINPUT, :customer_streetINPUT, :customer_cityINPUT, :customer_stateINPUT, :customer_zipINPUT);

-- update customer info based on the info entered from the update form
UPDATE Customers SET customer_first_name = :customer_first_nameINPUT, customer_last_name = :customer_last_nameINPUT, customer_email = :customer_emailINPUT, customer_phone = :customer_phoneINPUT, customer_street = :customer_streetINPUT, customer_city = :customer_cityINPUT, customer_state = :customer_stateINPUT, customer_zip = :customer_zipINPUT WHERE customer_id = :customer_ID_from_the_edit_form;

-- delete a customer info
DELETE FROM customers WHERE customer_id = :customer_id_from_delete_button;


-- Orders Page

-- get all Order info to populate from the Orders table
SELECT cstomers.customer_id, cars.car_id, order_date, credit_card_num, credit_card_exp_date FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id
LEFT JOIN cars ON orders.car_id = cars.card_id;

-- add a new order with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO orders (customer_id, car_id, order_date, credit_card_num, credit_card_exp_date) VALUES (:customer_idINPUT, :car_idINPUT, :order_dateINPUT, :credit_card_numINPUT, :credit_card_exp_dateINPUT);

-- update order info based on the info entered from the update form
UPDATE orders SET customer_id = :customer_idINPUT, car_id = :car_idINPUT, order_date = :order_dateINPUT, credit_card_num = :credit_card_numINPUT, credit_card_exp_date = :credit_card_exp_dateINPUT WHERE order_id = :order_id_from_edit_form;

-- delete an order
DELETE FROM orders WHERE order_id = :order_id_from_delete_button;

-- Cars Page

-- get all Car info to populate from the Cars table
SELECT car_manufactuerer, car_model, car_model_year, car_type, car_color, car_milage, car_price, tires.tire_id FROM cars
LEFT JOIN tires ON cars.tire_id = tires.tire_id;

-- add a new car with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO cars (car_manufactuerer, car_model, car_model_year, car_type, car_color, car_milage, car_price, tire_id) VALUES (:car_manufactuererINPUT, :car_modelINPUT, :car_model_yearINPUT, :car_typeINPUT, :car_colorINPUT, :car_milageINPUT, :car_priceINPUT, :tire_idINPUT);

-- update car info based on the info entered from the update form
UPDATE cars SET car_manufacturer = :car_manufacturerINPUT, car_model = :car_modelINPUT, car_model_year = :car_model_yearINPUT, car_type = :car_typeINPUT, car_color = :car_colorINPUT, car_mileage = :car_mileageINPUT, car_price = :car_priceINPUT, tire_id = :tire_idINPUT WHERE cars_id = cars_id_from_edit_form;

-- delete a car
DELETE FROM cars WHERE car_id = :car_id_from_delete_button;


-- Features page

-- get all Feature info to populate from the features table
SELECT * FROM features;

-- add a new feature with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO features (feat_name) VALUES (:feat_nameINPUT);

-- update features info based on the info entered from the update form
UPDATE features SET feat_name = :feat_nameINPUT WHERE feat_id = :feat_id_from_edit_form;

-- delete a feature
DELETE FROM features WHERE feat_id = :feat_id_from_delete_button;


-- Tires Page

-- get all Tire info to populate from the tire table
SELECT * FROM tires;

-- add a new feature with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO tires (tire_name, tire_milage) VALUES (:tire_nameINPUT, :tire_milageINPUT);

-- update tire info based on the info entered from the update form
UPDATE tires SET tire_name = :tire_nameINPUT, tire_milage = :tire_milageINPUT WHERE tire_id = :tire_id_from_edit_form;

-- delete a tire
DELETE FROM tires WHERE tire_id = :tire_id_from_delete_button;

-- Cars Features page

-- get all cars-features info to populate from the car-features table
SELECT * FROM cars_features_relations

-- add a new relationship with colon : character being used to
-- denote the varibales that will have data from the backend programming langauge 
INSERT INTO cars_features_relations (feat_id, car_id, notes) VALUES (:feat_idINPUT, :car_idINPUT, :notesINPUT);

-- update relatioinship info based on the info entered from the update form
UPDATE cars_features_relations SET feat_id = :feat_idINPUT, car_id = :car_idINPUT, notes = :notesINPUT WHERE feat_id = feat_id_from_edit_form;

-- delete a relationship
DELETE FROM cars_features_relations WHERE feat_id = :feat_id_from_delete_button;