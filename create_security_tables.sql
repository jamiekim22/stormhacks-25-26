-- Create tables for Security Assessment data in StormHacks25 database
USE StormHacks25;

-- Create Security Assessments table
CREATE TABLE SecurityAssessments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    security_score INT NOT NULL,
    resistance_level ENUM('Low', 'Medium', 'High') NOT NULL,
    social_engineering_susceptibility ENUM('Low', 'Medium', 'High') NOT NULL,
    feedback TEXT,
    scoring_explanation TEXT,
    FOREIGN KEY (employee_id) REFERENCES Employees(id) ON DELETE CASCADE
);

-- Create Data Collected table (for tracking what data was compromised)
CREATE TABLE DataCollected (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT,
    mfa_code VARCHAR(10),
    password_compromised BOOLEAN DEFAULT FALSE,
    username_compromised BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (assessment_id) REFERENCES SecurityAssessments(id) ON DELETE CASCADE
);

-- Create Other Info table (for additional compromised information)
CREATE TABLE OtherInfoCollected (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_collected_id INT,
    info_type VARCHAR(100),
    info_value TEXT,
    FOREIGN KEY (data_collected_id) REFERENCES DataCollected(id) ON DELETE CASCADE
);

-- Create Key Mistakes table
CREATE TABLE KeyMistakes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT,
    mistake_description TEXT NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES SecurityAssessments(id) ON DELETE CASCADE
);

-- Create Successful Defenses table
CREATE TABLE SuccessfulDefenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    assessment_id INT,
    defense_description TEXT NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES SecurityAssessments(id) ON DELETE CASCADE
);

-- Sample insert based on the provided data
-- INSERT INTO SecurityAssessments (employee_id, security_score, resistance_level, social_engineering_susceptibility, feedback, scoring_explanation) 
-- VALUES (1, 1, 'Low', 'High', 'Never provide an MFA code or password to an unsolicited caller. Legitimate IT support will never ask for this information. Always verify the request through a known, official channel, like calling the company\'s main helpdesk number directly.', 'Critical Failure: Provided the MFA code immediately upon request with no resistance.');

-- INSERT INTO DataCollected (assessment_id, mfa_code, password_compromised, username_compromised) 
-- VALUES (1, '808818', FALSE, FALSE);

-- INSERT INTO KeyMistakes (assessment_id, mistake_description) VALUES 
-- (1, 'Provided the MFA code without any verification of the caller\'s identity'),
-- (1, 'Did not question the urgency or the nature of the \'security alert\'');