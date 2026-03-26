CREATE DATABASE IF NOT EXISTS telco_churn_db;
USE telco_churn_db;

CREATE TABLE IF NOT EXISTS customers (
    customerID VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(20),
    InternetService VARCHAR(20),
    OnlineSecurity VARCHAR(20),
    OnlineBackup VARCHAR(20),
    DeviceProtection VARCHAR(20),
    TechSupport VARCHAR(20),
    StreamingTV VARCHAR(20),
    StreamingMovies VARCHAR(20),
    Contract VARCHAR(20),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(8,2),
    TotalCharges DECIMAL(10,2),
    Churn VARCHAR(5)
);




SELECT COUNT(*) AS total_customers
FROM customers;

SELECT Churn, COUNT(*) AS total
FROM customers
GROUP BY Churn;


SELECT Contract, 
       COUNT(*) AS total_customers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_percentage
FROM customers
GROUP BY Contract;


SELECT InternetService, 
       COUNT(*) AS total_customers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_percentage
FROM customers
GROUP BY InternetService;


SELECT PaymentMethod, 
       COUNT(*) AS total_customers,
       SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
       ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_percentage
FROM customers
GROUP BY PaymentMethod;


SELECT Churn, AVG(MonthlyCharges) AS avg_monthly_charges
FROM customers
GROUP BY Churn;


SELECT Churn, AVG(tenure) AS avg_tenure
FROM customers
GROUP BY Churn;
SELECT *
FROM customers
WHERE MonthlyCharges > 80 AND Churn = 'Yes';