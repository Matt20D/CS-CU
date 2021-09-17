#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 18:44:37 2021

@author: matt20d
"""

import matplotlib.pyplot as plt

def all_finances_chart():
    data   = [350, 400, 1000]
    labels = ['revenue', 'food_expenses', 'labor']
    plt.pie(data, labels = labels,autopct='%.1f%%', shadow = True, explode = (0.1, 0, 0))
    plt.title('All Transactions')
    plt.axis('equal')
    plt.savefig("chart.jpg")
    plt.show()
    plt.clf()

#all_finances_chart()

def busy_time():
    
    # first lets produce the popular hours chart
    data = [ 10, 20, 30, 40 ,50 ]
    labels = ['8 AM', '9 AM', '10 AM', '11 AM', '12 AM']

    plt.bar(labels, data)
    plt.title("Busiest Time of Day")
    plt.xlabel("Time of Day")
    plt.ylabel("Order Count")    
    plt.savefig("busy.jpg")
    plt.show()
    plt.clf()
    
    # then lets produce the popular day chart
    data = [12, 12, 6]
    labels = ['Thursday', 'Friday', 'Saturday']
    plt.barh(labels, data)
    plt.title("Most Popular Day of Week")
    plt.xlabel("Day of Week")
    plt.ylabel("Order Count")    
    plt.savefig("dow.jpg")
    plt.show()
    plt.clf()


def labor_charts():

    # do the chart dynamically, which can change for the count of each jobs we employ
    data = [16,10,15]
    job  = ['manager', 'waiter', 'cleaner']
    max_count = max(data)
    explode = []
    for i in range(0,len(data)):
        if data[i] != max_count:
            explode.append(0)
        else:
            explode.append(.1)
    
    plt.pie(data, labels = job, autopct='%.1f%%', shadow = True, explode=explode)
    plt.title('Count of each job type we employ')
    plt.axis('equal')
    plt.savefig("labor1.jpg")
    plt.show()
    plt.clf()
    
    # do double bar chart for employees who have been here the longest and worked the most
    # reference number  13
    name = ['Matthew', 'Daniel']
    days_since_hire = [1000, 800]
    hours_worked = [300, 300]
    
    width = .25
    bar1_tick = []
    for i in range(0, len(name)):
        bar1_tick.append(i)
    bar2_tick = [x + width for x in bar1_tick]
    
    plt.bar(bar1_tick, days_since_hire, width = width, label = 'days_since_hire')
    plt.bar(bar2_tick, hours_worked, width = width, label = 'total_hours_worked')
    
    plt.xticks([r+width for r in range(0,len(bar1_tick))] , labels = name)
    plt.title('Days since hire v total hours worked')
    plt.savefig("labor2.jpg")
    plt.legend()
    plt.show()
    plt.clf()
    
    
    
   
all_finances_chart()
busy_time()
labor_charts()