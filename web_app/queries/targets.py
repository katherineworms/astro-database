targets_select_all = """
SELECT id_target, name, type, IFNULL(ra, "") AS ra,
    IFNULL(deci, "") AS deci, IFNULL(epoch, "") AS epoch, IFNULL(notes, "") AS notes FROM Targets;
"""

get_all_target_names_and_id = """SELECT id_target, name FROM Targets;"""


targets_select_single_basic = """
SELECT * FROM Targets WHERE id_target = {id_target};
"""

targets_update_entry = """
UPDATE Targets
    SET name = {name}, type = {type}, ra = {ra}, deci = {deci}, epoch = {epoch}, notes = {notes}
    WHERE id_target = {id_target};
"""

targets_insert = """
INSERT INTO Targets (name, type, ra, deci, epoch, notes) VALUES
    ({name}, {type}, {ra}, {dec}, {epoch}, {notes});
"""