# main.py

#import requests
import argparse
import datetime
import os
from dotenv import load_dotenv
from filament_calculations import (
    calculate_cost,
    calculate_mass_per_meter,
    get_spools,
    parse_filament_input,
)
from snapshot_utils import compare_snapshots, save_snapshot

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Configuration
    # Read the Spoolman API URL from the environment variable or use the default
    #SPOOLMAN_API_URL="http://192.168.0.106:7912/api/v1"
    SPOOLMAN_API_URL = os.getenv("SPOOLMAN_API_URL", "http://localhost:7912/api/v1")

    #API_KEY = os.getenv("SPOOLMAN_API_KEY")  # Ensure your API key is set in the environment

    HEADERS = {
        #"Authorization": f"Bearer {API_KEY}",  # Uncomment if your API requires authentication
        "Content-Type": "application/json"
    }

    parser = argparse.ArgumentParser(description="Filament Cost Calculator")
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Take a snapshot of the current state of all filaments."
    )
    parser.add_argument(
        "--compare",
        nargs=2,
        metavar=('SNAPSHOT1', 'SNAPSHOT2'),
        help="Compare two snapshots by providing two snapshot file paths."
    )
    args = parser.parse_args()
    if args.snapshot:
        # Fetch spool data and save a snapshot
        spools = get_spools(SPOOLMAN_API_URL)
        if not spools:
            print("No spools found to snapshot.")
            return
        save_snapshot(spools)
    elif args.compare:
        # Compare two snapshot files
        snapshot1, snapshot2 = args.compare
        compare_snapshots(snapshot1, snapshot2)
    else:
        try:
            spools = get_spools(SPOOLMAN_API_URL)
            
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
                print(f"Remaining Filament Weight: {remaining_weight:.2f} grams")
                print(f"Material: {spool_material}, Diameter: {diameter_mm} mm, Density: {density} g/cm³")

                # Calculate mass per meter
                mass_per_meter = calculate_mass_per_meter(diameter_mm, density)
                #print(f"Estimated Mass per Meter: {mass_per_meter:.4f} g/m")

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
                print(f"Cost for this print: ${print_cost:.2f}")
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
            # how can i see the full error message? and the line it happened on


          

if __name__ == "__main__":
    main()