from app import app
from models import db
from data_loader import load_gtfs_data_from_csv

def setup_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Loading CSV data...")
        load_gtfs_data_from_csv('MTA_Subway_Stations.csv')
        print("Setup complete!")

if __name__ == '__main__':
    setup_database()