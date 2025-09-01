-- Step 1: Create the database
CREATE DATABASE empowerment;

-- Step 2: Use the database
 CREATE DATABASE empowerment;
USE empowerment;

-- Step 3: Create a users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    age VARCHAR(10),
    location VARCHAR(100)
);
