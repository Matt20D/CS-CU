W4111.001-Introduction to Databases 
Spring 2021
Databases Project Part 3 
submission Due March 22 at 11:59 PM
Group number 31

------------
Group Members
-------------
md3420 – Matthew Duran 
ms5767 – Meghan Shah

-------------------------
Google Cloud Credentials
project name – cs4111-001-team31
project id – cs4111-001-team31
project number – 434243893406 
<md3420@cs4111-instance-team3> VM instance

UNI tagged to the postgresql database is md3420
This is the command I type to access the db from our vm instance:
	psql -U md3420 -h 34.73.36.248 -d project1
	
Database URI
	PostgreSQL://md3420:apple@34.73.36.248/project1

Web Application URL
	http://104.196.211.246:8111/

--------------------------
---------------
Part 1 Proposal:
---------------

---------------
Static Content:
---------------

        1) Which menu items are in stock.

		We don't directly have the menu items in stock, but I have the composite 
		ingredients that are in stock plus each of the item's upcoming expiration 
		date. This query is a part of the one in number 4.

        2) profits/expenses on different days.

                This dynamic type of query was really complicated, so i didnt implement 
		this fullly. However, I made it a static query on the restaurant finances 
		web page. Here you will be able to choose 1 of 4 different webpages to surf. 
		You can see all of the restaurants finance together (with an accompanying chart), 
		or break it down by revenu, labor, and food costs. 

        3) Look at employee schedules, and see how much they are owed.

		This was created, along with some charts that report on count of jobs employed and 
		top 5 tenured staffers.

        4) What food items are most popular, from a total price perspective and a total order perspective.

		We create a table with the top 10 and bottom 10 menu items sold, and then pull in each of 
		the menu item's ingredients to let you know how much we have stored adn what the nearest 
		expiration date is. By combining the top/bottom 10 with the underlying ingredients, the 
		restaurant owner can see whether he can satisfy demand for his popular products, and is 
		over buying ingredients for his least popular products.

        5) These will most likely be static charts that use predefined queries for production,
           where users can choose from a drop down menu.

	   	There are plenty of charts in the static pages. In the "all_transactions" query page there 
		is a pie chart that tells us how the company's finances look. It is broken down by labor, 
		revenue, and food expenses. The portion of the pie chart with the highest weight will pop out. 
		In the "revenue" page I have charts that correspond to our busiest time of day, and most popular 
		day of the week. This information would allow the restaurant owner to better staff the restaurant. 
		On the "labor" page there is another pie chart which corresponds to the count of distinct employees 
		that we have. This would tell us if we are hiring too much/too little of a given job title. Also, 
		there is a chart of the top 5 tenured staffers, which is updated daily.

		All of the above charts, will of course be generated when the user clicks on the page, meaning that 
		it will not use stale data. If the underlying data in the DB would change then the above output would 
		also dynamically change in the underlying data queries. This leads to a robust reporting structure for 
		the website.

---------------
Dynamic Content:
---------------

        1) I added in the ability to modify our restaurant's menu, by updating the price of an item, the description 
	of an item, and inserting an item. I wanted to develop a way to delete menu items, but that would have required 
	formal triggers, which were not a requirement of the project
        
	2) With regards to the menu, we can query the databases to see all given transactions for a given menu item. 
	This is dynamic content, where the user inputs a menu item, and the tuples get rendered to the screen. This 
	application will be useful for the owners, when they decide what menu items that they will continue to stick with.

        3) I added in the ability to modify our mailing list. This table uses the registers for relation and dynamically 
	renders all of the mailing list participants to the screen. This table was very had to create (more on that later), 
	because I need to satisfy foreign key constraints for the underlying entities. But everything works swimmingly.

-----------------
Additional Notes:
-----------------
	With all of the inputs, the server should not lock up or crash on any user inputted data. I did some painstakingly 
	deep error checking to ensure that the server would not crash in the demo. (or in general).

	Also, I spent a lot of time with the jinja/html templates, and I am pretty proud of how everything came out. I 
	learned a lot, and this was definitely a challenging assignment. This is especially true when it comes to 
	modurlarizing the templates, and creating inheritence hierarchies. Overall, this was a good projectand I 
	definitely learned a lot and gained usefull skills.

