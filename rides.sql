use ola_project;
#1. Retrieve all successful bookings:
#SELECT * from rides where Booking_Status = 'Success';

#2. Find the average ride distance for each vehicle type:
#select Vehicle_Type, avg (Ride_distance)
#from rides
#group by Vehicle_Type;

#3.Get the total number of cancelled rides by customers:
#select  count(*) from rides where Booking_Status = 'Canceled_Rides_by_Customer'

#4.List the top 5 customers who booked the highest number of rides
#select Customer_ID, count(*) as total_rides from rides
#group by Customer_ID
#order by total_rides desc
#limit 5;

#5.Get the number of rides cancelled by drivers due to personal and car-related issues:
#SELECT COUNT(*)
#FROM rides
#WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

#6.Find the maximum and minimum driver ratings for Prime Sedan bookings
#SELECT 
 #   MIN(Driver_Ratings) AS minimum_rating,
  #  MAX(Driver_Ratings) AS maximum_rating
#FROM rides
#WHERE Vehicle_Type = 'Prime Sedan';

#7.. Retrieve all rides where payment was made using UPI:
#select * from rides 
#where Payment_Method ='UPI'

#8.Find the average customer rating per vehicle type
#select
#Vehicle_Type, avg(Customer_Rating) 
#from rides
#group by vehicle_type

#9.. Calculate the total booking value of rides completed successfully. 
#select 
#sum(Booking_Value) from rides
#where booking_status ='Success'

#10.List all incomplete rides along with the reason
#select incomplete_rides , incomplete_rides_reason
#from rides
#where Incomplete_Rides='yes'







