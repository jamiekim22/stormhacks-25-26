-- Insert fake security assessments for testing
-- Employee ID 1 - Multiple assessments showing improvement over time

INSERT INTO SecurityAssessments (
    employee_id, 
    security_score, 
    resistance_level, 
    social_engineering_susceptibility, 
    feedback, 
    scoring_explanation
) VALUES 
-- Employee 1 - Assessment 1 (older, poor performance)
(1, 35, 'Low', 'High', 
 'Employee fell for phishing email immediately and provided credentials without verification. Clicked on suspicious links and downloaded malicious attachment. No awareness of social engineering tactics.', 
 'Low score due to immediate response to phishing attempt, no verification steps taken, and complete credential disclosure.'),

-- Employee 1 - Assessment 2 (some improvement)
(1, 58, 'Medium', 'Medium', 
 'Employee showed some hesitation but still fell for vishing call after pressure tactics. Did ask one verification question but accepted fake answers. Some awareness but insufficient application.', 
 'Medium score reflects partial awareness - asked verification question but was easily convinced by social engineering pressure tactics.'),

-- Employee 1 - Assessment 3 (recent, much better)
(1, 82, 'High', 'Low', 
 'Employee successfully identified phishing attempt, verified caller identity through official channels, and reported suspicious activity to IT. Demonstrated excellent security awareness and proper protocols.', 
 'High score for following all security protocols: verification through official channels, rejection of suspicious requests, and proper incident reporting.'),

-- Employee 2 - Assessment 1 (moderate performance)
(2, 67, 'Medium', 'Medium', 
 'Employee was cautious but eventually provided some information after extended conversation. Recognized some red flags but was convinced by authority impersonation tactics.', 
 'Moderate score for initial caution and red flag recognition, but points deducted for eventual information disclosure under pressure.'),

-- Employee 2 - Assessment 2 (slight decline)
(2, 52, 'Low', 'High', 
 'Employee fell for CEO fraud email requesting urgent wire transfer. Failed to verify through established protocols despite training. Cited time pressure as excuse for bypassing security measures.', 
 'Lower score due to falling for authority-based social engineering despite recent training. Time pressure used as justification for protocol violations.'),

-- Employee 2 - Assessment 3 (recent improvement)
(2, 74, 'Medium', 'Low', 
 'Employee identified suspicious email patterns and forwarded to IT before responding. Made verification attempt but used secondary channel rather than primary official method. Good instincts but could improve procedure adherence.', 
 'Good score for suspicious activity recognition and IT notification. Room for improvement in following exact verification protocols.');