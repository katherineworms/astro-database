from flask import render_template, request, redirect, url_for
from web_app.main import bp
from web_app.main.forms import *
from web_app import mysql
from web_app.queries.night_logs import *
from web_app.queries.observation_sites import *
from web_app.queries.night_log_entries import *
from web_app.queries.observers import *
from web_app.queries.targets import *
from web_app.queries.night_logs_observers import *


# Index Page
@bp.route('/')
def index_page():
    return render_template("index.html")



##### Routes for Observation Sites #####
# Add to Observation Sites
@bp.route('/observation_sites', methods=['GET', 'POST'])
def observation_sites():
    form = ObservationSitesForm()
    cursor = mysql.connection.cursor()
    # Handle form submission to add.
    if request.method == 'POST':
        # Prepare data to save.
        name = None if form.name.data is None else "'" + form.name.data + "'"
        latitude = None if form.latitude.data is None else "'" + str(form.latitude.data) + "'"
        longitude = None if form.longitude.data is None else "'" + str(form.longitude.data) + "'"
        el = None if form.el.data is None else "'" + str(form.el.data) + "'"
        notes = None if form.notes.data is None else "'" + form.notes.data + "'"
        # Insert data!
        insert_sql = observation_sites_insert.format(name=name, latitude=latitude, longitude=longitude, elevation=el, notes=notes)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(observation_sites_select_all)
    results = cursor.fetchall()
    return render_template("observation_sites.html", results=results, form=form)

# Update Observation Sites
@bp.route('/observation_sites/update/<int:entry_id>', methods=['GET', 'POST'])
def observation_sites_update(entry_id):
    form = ObservationSitesForm()
    cursor = mysql.connection.cursor()
    # Get current data for initial values.
    cursor.execute(observation_sites_select_single_basic.format(id_observation_site=entry_id))
    current_entry = cursor.fetchall()
    if request.method == 'POST' and form.validate_on_submit():
        # Prepare data to save.
        id_observation_site = current_entry[0]["id_observation_site"]
        name = "NULL" if form.name.data is None else "'" + form.name.data + "'"
        latitude = None if form.latitude.data is None else "'" + str(form.latitude.data) + "'"
        longitude = None if form.longitude.data is None else "'" + str(form.longitude.data) + "'"
        el = None if form.el.data is None else "'" + str(form.el.data) + "'"
        notes = None if form.notes.data is None else "'" + form.notes.data + "'"
        # Fill in SQL String.
        sql = observation_sites_update_entry.format(name=name, latitude=latitude, longitude=longitude, elevation=el, notes=notes, id_observation_site = id_observation_site)
        # Execute update.
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        # Redirect to Observers table.
        return redirect(url_for("main.observation_sites"))
    # Set the initial values.  AFTER post to prevent overwritting submitted data.
    form.name.data = current_entry[0]["name"]
    form.latitude.data = current_entry[0]["latitude"]
    form.longitude.data = current_entry[0]["longitude"]
    form.el.data = current_entry[0]["elevation"]
    form.notes.data = current_entry[0]["notes"]
    return render_template("observation_sites_update.html", form=form)

# Delete from Observation Sites 
@bp.route('/observation_sites/delete/<int:entry_id>')
def delete_observation_site(entry_id):
    #mySQL query to delete observation site with the passed id
    query = "DELETE FROM Observation_sites WHERE id_observation_site = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to observation sites page
    return redirect("/observation_sites")



