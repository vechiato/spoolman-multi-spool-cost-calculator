import requests
import os
import math
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Configuration
# Read the Spoolman API URL from the environment variable or use the default
SPOOLMAN_API_URL = os.getenv("SPOOLMAN_API_URL", "http://localhost:7912/api/v1")
API_KEY = os.getenv("SPOOLMAN_API_KEY")  # Ensure your API key is set in the environment

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",  # Uncomment if your API requires authentication
    "Content-Type": "application/json"
}

def get_spools():
    """
    Fetches all spools from the Spoolman API and filters out archived spools.
    """
    endpoint = f"{SPOOLMAN_API_URL}/spool"
    response = requests.get(endpoint)  # , headers=HEADERS)

    if response.status_code == 200:
        spools = response.json()
        # Filter out archived spools
        active_spools = [spool for spool in spools if not spool.get('archived', False)]
        return active_spools
    else:
        raise Exception(f"Failed to fetch spools: {response.status_code} - {response.text}")

def calculate_cost(filament_used_grams, spool_weight_grams, spool_cost):
    """
    Calculates the cost of the filament used based on spool details.

    Parameters:
        filament_used_grams (float): Amount of filament used in grams.
        spool_weight_grams (float): Total weight of the filament on the spool in grams.
        spool_cost (float): Total cost of the spool.

    Returns:
        float: Cost of the filament used.
    """
    if spool_weight_grams == 0:
        raise ValueError("Spool weight is zero, cannot calculate cost per gram.")
    cost_per_gram = spool_cost / spool_weight_grams
    return filament_used_grams * cost_per_gram

def calculate_mass_per_meter(diameter_mm, density):
    """
    Calculates the mass per meter of the filament based on diameter and density.
    
    Parameters:
        diameter_mm (float): Diameter of the filament in millimeters.
        density (float): Density of the filament in g/cm^3.
    
    Returns:
        float: Mass per meter in grams per meter.
    """
    diameter_cm = diameter_mm / 10  # Convert mm to cm
    radius_cm = diameter_cm / 2
    cross_sectional_area_cm2 = math.pi * (radius_cm ** 2)  # in cm^2
    mass_per_cm = cross_sectional_area_cm2 * density  # in g/cm
    mass_per_meter = mass_per_cm * 100  # 100 cm in a meter
    return mass_per_meter  # in g/m

def parse_filament_input(user_input):
    """
    Parses the user input for filament used and extracts the value and unit.

    Parameters:
        user_input (str): The user input string (e.g., '100.1g', '1.34m', or '100')

    Returns:
        tuple: (value, unit) where unit is 'g' for grams or 'm' for meters.
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

def main():
    try:
        spools = get_spools()
        
        if not spools:
            print("No spools found.")
            return

        # Assign IDs to spools for easy selection
        spool_dict = {}
        print("Available Spools:")
        for idx, spool in enumerate(spools, start=1):
            spool_id = spool['id']
            spool_name = spool['filament']['name']
            spool_price = spool.get('price', 0.0)
            spool_material = spool['filament'].get('material', 'Unknown')
            spool_color = spool['filament'].get('color_hex', 'Unknown')
            print(f"{idx}. {spool_name} (ID: {spool_id}) Price: ${spool_price:.2f} Material: {spool_material} Color: {spool_color}")
            spool_dict[str(idx)] = spool # Mapping the selection number to the spool

        total_cost = 0.0
        summary = []
        another = 'y'

        while another.lower() == 'y':
            spool_choice = input("\nSelect a spool by number: ").strip()
            selected_spool = spool_dict.get(spool_choice)
            if not selected_spool:
                print("Invalid selection. Please try again.")
                continue

            # Extract necessary data from selected_spool
            spool_cost = float(selected_spool.get('price', 0.0))  # Price you paid for the spool
            spool_weight = float(selected_spool.get('initial_weight', 0))  # Total filament weight when new (grams)
            remaining_weight = float(selected_spool.get('remaining_weight', 0))  # Remaining filament weight (grams)

            spool_name = selected_spool['filament']['name']
            spool_material = selected_spool['filament'].get('material', 'Unknown')
            diameter_mm = float(selected_spool['filament'].get('diameter', 1.75))  # Default to 1.75 mm if not provided
            density = float(selected_spool['filament'].get('density', 1.24))  # Default PLA density if not provided

            print(f"\nSelected Spool: {spool_name}")
            print(f"Spool Cost: ${spool_cost:.2f}")
            print(f"Spool Weight (initial): {spool_weight} grams")
            print(f"Remaining Filament Weight: {remaining_weight:.2f} grams")
            print(f"Material: {spool_material}, Diameter: {diameter_mm} mm, Density: {density} g/cm³")

            # Calculate mass per meter
            mass_per_meter = calculate_mass_per_meter(diameter_mm, density)
            print(f"Estimated Mass per Meter: {mass_per_meter:.4f} g/m")

            # Prompt user for filament usage
            filament_input = input("Enter filament used for the print (e.g., '100g' or '1.34m'): ").strip()
            try:
                filament_value, unit = parse_filament_input(filament_input)
            except ValueError as e:
                print(f"Error: {e}")
                continue

            if unit == 'g':
                filament_used_grams = filament_value
            elif unit == 'm':
                filament_used_grams = filament_value * mass_per_meter
            else:
                print("Invalid unit. Please enter a valid value with 'g' for grams or 'm' for meters.")
                continue

            if filament_used_grams > remaining_weight:
                print("Error: Filament used exceeds remaining spool weight.")
                continue

            print_cost = calculate_cost(filament_used_grams, spool_weight, spool_cost)
            print(f"Cost for this spool: ${print_cost:.2f}")
            total_cost += print_cost

            # Add to summary
            summary.append({
                'spool_name': spool_name,
                'filament_used': filament_value,
                'unit': unit,
                'cost': print_cost
            })

            another = input("\nDo you want to add another spool? (y/n): ")

        # Display the summary
        print("\nSummary of Filament Usage:")
        print("{:<30} {:>15} {:>10} {:>15}".format('Spool Name', 'Filament Used', 'Unit', 'Cost'))
        print("-" * 75)
        for item in summary:
            print("{:<30} {:>15.2f} {:>10} {:>15.2f}".format(
                item['spool_name'],
                item['filament_used'],
                item['unit'],
                item['cost']
            ))
        print("-" * 75)
        print("{:<30} {:>40.2f}".format('Total Cost:', total_cost))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()