# Filament Cost Calculator

A Python script to calculate the real cost of a 3D print using slicer filament estimative and fetching actual costs of each spool from the Spoolman API. This tool helps 3D printing enthusiasts and professionals accurately estimate the filament costs for their prints, considering multiple spools and different units of measurement.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **Exclude Archived Spools**: Automatically filters out archived spools from the selection list.
- **Multiple Filament Calculation**: Supports cost calculation for prints using multiple spools.
- **Flexible Units**: Accepts filament usage input in grams or meters, with units specified directly in the input (e.g., `100g`, `50m`).
- **User-Friendly Interaction**: Provides detailed prompts and error messages to guide the user.
- **Summary Report**: Displays a formatted summary of all filaments used and their individual costs at the end.
- **Customizable API URL**: Reads the Spoolman API URL from the `.env` file or defaults to `http://localhost:7912`.
- **Filament Snapshot & Comparison**: Captures the current state of all filaments and compares snapshots to show usage and cost differences over time.

## Prerequisites

- **Python 3.6 or higher**

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/vechiato/filament-cost-calculator.git
   cd filament-cost-calculator
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate          # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: The `requirements.txt` file should contain at least:

   ```
   requests
   python-dotenv
   ```

## Configuration

1. **Set Up Environment Variables**

   Create a `.env` file in the project directory to store environment variables such as your Spoolman API URL and API key.

   ```bash
   touch .env
   ```

   Add the following to the `.env` file:

   ```ini
   # Spoolman API URL (default is http://localhost:7912/api/v1 if not set)
   SPOOLMAN_API_URL=http://your-spoolman-ip:7912/api/v1
   
   # Spoolman API Key (if required)
   SPOOLMAN_API_KEY=your_api_key_here
   ```

   - **SPOOLMAN_API_URL**: Replace `http://your-spoolman-api-url/api/v1` with your actual Spoolman API URL.
     - If you don't set this variable, the script defaults to `http://localhost:7912/api/v1`.
   - **SPOOLMAN_API_KEY**: Replace `your_api_key_here` with your actual Spoolman API key if your API requires authentication.
     - If your API doesn't require authentication, you can leave this unset.

## Usage

Run the script using Python:

```bash
python main.py
```

Follow the on-screen prompts to select spools and enter filament usage.

### Input Format

- **Spool Selection**: Enter the number corresponding to the spool you want to select.
- **Filament Usage**: Input the amount of filament used with units appended (e.g., `100g` for grams, `50m` for meters). If no unit is specified, the script assumes grams.

### Units

- **Grams (g)**: Enter filament usage in grams (e.g., `100g` or `100`).
- **Meters (m)**: Enter filament usage in meters (e.g., `50m`).

### Example Steps

1. **Select Spools**

   The script will display a list of available spools:

   ```
   Available Spools:
   1. PLA Red (ID: 1) Price: $16.49 Material: PLA Color: ff0000
   2. PLA White (ID: 2) Price: $10.99 Material: PLA Color: ffffff
   3. NYLON GREY (ID: 3) Price: $28.99 Material: NYLON Color: 808080
   4. PETG BLACK (ID: 4) Price: $15.99 Material: PETG Color: 000000
   ...
   ```

   Enter the number corresponding to the spool you wish to use.

2. **Enter Filament Usage**

   When prompted, enter the amount of filament used with the unit:

   ```
   Enter filament used for the print (e.g., '100g' or '1.5m'): 100g
   ```

3. **Add Additional Spools**

   After each spool, the script will ask if you want to add another spool:

   ```
   Do you want to add another spool? (y/n): y
   ```

4. **View Summary**

   Once you have entered all the spools and filament usage, the script will display a summary:

   ```
   Summary of Filament Usage:
   Spool Name                       Filament Used       Unit            Cost
   ---------------------------------------------------------------------------
   PLA Red                                100.34          g            1.65
   PLA White                               53.21          m            1.74
   ---------------------------------------------------------------------------
   Total Cost:                                                         3.40
   ```