##### Routes for Night Logs #####
# Add to Night Logs
@bp.route('/night_logs', methods=['GET', 'POST'])
def night_logs():
    form = NightLogForm()
    # Get observation site choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_sites_name_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices.
    choices = [(choice["id_observation_site"], choice["name"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.observation_site.choices = choices
    # Handle form submission to add.
    if request.method == 'POST' and int(form.observation_site.data) > 0:
        # Prepare data to save.
        night_date = "NULL" if form.night_date.data is None else "'" + form.night_date.data.strftime("%Y-%m-%d") + "'"
        start_time = "NULL" if form.start_time.data is None else "'" + form.start_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        end_time = "NULL" if form.end_time.data is None else "'" + form.end_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        observation_site = form.observation_site.data
        # Insert data!
        insert_sql = night_logs_insert.format(night_date=night_date, start_time=start_time, end_time=end_time, id_observation_site=observation_site)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(night_logs_select_all)
    results = cursor.fetchall()
    return render_template("night_logs.html", results=results, form=form)

# Update Night Logs
# Citation for the form.process to set the defualt of the SelectField:
# Date: 2023-11-16
# Based on:
# Source URL: https://wtforms.readthedocs.io/en/2.3.x/forms/
@bp.route('/night_logs/update/<int:entry_id>', methods=['GET', 'POST'])
def night_logs_update(entry_id):
    form = NightLogForm()
    # Get observation site choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_sites_name_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices.
    choices = [(choice["id_observation_site"], choice["name"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.observation_site.choices = choices
    # Get current data for initial values.
    cursor.execute(night_logs_select_single_basic.format(id_night_log=entry_id))
    current_entry = cursor.fetchall()
    if request.method == "POST":  # Form submitted.
        # Prepare data to save.
        id_night_log = current_entry[0]["id_night_log"]
        night_date = "NULL" if form.night_date.data is None else "'" + form.night_date.data.strftime("%Y-%m-%d") + "'"
        start_time = "NULL" if form.start_time.data is None else "'" + form.start_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        end_time = "NULL" if form.end_time.data is None else "'" + form.end_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        observation_site = form.observation_site.data
        # Fill in SQL String.
        sql = night_logs_update_entry.format(night_date=night_date, start_time=start_time, end_time=end_time, id_observation_site=observation_site, id_night_log=id_night_log)
        # Execute update.
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        # Redirect to Night Logs table.
        return redirect(url_for("main.night_logs"))
    # Set the initial values.  AFTER post to prevent overwritting submitted data.
    form.observation_site.default = current_entry[0]["id_observation_site"]
    form.process()
    form.night_date.data = current_entry[0]["night_date"]
    form.start_time.data = current_entry[0]["start_time"]
    form.end_time.data = current_entry[0]["end_time"]
    return render_template("night_logs_update.html", form=form)

# Delete from Night Logs
@bp.route('/night_logs/delete/<int:entry_id>')
def delete_night_logs(entry_id):
    #mySQL query to delete the night log with the passed id
    query = "DELETE FROM Night_logs WHERE id_night_log = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to night logs page
    return redirect("/night_logs")



##### Routes for Night Log Entries #####
# Add to Night log entries 
@bp.route('/night_log_entries', methods=['GET', 'POST'])
def night_log_entries():
    form = NightLogEntriesForm()
    # Get night logs choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_night_log_dates_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for night log.
    choices = [(choice["id_night_log"], choice["night_date"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.night_log_date.choices = choices
    # Get target choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_target_names_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for target.
    choices = [(choice["id_target"], choice["name"]) for choice in results]
    choices = [(-1, "None")] + choices  # Add placeholder option at the start.
    form.target.choices = choices
    # Handle form submission to add.
    if request.method == 'POST':
        # Prepare data to save.
        exposure_start_time_utc = "NULL" if form.start_time.data is None else "'" + form.start_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        exposure_length = "NULL" if form.exp_time.data is None else "'" + str(form.exp_time.data) + "'"
        elevation = "NULL" if form.el.data is None else "'" + str(form.el.data) + "'"
        azimuth = "NULL" if form.az.data is None else "'" + str(form.az.data) + "'"
        night_log = "'" + str(form.night_log_date.data) + "'"
        target = form.target.data
        if str(target) == "-1":
            target = "NULL"
        comments = "NULL" if form.comments.data is None else "'" + form.comments.data + "'"
        # Insert data!
        insert_sql = night_log_entries_insert.format(exposure_start_time_utc = exposure_start_time_utc, exposure_length = exposure_length, elevation = elevation, azimuth = azimuth, comments = comments, id_night_log = night_log, id_target = target)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(night_log_entries_select_all)
    results = cursor.fetchall()
    return render_template("night_log_entries.html", results=results, form=form)

# Update Night log entries 
@bp.route('/night_log_entries/update/<int:entry_id>', methods=['GET', 'POST'])
def night_log_entries_update(entry_id):
    form = NightLogEntriesForm()
    # Get night logs choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_night_log_dates_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for night log.
    choices = [(choice["id_night_log"], choice["night_date"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.night_log_date.choices = choices
    # Get target choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_target_names_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for target.
    choices = [(choice["id_target"], choice["name"]) for choice in results]
    choices = [(-1, "None")] + choices  # Add placeholder option at the start.
    form.target.choices = choices
    # Get current data for initial values.
    cursor.execute(night_logs_entries_select_single_basic.format(id_night_log_entry=entry_id))
    current_entry = cursor.fetchall()
    # Handle form submission to update.
    if request.method == 'POST':
        id_night_log_entry = current_entry[0]["id_night_log_entry"]
        exposure_start_time_utc = "NULL" if form.start_time.data is None else "'" + form.start_time.data.strftime("%Y-%m-%d %H:%M:%S") + "'"
        exposure_length = "NULL" if form.exp_time.data is None else "'" + str(form.exp_time.data) + "'"
        elevation = "NULL" if form.el.data is None else "'" + str(form.el.data) + "'"
        azimuth = "NULL" if form.az.data is None else "'" + str(form.az.data) + "'"
        night_log = str(form.night_log_date.data)
        target = str(form.target.data)
        if target == "-1":
            target = "NULL"
        comments = "NULL" if form.comments.data is None else "'" + form.comments.data + "'"
        # Insert data!
        update_sql = night_log_entries_update_query.format(
            exposure_start_time_utc = exposure_start_time_utc,
            exposure_length = exposure_length,
            elevation = elevation,
            azimuth = azimuth,
            comments = comments,
            id_night_log = night_log,
            id_target = target,
            id_night_log_entry = id_night_log_entry
        )
        cursor.execute(update_sql)
        mysql.connection.commit()
        return redirect(url_for("main.night_log_entries"))
    # Set the initial values.  AFTER post to prevent overwritting submitted data.
    form.target.default = current_entry[0]["id_target"]
    form.night_log_date.default = current_entry[0]["id_night_log"]
    form.process()  # To commit the select field defualts.
    form .start_time.data = current_entry[0]["exposure_start_time_utc"]
    form.exp_time.data = current_entry[0]["exposure_length"]
    form.el.data = current_entry[0]["elevation"]
    form.az.data = current_entry[0]["azimuth"]
    form.comments.data = current_entry[0]["comments"]
    return render_template("night_log_entries_update.html", form=form)

# Delete from night log entries 
@bp.route('/night_log_entries/delete/<int:entry_id>')
def delete_night_log_entries(entry_id):
    #mySQL query to delete the night log entry with the passed id
    query = "DELETE FROM Night_log_entries WHERE id_night_log_entry = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to night log entries page
    return redirect("/night_log_entries")



##### Routes for Observers #####
# Add to Observers
@bp.route('/observers', methods=['GET', 'POST'])
def observers():
    form = ObserverForm()
    cursor = mysql.connection.cursor()
    # Handle form submission to add.
    if request.method == 'POST':
        # Prepare data to save.
        surname = "NULL" if form.surname.data is None else "'" + form.surname.data + "'"
        given_name = "NULL" if form.given_name.data is None else "'" + form.given_name.data + "'"
        title = "NULL" if form.title.data is None else "'" + form.title.data + "'"
        email = "NULL" if form.email.data is None else "'" + form.email.data + "'"
        phone_number = "NULL" if form.phone_number.data is None else "'" + form.phone_number.data + "'"
        # Insert data!
        insert_sql = observers_insert.format(surname=surname, given_name=given_name, title=title, email=email, phone_number=phone_number)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(observers_select_all)
    results = cursor.fetchall()
    return render_template("observers.html", results=results, form=form)

# Update Observers
@bp.route('/observers/update/<int:entry_id>', methods=['GET', 'POST'])
def observers_update(entry_id):
    form = ObserverForm()
    cursor = mysql.connection.cursor()
    # Get current data for initial values.
    cursor.execute(observers_select_single_basic.format(id_observer=entry_id))
    current_entry = cursor.fetchall()
    if request.method == 'POST' and form.validate_on_submit():
        # Prepare data to save.
        id_observer = current_entry[0]["id_observer"]
        surname = "NULL" if form.surname.data is None else "'" + form.surname.data + "'"
        given_name = "NULL" if form.given_name.data is None else "'" + form.given_name.data + "'"
        title = "NULL" if form.title.data is None else "'" + form.title.data + "'"
        email = "NULL" if form.email.data is None else "'" + form.email.data + "'"
        phone_number = "NULL" if form.phone_number.data is None else "'" + form.phone_number.data + "'"
        # Fill in SQL String.
        sql = observers_update_entry.format(surname=surname, given_name=given_name, title=title, email=email, phone_number=phone_number, id_observer = id_observer)
        # Execute update.
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        # Redirect to Observers table.
        return redirect(url_for("main.observers"))
    # Set the initial values.  AFTER post to prevent overwritting submitted data.
    form.surname.data = current_entry[0]["surname"]
    form.given_name.data = current_entry[0]["given_name"]
    form.title.data = current_entry[0]["title"]
    form.email.data = current_entry[0]["email"]
    form.phone_number.data = current_entry[0]["phone_number"]
    return render_template("observers_update.html", form=form)

# Delete from Observers
@bp.route('/observers/delete/<int:entry_id>')
def delete_observers(entry_id):
    #mySQL query to delete observer with the passed id
    query = "DELETE FROM Observers WHERE id_observer = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to observers page
    return redirect("/observers")



##### Routes for Targets #####
# Add to Targets
@bp.route('/targets', methods=['GET', 'POST'])
def targets():
    form = TargetForm()
    cursor = mysql.connection.cursor()
    # Handle form submission to add.
    if request.method == 'POST':
        # Prepare data to save.
        name = None if form.name.data is None else "'" + form.name.data + "'"
        type = None if form.type.data is None else "'" + form.type.data + "'"
        ra = None if form.ra.data is None else "'" + form.ra.data + "'"
        dec = None if form.dec.data is None else "'" + form.dec.data + "'"
        epoch = None if form.epoch.data is None else "'" + form.epoch.data + "'"
        notes = None if form.notes.data is None else "'" + form.notes.data + "'"
        # Insert data!
        insert_sql = targets_insert.format(name=name, type=type, ra=ra, dec=dec, epoch=epoch, notes=notes)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(targets_select_all)
    results = cursor.fetchall()
    return render_template("targets.html", results=results, form=form)

# Update Targets
@bp.route('/targets/update/<int:entry_id>', methods=['GET', 'POST'])
def targets_update(entry_id):
    form = TargetForm()
    cursor = mysql.connection.cursor()
    # Get current data for initial values.
    cursor.execute(targets_select_single_basic.format(id_target=entry_id))
    current_entry = cursor.fetchall()
    if request.method == 'POST':
        # Prepare data to save.
        name = None if form.name.data is None else "'" + form.name.data + "'"
        type = None if form.type.data is None else "'" + form.type.data + "'"
        ra = None if form.ra.data is None else "'" + form.ra.data + "'"
        dec = None if form.dec.data is None else "'" + form.dec.data + "'"
        epoch = None if form.epoch.data is None else "'" + form.epoch.data + "'"
        notes = None if form.notes.data is None else "'" + form.notes.data + "'"
        # Fill in SQL String.
        sql = targets_update_entry.format(name=name, type=type, ra=ra, deci=dec, epoch=epoch, notes=notes, id_target = entry_id)
        # Execute update.
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        mysql.connection.commit()
        # Redirect to Targets table.
        return redirect(url_for("main.targets"))
    # Set the initial values.  AFTER post to prevent overwritting submitted data.
    form.name.data = current_entry[0]["name"]
    form.type.data = current_entry[0]["type"]
    form.ra.data = current_entry[0]["ra"]
    form.dec.data = current_entry[0]["deci"]
    form.epoch.data = current_entry[0]["epoch"]
    form.notes.data = current_entry[0]["notes"]
    return render_template("targets_update.html", form=form)

# Delete from Targets
@bp.route('/targets/delete/<int:entry_id>')
def delete_target(entry_id):
    #mySQL query to delete observation site with the passed id
    query = "DELETE FROM Targets WHERE id_target = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to observation sites page
    return redirect("/targets")



##### Routes for Observer and Night Date Relationship #####
# Add to Observer and Night Date Relationship
@bp.route('/night_logs_observers', methods=['GET', 'POST'])
def night_logs_observers():
    form = NightLogsObserversForm()
    # Get observers choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_observers_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for observer.
    choices = [(choice["id_observer"], f"{choice['given_name']} {choice['surname']} ({choice['email']})") for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.observer.choices = choices
    # Get night date choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_night_log_dates_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for target.
    choices = [(choice["id_night_log"], choice["night_date"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.night_date.choices = choices
    # Handle form submission to add.
    if request.method == 'POST':
        # Prepare data to save.
        observer = "NULL" if form.observer.data is None else form.observer.data
        night_log = "'" + str(form.night_date.data) + "'"
        # Insert data!
        insert_sql = night_logs_observers_insert.format(id_night_log = night_log, id_observer = observer)
        cursor.execute(insert_sql)
        mysql.connection.commit()
    # Get data for table
    cursor.execute(night_logs_observers_select_all)
    results = cursor.fetchall()
    return render_template("night_logs_observers.html", results=results, form=form)

# Update Observer and Night log Relationship 
@bp.route('/night_logs_observers/update/<int:entry_id>', methods=['GET', 'POST'])
def night_logs_observers_update(entry_id):
    form = NightLogsObserversForm()
    # Get observers choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_observers_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for observer.
    choices = [(choice["id_observer"], f"{choice['given_name']} {choice['surname']} ({choice['email']})") for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.observer.choices = choices
    # Get night date choices.
    cursor = mysql.connection.cursor()
    cursor.execute(get_all_night_log_dates_and_id)
    results = cursor.fetchall()
    # Set the drop-down choices for target.
    choices = [(choice["id_night_log"], choice["night_date"]) for choice in results]
    choices = [(-1, "[Select]")] + choices  # Add placeholder option at the start.
    form.night_date.choices = choices
    # Get current data for initial values.
    cursor.execute(night_logs_observers_select_single_basic.format(id_night_logs_has_observers=entry_id))
    current_entry = cursor.fetchall()
    # Handle form submission to add.
    if request.method == 'POST':
        id_night_logs_has_observers = current_entry[0]["id_night_logs_has_observers"]
        id_night_log = str(form.night_date.data)
        id_observer = str(form.observer.data)
        # Insert data!
        update_sql = night_log_observers_update_query.format(
            id_night_log = id_night_log,
            id_observer = id_observer,
            id_night_logs_has_observers = id_night_logs_has_observers
        )
        cursor.execute(update_sql)
        mysql.connection.commit()
        return redirect(url_for("main.night_logs_observers"))
    form.observer.default = current_entry[0]["id_observer"]
    form.night_date.default = current_entry[0]["id_night_log"]
    form.process()  # To commit the select field defualts.
    return render_template("night_logs_observers_update.html", form=form)

# Delete from observer and night date relationship 
@bp.route('/night_logs_observers/delete/<int:entry_id>')
def delete_night_logs_has_observers(entry_id):
    #mySQL query to delete observation site with the passed id
    query = "DELETE FROM Night_logs_has_observers WHERE id_night_logs_has_observers = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query,(entry_id,))
    mysql.connection.commit()

    # redirect back to observation sites page
    return redirect("/night_logs_observers")
