-- This document holds all of the SQL tables in my postgresql database
-- access the database with the following command
-- psql -U md3420 -h 34.73.36.248 -d project1
-- password: apple
-- \d shows the database
-- \d <tablename> shows the table schema
-- ctrl + l clears the terminal window

/* all of the following tables have been transferred into postresql 
   and all of the data has been inputted into the tables */
 
--------------------------------------- entity tables --------------------------------------------

Create table employee (
 employee_id varchar (10),
 hourly_salary numeric (5,2) not null,
 date_started date not null,
 phone_number varchar (13),
 name varchar (30) not null,
 job varchar (15) not null,
 Primary key (employee_id),
 Check (hourly_salary > 14) );

Create table hours_of_operation (
 day_of_week varchar (9),
 store_open time not null,
 store_close time not null,
 Primary key (day_of_week) );  

 Create table enterprise_finances (
 transaction_id varchar (15),
 date date, 
 Primary key (transaction_id));  

 Create table menu_items (
 recipe_name varchar (50),
 price numeric (5,2) not null,
 description varchar (200) not null,
 Primary key (recipe_name),
 Check (price > -1) );  

 Create table customer (
 customer_id varchar (10),
 name varchar (40),
 Primary key (customer_id) );  

 Create table mailing_list (
 email varchar (25)
 date_signed_up date not null,
 customer_birthday date,
 Primary key (email) );  

 Create table ingredients (
 item varchar (50),
 amount_stored int not null,
 expiration_date date,
 Primary key (item) );  

 Create table farmers (
 farmer_id varchar (10)
 name varchar (50) not null,
 ingredient varchar (50),
 ingredient_price numeric (7,2) not null,
 Primary key (farmer_id, ingredient), 
 Check (ingredient_price > -1) ); 

 Create table ingredient_transaction (
 transaction_id varchar (15),
 date date not null,
 number_of_items int not null,
 Primary Key (transaction_id),
 Check (number_of_items > 0) ); 

 Create table order_transaction (
 transaction_id varchar (15),
 timestamp timestamp not null,
 payment_type varchar (10) not null,
 number_of_items int not null,
 Primary Key (transaction_id, timestamp),
 Check (number_of_items > 0) ); 

 Create table labor_transaction (
 transaction_id varchar (15),
 date date not null,
 hours_worked numeric (5,2) not null,
 Primary Key (transaction_id),
 Check (hours_worked > -1) ) ; 

---------------------------------- relationship tables --------------------------------------------

Create table orders (
 customer_id varchar (10), 
 transaction_id varchar (15),
 timestamp timestamp,
 recipe_name varchar (30),
 Primary key (transaction_id, timestamp, customer_id, recipe_name),
 Foreign Key (transaction_id, timestamp) references order_transaction,
 Foreign key (customer_id) references customer,
 Foreign key (recipe_name) references menu_items);

Create table shift_schedule (
 transaction_id varchar (15),
 day_of_week varchar (9), 
 employee_id varchar (10),
 Primary Key (transaction_id, day_of_week, employee_id),
 Foreign Key (day_of_week) references hours_of_operation,
 Foreign Key (employee_id) references employee,
 Foreign Key (transaction_id) references labor_transaction );  
   

Create table ingredient_expenses (
 transaction_type varchar (20) not null, 
 transaction_id varchar (15),
 item varchar (50),  
 farmer_id varchar (10),
 ingredient varchar (50),
 Primary key (transaction_id, item, farmer_id, ingredient), 
 Foreign key (transaction_id) references ingredient_transaction,
 Foreign key (transaction_id) references enterprise_finances, 
 Foreign Key (farmer_id, ingredient) references farmers,
 Foreign Key (item) references ingredients, 
 Check (transaction_type = 'food_expenses') ); 

 Create table uses (
 recipe_name varchar (50),
 item varchar (50),
 Primary key (recipe_name, item),
 Foreign Key (recipe_name) references menu_items,
 Foreign Key (item) references ingredients ); 

 Create table buys_from (
 item varchar (50), 
 transaction_id varchar (15),
 farmer_id varchar (10),
 ingredient varchar (50),
 Primary key (item, transaction_id, farmer_id, ingredient),
 Foreign Key (farmer_id, ingredient) references farmers,
 Foreign Key (item) references ingredients,
 Foreign Key (transaction_id) references ingredient_transaction); 

 Create table food_sales (
 transaction_type varchar (20) not null, 
 transaction_id varchar (15),
 timestamp timestamp,
 customer_id varchar (10), 
 recipe_name varchar (50),
 Primary key (transaction_id, timestamp, customer_id, recipe_name),
 Foreign Key (transaction_id, timestamp) references order_transaction,
 Foreign Key (transaction_id) references enterprise_finances, 
 Foreign key (customer_id) references customer,
 Foreign key (recipe_name) references menu_items, 
 Check (transaction_type = 'revenue') );

