night_logs_select_all = """
SELECT Night_logs.id_night_log, Night_logs.night_date, Observers.surname, Observation_sites.name AS "observation_site", Night_logs.start_time, Night_logs.end_time,
    GROUP_CONCAT(CONCAT(IFNULL(CONCAT(Observers.title, " "), ""), Observers.given_name, " ", Observers.surname, " (", Observers.email, ")") SEPARATOR ', ') AS "Observers" From Night_logs
    LEFT JOIN Observation_sites ON Night_logs.id_observation_site = Observation_sites.id_observation_site
    LEFT JOIN Night_logs_has_observers ON Night_logs.id_night_log = Night_logs_has_observers.id_night_log
    LEFT JOIN Observers ON Night_logs_has_observers.id_observer = Observers.id_observer
    GROUP BY Night_logs.id_night_log
    ORDER BY Night_logs.night_date DESC;
"""

night_logs_select_single_basic = """
SELECT * FROM Night_logs WHERE id_night_log = {id_night_log};
"""

get_all_night_log_dates_and_id = """
SELECT id_night_log, night_date FROM Night_logs;"""

night_logs_insert = """
INSERT INTO Night_logs (night_date, start_time, end_time, id_observation_site) VALUES
    ({night_date}, {start_time}, {end_time}, {id_observation_site});
"""

night_logs_update_entry = """
UPDATE Night_logs
    SET night_date = {night_date}, start_time = {start_time}, end_time = {end_time}, id_observation_site = {id_observation_site}
    WHERE id_night_log = {id_night_log};
"""