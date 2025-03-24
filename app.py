
from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Calculate the differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance

def calculate_distances(current_lat, current_lon, locations):
    distances = {}

    for location in locations:
        lat, lon, venue, zone = location['lat'], location['long'], location.get('venue', ''), location.get('zone', '')
        distance = haversine(current_lat, current_lon, lat, lon)
        # Use a tuple of coordinates as the key
        distances[(lat, lon)] = {'distance': distance, 'venue': venue, 'zone': zone}

    # Sort distances and get the top 5 nearest locations
    sorted_distances = sorted(distances.items(), key=lambda x: x[1]['distance'])
    top5_nearest = sorted_distances[:5]

    # Extract latitudes, longitudes, distances, venue, and zone
    top5_coordinates = [{'lat': lat, 'long': lon, 'km': data['distance'], 'venue': data['venue'], 'zone': data['zone']}
                        for (lat, lon), data in top5_nearest]

    return top5_coordinates

@app.route('/nearest', methods=['POST'])
def nearest_locations():
    data = request.json

    current_location = (data['current']['lat'], data['current']['long'])
    locations_list = data['center']

    nearest_coordinates = calculate_distances(*current_location, locations_list)

    response = {
        "status": True,
        "message": "Centers For Face Verification",
        "data": nearest_coordinates
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