Create table registers_for (
 email varchar (25),
 customer_id varchar (10),
 Primary key (email, customer_id),
 Foreign key (email) references mailing _list,
 Foreign key (customer_id) references customer );
 
Create table labor_expenses (
 transaction_type varchar (20) not null, 
 transaction_id varchar (15),
 day_of_week varchar (9), 
 employee_id varchar (10),
 Primary Key (transaction_id, day_of_week, employee_id),
 Foreign Key (day_of_week) references hours_of_operation,
 Foreign Key (employee_id) references employee,
 Foreign Key (transaction_id) references enterprise_finances,
 Foreign Key (transaction_id) references labor_transaction,
 Check (transaction_type = 'labor') ); 

 --------------------------------------------------------------------------------------------------
 /*
 Other useful syntax:

 alter table hours_of_operation alter column day_of_week type varchar (9);

// to upload data into postgres
 psql -U md3420 -h 34.73.36.248 -d project1 -c "\copy employee (employee_id, hourly_salary, date_started, phone_number, name, job) from 'employee.cs
v' with delimiter ',' csv header"

alter table users alter column email drop not null;

my bruch restaurant database :-D


                List of relations
 Schema |          Name          | Type  | Owner  
--------+------------------------+-------+--------
 md3420 | buys_from              | table | md3420
 md3420 | customer               | table | md3420
 md3420 | employee               | table | md3420
 md3420 | enterprise_finances    | table | md3420
 md3420 | farmers                | table | md3420
 md3420 | food_sales             | table | md3420
 md3420 | hours_of_operation     | table | md3420
 md3420 | ingredient_expenses    | table | md3420
 md3420 | ingredient_transaction | table | md3420
 md3420 | ingredients            | table | md3420
 md3420 | labor_expenses         | table | md3420
 md3420 | labor_transaction      | table | md3420
 md3420 | mailing_list           | table | md3420
 md3420 | menu_items             | table | md3420
 md3420 | order_transaction      | table | md3420
 md3420 | orders                 | table | md3420
 md3420 | registers_for          | table | md3420
 md3420 | shift_schedule         | table | md3420
 md3420 | uses                   | table | md3420
(19 rows)



*/

SQL queries to submit:

select transaction_type from enterprise_finances e
left join food_sales f on f.transaction_id = e.transaction_id
left join ingredient_expenses i on i.transaction_id = e.transaction_id
left join labor_expenses l on l.transaction_id = e.transaction_id;

-- food related queries 

-- get the itemized order
select o.*, m.price, ot.number_of_items, m.price * ot.number_of_items as total_price from orders o
join menu_items m on m.recipe_name = o.recipe_name
join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp;

 customer_id | transaction_id |      timestamp      |            recipe_name            | price | number_of_items | total_price 
