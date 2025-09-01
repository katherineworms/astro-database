-- AstroDB - Astronomical Observation Database
-- Group 67
-- Andrew Neugarten and Katherine Worms
-- Data Manipulation Queries



------------------------ Night Logs Page ------------------------

-- Get all data for the Night_logs table:
-- Note:  Details regarding the GROUP_CONCAT function where found at the following URL:
-- https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat
SELECT Night_logs.id_night_log, Night_logs.night_date, Observers.surname, Observation_sites.name AS "observation_site", Night_logs.start_time, Night_logs.end_time,
    GROUP_CONCAT(CONCAT(IFNULL(CONCAT(Observers.title, " "), ""), Observers.given_name, " ", Observers.surname, " (", Observers.email, ")") SEPARATOR ', ') AS "Observers" From Night_logs
    LEFT JOIN Observation_sites ON Night_logs.id_observation_site = Observation_sites.id_observation_site
    LEFT JOIN Night_logs_has_observers ON Night_logs.id_night_log = Night_logs_has_observers.id_night_log
    LEFT JOIN Observers ON Night_logs_has_observers.id_observer = Observers.id_observer
    GROUP BY Night_logs.id_night_log
    ORDER BY Night_logs.night_date DESC;

-- Select all columns for a single night log row.  Used to populate the update form.
SELECT * FROM Night_logs WHERE id_night_log = :id_night_log;

-- Select night log id and night date
SELECT id_night_log, night_date FROM Night_logs;

-- get all Observation site IDs and Names to populate the Observation Site dropdown
SELECT id_observation_site, name FROM Observation_sites ORDER BY name;

-- INSERT into Night_logs: start a new night log
INSERT INTO Night_logs (night_date, start_time, end_time, id_observation_site) VALUES
(:night_dateInput, :start_timeInput, :end_timeInput, :id_observation_site_from_dropdownInput);

-- Update/edit any information Night_logs
UPDATE Night_logs
SET night_date = :night_dateInput, start_time = :start_timeInput, end_time = :end_timeInput, id_observation_site = :id_observation_site_from_dropdownInput
WHERE id_night_log = :id_night_log_from_the_update_form;

-- Delete a night log
DELETE FROM Night_logs WHERE id = :id_night_log_selected_from_browse_night_logs_page;




------------------------ Night Log Entries ------------------------

-- Get all night log entries.
SELECT Night_log_entries.id_night_log_entry, Night_logs.night_date, Night_log_entries.exposure_start_time_utc,
    Night_log_entries.exposure_length, Night_log_entries.elevation, Night_log_entries.azimuth,
    IFNULL(Targets.name, "") AS "target_name", IFNULL(Night_log_entries.comments, "") AS comments FROM Night_log_entries
    INNER JOIN Night_logs ON Night_log_entries.id_night_log = Night_logs.id_night_log
    LEFT JOIN Targets ON Night_log_entries.id_target = Targets.id_target
    ORDER BY Night_log_entries.exposure_start_time_utc DESC;

-- get all Night log IDs and Dates to populate the Night Log dropdown
SELECT id_night_log, night_date FROM Night_logs;

-- get all Target IDs and Names to populate the Target dropdown
SELECT id_target, name FROM Targets ORDER BY name;

-- Select a specific row by ID.  Used to populate update form's initial data.
SELECT * FROM Night_log_entries WHERE id_night_log_entry = :id_night_log_entryInput;

-- INSERT into Night_log_entries: add a new entry to an exisiting night log
INSERT INTO Night_log_entries (exposure_start_time_utc, exposure_length, elevation, azimuth, comments, id_night_log, id_target) VALUES
(:exposure_start_time_utcInput, :exposure_lengthInput, :elevationInput, :azimuthInput, :commentsInput, :id_night_log_from_dropdownInput, :id_target_from_dropdownInput);

-- Update/edit any info in Night Log Entries
UPDATE Night_log_entries
SET exposure_start_time_utc = :exposure_start_time_utcInput, exposure_length = :exposure_lengthInput, elevation = :elevationInput, azimuth = :azimuthInput, comments = :commentsInput,
id_night_log = :id_night_log_from_dropdownInput, target = :id_target_from_dropdownInput
WHERE id_night_log = :id_night_log_from_the_update_form;

-- Delete an entry from a night log
DELETE FROM Night_log_entries WHERE id = :id_night_log_entry_selected_from_browse_night_log_entries_page;




------------------------ Observation Sites ------------------------

-- Select all rows from the observation sites table.
SELECT id_observation_site, name, latitude, longitude, elevation, IFNULL(notes, "") AS notes FROM Observation_sites;

-- get all details from Observation_sites
SELECT * FROM Observation_sites;

-- Get all observation sites with observation_site_id
SELECT * FROM Observers WHERE id_observer = :id_observer;

