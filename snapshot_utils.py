# snapshot_utils.py
import json
import datetime

def save_snapshot(spools):
    """
    Saves the current state of all spools to a file named snapshot_<timestamp>.json.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"snapshot_{timestamp}.json"

    snapshot_data = []
    for spool in spools:
        snapshot_data.append({
            "id": spool.get("id"),
            "price": spool.get("price"),
            "initial_weight": spool.get("initial_weight"), 
            "remaining_weight": spool.get("remaining_weight"),
            "filament": {
                "name": spool["filament"].get("name"),
                "material": spool["filament"].get("material"),
                "color_hex": spool["filament"].get("color_hex"),
            },
        })

    with open(filename, "w") as snapshot_file:
        json.dump(snapshot_data, snapshot_file, indent=2)

    print(f"Snapshot saved to {filename}")


def compare_snapshots(snapshot1_path, snapshot2_path, show_zero_diff=False):
    """
    Compares two snapshot files and prints the differences in remaining_weight (grams) 
    and the approximate usage cost. By default, it only shows spools that changed. 
    Set 'show_zero_diff=True' to list all spools, even those with no changes.
    """
    with open(snapshot1_path, 'r') as f1:
        snapshot1_data = json.load(f1)
    with open(snapshot2_path, 'r') as f2:
        snapshot2_data = json.load(f2)

    # Convert snapshots to dicts keyed by spool ID
    snapshot1_dict = {item['id']: item for item in snapshot1_data}
    snapshot2_dict = {item['id']: item for item in snapshot2_data}

    print(f"\nComparing {snapshot1_path} and {snapshot2_path}...\n")
    print(f"{'Spool ID':<10} {'Name':<30} {'Weight Diff (g)':>15} {'Cost Used($)':>12}")
    print("-" * 70)

    total_weight_used = 0.0
    total_cost_used = 0.0

    # Gather results, then print them
    results = []

    # For each spool in snapshot2 (the 'end' state), compare to snapshot1 (the 'start' state)
    for spool_id, spool2 in snapshot2_dict.items():
        spool1 = snapshot1_dict.get(spool_id)
        if spool1:
            name = spool2['filament'].get('name', 'Unknown')
            rem_weight_1 = spool1.get('remaining_weight', 0.0)
            rem_weight_2 = spool2.get('remaining_weight', 0.0)
            weight_diff = rem_weight_1 - rem_weight_2

            if weight_diff != 0:
                spool_price = spool1.get('price', 0.0)
                spool_initial_weight = spool1.get('initial_weight', 1000.0)
                cost_used = 0.0
                if spool_initial_weight > 0:
                    # Approximate usage cost proportionally to used weight
                    cost_used = spool_price * (abs(weight_diff) / spool_initial_weight)
                results.append((spool_id, name, weight_diff, cost_used))

                total_weight_used += abs(weight_diff)
                total_cost_used += cost_used
            else:
                # If 'show_zero_diff' is True, also include spools with weight_diff = 0
                if show_zero_diff:
                    results.append((spool_id, name, 0.0, 0.0))
        else:
            # This spool wasn't in snapshot1—could print or ignore
            if show_zero_diff:
                name2 = spool2['filament'].get('name', 'Unknown')
                results.append((spool_id, name2, 0.0, 0.0))

    # Optionally, sort results by spool_id or weight diff
    # results.sort(key=lambda x: x[0])  # by spool_id

    for spool_id, name, weight_diff, cost_used in results:
        print(f"{spool_id:<10} {name:<30} {weight_diff:>15.2f} {cost_used:>12.2f}")

    # Print a final summary line
    print("-" * 70)
    print(f"{'TOTAL':<10} {'':<30} {total_weight_used:>15.2f} {total_cost_used:>12.2f}")