-------------+----------------+---------------------+-----------------------------------+-------+-----------------+-------------
 5489501742  | 45000          | 2021-02-02 10:04:23 | Buttermilk Biscuit                |  5.00 |               2 |       10.00
 5489501742  | 45000          | 2021-02-02 10:05:23 | Soft Scrambled Eggs               | 17.00 |               1 |       17.00
 5489501742  | 45000          | 2021-02-02 10:06:23 | Orange Juice                      |  4.75 |               1 |        4.75
 3921569919  | 45001          | 2021-02-02 09:50:36 | Simple Green Salad                |  6.00 |               3 |       18.00
 3921569919  | 45001          | 2021-02-02 09:51:36 | Custard French Toast              | 15.00 |               2 |       30.00
 3921569919  | 45001          | 2021-02-02 09:52:36 | House Made Granola                | 11.00 |               1 |       11.00
 3921569919  | 45001          | 2021-02-02 09:53:36 | Fried Egg Sandwich                | 14.00 |               1 |       14.00
 6871478682  | 45002          | 2021-02-02 08:14:55 | The Plow                          | 19.00 |               1 |       19.00
 6871478682  | 45002          | 2021-02-02 08:15:55 | Market Fruit                      |  9.00 |               2 |       18.00
 6871478682  | 45002          | 2021-02-02 08:16:55 | Grilled Cheese                    | 16.00 |               1 |       16.00
 6871478682  | 45002          | 2021-02-02 08:17:55 | Cold-Smoked Salmon Toast          | 24.00 |               1 |       24.00
 903098016   | 45003          | 2021-02-02 08:18:55 | Chicory Salad                     | 14.50 |               1 |       14.50
 903098016   | 45003          | 2021-02-03 08:24:47 | Plow Burger                       | 17.00 |               1 |       17.00
 5775628707  | 45004          | 2021-02-03 09:54:52 | One Pancake                       |  6.00 |               2 |       12.00
 5775628707  | 45004          | 2021-02-03 09:55:52 | Chicken Apple Sausage             |  7.00 |               1 |        7.00
 5775628707  | 45004          | 2021-02-03 09:56:52 | Buttermilk Biscuit                |  5.00 |               2 |       10.00
 1724244169  | 45005          | 2021-02-03 09:31:27 | Chia Bowl                         | 11.00 |               1 |       11.00
 1724244169  | 45005          | 2021-02-03 09:32:27 | Buttermilk Biscuit                |  5.00 |               2 |       10.00
 5330362158  | 45006          | 2021-02-04 09:27:18 | Lemon Ricotta Pancakes            | 17.00 |               1 |       17.00
 5330362158  | 45006          | 2021-02-04 09:28:18 | Two Pastured Eggs                 |  6.00 |               1 |        6.00
 5330362158  | 45006          | 2021-02-04 09:29:18 | Soft Scrambled Eggs               | 17.00 |               1 |       17.00
 5330362158  | 45006          | 2021-02-04 09:30:18 | Dungeness Crab Scramble           | 26.00 |               1 |       26.00
 5092005176  | 45007          | 2021-02-04 10:33:41 | House Made Granola                | 11.00 |               1 |       11.00
 5092005176  | 45007          | 2021-02-04 10:34:41 | Mimosa                            | 11.00 |               2 |       22.00
 4333005231  | 45008          | 2021-02-04 12:42:09 | Grapefruit Mimosa                 | 11.50 |               4 |       46.00
 1861769465  | 45009          | 2021-02-04 08:16:31 | Iced Tea                          |  3.75 |               3 |       11.25
 1861769465  | 45009          | 2021-02-04 08:17:31 | Chicory Salad                     | 14.50 |               3 |       43.50
 9843832570  | 45010          | 2021-02-04 12:19:12 | Breakaway Cold-Brewed Iced Matcha |  5.00 |               1 |        5.00
 9837727207  | 45011          | 2021-02-04 11:16:05 | Two Egg Breakfast                 | 17.50 |               1 |       17.50
 9837727207  | 45011          | 2021-02-04 11:17:05 | Five Mountains Organic Tea        |  3.75 |               1 |        3.75

-- get the total order for a transaction grouped by customer & transaction_id
select customer_id, o.transaction_id, sum(m.price * ot.number_of_items) as total_price from orders o
join menu_items m on m.recipe_name = o.recipe_name
join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp
group by customer_id, o.transaction_id;

 customer_id | transaction_id | total_price 
-------------+----------------+-------------
 5092005176  | 45007          |       33.00
 6871478682  | 45002          |       77.00
 5330362158  | 45006          |       66.00
 5775628707  | 45004          |       29.00
 1724244169  | 45005          |       21.00
 1861769465  | 45009          |       54.75
 9843832570  | 45010          |        5.00
 9837727207  | 45011          |       21.25
 4333005231  | 45008          |       46.00
 903098016   | 45003          |       31.50
 5489501742  | 45000          |       31.75
 3921569919  | 45001          |       73.00
