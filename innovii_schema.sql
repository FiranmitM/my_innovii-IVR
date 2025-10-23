-- File Location: /etc/asterisk/innovii_schema.sql
-- Database Schema for INNOVII IVR System
-- Import this file: mysql -u innovii -p'innovii@1234' innovii < /etc/asterisk/innovii_schema.sql

-- Drop tables if they exist (for fresh installation)
DROP TABLE IF EXISTS call_logs;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS lesson_progress;
DROP TABLE IF EXISTS subscribers;

-- Subscribers table
CREATE TABLE subscribers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    subscribed TINYINT(1) DEFAULT 1,
    preferred_language VARCHAR(10) DEFAULT 'amharic',
    subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_call_date TIMESTAMP NULL,
    total_calls INT DEFAULT 0,
    INDEX idx_phone (phone_number),
    INDEX idx_subscribed (subscribed)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Lesson progress tracking
CREATE TABLE lesson_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    service_type ENUM('beauty', 'mother_health', 'child_health') NOT NULL,
    current_lesson INT DEFAULT 1,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    lessons_completed INT DEFAULT 0,
    FOREIGN KEY (phone_number) REFERENCES subscribers(phone_number) ON DELETE CASCADE,
    UNIQUE KEY unique_progress (phone_number, service_type),
    INDEX idx_phone_service (phone_number, service_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Questions asked by users
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    service_type ENUM('beauty', 'health') NOT NULL,
    question_audio_file VARCHAR(255),
    asked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    answered TINYINT(1) DEFAULT 0,
    answer_audio_file VARCHAR(255) NULL,
    FOREIGN KEY (phone_number) REFERENCES subscribers(phone_number) ON DELETE CASCADE,
    INDEX idx_phone (phone_number),
    INDEX idx_date (asked_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Call logs for analytics
CREATE TABLE call_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    call_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    call_duration INT DEFAULT 0,
    service_accessed VARCHAR(50),
    language_used VARCHAR(10),
    menu_path TEXT,
    FOREIGN KEY (phone_number) REFERENCES subscribers(phone_number) ON DELETE CASCADE,
    INDEX idx_phone (phone_number),
    INDEX idx_date (call_start)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert some test data for testing
INSERT INTO subscribers (phone_number, subscribed, preferred_language) VALUES
('1001', 1, 'amharic'),
('1002', 1, 'oromo'),
('1003', 0, 'amharic');

-- Insert initial lesson progress for test users
INSERT INTO lesson_progress (phone_number, service_type, current_lesson) VALUES
('1001', 'beauty', 1),
('1001', 'mother_health', 1),
('1002', 'beauty', 1);

-- Grant permissions (ensure the innovii user has full access)
GRANT ALL PRIVILEGES ON innovii.* TO 'innovii'@'localhost';
FLUSH PRIVILEGES;

-- Show created tables
SHOW TABLES;
