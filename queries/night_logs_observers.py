night_logs_observers_select_all = """
SELECT Night_logs_has_observers.id_night_logs_has_observers,
    CONCAT(IFNULL(CONCAT(Observers.title, " "), ""), Observers.given_name, " ", Observers.surname, " (", Observers.email, ")") AS "observer",
    Night_logs.night_date FROM Night_logs_has_observers
    INNER JOIN Observers ON Night_logs_has_observers.id_observer = Observers.id_observer
    INNER JOIN Night_logs ON Night_logs_has_observers.id_night_log = Night_logs.id_night_log;
"""

night_logs_observers_insert = """
INSERT INTO Night_logs_has_observers (id_night_log, id_observer) VALUES
    ({id_night_log}, {id_observer});
"""

night_logs_observers_select_single_basic = """
SELECT * FROM Night_logs_has_observers WHERE id_night_logs_has_observers = {id_night_logs_has_observers};
"""

# Edit/Update a Night Log/Observer
night_log_observers_update_query = """
UPDATE Night_logs_has_observers
    SET id_night_log = {id_night_log}, id_observer = {id_observer}
    WHERE id_night_logs_has_observers = {id_night_logs_has_observers};
"""
