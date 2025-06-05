-- Opret løbere
CREATE TABLE Runner (
    Runner_ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Joined_date DATE NOT NULL
);

-- Opret løb 
CREATE TABLE Run_event (
    Run_event_ID SERIAL PRIMARY KEY,
    Date DATE NOT NULL,
    Duration INTERVAL NOT NULL,
    Temperature INTEGER,
    Distance FLOAT
);

-- Registrering af deltagelse
CREATE TABLE Participation (
    Runner_ID INT REFERENCES Runner(Runner_ID),
    Run_event_ID INT REFERENCES Run_event(Run_event_ID),
    Run_Distance FLOAT NOT NULL,
    Run_Time INTERVAL NOT NULL,
    PRIMARY KEY (Runner_ID, Run_event_ID)
);




