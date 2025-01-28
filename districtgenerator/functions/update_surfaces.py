### These functions are used to update the surfaces of the buildings
### Based on the TECDEM data model ( https://github.com/TUB-DVG/TECDEM ) detailed geometry analysis can be integrated
### The functions are used in the datahandler class

import json 


def extract_surface_areas(building_data):
    """
    Extract free wall areas and total wall areas per direction from building geometry data.
    
    Args:
        building_data (Envelope): Envelope object containing building geometry data
         with orientation angles and surface areas from the archetypes
        
    Returns:
        tuple: Two dictionaries containing:
            - free_areas: Free wall areas grouped by cardinal direction (N,S,E,W)
            - opaque_areas: Total wall areas grouped by cardinal direction (N,S,E,W)
    """
    # Initialize dictionaries to store areas by direction
    free_areas = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
    opaque_areas = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
    
    # Process each surface orientation
    for key, value in building_data.items():
        # Skip the gml_id entry
        if key == 'gml_id':
            continue
            
        
        try:
            angle = float(key)
        except ValueError:
            continue
            
        # Normalize angle to 0-360 range
        angle = angle % 360
        
        # Determine cardinal direction based on angle
        # TODO check Teaser data model
        if 315 <= angle or angle < 45:
            direction = 'north'
        elif 45 <= angle < 135:
            direction = 'east'
        elif 135 <= angle < 225:
            direction = 'south'
        else:  # 225 <= angle < 315
            direction = 'west'
            
        # Add areas to corresponding direction
        free_areas[direction] += value.get('free_wall_area', 0)
        opaque_areas[direction] += value.get('connected_wall_area', 0)
        
    return free_areas, opaque_areas


def extract_window_areas(free_areas, opaque_areas, building_data):
    """
    Extract window areas per direction from building geometry data.
    
    Args:
        free_areas (dict): Dictionary containing free wall areas by direction (north,south,east,west)
        opaque_areas (dict): Dictionary containing total opaque wall areas by direction (north,south,east,west)
        building_data (Envelope): Envelope object containing the building data 
         with orientation angles and surface areas from the archetypes
        
    Returns:
        dict: Window areas grouped by cardinal direction (north,south,east,west)
    """
    updated_window_areas = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
    
    # Calculate window areas based on free wall area and target window ratio
    for direction in updated_window_areas:
        free_area = free_areas[direction]
        if free_area > 0:
            # Calculate window area as percentage of free wall area
            window_area = ( free_area /  ( opaque_areas[direction] + free_area ) ) * building_data[direction]
            # Ensure window area doesn't exceed free wall area
            updated_window_areas[direction] = min(window_area, free_area)
            
    return updated_window_areas
