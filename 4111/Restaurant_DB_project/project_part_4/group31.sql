/*
Database project part 4
Advanced SQL features
Matthew Duran (md3420)
Meghan Shah (ms5767)


This file contains all of the code that we used to expand our database schema from
parts 1-3. We will provide the actual code that was used to build the database 
infrastructure, as well as the queries that accompany it. 
*/

---------------------------- Text Attributes ---------------------------------------

-- reviews table code
create table reviews(
	review TEXT not null, 
	rev_id varchar(15), 
	timestamp timestamp, 
	cust_id varchar(10), 
	foreign key (cust_id) references customer, 
	primary key(rev_id)
);

-- example insert into this table
insert into reviews(rev_id, cust_id, timestamp, review) 
values (800005, 6871478682,'2021-02-12 5:31:22-07',
'Eating this food was the taste equivalent of hearing nails on a 
chalkboard. Painful. Would you rather eat dirt
or eat at this restaurant? Easy, dirt. That is all. Save yourself.');

-- Text Query 1
select review from reviews where to_tsvector(review) @@ to_tsquery('pancakes');

-- Text Query 2
select r.review, c.name from reviews as r, customer as c  
WHERE to_tsvector(review) @@ to_tsquery('recommend | great | delicious & !beware') AND c.customer_id=r.cust_id;

-- Text Query 3
select r.review, c.name from reviews as r, customer as c  
WHERE to_tsvector(review) @@ to_tsquery('recommend | good | delicious & !beware') AND c.customer_id=r.cust_id;

-------------------------------------------------------------------------------------

-------------------------- Array Attributes -----------------------------------------

-- performance reviews create table code
create table performance_reviews(
	employee_id varchar(15), 
	manager_id varchar(15),
	emp_performance_rating_bymonth integer[], 
	emp_satisfaction_rating_bymonth integer[], 
	primary key(employee_id), 
	foreign key(employee_id)
);

-- example insert into this table
insert into performance_reviews values 
(25447, 18230, '{6,7,7,8,9,9,9,10,9,10,10,10}','{10,10,9,8,10,10,10,10,10,10,10,10}');

/*
Array Queries

Explanation:

This complicated nested query will unnest the array with employee performance
reviews per month, and take the average monthly performance for the first and 
second half of the year. Those employees with second half performance that is
better than the first half are in line for raises, while the opposite people may
be recieving paycuts
*/

-- Query 1: one person in line for a pay cut.
with avg1 as (with first_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as first_half_perf from first_half
where array_order in (1,2,3,4,5,6)
group by employee_id),

avg2 as (with second_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as second_half_perf from second_half
where array_order in (7,8,9,10,11,12)
group by employee_id)

select avg1.*, second_half_perf from avg1
join avg2 on avg2.employee_id = avg1.employee_id
where first_half_perf > second_half_perf;

-- Query 2: all the people in line for pay raises.
with avg1 as (with first_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as first_half_perf from first_half
where array_order in (1,2,3,4,5,6)
group by employee_id),

avg2 as (with second_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as second_half_perf from second_half
where array_order in (7,8,9,10,11,12)
group by employee_id)

select avg1.*, second_half_perf from avg1
join avg2 on avg2.employee_id = avg1.employee_id
where first_half_perf < second_half_perf;
-------------------------------------------------------------------------------------

-------------------------------- Trigger Code ---------------------------------------

-- this table will hold all changes made to the menu
create table menu_audit (
	operation char(1) not null,
	timestamp timestamp not null,
	recipe_name varchar(50) not null,
	price numeric(5,2) not null,
	description varchar(200)
);

-- Trigger 1 --
-- trigger upon insertion into the menu table
create function menu_insert() returns trigger as $menu_insert$
	
	declare
		count_primary_key integer;

	begin
			
		--
		-- check for valid inputs 
		--
		if NEW.recipe_name is null or length(NEW.recipe_name) > 50 then
			raise exception 'Bad recipe name input';
		end if;

		if NEW.price < 0 then
			raise exception '% cant be sold for negative dollars', NEW.recipe_name;
		end if;

		if length(NEW.description) > 200 then
			raise exception '% has too long of a description', NEW.recipe_name;
		end if;

		-- ensure that this is not already a primary key
		select count(*) into count_primary_key from menu_items where recipe_name = NEW.recipe_name;
		if count_primary_key > 0 then
			raise exception '% cant be a primary key it is already in the table', NEW.recipe_name;
		end if;

		--
		-- price = price * sales tax
		--
		NEW.price = NEW.price * 1.08875;
		
		--
		-- create a row that reflects the changes made to our menu and insert it
		--
		insert into menu_audit select 'I', now(), NEW.*;

		-- return the new tuple to be inserted
		return new;

	end;
$menu_insert$ language plpgsql;

create trigger menu_insert
before insert on menu_items
	for each row execute function menu_insert();

-- Trigger 2 --
-- trigger on price update, multiply desired price by sales tax 8.875%
create function menu_update_price() returns trigger as $menu_update_price$
	begin

		-- check to see if price is valid
		if NEW.price < 0 then
			raise exception '% cant be sold for negative dollars', NEW.recipe_name;
		end if;

		--
		-- price = price * sales tax
		--
		NEW.price = NEW.price * 1.08875;
	
		--
		-- create a row that reflects the changes made to our menu and insert it
		--
		insert into menu_audit select 'U', now(), NEW.*;

		-- return the new tuple to be inserted
		return new;

	end;
$menu_update_price$ language plpgsql;

create trigger menu_update_price
before update of price on menu_items
	for each row execute function menu_update_price();

-- Trigger 3 --
-- trigger to update desc
create function menu_update_desc() returns trigger as $menu_update_desc$
	begin

		-- check length of the input string
		if length(NEW.description) > 200 then
			raise exception '% has too long of a description', NEW.recipe_name;
		end if;
	
		--
		-- create a row that reflects the changes made to our menu and insert it
		--
		insert into menu_audit select 'U', now(), NEW.*;

		-- return the new tuple to be inserted
		return new;

	end;
$menu_update_desc$ language plpgsql;

create trigger menu_update_desc
before update of description on menu_items
	for each row execute function menu_update_desc();

-- Trigger 4 --
-- referenced tables: food_sales, orders, uses
create function menu_item_del() returns trigger as $menu_item_del$
	
	declare
		fs_refs integer;
		ord_refs integer;
		use_refs integer;

	begin
		select count(*) into fs_refs from food_sales fs where fs.recipe_name = OLD.recipe_name;
		select count(*) into ord_refs from orders o where o.recipe_name = OLD.recipe_name;
		select count(*) into use_refs from uses u where u.recipe_name = OLD.recipe_name;
	
		if fs_refs > 0 then
			raise exception 'cannot delete %, % foreign key reference(s) in food_sales table', OLD.recipe_name, fs_refs;
			rollback;
		end if;

		if ord_refs > 0 then 
			raise exception 'cannot delete %, % foreign key reference(s) in orders table', OLD.recipe_name, ord_refs;
			rollback;
		end if;

		if use_refs > 0 then
			raise exception 'cannot delete %, % foreign key reference(s) in uses table', OLD.recipe_name, use_refs;
			rollback;
		end if;

		--
		-- if we make it here then create a row that reflects the changes made to our menu and execute
		--
		insert into menu_audit select 'D', now(), OLD.*;

		-- return the old tuple deleted 
		return OLD;

	end;
$menu_item_del$ language plpgsql;

create trigger menu_item_del
before delete on menu_items
	for each row execute function menu_item_del();

-------------------------------------------------------------------------------------

--------------------------------- end of file ---------------------------------------