-- INSERT into Observation_sites: add new site
INSERT INTO Observation_sites (name, latitude, longitude, elevation, notes) VALUES
(:nameInput, :latitudeInput, :longitudeInput, :elevationInput, :notesInput);

UPDATE Observation_sites
SET name = :nameInput, latitude = :latitudeInput, longitude = :longitudeInput, elevation = :elevationInput, notes = :notes,
WHERE id_observation_site = :id_observation_site_from_the_update_form;

-- Delete an observation site
DELETE FROM Observation_sites WHERE id = :id_observation_site_selected_from_browse_observation_site_page;




------------------------ Observers ------------------------

-- Get all observers and their observation night.
SELECT Observers.id_observer, Observers.surname, Observers.given_name,
    Observers.title, Observers.email, Observers.phone_number,
    IFNULL(GROUP_CONCAT(Night_logs.night_date SEPARATOR ', '), "") AS "night_dates" FROM Observers
    LEFT JOIN Night_logs_has_observers ON Observers.id_observer = Night_logs_has_observers.id_observer
    LEFT JOIN Night_logs ON Night_logs_has_observers.id_night_log = Night_logs.id_night_log
    GROUP BY Observers.id_observer;

-- Get all observers with observer_id
SELECT * FROM Observers WHERE id_observer = :id_observer;

-- Get all observers and id
SELECT id_observer, given_name, surname, email FROM Observers;

-- INSERT into Observers: add new Observer
INSERT INTO Observers (surname, given_name, title, email, phone_number) VALUES
(:surnameInput, :given_nameInput, :titleInput, :emailInput, :phone_numberInput);

-- Update Observer info
UPDATE Observers
SET surname = :surnameInput, given_name = :given_nameInput, title = :titleInput, email = :emailInput, phone_number = :phone_numberInput
WHERE id_observer = :id_observer_from_the_update_form;

-- Delete an observer
DELETE FROM Observers WHERE id = :id_observer_selected_from_browse_observers_page;




------------------------ Targets ------------------------

-- Select all rows from the targets table.
SELECT id_target, name, type, IFNULL(ra, "") AS ra,
    IFNULL(deci, "") AS deci, IFNULL(epoch, "") AS epoch, IFNULL(notes, "") AS notes FROM Targets;

-- Get target id and name from targets
SELECT id_target, name FROM Targets;

-- Get everything for a specific target id
SELECT * FROM Targets WHERE id_target = :id_target;

-- INSERT into Targets: add new Target
INSERT INTO Targets (name, type, ra, deci, epoch, notes) VALUES
(:nameInput, :typeInput, :raInput, :deciInput, :epochInput, :notesInput);

-- Update Targets
UPDATE Targets
SET name = :nameInput, type = :typeInput, ra = :raInput, deci = :deciInput, epoch = :epochInput, notes = :notesInput
WHERE id_target = :id_target_from_the_update_form;

-- Delete a target
DELETE FROM Targets WHERE id = :id_target_selected_from_browse_targets_page;




------------------------ Observer and Night Date Relationship ------------------------

-- Get all observers and night_dates from the night log observers relationship table.
SELECT Night_logs_has_observers.id_night_logs_has_observers,
    CONCAT(IFNULL(CONCAT(Observers.title, " "), ""), Observers.given_name, " ", Observers.surname, " (", Observers.email, ")") AS "observer",
    Night_logs.night_date FROM Night_logs_has_observers
    INNER JOIN Observers ON Night_logs_has_observers.id_observer = Observers.id_observer
    INNER JOIN Night_logs ON Night_logs_has_observers.id_night_log = Night_logs.id_night_log;

-- get all Night log IDs and Dates to populate the Night dropdown
SELECT id_night_log, night_date FROM Night_logs;

-- get all Observer IDs and Names to populate the Observer dropdown
SELECT id_observer, name FROM Observers;

-- Select a specific row.  Used to populate update form with initial data.
SELECT * FROM Night_logs_has_observers WHERE id_night_logs_has_observers = :id_night_logs_has_observersinput;

--INSERT INTO Night_logs_has_observers (M:N relationship addition)
INSERT INTO Night_logs_has_observers (id_night_log, id_observer) VALUES
(:id_night_log_from_dropdownInput, :id_obsever_from_dropdownInput);

--Edit/Update a Night Log/Observer
UPDATE Night_logs_has_observers
SET id_night_log = :update_night_log_drop_down, id_observer = :update_observer_drop_down
WHERE id_night_logs_has_observers = :id_night_logs_has_observers;

--Dis-associate a night log from an observer (M:M relationship deletion)
DELETE FROM Night_logs_has_observers WHERE id_night_log = :id_night_log_selected_from_night_log_and_observer_list AND id_observer = :id_observer_selected_from_night_log_and_observer_list;
