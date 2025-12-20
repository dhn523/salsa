from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from MTAInfo import get_next_trains
from requests import request
from flask import request
from models import db, GTFSStop  # Import your new model for DB

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gtfs_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Take this out for one time script with DB
# with app.app_context():
#     db.create_all()
#     print("Database tables created!")
#     load_gtfs_data_from_csv('MTA_Subway_Stations.csv')

@app.route('/')
def pookie():
    testing  = False
    if testing:
        return render_template('frontPage_test.html')
    else:
        return render_template('frontPage.html')

@app.route('/typeahead')
def typeahead():
    return render_template('typeahead_testing.html')

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/favorite')
def favorite():
    return render_template('favorites_ad.html')

@app.route('/holiday')
def holiday():
    return render_template('holiday.html')

@app.route('/mainholiday')
def mainholiday():
    return render_template('holiday_ads.html')

@app.route('/api/favorites/train-times/<stop_id>')
def get_favorite_train_times(stop_id):
    """Get train times for a favorite stop"""
    # Define the routes for each stop
    stop_routes = {
        'F21N': 'F G',
        'R28N': 'R W',
        'A40N': 'A C',
        'R27S': 'R W',
        'M16S': 'J M Z'
    }
    
    routes_text = stop_routes.get(stop_id, '')
    arrivals = get_next_trains(stop_id, 3)
    
    if arrivals and len(arrivals) > 0:
        # Format the data for the frontend
        train_times = [
            {
                'route': arrival[0],
                'minutes': arrival[1]
            }
            for arrival in arrivals
        ]
        return jsonify(train_times)
    else:
        return jsonify([])

@app.route('/api/stops/search')
def search_stops():
    """Search stops by name"""
    query = request.args.get('q', '')
    if query:
        stops = GTFSStop.query.filter(GTFSStop.stop_name.contains(query)).all()
        return jsonify([stop.to_dict() for stop in stops])
    return jsonify([])

@app.route('/api/stops')
def get_all_stops():
    """Get all stops"""
    stops = GTFSStop.query.all()
    return jsonify([stop.to_dict() for stop in stops])


# Most basic display with the information for the Northbound F train at Carroll St
@app.route('/routes')
def home_routes():

    station_id = request.args.get('station')
    if not station_id:
        station_id = "F21N"
    arrivals = get_next_trains(station_id, 3)  # Get 3 trains instead of just 1
    
    if arrivals and len(arrivals) > 0:
        # First train for main display
        next_train_minutes = arrivals[0][1]
        current_route = arrivals[0][0]  # Assuming route is the first element in the tuple
        
        # Extract minutes and routes for all trains
        next_trains = [arrival[1] for arrival in arrivals]
        next_routes = [arrival[0] for arrival in arrivals]  # Extract routes
        
        # print(f"All arrivals: {arrivals}")
        # print(f"Minutes array: {next_trains}")
        # print(f"Routes array: {next_routes}")
    else:
        next_train_minutes = "N/A"
        current_route = "F"  # Default route
        next_trains = []
        next_routes = []
    
    return render_template('frontPage_basicRoute.html', 
                         minutes=next_train_minutes,
                         current_route=current_route,
                         next_trains=next_trains,
                         next_routes=next_routes)


@app.route('/test')
def test():
    pass


if __name__ == "__main__":
    app.run(debug=True)