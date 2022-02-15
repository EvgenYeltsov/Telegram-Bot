from app import db


# Table model

class trafo_list(db.Model):
	""" For correct migration existing DB, class name in lower case """

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name_substation = db.Column(db.String)
	customer_name =db.Column(db.String)
	country = db.Column(db.String)
	transformer_type = db.Column(db.String)
	asset_group = db.Column(db.String)
	serial_number = db.Column(db.String, nullable=False )
	manufacturing_year = db.Column(db.Integer)
	brand = db.Column(db.String)
	operational_status = db.Column(db.String)
	application = db.Column(db.String)
	number_phases = db.Column(db.String)
	insulation_type = db.Column(db.String)
	type_oil = db.Column(db.String)
	type_cooling_equipment = db.Column(db.String)
	rated_voltage_hv = db.Column(db.Integer)
	rated_voltage_mv = db.Column(db.Integer)
	rated_voltage_lv = db.Column(db.Integer)
	rated_power = db.Column(db.Integer)
	vector_group = db.Column(db.String)
	number_tapchanger = db.Column(db.String)
	type_tapchanger = db.Column(db.String)
	type_cooling = db.Column(db.String)


class users_list(db.Model):

	__tablename__ ='users'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	user_name = db.Column(db.String)
	user_email = db.Column(db.String, nullable=False)
	user_telegram_id = db.Column(db.Integer, nullable=False)
	permission_status = db.Column(db.Boolean, default=False, nullable=False)
	verifying_status = db.Column(db.Boolean, default=False, nullable=False)
