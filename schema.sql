CREATE TABLE participants (
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    email VARCHAR(255) NOT NULL,
    team_name VARCHAR(100) NOT NULL,
    qr_data MEDIUMTEXT NOT NULL

);
