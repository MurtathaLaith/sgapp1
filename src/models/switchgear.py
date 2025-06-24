from src.models.user import db
import json

class Manufacturer(db.Model):
    __tablename__ = 'manufacturers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50))
    website = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'website': self.website
        }

class Contactor(db.Model):
    __tablename__ = 'contactors'
    
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    current_rating = db.Column(db.Float, nullable=False)  # Amperes
    voltage_rating = db.Column(db.Integer, nullable=False)  # Volts
    power_rating_hp = db.Column(db.Float)  # HP at 460V
    power_rating_kw = db.Column(db.Float)  # kW at 400V
    utilization_category = db.Column(db.String(10), default='AC-3')
    coil_voltage = db.Column(db.Integer, default=24)
    auxiliary_contacts = db.Column(db.String(20), default='1NO+1NC')
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    datasheet_url = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'manufacturer_id': self.manufacturer_id,
            'model': self.model,
            'current_rating': self.current_rating,
            'voltage_rating': self.voltage_rating,
            'power_rating_hp': self.power_rating_hp,
            'power_rating_kw': self.power_rating_kw,
            'utilization_category': self.utilization_category,
            'coil_voltage': self.coil_voltage,
            'auxiliary_contacts': self.auxiliary_contacts,
            'price': self.price,
            'image_url': self.image_url,
            'datasheet_url': self.datasheet_url
        }

class OverloadRelay(db.Model):
    __tablename__ = 'overload_relays'
    
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    current_range_min = db.Column(db.Float, nullable=False)  # Minimum current in Amperes
    current_range_max = db.Column(db.Float, nullable=False)  # Maximum current in Amperes
    trip_class = db.Column(db.String(10), default='Class 10')
    reset_type = db.Column(db.String(20), default='Manual')
    price = db.Column(db.Float)
    image_url = db.Column(db.String(200))
    datasheet_url = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'manufacturer_id': self.manufacturer_id,
            'model': self.model,
            'current_range_min': self.current_range_min,
            'current_range_max': self.current_range_max,
            'trip_class': self.trip_class,
            'reset_type': self.reset_type,
            'price': self.price,
            'image_url': self.image_url,
            'datasheet_url': self.datasheet_url
        }

class StartingMethod(db.Model):
    __tablename__ = 'starting_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    min_power_hp = db.Column(db.Float)  # Minimum motor power in HP
    max_power_hp = db.Column(db.Float)  # Maximum motor power in HP
    starting_current_factor = db.Column(db.Float, default=6.0)  # Multiple of FLC
    contactors_required = db.Column(db.Integer, default=1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_power_hp': self.min_power_hp,
            'max_power_hp': self.max_power_hp,
            'starting_current_factor': self.starting_current_factor,
            'contactors_required': self.contactors_required
        }

