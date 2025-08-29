import csv
from flask import Flask
from models import db, GTFSStop

def load_gtfs_data_from_csv(csv_file_path):
    """Load GTFS data from CSV file"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gtfs_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Convert coordinates to float if they exist
                latitude = float(row['GTFS Latitude']) if row.get('GTFS Latitude') and row['GTFS Latitude'].strip() else None
                longitude = float(row['GTFS Longitude']) if row.get('GTFS Longitude') and row['GTFS Longitude'].strip() else None
                
                stop = GTFSStop(
                    gtfs_stop_id=row.get('GTFS Stop ID'),
                    station_id=row.get('Station ID'),
                    complex_id=row.get('Complex ID'),
                    division=row.get('Division'),
                    line=row.get('Line'),
                    stop_name=row.get('Stop Name'),
                    borough=row.get('Borough'),
                    cbd=row.get('CBD'),
                    daytime_routes=row.get('Daytime Routes'),
                    structure=row.get('Structure'),
                    gtfs_latitude=latitude,
                    gtfs_longitude=longitude,
                    north_direction_label=row.get('North Direction Label'),
                    south_direction_label=row.get('South Direction Label'),
                    ada=row.get('ADA'),
                    ada_northbound=row.get('ADA Northbound'),
                    ada_southbound=row.get('ADA Southbound'),
                    ada_notes=row.get('ADA Notes'),
                    georeference=row.get('Georeference')
                )
                
                db.session.add(stop)
            
            db.session.commit()
            print(f'Successfully loaded data from {csv_file_path}')

if __name__ == '__main__':
    # Usage: python data_loader.py
    load_gtfs_data_from_csv('MTA_Subway_Stations.csv')