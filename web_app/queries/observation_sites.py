observation_sites_select_all = """SELECT * FROM Observation_sites;"""

get_all_sites_name_and_id = """SELECT id_observation_site, name FROM Observation_sites;"""

observation_sites_select_single_basic = """
SELECT * FROM Observation_sites WHERE id_observation_site = {id_observation_site};
"""

observation_sites_insert = """
INSERT INTO Observation_sites (name, latitude, longitude, elevation, notes) VALUES
    ({name}, {latitude}, {longitude}, {elevation}, {notes});
"""

observation_sites_update_entry = """
UPDATE Observation_sites
    SET name = {name}, latitude = {latitude}, longitude = {longitude}, elevation = {elevation}, notes = {notes}
    WHERE id_observation_site = {id_observation_site};
"""