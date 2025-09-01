from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, FloatField, TextAreaField, StringField, DecimalField
from wtforms.fields import DateTimeLocalField, DateField
from wtforms.validators import DataRequired

class NightLogForm(FlaskForm):
    night_date = DateField("*Night Date (UTC)", validators=[DataRequired()])
    start_time = DateTimeLocalField("Start Time (UTC)")
    end_time = DateTimeLocalField("End Time (UTC)")
    observation_site = SelectField("Observation Site")
    submit = SubmitField("Save!")
    #exp_time = FloatField("Exposure Time (S)", id="night_log_form_exp_time", validators=[DataRequired()])
    #el = FloatField("Telescope Elevation", id="night_log_form_el", validators=[DataRequired()])
    #az = FloatField("Telescope Azimuth", id="night_log_form_az", validators=[DataRequired()])

class NightLogEntriesForm(FlaskForm):
    start_time = DateTimeLocalField("*Exposure Start Time (UTC)", validators=[DataRequired()])
    exp_time = FloatField("*Exposure Length (S)", validators=[DataRequired()])
    el = FloatField("*Telescope Elevation", validators=[DataRequired()])
    az = FloatField("*Telescope Azimuth", validators=[DataRequired()])
    comments = TextAreaField("Comments")
    night_log_date = SelectField("*Night Log")
    target = SelectField("Target")
    submit = SubmitField("Save!")

class ObservationSitesForm(FlaskForm):
    name = StringField("*Name", validators=[DataRequired()])
    latitude = DecimalField("*Latitude", validators=[DataRequired()])
    longitude = DecimalField("*Longitude", validators=[DataRequired()])
    el = FloatField("*Elevation", validators=[DataRequired()])
    notes = StringField("Notes")
    submit = SubmitField("Save!")

class ObserverForm(FlaskForm):
    surname = StringField("*Surname", validators=[DataRequired()])
    given_name = StringField("*Given Name", validators=[DataRequired()])
    title = StringField("Title")
    email = StringField("*Email", validators=[DataRequired()])
    phone_number = StringField("Phone Number")
    submit = SubmitField("Save!")

class TargetForm(FlaskForm):
    name = StringField("*Name", validators=[DataRequired()])
    type = StringField("*Target Type", validators=[DataRequired()])
    ra = StringField("Right Ascension", validators=[])
    dec = StringField("Declination", validators=[])
    epoch = StringField("Epoch", validators=[])
    notes = StringField("Notes", validators=[])
    submit = SubmitField("Save!")

class NightLogsObserversForm(FlaskForm):
    db_id = IntegerField("ID")
    observer = SelectField("*Observer", validators=[DataRequired()])
    night_date = SelectField("*Night", validators=[DataRequired()])
    submit = SubmitField("Save!")