---------------------
Webpage Descriptions:
---------------------

	The 2 most interesting webpages that I have are the menu and the mailing list. Don't get me wrong, I love the 
	Enterprise Finances pages that have all of the static content and charts, and those are certaintly useful. 
	But the power of RDBMS is the ability to dynamically serve content.

-------------
Menu Webpage:
-------------

	Here we can display the full menu that we offer customers, along with the item's price and description. 
	On this page, we can not only modify the price and desctiption, but also add menu items. Unfortunately, 
	I can't support a delete option because we didnt have any triggers in the DB. Those triggers are necessary, 
	because If I delete one of these items there would be a foreign key violation. I am able to support deletions 
	on the mailing list (more on this later).

	The menu will be displayed at all times, and you will be prompted to either view/alter the menu or see specific 
	sales data for an item.

	altering: There are two options, insert and update. Both of these require submitting a text string that the 
	database will parse. Below are the input formats:

	insert: insert, menu_item, price, description
	update: usage: update, menu_item, col, col_value 

	Example1: insert, Grilled Cheese, 10.50, Bread, Cheese, Tomato, Bacon ; Note: description can be NULL
	Example2: update, Burger, price, 10
	Example3: update, Burger, description, Veggie, tomato

	Based on the first argument, I will go through some python logic to execute either an insert or an update. 
	These two functions require cleaning the input arguments and then ensuring that they are of a form that could 
	be fed into postgres tables without issue. Furthermore, a confirmation of what was typed in will be returned 
	to the user in a table below the submit button. Here you will see that the input was either "good" meaning 
	successful, or "bad" meaning failed.

	The reason that I have the menu up at all times is so that you can instantly see the changes.

-----------
Sales Data:
-----------

	Simarly to the altering functionality, I take in a user input which I pass directly to a sql query in the 
	backend so that I can see sales for given items. This will be useful for the owners to see on a item by item 
	basis how the product is selling. 

	The sales data, will be served right below the text input box (if there is any for a given item).

---------------------
Mailing List Webpage:
---------------------

	This one is my favorite, given the underlying mechanics that need to take place. There are 2 options for this 
	page, either delete or insert a person into the mailing list. Below is the input necessary to complete the alterations.

	insert mailing list entry	usage: insert, name (not NULL), email (not NULL), birthday
	delete mailing list entry	usage: delete, name (not NULL)

	First, if you pass in fields that are null, the page will just refresh (thanks to python logic) becaue if we 
	try to input fields that are null, that would violate table constraints and the server would die. This is not good.

	This "registers for" page is a relationship between the mailing list (list of emails) and customer (customer data) 
	entities. So deletions and insertions from this table need to be carefully managed, unless I employed triggers 
	(which I do not). To insert, i need to clean all of the arguments and ensure that they of the appropriate argument 
	lengths for the underlying table. Then I make sure that the email and names, are not already in their respective 
	tables, since those are primary keys. If they arent, then just insert them in and no big deal. If one of them is 
	in a given table, then I will skip inserting for that respective table. Lastly, I make sure that the email/name 
	combo is not already on the "registers for" table.

	Deletions are trickier. First I need to delete from the registers for table, because of key constraints in the 
	underlying tables. Then I will delete the email only from the mailing list page, but I will keep the customer 
	name in the customer table. I keep the name there, because it makes sense to me that people will choose to sign 
	up/remove themselves from mailing lists. But we would want to keep their customer data because they were clearly 
	a customer, and probably ordered stuff. Then, if they choose to sign back up for the mailing list later they can 
	and we will already have their name and customer ID.

	These were some of the challenges that I came across in the menu page, but that would have been harder to 
	implement without cascading triggers.

	All said and done, I am very proud of the DB and webserver overall. It was a lot of work and challenging, 
	but I learned a ton of skills. 

------------------
Coding References:
------------------

	On the homepage you will be able to link to my references.txt (which i will also supply with the readme).

---------------------------
Modules I needed to import:
---------------------------

	import matplotlib.pyplot as plt
	from datetime import date
	import random

	I needed to explicitly install matplotlib for this server, I hope that you dont need to.