(12 rows)


-- at what time are we the busiest? We can use this query to staff our restaurant appropriately
select extract(hour from timestamp) as order_hour, count(*)
from orders
group by order_hour
order by count(*) desc;

 order_hour | count 
------------+-------
          9 |    13
          8 |     8
         10 |     5
         12 |     2
         11 |     2
(5 rows)


-- what is our most popular food_item?


-- get our itemized food expenses

select bf.*, it.number_of_items, f.ingredient_price, it.number_of_items * f.ingredient_price as total_price 
from buys_from bf
join farmers f on f.farmer_id = bf.farmer_id and f.ingredient = bf.ingredient
join ingredient_transaction it on it.transaction_id = bf.transaction_id;

            item            | transaction_id | farmer_id  |         ingredient         | number_of_items | ingredient_price | total_price 
----------------------------+----------------+------------+----------------------------+-----------------+------------------+-------------
 Capers                     | ing_205475     | 356285775  | Capers                     |               2 |            15.35 |       30.70
 Agnello Farms Patty        | ing_205476     | 5352354398 | Agnello Farms Patty        |               3 |             7.58 |       22.74
 Cheddar                    | ing_205477     | 5352354398 | Cheddar                    |               3 |            14.12 |       42.36
 Avocado                    | ing_205478     | 7421656618 | Avocado                    |               2 |             3.59 |        7.18
 Almonds                    | ing_205479     | 5604808898 | Almonds                    |               5 |            14.52 |       72.60
 Ham                        | ing_205480     | 6146407633 | Ham                        |               3 |             9.87 |       29.61
 Sausage                    | ing_205481     | 6146407633 | Sausage                    |               3 |             2.71 |        8.13
 Potatoes                   | ing_205482     | 831885188  | Potatoes                   |               5 |            10.40 |       52.00
 Ricotta                    | ing_205483     | 6410418548 | Ricotta                    |               5 |             7.13 |       35.65
 Straus Whole Milk Yogurt   | ing_205484     | 6453973484 | Straus Whole Milk Yogurt   |               5 |             2.04 |       10.20
 Almond Milk                | ing_205485     | 6410418548 | Almond Milk                |               4 |             1.64 |        6.56
 Shittake Mushrooms         | ing_205486     | 3572294229 | Shittake Mushrooms         |               5 |            14.06 |       70.30
 Vanilla Mascarpone Cream   | ing_205487     | 4188003859 | Vanilla Mascarpone Cream   |               4 |            13.56 |       54.24
 Acme Bun                   | ing_205488     | 6064610803 | Acme Bun                   |              10 |             2.76 |       27.60
 Equator Drip Coffee        | ing_205489     | 337070018  | Equator Drip Coffee        |               4 |             3.10 |       12.40
 Five Mountains Organic Tea | ing_205490     | 2028216955 | Five Mountains Organic Tea |               7 |            13.85 |       96.95
 Raspberries                | ing_205491     | 9196837229 | Raspberries                |               4 |            12.18 |       48.72
 Brioche                    | ing_205492     | 798083660  | Brioche                    |               7 |            13.60 |       95.20
 Garlic                     | ing_205493     | 798083660  | Garlic                     |               7 |             4.58 |       32.06


-- total the expenses by transaction

select bf.transaction_id, sum(it.number_of_items * f.ingredient_price) as total_price 
from buys_from bf
join farmers f on f.farmer_id = bf.farmer_id and f.ingredient = bf.ingredient
join ingredient_transaction it on it.transaction_id = bf.transaction_id
group by bf.transaction_id;

 transaction_id | total_price 
----------------+-------------
 ing_205478     |        7.18
 ing_205485     |        6.56
 ing_205480     |       29.61
 ing_205490     |       96.95
 ing_205493     |       32.06
 ing_205483     |       35.65
 ing_205482     |       52.00
 ing_205486     |       70.30
 ing_205491     |       48.72
 ing_205476     |       22.74
 ing_205479     |       72.60
 ing_205484     |       10.20
 ing_205487     |       54.24
 ing_205489     |       12.40
 ing_205492     |       95.20
 ing_205488     |       27.60
 ing_205475     |       30.70
 ing_205477     |       42.36
 ing_205481     |        8.13


