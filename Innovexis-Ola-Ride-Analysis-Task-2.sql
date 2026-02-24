create database Innovexis_Task_2;
use Innovexis_Task_2;
select * from `ola_data.csv`;
-- Checking Duplicates -- 
select count(*) as Total_count, Customer_ID from `ola_data.csv` group by Customer_ID having count(*) > 1;
select Distinct Customer_ID from `ola_data.csv`;

-- Checking nulls -- 
select Distinct Customer_ID,Payment_Method from `ola_data.csv` where Payment_Method is null;
set sql_safe_updates = 0;
update `ola_data.csv` set payment_method = "UPI" where Vehicle_Type in('Prime Sedan', 'Prime SUV', 'Prime Plus');
update `ola_data.csv` set payment_method = "Cash" where Vehicle_Type in('Mini', 'Auto', 'Bike','eBike');

-- All Successfull Bookings --
select Distinct Customer_ID, Booking_Status from `ola_data.csv` where Booking_Status = "Success";

-- Average ride distance per vehicle type -- 
select round(avg(Ride_Distance),0) as Average_distance, Vehicle_Type from `ola_data.csv` group by Vehicle_Type;

-- Total number of cancelled rides by customers -- 
select Canceled_Rides_by_Customer,count(*) as Total_Customers from `ola_data.csv` where Canceled_Rides_by_Customer not in("NULL") group by Canceled_Rides_by_Customer;

-- Top 5 Customers Who booked the highest numbers of rides -- 
select Customer_ID,count(*) as Total_count from `ola_data.csv` where Booking_Status = "Success" group by Customer_ID order by Total_count DESC limit 5;

-- Number of bookings cancelled by drivers due to some personal and car related issues --
select Canceled_Rides_by_Driver, count(*) as Total_Canceled from `ola_data.csv` where Canceled_Rides_by_Driver in('Personal & Car related issue') group by Canceled_Rides_by_Driver;

-- max and min driver ratings for prime sedan -- 
select max(Driver_Ratings) as max_rating, min(Driver_ratings) as min_rating from `ola_data.csv` where Vehicle_Type = "Prime Sedan";

-- All rides having payment mode UPI --
select * from `ola_data.csv` where Payment_Method = "UPI";

-- average customer rating per vehicle type -- 
select Vehicle_Type,round(avg(Customer_Rating),4) as avg_rating from `ola_data.csv` group by Vehicle_Type;

-- Total booking value for rides completed successfully -- 
select Customer_ID, sum(Booking_Value) as Total_Revenue from `ola_data.csv` where Booking_Status = "Success" 
group by Customer_ID;

-- List all incomplete rides with reason -- 
select * from `ola_data.csv` where Incomplete_Rides = "Yes"; 