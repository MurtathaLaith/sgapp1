from flask import Blueprint, jsonify, request
import math

switchgear_bp = Blueprint('switchgear', __name__)

@switchgear_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Motor Switchgear API is running"})

@switchgear_bp.route('/starting-methods', methods=['GET'])
def get_starting_methods():
    from src.models.switchgear import StartingMethod
    methods = StartingMethod.query.all()
    return jsonify([method.to_dict() for method in methods])

@switchgear_bp.route('/calculate', methods=['POST'])
def calculate_recommendation():
    try:
        data = request.get_json()
        power_hp = float(data.get('power_hp', 0))
        power_kw = float(data.get('power_kw', 0))
        voltage = int(data.get('voltage', 460))
        frequency = int(data.get('frequency', 60))
        starting_method_id = int(data.get('starting_method_id', 1))
        
        # Calculate full load current
        if power_hp > 0:
            # Convert HP to kW if needed
            if power_kw == 0:
                power_kw = power_hp * 0.746
        
        # Calculate FLC using standard formula
        flc = (power_kw * 1000) / (math.sqrt(3) * voltage * 0.85)  # Assuming 85% efficiency
        
        # Get starting method
        from src.models.switchgear import StartingMethod, Contactor, OverloadRelay
        starting_method = StartingMethod.query.get(starting_method_id)
        
        # Select contactor based on FLC
        contactor = Contactor.query.filter(
            Contactor.current_rating >= flc * 1.25,
            Contactor.voltage_rating >= voltage
        ).order_by(Contactor.current_rating).first()
        
        # Select overload relay
        overload = OverloadRelay.query.filter(
            OverloadRelay.current_range_min <= flc,
            OverloadRelay.current_range_max >= flc
        ).first()
        
        # Calculate circuit breaker size (125% of FLC)
        cb_rating = math.ceil(flc * 1.25)
        
        # Build response
        result = {
            'motor_specifications': {
                'power_hp': power_hp,
                'power_kw': power_kw,
                'voltage': voltage,
                'frequency': frequency,
                'full_load_current': round(flc, 2)
            },
            'starting_method': starting_method.to_dict() if starting_method else None,
            'recommendations': {
                'contactor': contactor.to_dict() if contactor else None,
                'overload_relay': overload.to_dict() if overload else None,
                'circuit_breaker_rating': cb_rating,
                'quantity': {
                    'contactors': starting_method.contactors_required if starting_method else 1,
                    'overload_relays': 1
                }
            },
            'cost_estimate': {
                'contactor_cost': (contactor.price * (starting_method.contactors_required if starting_method else 1)) if contactor and contactor.price else 0,
                'overload_cost': overload.price if overload and overload.price else 0,
                'total_cost': ((contactor.price * (starting_method.contactors_required if starting_method else 1)) if contactor and contactor.price else 0) + (overload.price if overload and overload.price else 0)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

