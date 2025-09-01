night_log_entries_select_all = """
SELECT Night_log_entries.id_night_log_entry, Night_logs.night_date, Night_log_entries.exposure_start_time_utc,
    Night_log_entries.exposure_length, Night_log_entries.elevation, Night_log_entries.azimuth,
    IFNULL(Targets.name, "") AS "target_name", IFNULL(Night_log_entries.comments, "") AS comments FROM Night_log_entries
    INNER JOIN Night_logs ON Night_log_entries.id_night_log = Night_logs.id_night_log
    LEFT JOIN Targets ON Night_log_entries.id_target = Targets.id_target
    ORDER BY Night_log_entries.exposure_start_time_utc DESC;
"""

night_logs_entries_select_single_basic = """
SELECT * FROM Night_log_entries WHERE id_night_log_entry = {id_night_log_entry};
"""

night_log_entries_insert = """
INSERT INTO Night_log_entries (exposure_start_time_utc, exposure_length, elevation, azimuth, comments, id_night_log, id_target) VALUES
    ({exposure_start_time_utc}, {exposure_length}, {elevation}, {azimuth}, {comments}, {id_night_log}, {id_target});
"""

# Update/edit any info in Night Log Entries
night_log_entries_update_query = """
UPDATE Night_log_entries
SET exposure_start_time_utc = {exposure_start_time_utc}, exposure_length = {exposure_length},
elevation = {elevation}, azimuth = {azimuth}, comments = {comments},
id_night_log = {id_night_log}, id_target = {id_target}
WHERE id_night_log_entry = {id_night_log_entry};
"""
