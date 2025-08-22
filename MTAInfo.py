import requests
from google.transit import gtfs_realtime_pb2
import datetime

class MTAClient:
    def __init__(self, api_key=None):
        """
        Initialize MTA API client
        
        Args:
            api_key (str): MTA API key (optional)
        """
        self.base_url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds"
        self.api_key = api_key
        
    
    def get_next_arrivals(self, stop_id, num_arrivals=3, routes_text="A C E B D F M G J Z N Q R W L SIR 1 2 3 4 5 6 7 S"):
        """
        Get the next train arrivals in minutes for a specific stop
        
        Args:
            stop_id (str): MTA stop ID (e.g., 'F21N')
            num_arrivals (int): Number of arrivals to return (default: 3)
            routes_text (str): Space-separated routes to filter by (e.g., "F B D")
            
        Returns:
            list: List of tuples (route_id, minutes_until_arrival)
                Returns empty list if error or no data
        """
        # Determine which feeds to call based on routes_text
        feeds_to_call = set()
        
        if routes_text:
            routes = routes_text.upper().split()
            
            for route in routes:
                if route in ['A', 'C', 'E']:
                    feeds_to_call.add('ace')
                elif route in ['B', 'D', 'F', 'M']:
                    feeds_to_call.add('bdfm')
                elif route == 'G':
                    feeds_to_call.add('g')
                elif route in ['J', 'Z']:
                    feeds_to_call.add('jz')
                elif route in ['N', 'Q', 'R', 'W']:
                    feeds_to_call.add('nqrw')
                elif route == 'L':
                    feeds_to_call.add('l')
                elif route == 'SIR':
                    feeds_to_call.add('si')
                elif route in ['1', '2', '3', '4', '5', '6', '7', 'S']:
                    feeds_to_call.add('')
                # If route doesn't match any category, we add empty string
                # but since we're using a set, we'll handle this differently
        else:
            # Fallback to original logic if no routes_text provided
            if stop_id[0] in ['B', 'D', 'F', 'M']:
                feeds_to_call.add('bdfm')
            elif stop_id[0] in ['J', 'Z']:
                feeds_to_call.add('jz')
            # Add other stop_id logic as needed for other lines
        
        # If no valid feeds found, return empty list
        if not feeds_to_call:
            return []
        
        # Collect all arrivals from all relevant feeds
        all_arrivals = []
        
        for feed_name in feeds_to_call:
            if feed_name:  # Skip empty string cases
                feed = self._get_feed(feed_name)
                if feed:
                    arrivals = self._parse_arrivals_for_stop(feed, stop_id)
                    if arrivals:
                        all_arrivals.extend(arrivals)
        
        # If no arrivals found, return empty list
        if not all_arrivals:
            return []
        
        # Sort by arrival time and get next arrivals
        all_arrivals.sort(key=lambda x: x[1])
        current_time = int(datetime.datetime.now().timestamp())
        
        # Convert to minutes and filter future arrivals only
        next_arrivals = []
        for route, arr_time in all_arrivals:
            minutes = int((arr_time - current_time) / 60)
            if minutes >= 0:  # Only future arrivals
                next_arrivals.append((route, minutes))
        
        # Filter by routes if routes_text was provided
        if routes_text:
            requested_routes = set(routes_text.upper().split())
            next_arrivals = [(route, minutes) for route, minutes in next_arrivals 
                            if route in requested_routes]
        
        return next_arrivals[:num_arrivals]

    def _get_feed(self, feed_type='bdfm'):
        """
        Get real-time feed data for subway lines
        
        Returns:
            gtfs_realtime_pb2.FeedMessage or None
        """
        
        endpoint = f"{self.base_url}/nyct%2Fgtfs-{feed_type}"
        
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key
            
        try:
            response = requests.get(endpoint, headers=headers, timeout=30)
            response.raise_for_status()
            
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            return feed
            
        except Exception as e:
            print(f"Error fetching/parsing data: {e}")
            return None
    
    def _parse_arrivals_for_stop(self, feed, stop_id):
        """
        Parse arrivals for a specific stop from GTFS-RT feed
        
        Args:
            feed: GTFS-RT FeedMessage object
            stop_id (str): Stop ID to filter for
            
        Returns:
            list: List of tuples (route_id, arrival_timestamp)
        """
        arrivals = []
        
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip_update = entity.trip_update
                route_id = trip_update.trip.route_id
                
                for stop_update in trip_update.stop_time_update:
                    if stop_update.stop_id == stop_id and stop_update.HasField('arrival'):
                        arrival_time = stop_update.arrival.time
                        arrivals.append((route_id, arrival_time))
        
        return arrivals

# Convenience function for quick usage
def get_next_trains(stop_id, num_arrivals=3, api_key=None):
    """
    Quick function to get next train arrivals
    
    Args:
        stop_id (str): MTA stop ID (e.g., 'F21N')
        num_arrivals (int): Number of arrivals to return
        api_key (str): Optional MTA API key
        
    Returns:
        list: List of tuples (route_id, minutes_until_arrival)
    """
    client = MTAClient(api_key)
    return client.get_next_arrivals(stop_id, num_arrivals)

# Example usage
if __name__ == "__main__":
    # Example: Get next 3 trains at F21N stop
    stop_id = "F21N"
    arrivals = get_next_trains(stop_id)
    
    print(arrivals)
    print(arrivals[0][1])

    if arrivals:
        print(f"Next trains at stop {stop_id}:")
        for route, minutes in arrivals:
            if minutes == 0:
                print(f"{route} train: Now")
            elif minutes == 1:
                print(f"{route} train: 1 minute")
            else:
                print(f"{route} train: {minutes} minutes")
    else:
        print("No arrival data available")

    stop_id = "M16S"
    arrivals = get_next_trains(stop_id)
    
    print(arrivals)
    print(arrivals[0][1])

    if arrivals:
        print(f"Next trains at stop {stop_id}:")
        for route, minutes in arrivals:
            if minutes == 0:
                print(f"{route} train: Now")
            elif minutes == 1:
                print(f"{route} train: 1 minute")
            else:
                print(f"{route} train: {minutes} minutes")
    else:
        print("No arrival data available")
        
    # You can also use the class directly:
    # client = MTAClient()
    # arrivals = client.get_next_arrivals("F21N", 3)