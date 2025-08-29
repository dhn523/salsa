from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class GTFSStop(db.Model):
    __tablename__ = 'gtfs_stops'
    
    id = db.Column(db.Integer, primary_key=True)
    gtfs_stop_id = db.Column(db.String(20), nullable=False, unique=True)
    station_id = db.Column(db.String(20))
    complex_id = db.Column(db.String(20))
    division = db.Column(db.String(10))
    line = db.Column(db.String(10))
    stop_name = db.Column(db.String(100), nullable=False)
    borough = db.Column(db.String(20))
    cbd = db.Column(db.String(10))
    daytime_routes = db.Column(db.String(50))
    structure = db.Column(db.String(20))
    gtfs_latitude = db.Column(db.Float)
    gtfs_longitude = db.Column(db.Float)
    north_direction_label = db.Column(db.String(50))
    south_direction_label = db.Column(db.String(50))
    ada = db.Column(db.String(10))
    ada_northbound = db.Column(db.String(10))
    ada_southbound = db.Column(db.String(10))
    ada_notes = db.Column(db.Text)
    georeference = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<GTFSStop {self.gtfs_stop_id}: {self.stop_name}>'
    
    def to_dict(self):
        """Convert the model instance to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'gtfs_stop_id': self.gtfs_stop_id,
            'station_id': self.station_id,
            'complex_id': self.complex_id,
            'division': self.division,
            'line': self.line,
            'stop_name': self.stop_name,
            'borough': self.borough,
            'cbd': self.cbd,
            'daytime_routes': self.daytime_routes,
            'structure': self.structure,
            'gtfs_latitude': self.gtfs_latitude,
            'gtfs_longitude': self.gtfs_longitude,
            'north_direction_label': self.north_direction_label,
            'south_direction_label': self.south_direction_label,
            'ada': self.ada,
            'ada_northbound': self.ada_northbound,
            'ada_southbound': self.ada_southbound,
            'ada_notes': self.ada_notes,
            'georeference': self.georeference,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
#     @classmethod
#     def get_by_gtfs_id(cls, gtfs_stop_id):
#         """Get a stop by its GTFS Stop ID"""
#         return cls.query.filter_by(gtfs_stop_id=gtfs_stop_id).first()
    
#     @classmethod
#     def get_by_borough(cls, borough):
#         """Get all stops in a specific borough"""
#         return cls.query.filter_by(borough=borough).all()
    
#     @classmethod
#     def get_by_line(cls, line):
#         """Get all stops on a specific line"""
#         return cls.query.filter_by(line=line).all()
    
#     @classmethod
#     def get_ada_accessible(cls):
#         """Get all ADA accessible stops"""
#         return cls.query.filter_by(ada='Y').all()
    
#     @classmethod
#     def search_by_name(cls, name_pattern):
#         """Search stops by name pattern"""
#         return cls.query.filter(cls.stop_name.like(f'%{name_pattern}%')).all()
    
#     @classmethod
#     def get_nearby_stops(cls, latitude, longitude, radius=0.01):
#         """Get stops within a certain radius of given coordinates"""
#         return cls.query.filter(
#             ((cls.gtfs_latitude - latitude) ** 2 + 
#              (cls.gtfs_longitude - longitude) ** 2) <= radius ** 2
#         ).all()


# # Example usage functions for your Flask app
# def create_sample_data():
#     """Create some sample data for testing"""
#     sample_stops = [
#         {
#             'gtfs_stop_id': 'R01',
#             'station_id': 'STN001',
#             'complex_id': 'COMPLEX001',
#             'division': 'BMT',
#             'line': 'R',
#             'stop_name': 'Times Sq-42 St',
#             'borough': 'Manhattan',
#             'cbd': 'Yes',
#             'daytime_routes': 'N,Q,R,W,S,1,2,3,7',
#             'structure': 'Underground',
#             'gtfs_latitude': 40.755477,
#             'gtfs_longitude': -73.987691,
#             'north_direction_label': 'Uptown & Queens',
#             'south_direction_label': 'Downtown & Brooklyn',
#             'ada': 'Y',
#             'ada_northbound': 'Y',
#             'ada_southbound': 'Y',
#             'ada_notes': 'Fully accessible',
#             'georeference': 'POINT(-73.987691 40.755477)'
#         }
#     ]
    
#     for stop_data in sample_stops:
#         stop = GTFSStop(**stop_data)
#         db.session.add(stop)
    
#     db.session.commit()


# def bulk_insert_from_csv(csv_file_path):
#     """Bulk insert data from a CSV file"""
#     import csv
    
#     with open(csv_file_path, 'r') as file:
#         csv_reader = csv.DictReader(file)
#         stops_to_add = []
        
#         for row in csv_reader:
#             # Convert string coordinates to float if they exist
#             latitude = float(row['GTFS Latitude']) if row['GTFS Latitude'] else None
#             longitude = float(row['GTFS Longitude']) if row['GTFS Longitude'] else None
            
#             stop = GTFSStop(
#                 gtfs_stop_id=row['GTFS Stop ID'],
#                 station_id=row['Station ID'],
#                 complex_id=row['Complex ID'],
#                 division=row['Division'],
#                 line=row['Line'],
#                 stop_name=row['Stop Name'],
#                 borough=row['Borough'],
#                 cbd=row['CBD'],
#                 daytime_routes=row['Daytime Routes'],
#                 structure=row['Structure'],
#                 gtfs_latitude=latitude,
#                 gtfs_longitude=longitude,
#                 north_direction_label=row['North Direction Label'],
#                 south_direction_label=row['South Direction Label'],
#                 ada=row['ADA'],
#                 ada_northbound=row['ADA Northbound'],
#                 ada_southbound=row['ADA Southbound'],
#                 ada_notes=row['ADA Notes'],
#                 georeference=row['Georeference']
#             )
#             stops_to_add.append(stop)
        
#         # Bulk insert for better performance
#         db.session.bulk_save_objects(stops_to_add)
#         db.session.commit()