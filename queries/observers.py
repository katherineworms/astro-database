observers_select_all = """
SELECT Observers.id_observer, Observers.surname, Observers.given_name,
    Observers.title, Observers.email, Observers.phone_number,
    IFNULL(GROUP_CONCAT(Night_logs.night_date SEPARATOR ', '), "") AS "night_dates" FROM Observers
    LEFT JOIN Night_logs_has_observers ON Observers.id_observer = Night_logs_has_observers.id_observer
    LEFT JOIN Night_logs ON Night_logs_has_observers.id_night_log = Night_logs.id_night_log
    GROUP BY Observers.id_observer;
"""

observers_select_single_basic = """
SELECT * FROM Observers WHERE id_observer = {id_observer};
"""

get_all_observers_and_id = """SELECT id_observer, given_name, surname, email FROM Observers;"""

observers_insert = """
INSERT INTO Observers (surname, given_name, title, email, phone_number) VALUES
    ({surname}, {given_name}, {title}, {email}, {phone_number});
"""

observers_update_entry = """
UPDATE Observers
    SET surname = {surname}, given_name = {given_name}, title = {title}, email = {email}, phone_number = {phone_number}
    WHERE id_observer = {id_observer};
"""