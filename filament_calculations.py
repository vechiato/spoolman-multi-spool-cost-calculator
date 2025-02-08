# filament_calculations.py

import math
import re

import requests

def calculate_cost(filament_used_grams, spool_weight_grams, spool_cost):
    """
    Calculates the cost of the filament used based on spool details.
    """
    if spool_weight_grams == 0:
        raise ValueError("Spool weight is zero, cannot calculate cost per gram.")
    if filament_used_grams < 0:
        raise ValueError("Filament used cannot be negative.")
    cost_per_gram = spool_cost / spool_weight_grams
    return filament_used_grams * cost_per_gram

def calculate_mass_per_meter(diameter_mm, density):
    """
    Calculates the mass per meter of the filament based on diameter and density.
    Assumes a default diameter of 1.75 mm if not provided or if zero.
    """
    if diameter_mm <= 0:
        diameter_mm = 1.75  # Default diameter in mm
    diameter_cm = diameter_mm / 10  # Convert mm to cm
    radius_cm = diameter_cm / 2
    cross_sectional_area_cm2 = math.pi * (radius_cm ** 2)  # in cm^2
    mass_per_cm = cross_sectional_area_cm2 * density  # in g/cm
    mass_per_meter = mass_per_cm * 100  # 100 cm in a meter
    return mass_per_meter  # in g/m

def parse_filament_input(user_input):
    """
    Parses the user input for filament used and extracts the value and unit.
    """
    user_input = user_input.strip().lower()
    pattern = r'^([\d.]+)\s*([gm])?$'
    match = re.match(pattern, user_input)
    if not match:
        raise ValueError("Invalid input format. Please enter a number followed by 'g' or 'm', or just a number.")
    value_str, unit = match.groups()
    value = float(value_str)
    if not unit:
        unit = 'g'  # Default to grams if unit is not specified
    return value, unit

def get_spools(SPOOLMAN_API_URL):
    """
    Fetches all spools from the Spoolman API and filters out archived spools.
    """
    endpoint = f"{SPOOLMAN_API_URL}/spool" 
    # the SPOOLMAN_API_URL variable is defined in the main.py file and read from the .env file but it is not available here. how do we fix this?

    response = requests.get(endpoint)  # , headers=HEADERS)

    if response.status_code == 200:
        spools = response.json()
        # Filter out archived spools
        active_spools = [spool for spool in spools if not spool.get('archived', False)]
        return active_spools
    else:
        raise Exception(f"Failed to fetch spools: {response.status_code} - {response.text}")