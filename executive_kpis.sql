/*This script extracts business metrics from the 
car_sales_data table. The results from these queries inputed into SQLite (DB Browser for SQLite)
validate the executive KPIs and leaderboards built in the final Tableau dashboard.
*/

--Checking dataset works
SELECT * 
FROM car_sales_data 
LIMIT 10;

--Total company performance
SELECT 
    SUM("Sale Price") AS Total_Revenue,
    SUM("Commission Earned") AS Total_Commission,
    AVG("Sale Price") AS Average_Sale_Price
FROM car_sales_data;

--Salesperson leaderboard
SELECT 
    Salesperson,
    COUNT(*) AS Total_Cars_Sold,
    SUM("Sale Price") AS Total_Revenue
FROM car_sales_data
GROUP BY Salesperson
ORDER BY Total_Revenue DESC;


--Most value vehicles(top 25)
SELECT	
	"Car Make",
	"Car Model",
	COUNT(*) AS Total_Units_Sold,
	SUM("Sale Price") AS Total_Revenue,
	AVG("Sale Price") AS Average_Price
FROM car_sales_data
GROUP BY "Car Make", "Car Model"
ORDER BY Total_Revenue DESC