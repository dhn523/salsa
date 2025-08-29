-- GTFS Transit Data SQLite Database Schema
-- Drop table if it exists (uncomment if needed)
-- DROP TABLE IF EXISTS gtfs_stops;

CREATE TABLE gtfs_stops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gtfs_stop_id TEXT NOT NULL UNIQUE,
    station_id TEXT,
    complex_id TEXT,
    division TEXT,
    line TEXT,
    stop_name TEXT NOT NULL,
    borough TEXT,
    cbd TEXT,
    daytime_routes TEXT,
    structure TEXT,
    gtfs_latitude REAL,
    gtfs_longitude REAL,
    north_direction_label TEXT,
    south_direction_label TEXT,
    ada TEXT,
    ada_northbound TEXT,
    ada_southbound TEXT,
    ada_notes TEXT,
    georeference TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_gtfs_stop_id ON gtfs_stops(gtfs_stop_id);
CREATE INDEX idx_station_id ON gtfs_stops(station_id);
CREATE INDEX idx_complex_id ON gtfs_stops(complex_id);
CREATE INDEX idx_borough ON gtfs_stops(borough);
CREATE INDEX idx_line ON gtfs_stops(line);
CREATE INDEX idx_stop_name ON gtfs_stops(stop_name);
CREATE INDEX idx_coordinates ON gtfs_stops(gtfs_latitude, gtfs_longitude);

-- Create a trigger to update the updated_at timestamp
CREATE TRIGGER update_gtfs_stops_timestamp 
    AFTER UPDATE ON gtfs_stops
BEGIN
    UPDATE gtfs_stops SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Sample insert statement (uncomment and modify as needed)
/*
INSERT INTO gtfs_stops (
    gtfs_stop_id, station_id, complex_id, division, line, stop_name, 
    borough, cbd, daytime_routes, structure, gtfs_latitude, gtfs_longitude,
    north_direction_label, south_direction_label, ada, ada_northbound, 
    ada_southbound, ada_notes, georeference
) VALUES (
    'R01', 'STN001', 'COMPLEX001', 'BMT', 'R', 'Times Sq-42 St', 
    'Manhattan', 'Yes', 'N,Q,R,W,S,1,2,3,7', 'Underground', 40.755477, -73.987691,
    'Uptown & Queens', 'Downtown & Brooklyn', 'Y', 'Y', 'Y', 
    'Fully accessible', 'POINT(-73.987691 40.755477)'
);
*/