from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from MTAInfo import get_next_trains
from requests import request
from flask import request
from models import db, GTFSStop  # Import your new model

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gtfs_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Take this out for one time script
# with app.app_context():
#     db.create_all()
#     print("Database tables created!")
#     load_gtfs_data_from_csv('MTA_Subway_Stations.csv')

@app.route('/')
def pookie():
    testing  = True
    if testing:
        return render_template('frontPage_test.html')
    else:
        return render_template('frontPage.html')


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
    
    return render_template('frontPage_routes.html', 
                         minutes=next_train_minutes,
                         current_route=current_route,
                         next_trains=next_trains,
                         next_routes=next_routes)


# @app.route('/')
# def home():
#     test = "F21N"
#     arrivals = get_next_trains(test, 3)  # Get 3 trains instead of just 1
    
#     if arrivals and len(arrivals) > 0:
#         # First train for main display
#         next_train_minutes = arrivals[0][1]
        
#         # Extract just the minutes for the next trains
#         next_trains = [arrival[1] for arrival in arrivals]
        
#         # print(f"All arrivals: {arrivals}")
#         # print(f"Minutes array: {next_trains}")
#     else:
#         next_train_minutes = "N/A"
#         next_trains = []
    
#     return render_template('frontPage_mvp.html', 
#                          minutes=next_train_minutes, 
#                          next_trains=next_trains)

@app.route('/test')
def test():
    pass


if __name__ == "__main__":
    app.run(debug=True)