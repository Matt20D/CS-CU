
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

import matplotlib.pyplot as plt
from datetime import date
import random

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@34.73.36.248/project1
#
# For example, if you had username zy2431 and password 123123, then the following line would be:
#
#     DATABASEURI = "postgresql://zy2431:123123@34.73.36.248/project1"
#
DATABASEURI = "postgresql://md3420:apple@34.73.36.248/project1" 

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  
  #
  #context = dict(data = names)
  #if request.form == 1:
  #    context = dict(data = 1)
  #
  
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("homepage.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/references') # this will end up being my references.txt
def references():
  return render_template("references.html")

##############################################################
#                                                            #
# RECEIVE INPUT FROM THE WEBPAGE AND DECIDE CONTROL FLOW     #
#                                                            #
##############################################################

# basically we need to have a list of queries in the '/' method
# every time a user inputs a new value, we will redirect to '/'
# where we will have an if/elif/elif statement that will allow us
# to choose the proper query
@app.route('/user_input', methods=['POST'])
def user_input():
    
    # parse the user input
    menu_item = request.form['query number']

    # This will be our control flow that sends users to different webpages
    # to see different query executions, based on user inputs
    if menu_item == '1':
        return redirect('/finances')
    elif menu_item == '2':
        return redirect('/menu')
    elif menu_item == '3':
        return redirect('/mailing_list')
    else: # redirect back to the homepage
        try:
            print("error: %d is an invalid menu choice\n" % menu_item)
        except:
            print("error: %s is an invalid menu choice\n" % menu_item)
        return redirect('/')

# get the input from the menu webpage
@app.route('/menu_input', methods=['POST'])
def menu_input():

  # parse the user input
  user_input = request.form['query']

  # determine which page to render
  if user_input == '1':
      return redirect('/menu_altering')
  elif user_input == '2':
      return redirect('/menu_sales')
  else:
      try:
            print("error: %d is an invalid menu choice\n" % user_input)
      except:
            print("error: %s is an invalid menu choice\n" % user_input)
      return redirect('/menu')

# here is where I will execute the particular queries that 
# were input from the user regarding menu_sales
@app.route('/menu_sales_input', methods=['POST'])
def menu_sales_input():

    # remember context is a list of two lists. l[0] is menu, l[1] is sales
    context = get_menu_from_db() # this will get rendered at all times

    # parse the user request
    user_input = request.form['query']
    user_input = user_input.strip()

    # execute the query
    cursor = g.conn.execute("""select o.*, ot.payment_type, m.price, ot.number_of_items, m.price * ot.number_of_items
    as total_price from orders o
    join menu_items m on m.recipe_name = o.recipe_name
    join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp
    where m.recipe_name = %s;""", user_input)

    # add query results to this list
    orders_for_spec_item = []

    # for a given row, we will append each cell to the list. In jinja we will populate the 
    # table one cell at a time.
    for result in cursor:
        temp = []  
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        temp.append(result[5])
        temp.append(result[6])
        temp.append(result[7])
        orders_for_spec_item.append(temp)

    cursor.close()

    # first list item is the menu, so that we can see what options
    # are available
    # make the second list item the query results
    context['data'][1] = orders_for_spec_item
    return render_template("menu_sales.html", **context)

# here is where I will execute the particular queries that 
# were input from the user regarding menu_altering
@app.route('/menu_altering_input', methods=['POST'])
def menu_altering_input():

  # retrieve user_input and store for return message
  user_input_str = request.form['query']

  # split the string by commas
  user_input = user_input_str.split(',')

  is_input_bad = 0 # initialize to false

  # If we make it here we have parsed the input
  query_mode = user_input[0]
  del user_input[0] # get rid of the query type from the parsed input
  
  #
  # determine which dynamic query we are going to do. I can only support insert and update
  #
  if query_mode.lower().strip() == 'insert':
    
    # execute the insert
    if execute_insert(user_input) == 1:
        is_input_bad = 1
    
    # query the database for the menu and append appropriate return message
    context = get_menu_from_db()
    context = add_message(context, user_input_str, is_input_bad) # append the user input to this dict
    
    # render the updated page
    return render_template("menu_altering.html", **context)
  
  elif query_mode.lower().strip() == 'update':

    # execute the update
    if execute_update(user_input) == 1:
        is_input_bad = 1

    # query the database for the menu and append the appropriate return message
    context = get_menu_from_db() 
    context = add_message(context, user_input_str, is_input_bad) # append the user input to this dict
    
    # render the updated page
    return render_template("menu_altering.html", **context)
  
  # if the input is bad, we just re-load the landing page
  else:

    # set bad input flag for the return message
    is_input_bad = 1

    # query the database for the menu and append the appropriate return message
    context = get_menu_from_db()
    context = add_message(context, user_input_str, is_input_bad) # append the user input to this dict

    # print an error log, and re render the page
    print("error: %s is not a supported query type" % query_mode)
    return render_template("menu_altering.html", **context)

# this function will take a dictionary and append the 
# user message to dictionary loc 1
def add_message(query: dict, message: str, flag: int) -> dict:

    user_in_as_list = []

    # there was an error
    if flag == 1:

        # probably want to turn into a function later on
        error_message = "Bad User Input: "
        error_message += message 
        user_in_as_list.append(error_message)

    # there was an error
    else:
        
        # probably want to turn into a function later on
        ret_message = "User Input: "
        ret_message += message
        user_in_as_list.append(ret_message)

    # append the error message to the context dict
    query['data'][1] = user_in_as_list 

    return query

# actual finances landing page that will get rendered
@app.route('/finances')
def finances():
  return render_template("finances.html")

# actual menu landing page that will get rendered
@app.route('/menu')
def menu():
    context = get_menu_from_db() # this will get rendered at all times
    return render_template("menu_home.html", **context)

# actual menu landing page that will get rendered
@app.route('/menu_altering')
def menu_altering():
    context = get_menu_from_db() # this will get rendered at all times
    return render_template("menu_altering.html", **context)

# actual menu landing page that will get rendered
@app.route('/menu_sales')
def menu_sales():

    context = get_menu_from_db() # this will get rendered at all times
    return render_template("menu_sales.html", **context)

# actual mailing list landing page that will get rendered
@app.route('/mailing_list')
def mail():

    context = get_mailing_list_from_db() # this will be rendered at all times
    return render_template("/mail.html", **context)

# get the input from the mail page
@app.route('/mail_input', methods=['POST'])
def mail_input():

    # retrieve user_input and store for return message
    user_input_str = request.form['query']
    print(user_input_str)

    # split the string by commas
    user_input = user_input_str.split(',')

    is_input_bad = 0 # initialize to false

    # If we make it here we have parsed the input
    query_mode = user_input[0]
    del user_input[0] # get rid of the query type from the parsed input

    # perform insert
    if query_mode.strip().lower() == 'insert':

        # get the date ready as a parameter for the insert
        today = date.today()
        d_format = str(today.strftime("%m-%d-%Y"))

        # execute the insert and see if the data input was bad
        if execute_mail_insert(user_input, d_format) == 1:
            is_input_bad = 1

        context = get_mailing_list_from_db() # this will be rendered at all times
        context = add_message(context, user_input_str, is_input_bad) # append the value to the dict
        return render_template("/mail.html", **context)
    
    # perform deletion
    elif query_mode.strip().lower() == 'delete':
        
        # execute the deletion and see if the data input was bad
        if execute_mail_deletion(user_input) == 1:
            is_input_bad = 1

        context = get_mailing_list_from_db() # this will be rendered at all times
        context = add_message(context, user_input_str, is_input_bad) # append the value to the dict
        return render_template("/mail.html", **context)

    # bad input
    else:

        is_input_bad = 1

        context = get_mailing_list_from_db() # this will be rendered at all times
        context = add_message(context, user_input_str, is_input_bad) # append the user input to this dict

        # print an error log, and re render the page
        print("error: %s is not a supported query type" % query_mode)
        return render_template("/mail.html", **context)

# given the user input, we will chose a slice of the data
# that will be rendered on the same version of the /finances
# landing page. Thus we will create 4 templates that inhereit from finances
# , with the names *_finances
# all of these queries will be like a "since inception" timeline
# i.e. they are static and no way to slice the data
@app.route('/finances_input', methods=['POST'])
def finances_input():

  # get the user_input
  finance_slice = request.form['cut']

  # control flow for what slice of data will render according to inhereted templates
  if finance_slice.lower() == 'all':
      all_finances_chart() # create a chart that will be embedded in the html
      context = all_finances() # run the query that pulls in all financial data
      return render_template("all_finances.html", **context) # inherits template from the finances.html page

  elif finance_slice.lower() == 'revenue':
      # create charts for our most busy times of day, and busy days of the week by order count
      restaurant_charts()
      context = orders() # run the query that pulls in all itemized transactions
      return render_template("revenue_finances.html", **context) # inherits template from the finances.html page
  
  elif finance_slice.lower() == 'labor': # here we will show the actual transaction details
      # create various charts relating to slices of our labor data
      labor_charts()
      context = labor_stuff() # run the query that pulls in all labor transactions
      return render_template("labor_finances.html", **context) # inherits template from the finances.html page
  
  elif finance_slice.lower() == 'food_costs': # here we will show the actual transaction details
      # will need to execute a function here that does the code and populates the child template
      context = ingredient_stuff() # run a multitude of queries relating to our ingredient stores
      return render_template("food_costs_finances.html",**context) # inherits template from the finances.html page
  
  # if one of the above choices aren't input, then reload the page
  else:
      return redirect('/finances')


###############################################################
#                                                             #
# EXECUTE QUERIES AND AND CHARTS AND SEND TO CORRECT LOCATION #
#                                                             #
###############################################################

# this function performs the all_finances query
# pull in all transactions, revenue, labor, and food costs
def all_finances() -> dict:

  # This list will hold 2 queries total  
  total_book = []

  #
  # Query 1, get the bottom line for our restaurant
  #
  bottom_line = []
  
  # execute the query
  cursor = g.conn.execute("""with book_adj as (with book as (select transaction_type, sum(total_price) as total_price
    from all_finances
    group by transaction_type)
    select *, 
    case when transaction_type = 'labor' then -1 * total_price 
    when transaction_type = 'food_expenses' then -1 * total_price 
    else total_price 
    end as accounting
    from book)
    select sum(book_adj.accounting) as bottom_line from book_adj;""")

  # parse the query
  for result in cursor:
      bottom_line.append(result) # we are just getting a sum total, one col and one row

  cursor.close()

  # add subquery to the total_book
  total_book.append(bottom_line)

  #
  # Query 2, get all financial transactions
  #
    
  # This is a view we defined, since the underlying with syntax was
  # very convoluted.
  cursor = g.conn.execute("select * from all_finances")

  finances = []

  # for a given row, we will append each cell to the list. In jinja we will populate the 
  # table one cell at a time.
  for result in cursor:
    temp = []  
    temp.append(result[0])
    temp.append(result[1])
    temp.append(result[2])
    temp.append(result[3])
    finances.append(temp)

  cursor.close()

  # append the results to the total book
  total_book.append(finances)
 
  # return a dictionary mapping of the data
  total_book = dict(data = total_book)
  return total_book

# generate a chart for our total book
def all_finances_chart():

    # generate the data
    cursor = g.conn.execute("""select transaction_type, sum(total_price) as total_price
    from all_finances
    group by transaction_type;""")
    
    labels = []
    data = []
    for result in cursor:
        labels.append(result[0])
        data.append(float(result[1]))

    cursor.close()

    # produce the chart and save it
    plt.pie(data, labels = labels,autopct='%.1f%%', shadow = True, explode = (0.1, 0, 0))
    plt.title('All Transactions')
    plt.axis('equal')
    plt.savefig('static/chart.jpg')
    plt.clf() # clear plot

# pull in itemized orders
def orders() -> dict:

  # pull in all orders
  cursor = g.conn.execute("""select o.*, ot.payment_type, m.price, ot.number_of_items, m.price * ot.number_of_items
  as total_price from orders o
  join menu_items m on m.recipe_name = o.recipe_name
  join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp;
  """)

  orders = []

  # for a given row, we will append each cell to the list. In jinja we will populate the 
  # table one cell at a time.
  for result in cursor:
    temp = []  
    temp.append(result[0])
    temp.append(result[1])
    temp.append(result[2])
    temp.append(result[3])
    temp.append(result[4])
    temp.append(result[5])
    temp.append(result[6])
    temp.append(result[7])
    orders.append(temp)

  cursor.close()

  # return a dictionary mapping of the data
  orders = dict(data = orders)
  return orders

# get the menu from the Database
# this will be called before and after updates to see
# any changes that have been made
def get_menu_from_db() -> dict:

    # pull in the menu
    cursor = g.conn.execute("""select * from menu_items;""")
    final_return = []

    menu_items = []
    for result in cursor:
        #print(result)
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        
        # I don't want None being populated to my screen
        if result[2] == None:
            temp.append("")
        else:
            temp.append(result[2])
        menu_items.append(temp)

    cursor.close()

    # append the query result to final_list
    final_return.append(menu_items)

    # this list will hold the future user input
    # we will return the input back to the user
    future_user_input = []
    final_return.append(future_user_input)

    # convert to dictionary
    final_return = dict(data = final_return)
    return final_return

# pull in all labor transactions
def labor_stuff() -> dict:

    # pull in all labor trans
    cursor = g.conn.execute("""select s.*,  e.name, e.job, e.hourly_salary, l.date, 
    l.hours_worked, round(e.hourly_salary * l.hours_worked,2) as money_owed  from shift_schedule s
    join employee e on e.employee_id = s.employee_id
    join labor_transaction l on l.transaction_id = s.transaction_id;""")

    labor = []

    for result in cursor:
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        temp.append(result[5])
        temp.append(result[6])
        temp.append(result[7])
        temp.append(result[8])
        labor.append(temp)

    cursor.close()

    # return a dictionary mapping of the data
    labor = dict(data = labor)
    return labor

# execute various ingredient table queries
def ingredient_stuff():

    # this list will hold multiple 3 sub query results
    ingredient_stuff = []
    
    #
    # query 1
    # pull in all ingredient purchases
    #
    cursor = g.conn.execute("""select b.transaction_id, b.farmer_id, f.name, i.date, 
    f.ingredient, i.number_of_items, f.ingredient_price, i.number_of_items * f.ingredient_price as total_cost from buys_from b
    join ingredient_transaction i on i.transaction_id = b.transaction_id
    join farmers f on f.farmer_id = b.farmer_id and f.ingredient=b.ingredient;
    """);

    purchases = []

    for result in cursor:
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        temp.append(result[5])
        temp.append(result[6])
        temp.append(result[7])
        purchases.append(temp)

    cursor.close()
    
    # add this full query 1 result to the total_list
    ingredient_stuff.append(purchases)

    #
    # query 2
    # pull in top 10 sellers by price, along with the amount stored of each ingredient and their expiration date
    #
    cursor = g.conn.execute("""with top10 as (select m.recipe_name, ot.number_of_items * m.price as total_price from orders o
    left join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp
    left join menu_items m on m.recipe_name = o.recipe_name
    order by total_price desc
    limit 10)
    select top10.recipe_name, total_price, i.* from top10
    left join uses u on u.recipe_name = top10.recipe_name
    left join ingredients i on i.item = u.item
    order by total_price desc;""")

    top10 = []

    for result in cursor:
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        top10.append(temp)

    cursor.close()
    
    # add this full query 2 result to the total_list
    ingredient_stuff.append(top10)

    #
    # query 3
    # pull in bot 10 sellers by price, along with the amount stored of each ingredient and their expiration date
    #
    cursor = g.conn.execute("""with bot10 as (select m.recipe_name, ot.number_of_items * m.price as total_price from orders o
    left join order_transaction ot on ot.transaction_id = o.transaction_id and ot.timestamp = o.timestamp
    left join menu_items m on m.recipe_name = o.recipe_name
    order by total_price asc
    limit 10) 
    select bot10.recipe_name, total_price, i.* from bot10
    left join uses u on u.recipe_name = bot10.recipe_name
    left join ingredients i on i.item = u.item
    order by total_price asc;""")

    bot10 = []

    for result in cursor:
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        bot10.append(temp)

    cursor.close()
    
    # add this full query 2 result to the total_list
    ingredient_stuff.append(bot10)

    # return a dictionary mapping of the data
    ingredients = dict(data = ingredient_stuff)
    return ingredients

# produce charts on our most busy hours of the day and busy days of the week, by order count
def restaurant_charts():
    
    #
    # run query 1 and create chart
    #
    cursor = g.conn.execute("""select extract(hour from timestamp) as order_hour, 
    count(*) from orders
    group by order_hour
    order by order_hour;""")

    data = []
    labels = []

    # parse the query results
    for result in cursor:
        if result[0] < 12:
            temp = str(int(result[0])) + " AM"
        else:
            temp = str(int(result[0])) + " PM"
        labels.append(temp)
        data.append(int(result[1]))

    cursor.close()

    # produce the chart and save it
    plt.bar(labels, data)
    plt.title("Busiest Time of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Order Count")    
    plt.savefig("static/busy.jpg")
    plt.clf() # clear the plot

    #
    # run query 2 and create chart
    #
    cursor = g.conn.execute("""with popular_day as (select *,
    case when extract(dow from timestamp) = 1 then 'Monday' 
    when extract(dow from timestamp) = 2 then 'Tuesday'
    when extract(dow from timestamp) = 3 then 'Wednesday' 
    when extract(dow from timestamp) = 4 then 'Thurdsday'
    when extract(dow from timestamp) = 5 then 'Friday' 
    when extract(dow from timestamp) = 6 then 'Saturday'
    when extract(dow from timestamp) = 7 then 'Sunday' 
    else 'Error' end as DOW, extract(dow from timestamp) as day_num from orders)
    select day_num, dow, count(*) from popular_day
    group by day_num, dow
    order by day_num;""")

    data = []
    labels = []

    # parse the query results
    for result in cursor:
        labels.append(result[1])
        data.append(result[2])
    
    cursor.close()

    # then lets produce the popular day chart
    plt.barh(labels, data)
    plt.title("Most Popular Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Order Count")    
    plt.savefig("static/dow.jpg")
    plt.clf() # clear the current plot

# pull in data to produce various labor_charts
def labor_charts():

    #
    # run query 1 and create first labor chart
    #
    cursor = g.conn.execute("""select job, count(*)
    from employee group by job;""")

    data = []
    job  = []

    # parse the query results
    for result in cursor:
        job.append(result[0])
        data.append(int(result[1]))

    cursor.close()

    # prepare some metrics for the style of the chart
    max_count = max(data)
    explode = []
    for i in range(0,len(data)):
        if data[i] != max_count:
            explode.append(0)
        else:
            explode.append(.1)

    # produce the actual chart
    plt.pie(data, labels = job, autopct='%.1f%%', shadow = True, explode=explode)
    plt.title('Count of each job type we employ')
    plt.axis('equal')
    plt.savefig("static/labor1.jpg")
    plt.show()
    plt.clf()

    #
    # run query 2 and create first labor chart
    #
    cursor = g.conn.execute("""select distinct * from (select e.name, e.date_started, 
    date_part('days', now() - date_started) as days_employed, l.hours_worked
    from shift_schedule s
    join employee e on e.employee_id = s.employee_id
    join labor_transaction l on l.transaction_id = s.transaction_id) as x
    order by days_employed desc
    limit 5;""")
    
    # store the data    
    name = []
    since_hire = []

    # parse the results
    for result in cursor:
        name.append(result[0])
        since_hire.append(int(result[2]))

    cursor.close()

    # produce the actual chart
    # do bar chart for employees who have been here the longest 
    # plot the distinct bars
    plt.bar(name, since_hire)

    # finish the actual style
    plt.title('Top 5 tenured staffers')
    plt.savefig("static/labor2.jpg")
    plt.clf()

# execute the menu insert, if the params allow us to
# return a flag for if the query succeeded or not
def execute_insert(request: list) -> int:
    
    # initialize the variables
    menu_item = ""
    price = 0
    description = ""
    
    # ensure that we can at least satisfy the menu_item and price
    # those are primary keys
    if len(request) < 2:
        print("error: not enough params for query\n")
        return 1

    # parse the menu_item name and check that it is not larger than
    # menu varchar constraint, i.e. 50
    menu_item = request[0]
    menu_item = menu_item.strip()
    del request[0]
    if len(menu_item) > 50:
        print("error: recipe_name key is too long\n")
        return 1

    # get all of the menu items, and compare it against the desired
    # input. We cannot have any duplicate keys and do not want to 
    # fail sql input constrints. So query DB, and check if key exists already
    cursor = g.conn.execute('select recipe_name from menu_items;')
    for item in cursor:
        if menu_item == item[0].strip():
            print("error: key = %s is already in the menu_items table\n" % menu_item)
            cursor.close()
            return 1

    cursor.close()

    # try to parse the string as a float
    # if not return
    try:
        price = round(float(request[0]),2)
        del request[0]
        if price < 0: # this will violate the price constraint
            print("error: price is negative, will break table constraint\n")
            return 1
        price = str(price)

    except:
        return 1

    # get the description
    if len(request) == 0 or request[0] == "NULL":
        descprition = "NULL"

    else:
        for i in range(0, len(request)):
            description += request[i]
            if i == (len(request)-1):
                continue
            else:
                description += ", "
    
    if len(description) > 200:
        print("error: description = %s is too long, will break table constraint\n" % description)
        return 1

    # if we make it here, then we are goog to execute the query
    g.conn.execute('insert into menu_items(recipe_name, price, description) values (%s, %s, %s)', (menu_item, price, description))

    # no issues
    return 0

# execute the menu update, if the params allow us to
# return a flag for if the query succeeded or not
def execute_update(request: list) -> int:
    
    # ensure that we can actually execute a given query
    if len(request) < 3:
        print("error: not enough params for query\n")
        return 1

    # initialize the variables
    # variables should be of the following format
    # request = [menu_item, column_to_update, column_value]
    menu_item = request[0].strip()
    del request[0]
    field_to_update = request[0].strip()
    del request[0]
    #
    # Ensure that the query will not fail, i.e. there exists this menu_item
    #
    valid_menu_item = 0

    # get all of the menu items, and compare it against the desired
    # input. We want to ensure that the input matches an existing key
    cursor = g.conn.execute('select recipe_name from menu_items;')
    for item in cursor:
        if menu_item == item[0].strip():
            valid_menu_item = 1
            break

    if valid_menu_item == 0:
        print("error: key = %s is not able to be updated, it is not a key\n" % menu_item)

    #
    # ensure that we can support the given field and if the param checks pass
    # execute the query
    #
    if field_to_update == 'price':
        
        # try to parse the string as a float
        # if not return
        try:
            price = round(float(request[0]),2)
            del request[0]
            if price < 0: # this will violate the price constraint
                print("error: price is negative, will break table constraint\n")
                return 1
            price = str(price)

            # if we make it here, then we are going to execute the query
            g.conn.execute('update menu_items set price = %s where recipe_name = %s', (price, menu_item))

        except:
            print("error: %s price will break the table constraint\n")
            return 1
    
    elif field_to_update == 'description':
    
        description = ""

        # get the description
        if len(request) == 0 or request[0] == "NULL":
            descprition = "NULL"

        else:
            for i in range(0, len(request)):
                description += request[i]
                if i == (len(request)-1):
                    continue
                else:
                    description += ", "
    
        if len(description) > 200:
            print("error: description = %s is too long, will break table constraint\n" % description)
            return 1

        # if we make it here, then we are going to execute the query
        g.conn.execute('update menu_items set description = %s where recipe_name = %s;', (description, menu_item))

    else:

        print("error: cannot update the following field in menu_items [%s]\n" % field_to_update)
        return 1
    
    # no issues
    return 0

# execute the deletion of a person from the mailing list
def execute_mail_deletion(request) -> int:

    # check that we can satisfy the SQL delete
    if len(request) != 1:
        print("error: incorrect params for the query\n")
        return 1

    # parse the name and check that it is not larger than
    # menu varchar constraint, i.e. 40
    name_or_email = request[0]
    name_or_email = name_or_email.strip()
    del request[0]
    if len(name_or_email) > 40:
        print("error: key = %s is too long\n" % name_or_email)
        return 1

    #
    # Determine if we are working with a name or an email
    #
    is_name = 0
    is_email = 0

    # save the data to manipulate the underlying tables
    cust_id = 0 # will only update if we are going to delete off of a name
    cust_email = 0
    cursor = g.conn.execute("""select rf.customer_id, c.name, rf.email from registers_for rf
    join mailing_list m on m.email = rf.email
    join customer c on c.customer_id = rf.customer_id;""")

    for result in cursor:
        customer_id = result[0].strip()
        cname = result[1].strip()
        email = result[2].strip()

        if name_or_email == cname:
            is_name = 1
            cust_id = customer_id # save the cust id
            cust_email = email # save the cust email
            break
        
        elif name_or_email == email:
            is_email = 1
            cust_email = email # save the cust id
            cust_id = customer_id # save the cust email
            break

    cursor.close()

    #
    # Perform the deletion from the active mailing list, i.e. registers for and in the
    # mailing list, we will keep the customer name and ID around, becuase that is valuable.
    # This type of work would be better handled by triggers, but no TIME to fix
    # However, this does work. I am able to add to list, remove from list, add to list
    # which means that no foreign key constraints are being messed up
    #
    if is_name == 1:
        g.conn.execute('delete from registers_for where customer_id = %s;', cust_id)
        g.conn.execute('delete from mailing_list where email = %s;', cust_email)
    elif is_email == 1:
        g.conn.execute('delete from registers_for where email = %s;', email)
        g.conn.execute('delete from mailing_list where email = %s;', cust_email)
    else:

        # if the input is not either a valid email, or name, the query will fail
        # return error
        print("error: sorry that name/email is not in the table\n")
        return 1

# execute the insert of arguments into the mailing list
def execute_mail_insert(request: list, date: str) -> int:
    
    # initialize the variables
    name = ""
    email = ""
    birthday = ""
    today = date

    # ensure that we can at least satisfy the SQL insert
    if len(request) != 2 and len(request) != 3:
        print("error: not enough params for query\n")
        return 1

    # parse the name and check that it is not larger than
    # menu varchar constraint, i.e. 40
    name = request[0]
    name = name.strip()
    del request[0]
    if len(name) > 40:
        print("error: name key is too long\n")
        return 1

    # parse the email and check that it is not larger than
    # menu varchar constraint, i.e. 40
    email = request[0]
    email = str(email.strip())
    del request[0]
    if len(email) > 40:
        print("error: email key is too long\n")
        return 1

    # get the birthday if it exists
    if len(request) == 0 or request[0] == "NULL":
        birthday = None

    else:
        birthday = str(request[0].strip())
        del request[0]
        # could do some further error checking on date param

    #
    # Check set of primary keys for each table to see if the keys already exist
    #

    # set of ints, use to check my randomly generated id
    custid_key = set()
    custid = 0 # use this custid if the name already exists in the DB
    customer_exists = 0

    # check to see if this name already exists, if it does make a not
    # this will tell us that we already track the customer.
    cursor = g.conn.execute('select customer_id, name from customer;')
    for item in cursor:

        # add the custid to a set in int form
        custid_key.add(int(item[0]))

        # if the customer already exists, lets pull the data
        # not a problem because we want to keep customer data regardless
        # if they choose to stay on mailing list or leave it
        if name == item[1].strip():
            print("key = %s is already in the customer table\n" % name)
            customer_exists = 1
            custid = int(item[0])

    cursor.close()

    # if the email already exists in registers_for then we are done
    cursor = g.conn.execute("""select email from registers_for;""")
    for em in cursor:

        if email == em[0].strip():
            print("error: key = %s is already in the mailing_list table\n" % email)
            cursor.close()
            return 1

    cursor.close()

    #
    # At this point the customer may or may not exist, but is definitely not
    # in the registers for relation or the mailing list
    #

    # if the customer didnt exist, then generate a customer id
    if customer_exists == 0:

        # generate a customer id, until one doesn't exist in the key set
        custid = random.randrange(1,9999999999)
        while True:

            # generate a random ID, and ensure that it is not already
            # a primary key
            custid = random.randrange(1,9999999999)
            if custid not in custid_key:
                break

    # convert the custid to a string
    custid = str(custid)

    # if the customer exists, then we need to add the email to the mailing list
    if customer_exists == 1:
    
        g.conn.execute('insert into mailing_list(email, date_signed_up, customer_birthday) values(%s, %s, %s);', (email, today, birthday))
        g.conn.execute('insert into registers_for(email, customer_id) values(%s, %s);', (email, custid))
    
    # the customer didnt exist, so we need to add everything
    elif customer_exists == 0:

        g.conn.execute('insert into mailing_list(email, date_signed_up, customer_birthday) values(%s, %s, %s);', (email, today, birthday))
        g.conn.execute("insert into customer(customer_id, name) values(%s, %s);", (custid, name))
        g.conn.execute('insert into registers_for(email, customer_id) values(%s, %s);', (email, custid))

    # no issues
    return 0

# get the mailing list from the DB
# save room for returning list to user, like in other dynamic sections
def get_mailing_list_from_db() -> dict:

    # pull in the mailing list
    cursor = g.conn.execute(""" select rf.customer_id, c.name, rf.email, m.date_signed_up, m.customer_birthday from registers_for rf
    join mailing_list m on m.email = rf.email
    join customer c on c.customer_id = rf.customer_id;""")

    final_return = []

    mailing_list = []
    
    for result in cursor:
        temp = []
        temp.append(result[0])
        temp.append(result[1])
        temp.append(result[2])
        temp.append(result[3])
        temp.append(result[4])
        
        # I don't want None being populated to my screen
        if result[1] == None:
            temp[1] = [""]
        
        if result[3] == None:
            temp[3] = [""]

        if result[4] == None:
            temp[4] = [""]
        
        mailing_list.append(temp)

    cursor.close()

    # append the query result to final_list
    final_return.append(mailing_list)

    # this list will hold the future user input
    # we will return the input back to the user
    future_user_input = []
    final_return.append(future_user_input)

    # convert to dictionary
    final_return = dict(data = final_return)
    return final_return


###############################################################
#                                                             #
# 			    Main                              #
#                                                             #
###############################################################



@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

# main
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()

