-- Table structure for table Customers
DROP TABLE IF EXISTS customers;

CREATE TABLE `customers` (
    `customer_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `customer_first_name` varchar(255) NOT NULL,
    `customer_last_name` varchar(255) NOT NULL,
    `customer_email` varchar(255) NOT NULL,
    `customer_phone` varchar(255) NOT NULL,
    `customer_street` varchar(255) NOT NULL,
    `customer_city` varchar(255) NOT NULL,
    `customer_state` varchar(255) NOT NULL,
    `customer_zip` varchar(255) NOT NULL
)ENGINE=InnoDB;

-- Dumping data for table Customers
INSERT INTO customers (
customer_first_name, customer_last_name, customer_email, customer_phone, customer_street, customer_city, customer_state, customer_zip)
VALUES ('Dinkledorf', 'Dumbleydore', 'hotwizardwanding@owlmail.com', 0990909090, '1234 Street St.', 'Hogwarts', 'Dead', 93219),
('John', 'Johnson', 'johnjohnsonjajohnson@johnsonmail.com', 5034205555, '1234 John St.', 'Johnsonville', 'CA', 93321),
('EElawn', 'Musket', 'weedmartian420@hotmail.com', 4322344444, '322 Rich People Ave.', 'Colony', 'MA', 31291),
('Billy', 'Gates', 'buyinggf@outlook.com', 6780184911, '892 Alimony Ave.', 'San Francisco', 'CA', 89128),
('Dan', 'Smith', 'dansmith@gmail.com', 5037870231, '492 Normal Way', 'Salem', 'OR', 92991);

-- Table structure for table Features
DROP TABLE IF EXISTS features;

CREATE TABLE `features` (
    `feat_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `feat_name` varchar(255) NOT NULL
)ENGINE=InnoDB;


-- Dumping data for table Features
INSERT INTO features (
feat_name)
VALUES('Background Speaker'),
('Chrome Rims'),
('.50 cal machine gun turret'),
('Chrome Spinnners'),
('Hydraulics');

-- Table structue for table Tires
DROP TABLE IF EXISTS tires;

CREATE TABLE `tires` (
    `tire_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tire_name` varchar(255) NOT NULL,
    `tire_mileage` varchar(255) NOT NULL
)ENGINE=InnoDB;

-- Dumping data for table Tires
INSERT INTO tires (
tire_name, tire_mileage)
VALUES ('Continental', 500000),
('Michelin', 450000),
('Firestone', 300000);

-- Table structure for table Cars
DROP TABLE IF EXISTS cars;

CREATE TABLE `cars` (
    `car_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `car_manufacturer` varchar(255) NOT NULL,
    `car_model` varchar(255) NOT NULL,
    `car_model_year` varchar(255) NOT NULL,
    `car_type` varchar(255) NOT NULL,
    `car_color` varchar(255) NOT NULL,
    `car_mileage` varchar(255) NOT NULL,
    `car_price` varchar(255) NOT NULL,
    `tires_num` int(11) DEFAULT NULL,
    FOREIGN KEY (`tires_num`) REFERENCES `tires` (`tire_id`)
)ENGINE=InnoDB;


-- Dumping data for table Cars
INSERT INTO cars (
car_manufacturer, car_model, car_model_year, car_type, car_color,  car_mileage, car_price, tires_num)
VALUES ('Toyota', 'AE86', 1984, 'Hatchback', 'White', 31000, 80000, (SELECT tire_id FROM tires WHERE tire_name = 'Michelin')),
('BMW', 'M3 GTR GT', 2001, 'Coupe', 'Silver', 16000, 215000, (SELECT tire_id FROM tires WHERE tire_name = 'Continental')),
('Subaru', 'WRX STI', 2006, 'Sedan', 'Red', 12000, 65000, (SELECT tire_id FROM tires WHERE tire_name = 'Firestone'));

-- Table strucutre for M:M intersection table Cars-Features
DROP TABLE IF EXISTS cars_features_relations;

CREATE TABLE `cars_features_relations` (
    `car_feat_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `car_id` int(11) NOT NULL,
    `feat_id` int(11) NOT NULL,
    `notes` varchar(255),
    FOREIGN KEY(`car_id`) REFERENCES `cars` (`car_id`),
    FOREIGN KEY (`feat_id`) REFERENCES `features` (`feat_id`)
)ENGINE=InnoDB;

-- Dumping data for table Cars-Features
INSERT INTO cars_features_relations (
car_id, feat_id, notes)
VALUES ((SELECT car_id FROM cars WHERE car_model = 'AE86'), (SELECT feat_id FROM features where feat_name = 'Background Speaker'), 'Background speakers must be installed before leaving dealership'),
((SELECT car_id FROM cars WHERE car_model = 'M3 GTR GT'), (SELECT feat_id FROM features where feat_name = 'Chrome Rims'), 'Chrome rims are out of stock right now. Will notify customer when they arrive and provide free installation'),
((SELECT car_id FROM cars WHERE car_model = 'WRX STI'), (SELECT feat_id FROM features where feat_name = '.50 cal machine gun turret'), 'Mounted and ready for the zombie apocalypse!');

-- Table structure for table Orders
DROP TABLE IF EXISTS orders;

CREATE TABLE `orders` (
    `order_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `customer_num` int(11) NOT NULL,
    `car_num` int(11) NOT NULL,
    `order_date` varchar(255) NOT NULL,
    `credit_card_num` varchar(255) NOT NULL,
    `credit_card_exp_date` varchar(255) NOT NULL,
    FOREIGN KEY (`customer_num`) REFERENCES `customers` (`customer_id`),
    FOREIGN KEY (`car_num`) REFERENCES `cars` (`car_id`)
)ENGINE=InnoDB; 

-- Dumping data for table Orders
INSERT INTO orders (
customer_num, car_num, order_date, credit_card_num, credit_card_exp_date)
VALUES ((SELECT customer_id FROM customers WHERE customer_last_name = 'Dumbleydore'), (SELECT car_id FROM cars WHERE car_model = 'AE86'), '04-23-2021', 1111222233334444, '05-01-2021'),
((SELECT customer_id FROM customers WHERE customer_last_name = 'Johnson'), (SELECT car_id FROM cars WHERE car_model = 'M3 GTR GT'), '04-23-2021', 4444333322221111, '05-01-2021');