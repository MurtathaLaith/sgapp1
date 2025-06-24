#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models.user import db
from src.models.switchgear import Manufacturer, Contactor, OverloadRelay, StartingMethod

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if data already exists
        if Manufacturer.query.count() > 0:
            print("Database already initialized")
            return
        
        # Add manufacturers
        manufacturers = [
            Manufacturer(name='ABB', country='Switzerland', website='https://new.abb.com'),
            Manufacturer(name='Schneider Electric', country='France', website='https://www.se.com'),
            Manufacturer(name='Siemens', country='Germany', website='https://www.siemens.com'),
            Manufacturer(name='Eaton', country='USA', website='https://www.eaton.com')
        ]
        
        for mfg in manufacturers:
            db.session.add(mfg)
        db.session.commit()
        
        # Add contactors
        contactors = [
            Contactor(manufacturer_id=1, model='A9-30-10', current_rating=32, voltage_rating=600, power_rating_hp=15, power_rating_kw=11, price=45.00),
            Contactor(manufacturer_id=1, model='A12-30-10', current_rating=40, voltage_rating=600, power_rating_hp=20, power_rating_kw=15, price=55.00),
            Contactor(manufacturer_id=2, model='LC1D25M7', current_rating=25, voltage_rating=600, power_rating_hp=10, power_rating_kw=7.5, price=38.00),
            Contactor(manufacturer_id=2, model='LC1D32M7', current_rating=32, voltage_rating=600, power_rating_hp=15, power_rating_kw=11, price=48.00),
            Contactor(manufacturer_id=3, model='3RT1026-1BB40', current_rating=25, voltage_rating=600, power_rating_hp=10, power_rating_kw=7.5, price=42.00)
        ]
        
        for contactor in contactors:
            db.session.add(contactor)
        db.session.commit()
        
        # Add overload relays
        overloads = [
            OverloadRelay(manufacturer_id=1, model='TF42-16', current_range_min=11, current_range_max=16, price=65.00),
            OverloadRelay(manufacturer_id=1, model='TF42-25', current_range_min=17, current_range_max=25, price=65.00),
            OverloadRelay(manufacturer_id=2, model='LRD21', current_range_min=12, current_range_max=18, price=58.00),
            OverloadRelay(manufacturer_id=2, model='LRD22', current_range_min=16, current_range_max=24, price=58.00)
        ]
        
        for overload in overloads:
            db.session.add(overload)
        db.session.commit()
        
        # Add starting methods
        methods = [
            StartingMethod(name='Direct On-Line (DOL)', description='Direct connection to supply', min_power_hp=0.5, max_power_hp=15, contactors_required=1),
            StartingMethod(name='Star-Delta', description='Reduced voltage starting', min_power_hp=5, max_power_hp=500, contactors_required=3),
            StartingMethod(name='Soft Starter', description='Electronic soft starting', min_power_hp=5, max_power_hp=500, contactors_required=1),
            StartingMethod(name='Variable Frequency Drive', description='Electronic speed control', min_power_hp=1, max_power_hp=1000, contactors_required=1)
        ]
        
        for method in methods:
            db.session.add(method)
        db.session.commit()
        
        print("Database initialized successfully!")
        print(f"Added {len(manufacturers)} manufacturers")
        print(f"Added {len(contactors)} contactors")
        print(f"Added {len(overloads)} overload relays")
        print(f"Added {len(methods)} starting methods")

if __name__ == '__main__':
    init_database()

