import numpy as np
import pandas as pd

def generate_synthetic_datacenter_data(
    num_racks=50,
    num_samples=1000,
    random_seed=42
):
    """
    Generate synthetic data center rack-level thermal telemetry.

    Each row represents a snapshot in time for a given rack.
    This data is physics-inspired, not random noise.
    """

    np.random.seed(random_seed)

    rack_ids = [f"R{str(i).zfill(2)}" for i in range(1, num_racks + 1)]
    data = []

    for _ in range(num_samples):
        rack_id = np.random.choice(rack_ids)

        # IT load (kW)
        load_kw = np.random.uniform(3.0, 12.0)

        # Fan speed (normalized 0–1)
        fan_speed = np.random.uniform(0.5, 1.0)

        # Airflow (CFM) proportional to fan speed
        airflow = fan_speed * np.random.uniform(800, 1600)

        # Inlet temperature (°C)
        inlet_temp = np.random.normal(22, 2)

        # Heat rise depends on load and airflow
        delta_temp = (load_kw * 8) / airflow * 100
        outlet_temp = inlet_temp + delta_temp + np.random.normal(0, 0.5)

        data.append([
            rack_id,
            inlet_temp,
            outlet_temp,
            airflow,
            fan_speed,
            load_kw
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "rack_id",
            "inlet_temp",
            "outlet_temp",
            "airflow",
            "fan_speed",
            "load_kw"
        ]
    )

    return df


if __name__ == "__main__":
    df = generate_synthetic_datacenter_data()
    df.to_csv("data/synthetic/rack_thermal_data.csv", index=False)
    print("Synthetic data generated and saved.")
