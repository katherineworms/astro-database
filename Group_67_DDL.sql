-- AstroDB - Astronomical Observation Database
-- Group 67
-- Andrew Neugarten and Katherine Worms
-- Data Definition Queries



SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS Observation_sites, Observers, Targets, Night_logs, Night_log_entries;


-- Create Observation_sites table
CREATE OR REPLACE TABLE Observation_sites (
    id_observation_site INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL,
    latitude DECIMAL(19,6) NOT NULL,
    longitude DECIMAL(19,6) NOT NULL,
    elevation FLOAT NOT NULL,
    notes VARCHAR(300),
    PRIMARY KEY (id_observation_site)
);

-- Create Night_logs table
CREATE OR REPLACE TABLE Night_logs (
    id_night_log INT NOT NULL AUTO_INCREMENT,
    night_date DATE NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    id_observation_site INT NOT NULL,
    PRIMARY KEY (id_night_log),
    UNIQUE (night_date),
    FOREIGN KEY (id_observation_site) REFERENCES Observation_sites(id_observation_site)
    ON DELETE CASCADE
);

-- Create Observers table
CREATE OR REPLACE TABLE Observers (
    id_observer INT NOT NULL AUTO_INCREMENT,
    surname VARCHAR(300) NOT NULL,
    given_name VARCHAR(300) NOT NULL,
    title VARCHAR(45),
    email VARCHAR(300) NOT NULL,
    phone_number VARCHAR(45),
    PRIMARY KEY (id_observer), 
    UNIQUE (email)
);

-- Create Night_log_entries table
CREATE OR REPLACE TABLE Night_log_entries (
    id_night_log_entry INT NOT NULL AUTO_INCREMENT,
    exposure_start_time_utc DATETIME NOT NULL,
    exposure_length FLOAT NOT NULL,
    elevation FLOAT NOT NULL,
    azimuth DECIMAL(19,3) NOT NULL,
    comments MEDIUMTEXT,
    id_night_log INT NOT NULL,
    id_target INT NULL,
    PRIMARY KEY (id_night_log_entry),
    UNIQUE (id_night_log_entry),
    FOREIGN KEY (id_night_log) REFERENCES Night_logs(id_night_log) ON DELETE CASCADE,
    FOREIGN KEY (id_target) REFERENCES Targets(id_target) ON DELETE SET NULL
);

-- Create Targets table
CREATE OR REPLACE TABLE Targets (
    id_target INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL,
    type VARCHAR(45) NOT NULL DEFAULT 'star',
    ra VARCHAR(45),
    deci VARCHAR(45),
    epoch VARCHAR(45),
    notes VARCHAR(300),
    PRIMARY KEY (id_target)
);

-- Create Night_logs_has_observers table
CREATE OR REPLACE TABLE Night_logs_has_observers (
    id_night_logs_has_observers INT NOT NULL AUTO_INCREMENT,
    id_night_log INT NOT NULL,
    id_observer INT NOT NULL,
    PRIMARY KEY (id_night_logs_has_observers),
    FOREIGN KEY (id_night_log) REFERENCES Night_logs(id_night_log) ON DELETE CASCADE,
    FOREIGN KEY (id_observer) REFERENCES Observers(id_observer) ON DELETE CASCADE
);




-- Insert example data into tables
INSERT INTO Observation_sites (
    name,
    latitude,
    longitude,
    elevation,
    notes
)
VALUES
(
    "Lowell - NURO",
    35.096944,
    -111.535833,
    2163,
    "Reflecting telescope, primary mirror = 0.79m"
),
(
    "Subaru Telescope",
    19.8256,
    -155.4761,
    4139,
    "Ritchey-Chretien"
),
(
    "IRTF",
    19.8263,
    -155.473,
    4205,
    NULL
);

INSERT INTO Observers (
    surname,
    given_name,
    title,
    email,
    phone_number
)
VALUES
(
    "Neugarten",
    "Andrew",
    "Mr.",
    "1@example.com",
    "+1 (555) 555-5555"
),
(
    "Worms",
    "Katherine",
    "Mrs.",
    "2@example.com",
    "+1 (555) 555-5555"
),
(
    "Inconnue",
    "Femme",
    "Mme",
    "3@example.com",
    "+33 5 55 55 55 55"
),
(
    "Doe",
    "John",
    NULL,
    "4@example.com",
    "+1 (555) 555-5555"
);

INSERT INTO Targets (
    name,
    type,
    ra,
    deci,
    epoch,
    notes
)
VALUES
(
    "AZ Vir",
    "Binary Star",
    "13 43 25.65",
    "+04 36 57.0",
    "J2000.0",
    "10.74 - 11.37 V"
),
(
    "KID 11405559",
    "Binary Star",
    "19 32 54.15",
    "+49 14 33.3",
    "J2000.0",
    "W Ursae Majoris-type eclipsing binary."
),
(
    "Saturn",
    "Planet",
    NULL,
    NULL,
    NULL,
    "Lots of rings!"
),
(
    "Virgo",
    "Star",
    "02 31 49.09",
    "+89 15 50.8",
    "J2000.0",
    NULL
);

INSERT INTO Night_logs (
    night_date,
    start_time,
    end_time,
    id_observation_site
)
VALUES
(
    "2023-10-01",
    "2023-10-01 18:00:00",
    "2023-10-02 06:00:00",
    1
),
(
    "2023-10-02",
    "2023-10-02 18:00:00",
    "2023-10-03 06:00:00",
    1
),
(
    "2023-10-05",
    "2023-10-06 00:00:00",
    "2023-10-02 06:05:00",
    2
),
(
    "2023-10-08",
    "2023-10-08 19:00:00",
   "2023-10-09 00:00:00",
    2
),
(
    "2023-10-09",
    NULL,
    NULL,
    3
);

INSERT INTO Night_log_entries (
    exposure_start_time_utc,
    exposure_length,
    elevation,
    azimuth,
    comments,
    id_night_log,
    id_target
)
VALUES
(
    "2023-10-01 18:00:00",
    60,
    90.400,
    45.000,
    NULL,
    1,
    1
),
(
    "2023-10-01 18:01:30",
    60,
    89.767,
    46.000,
    "Aborted due to clouds",
    1,
    1
),
(
    "2023-10-01 18:03:00",
    60,
    88.995,
    46.900,
    NULL,
    1,
    1
),
(
    "2023-10-02 18:00:00",
    45,
    60.554,
    45.612,
    "Unusable, headlights.",
    2,
    2
),
(
    "2023-10-06 00:00:00",
    600,
    54.635,
    77.568,
    NULL,
    3,
    4
),
(
    "2023-10-08 19:00:00",
    18000,
    30.123,
    45.586,
    NULL,
    4,
    3
);

INSERT INTO Night_logs_has_observers (
    id_night_log,
    id_observer
)
VALUES
(
    1,
    1
),
(
    1,
    2
),
(
    2,
    3
),
(
    3,
    4
),
(
    4,
    4
),
(
    5,
    3
);



SET FOREIGN_KEY_CHECKS = 1;
COMMIT;
