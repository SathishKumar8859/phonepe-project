SELECT * FROM phonepe.transactions;
select * from top_transaction;
select * from transaction_hover;
select state,year,sum(amount) as total_amount
from transactions 
group by state, year
order by year asc;

select quarter,year,sum(amount) as total_amount
from transactions 
group by quarter,year
order by quarter, year ;

SELECT quarter, year, 
SUM(amount) AS total_amount ,avg(amount) as avg_amount , max(amount) as max_amount , min(amount) as min_amount
FROM transactions
GROUP BY quarter, year
ORDER BY year ASC, quarter ASC;

-- top 10 transaction by state
select state,sum(amount)as total_amount
from transactions
group by state
order by total_amount desc limit 10;

select transaction_name,sum(count)as Total_count,sum(amount)as total_amount 
from transactions
group by transaction_name
order by total_amount desc;

select * from insurance;
select transaction_type,sum(count),sum(amount) 
from insurance
group by transaction_type;

select
 state, year,sum(count)as Total_count,sum(amount)as Total_amount
 from insurance
group by state, year
order by year ;

select quarter,sum(amount)as Total_amount,sum(Count)as Totyal_count 
from insurance
group by quarter
order by Total_amount desc;

select year,quarter,sum(amount)as Total_amount,sum(Count)as Totyal_count 
from insurance
group by year,quarter
order by Total_amount desc;

select * from user ;

select brand,sum(count)as Total_count
from user
group by brand ;

select brand,sum(count)as Total_count , sum(percentage) as total_percentage
from user
group by brand 
order by Total_count desc;

select state,brand,sum(count)as Total_count , sum(percentage) as total_percentage
from user
group by state,brand 
order by Total_count desc;

select state,brand,sum(count)as Total_count 
from user
group by state,brand 
order by Total_count desc;

select year,brand, sum(percentage)as Total_count 
from user
group by year,brand 
order by Total_count desc;

select * from top_insurance;
select category, entityname,sum(insuranceCount) as Total_insurance , sum(insuranceAmount)as total_amount
from top_insurance
group by category, entityname 
order by category;

select category,sum(insuranceCount) as Total_insurance , sum(insuranceAmount)as total_amount
from top_insurance
group by category
order by category;
select year,quarter,sum(insuranceCount) as Total_insurance , sum(insuranceAmount)as total_amount
from top_insurance
group by year,quarter 
order by year,quarter ;

select * from user_hover;
select year,quarter,sum(registeredUsers) as Total_registeredUsers , sum(appOpens)as total_appOpens
from user_hover
group by year,quarter 
order by year,quarter ;

select sate, year,quarter,sum(registeredUsers) as Total_registeredUsers , sum(appOpens)as total_appOpens
from user_hover
group by sate,year,quarter 
order by year,quarter ;

select quarter,sum(registeredUsers) as Total_registeredUsers , sum(appOpens)as total_appOpens
from user_hover
group by quarter 
order by quarter ;

select t.year,u.brand,u.quarter,t.total_amount from
(select	year , sum(amount) as total_amount 
from transactions group by year ) as t
join user as u
on  u.year = t.year 
order by total_amount ;

