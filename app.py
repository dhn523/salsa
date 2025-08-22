from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from MTAInfo import get_next_trains
from requests import request
from flask import request

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap(app)

@app.route('/')
def home():
    test = "F21N"
    arrivals = get_next_trains(test, 3)  # Get 3 trains instead of just 1
    
    if arrivals and len(arrivals) > 0:
        # First train for main display
        next_train_minutes = arrivals[0][1]
        
        # Extract just the minutes for the next trains
        next_trains = [arrival[1] for arrival in arrivals]
        
        # print(f"All arrivals: {arrivals}")
        # print(f"Minutes array: {next_trains}")
    else:
        next_train_minutes = "N/A"
        next_trains = []
    
    return render_template('frontPage.html', 
                         minutes=next_train_minutes, 
                         next_trains=next_trains)

@app.route('/test')
def test():
    # minutes = 5  # Your variable here
    station_id = request.args.get('station')
    if not station_id:
        station_id = "F21N"
    arrivals = get_next_trains(station_id)
    print(arrivals)
    if arrivals:
        next_train_minutes = arrivals[0][1]  # Minutes for next train
        if next_train_minutes == 0:
            next_train_minutes = arrivals[1][1]  # Now
    else:
        next_train_minutes = "N/A"
    print(f"Next train arrives in: {next_train_minutes} minutes")
    return render_template('test.html', minutes=next_train_minutes)


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

@app.route('/pookie')
def pookie():
    return render_template('pookie.html')

if __name__ == "__main__":
    app.run(debug=True)