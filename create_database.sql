-- Create StormHacks25 Database
CREATE DATABASE StormHacks25;

-- Use the StormHacks25 database
USE StormHacks25;

-- Create Employees table
CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15)
);

-- Optional: Insert some sample data (uncomment if needed)
-- INSERT INTO Employees (name, phone_number) VALUES 
-- ('John Doe', '555-0123'),
-- ('Jane Smith', '555-0456'),
-- ('Mike Johnson', '555-0789');