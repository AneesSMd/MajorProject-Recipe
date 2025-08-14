CREATE DATABASE IF NOT EXISTS food;

-- Switch to the created database
USE food;

-- Create the user table
CREATE TABLE `users` (
    `username` VARCHAR(225),
    `email` VARCHAR(225),
    `password` VARCHAR(225)
    );
