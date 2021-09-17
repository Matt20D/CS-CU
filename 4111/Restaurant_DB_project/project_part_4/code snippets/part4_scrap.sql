-- array query

with first_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as first_half_perf from first_half
where array_order in (1,2,3,4,5,6)
group by employee_id;


with second_half as (select employee_id, array_order, performance
from performance_reviews, unnest(emp_performance_rating_bymonth)
with ordinality as T (performance, array_order))
select employee_id, avg(performance) as first_half_perf from second_half
where array_order in (7,8,9,10,11,12)
group by employee_id;


-- this is the big one
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
join avg2 on avg2.employee_id = avg1.employee_id;