## Example Output

   ```
   Available Spools:
   1. PLA Red (ID: 1) Price: $16.49 Material: PLA Color: ff0000
   2. PLA White (ID: 2) Price: $10.99 Material: PLA Color: ffffff
   3. NYLON GREY (ID: 3) Price: $28.99 Material: NYLON Color: 808080
   4. PETG BLACK (ID: 4) Price: $15.99 Material: PETG Color: 000000
   ...

   Select a spool by number: 1

   Selected Spool: PLA Red
   Spool Cost: $16.49
   Remaining Filament Weight: 912.13 grams
   Material: PLA, Diameter: 1.75 mm, Density: 1.24 g/cm³

   Enter filament used for the print (e.g., '100g' or '1.5m'): 100.34g

   Cost for this print: $1.65

   Do you want to add another spool? (y/n): y

   Select a spool by number: 2

   Selected Spool: PLA White
   Spool Cost: $10.99
   Remaining Filament Weight: 440.00 grams
   Material: PLA, Diameter: 1.75 mm, Density: 1.24 g/cm³

   Enter filament used for the print (e.g., '100g' or '1.5m'): 53.21m

   Cost for this print: $1.74

   Do you want to add another spool? (y/n): n

   Summary of Filament Usage:
   Spool Name                       Filament Used       Unit            Cost
   ---------------------------------------------------------------------------
   PLA Red                                100.34          g            1.65
   PLA White                               53.21          m            1.74
   ---------------------------------------------------------------------------
   Total Cost:                                                         3.40
   ```

## Filament Snapshot and Comparison

This feature allows you to take snapshots of the current state of all filaments and compare the filament usage and costs between different snapshots.

### Taking a Snapshot

To take a snapshot of the current state of all filaments, run the following command:

```bash
python main.py --snapshot
```
This command captures the current state of all filaments, including their remaining weights and costs, and stores it with a timestamp.

### Comparing Snapshots
To compare two snapshots and determine the filament usage and costs spent between them, run the following command:

```bash
python main.py --compare <snapshot1> <snapshot2>
```
Replace <snapshot1> and <snapshot2> with the identifiers of the snapshots you want to compare. The command will display the comparison results, showing the filament usage and costs spent between the two snapshots.

### Example
1. Take a Snapshot:
```bash
python main.py --snapshot
```

2. Compare Snapshots:
```bash 
python main.py --compare snapshot_2025-02-08_10-00-00.json snapshot_2025-02-08_15-00-00.json
```
This will compare the snapshots taken at 10:00 AM and 3:00 PM on February 8, 2025, and display the filament usage and costs spent between these times.

#### Example output 
```
Comparing snapshot_2025-02-08_10-00-0.json and snapshot_2025-02-08_15-00-00.json...

Spool ID   Name                           Weight Diff (g)  Cost Used($)
----------------------------------------------------------------------
1          PLA RED                                 200.00         3.30
4          PLA GREY                                 50.00         0.82
12         PLA ORANGE                              141.45         1.55
----------------------------------------------------------------------
TOTAL                                              391.45         5.68
```
## Running Unit Tests
To ensure the correctness of the code, unit tests have been provided. You can run the tests using the unittest framework.

1. Run the tests:
```bash
python -m unittest discover
```
2. Measure code coverage:
```bash
coverage run -m unittest discover
```
3. Generate a coverage report:
```bash
coverage report
```

### Example Coverage Report
   ```
   Name                            Stmts   Miss  Cover
   ---------------------------------------------------
   filament_calculations.py           38      1    97%
   test_filament_calculations.py      46      1    98%
   ---------------------------------------------------
   TOTAL                              84      2    98%
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**

   ```bash
   git commit -am 'Add your feature'
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- **Spoolman API**: This script utilizes the Spoolman API for fetching spool data. [Spoolman API Documentation](https://donkie.github.io/Spoolman/)

---

*This README was created to provide clear instructions and information about the Filament Cost Calculator script. If you have any questions or need further assistance, please feel free to reach out.*
