"""Example Flask server using the Ship to Shore validator."""

from flask import Flask, request, jsonify
from src.validators.index import ShipToShore
from src.index import validate, ValidationError

app = Flask(__name__)


@app.route('/rotterdam-pilot', methods=['POST'])
def rotterdam_pilot():
    """Validate Ship to Shore data for Rotterdam Pilot."""
    try:
        validated_data = validate(ShipToShore, request.json)
        return jsonify({
            "success": True,
            "message": "validation passed",
            "data": validated_data.model_dump(by_alias=True)
        }), 200
    except ValidationError as err:
        return jsonify(err.to_json()), 400
    except Exception:
        return jsonify({"message": "Internal server error"}), 500


if __name__ == '__main__':
    print("Server is running at http://localhost:3000")
    app.run(port=3000, debug=False)
