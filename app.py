from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from MTAInfo import get_next_trains

app = Flask(__name__, template_folder="templates", static_folder="static")

bootstrap = Bootstrap(app)

@app.route('/')
def home():
    arrivals = get_next_trains("F21N", 3)  # Get 3 trains instead of just 1
    
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
    arrivals = get_next_trains("F21N")
    print(arrivals)
    if arrivals:
        next_train_minutes = arrivals[0][1]  # Minutes for next train
        if next_train_minutes == 0:
            next_train_minutes = arrivals[1][1]  # Now
    else:
        next_train_minutes = "N/A"
    print(f"Next train arrives in: {next_train_minutes} minutes")
    return render_template('test.html', minutes=next_train_minutes)


if __name__ == "__main__":
    app.run(debug=True)