-- labor transactions

-- this is the total amount owed to our employees for a day's work
select l.transaction_type, l.transaction_id, l.employee_id, lt.hours_worked * e.hourly_salary money_owed 
from labor_expenses l
join employee e on e.employee_id = l.employee_id
join labor_transaction lt on lt.transaction_id = l.transaction_id;

transaction_type | transaction_id | employee_id | money_owed 
------------------+----------------+-------------+------------
 labor            | 187691         | 16096       |    85.0000
 labor            | 187692         | 11284       |    68.0000
 labor            | 187693         | 12236       |   102.0000
 labor            | 187694         | 10223       |   120.0000
 labor            | 187695         | 27489       |    51.0000
 labor            | 187696         | 36708       |   123.0000
 labor            | 187697         | 14903       |    85.0000
 labor            | 187698         | 25285       |    85.0000
 labor            | 187699         | 31276       |    85.0000
 labor            | 187700         | 35761       |    68.0000
 labor            | 187701         | 15795       |    85.0000
 labor            | 187702         | 33288       |    85.0000
 labor            | 187703         | 48880       |    68.0000
 labor            | 187704         | 32410       |    85.0000
 labor            | 187706         | 15457       |    99.0000
 labor            | 187707         | 36708       |   123.0000
 labor            | 187708         | 10223       |   120.0000



-- now on to the total book

-- this is the total amount owed to our employees for a day's work
-- this is not done we need some sort of correlated query to get all the data together

-- labor
select l.transaction_type, l.transaction_id, lt.hours_worked * e.hourly_salary as money_owed 
from labor_expenses l
join employee e on e.employee_id = l.employee_id
join labor_transaction lt on lt.transaction_id = l.transaction_id;

-- food expenses

select ie.transaction_type, ie.transaction_id, sum(it.number_of_items * f.ingredient_price) as total_price 
from ingredient_expenses ie
join farmers f on f.farmer_id = ie.farmer_id and f.ingredient = ie.ingredient
join ingredient_transaction it on it.transaction_id = ie.transaction_id
group by ie.transaction_type, ie.transaction_id;

-- revenue
select fs.transaction_type, fs.transaction_id, sum(ot.number_of_items * m.price) as total_price
from food_sales fs
join orders o on o.transaction_id = fs.transaction_id and o.timestamp = fs.timestamp
join order_transaction ot on ot.timestamp = o.timestamp and ot.transaction_id = o.transaction_id
join menu_items m on m.recipe_name = o.recipe_name
group by fs.transaction_type, fs.transaction_id;

-- this allowed me to create a better view for totaling up the data
create view all_finances as with labor as (select l.transaction_type, l.transaction_id, round(lt.hours_worked * e.hourly_salary,2) as total_price from labor_expenses l
join employee e on e.employee_id = l.employee_id
join labor_transaction lt on lt.transaction_id = l.transaction_id),
food_expenses as (select ie.transaction_type, ie.transaction_id, sum(it.number_of_items * f.ingredient_price) as total_price
from ingredient_expenses ie
join farmers f on f.farmer_id = ie.farmer_id and f.ingredient = ie.ingredient
join ingredient_transaction it on it.transaction_id = ie.transaction_id
group by ie.transaction_type, ie.transaction_id),
revenue as (select fs.transaction_type, fs.transaction_id, sum(ot.number_of_items * m.price) as total_price from food_sales fs
join orders o on o.transaction_id = fs.transaction_id and o.timestamp = fs.timestamp
join order_transaction ot on ot.timestamp = o.timestamp and ot.transaction_id = o.transaction_id
join menu_items m on m.recipe_name = o.recipe_name
group by fs.transaction_type, fs.transaction_id)
select e.*, transaction_type, total_price from enterprise_finances e
join labor on labor.transaction_id = e.transaction_id
union
select e.*, transaction_type, total_price from enterprise_finances e
join food_expenses fe on fe.transaction_id = e.transaction_id
union
select e.*, transaction_type, total_price from enterprise_finances e
join revenue r on r.transaction_id = e.transaction_id
order by date asc;
