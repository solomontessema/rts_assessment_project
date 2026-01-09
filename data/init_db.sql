-- 1. Connect to the project database (Run this if database already exists)
-- \c real_estate_corp;

-- 2. Drop tables if they exist to start fresh
DROP TABLE IF EXISTS Financials;
DROP TABLE IF EXISTS Properties;

-- 3. Create Properties Table
-- Stores the physical characteristics of the assets
CREATE TABLE Properties (
    property_id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    metro_area VARCHAR(100) NOT NULL,
    sq_footage INTEGER CHECK (sq_footage > 0),
    property_type VARCHAR(50) NOT NULL -- Residential, Commercial, Industrial
);

-- 4. Create Financials Table
-- Stores the performance metrics, linked to Properties
CREATE TABLE Financials (
    financial_id SERIAL PRIMARY KEY,
    property_id INTEGER UNIQUE REFERENCES Properties(property_id) ON DELETE CASCADE,
    revenue NUMERIC(15, 2) DEFAULT 0,
    net_income NUMERIC(15, 2) DEFAULT 0,
    expenses NUMERIC(15, 2) DEFAULT 0
);

-- 5. Insert 20 Sample Property Records
INSERT INTO Properties (address, metro_area, sq_footage, property_type) VALUES
('101 Wall St', 'New York', 50000, 'Commercial'),
('202 Ocean Dr', 'Miami', 3500, 'Residential'),
('303 Industrial Pkwy', 'Chicago', 25000, 'Industrial'),
('404 Tech Ln', 'San Francisco', 12000, 'Commercial'),
('505 Maple Ave', 'Chicago', 2800, 'Residential'),
('606 Warehouse Way', 'New York', 30000, 'Industrial'),
('707 Sunset Blvd', 'Los Angeles', 4500, 'Residential'),
('808 Commerce St', 'Austin', 15000, 'Commercial'),
('909 Factory Rd', 'Detroit', 40000, 'Industrial'),
('111 Pine Cir', 'Atlanta', 3200, 'Residential'),
('222 Market Sq', 'Philadelphia', 22000, 'Commercial'),
('333 River Rd', 'Chicago', 18000, 'Industrial'),
('444 Peak View', 'Denver', 3100, 'Residential'),
('555 Plaza Dr', 'Dallas', 27000, 'Commercial'),
('666 Bridge St', 'Seattle', 9000, 'Industrial'),
('777 Valley Rd', 'Phoenix', 2900, 'Residential'),
('888 Center St', 'Boston', 14000, 'Commercial'),
('999 Port Ave', 'Houston', 55000, 'Industrial'),
('123 Garden Ln', 'Portland', 2600, 'Residential'),
('456 Urban Sq', 'New York', 19000, 'Commercial');

-- 6. Insert Corresponding Financial Records
-- Populating data for all 20 properties
INSERT INTO Financials (property_id, revenue, net_income, expenses) VALUES
(1, 5000000, 1500000, 3500000), (2, 120000, 45000, 75000),
(3, 1200000, 400000, 800000),  (4, 2500000, 900000, 1600000),
(5, 85000, 30000, 55000),      (6, 3000000, 1100000, 1900000),
(7, 150000, 60000, 90000),     (8, 1800000, 700000, 1100000),
(9, 4500000, 1200000, 3300000),(10, 95000, 35000, 60000),
(11, 2200000, 850000, 1350000),(12, 1800000, 600000, 1200000),
(13, 110000, 40000, 70000),    (14, 3100000, 1300000, 1800000),
(15, 950000, 300000, 650000),  (16, 90000, 25000, 65000),
(17, 1600000, 650000, 950000), (18, 5200000, 2100000, 3100000),
(19, 88000, 32000, 56000),     (20, 2400000, 950000, 1450000);