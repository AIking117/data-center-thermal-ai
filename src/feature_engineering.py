import pandas as pd
import os

def engineer_features(df):
    """
    Transforms raw datacenter rack telemetry into engineered features.

    Args:
        df (pd.DataFrame): Input DataFrame with columns:
            - rack_id
            - inlet_temp
            - outlet_temp
            - airflow
            - fan_speed
            - load_kw

    Returns:
        pd.DataFrame: DataFrame with original columns plus new engineered features:
            - delta_temp
            - cooling_efficiency
            - airflow_per_kw
            - fan_speed_per_kw
            - thermal_risk_flag
    """
    # Calculate delta_temp: difference between outlet and inlet temperatures
    df['delta_temp'] = df['outlet_temp'] - df['inlet_temp']

    # Calculate cooling_efficiency: delta_temp divided by load_kw
    # Note: Assumes load_kw > 0; handle division by zero if necessary
    df['cooling_efficiency'] = df['delta_temp'] / df['load_kw']

    # Calculate airflow_per_kw: airflow divided by load_kw
    df['airflow_per_kw'] = df['airflow'] / df['load_kw']

    # Calculate fan_speed_per_kw: fan_speed divided by load_kw
    df['fan_speed_per_kw'] = df['fan_speed'] / df['load_kw']

    # Calculate thermal_risk_flag: 1 if inlet_temp > 27 or delta_temp > 20, else 0
    df['thermal_risk_flag'] = ((df['inlet_temp'] > 27) | (df['delta_temp'] > 20)).astype(int)

    return df

if __name__ == "__main__":
    # Define file paths
    input_path = os.path.join('data', 'synthetic', 'rack_thermal_data.csv')
    output_path = os.path.join('data', 'processed', 'rack_features.csv')

    # Read the input CSV
    df = pd.read_csv(input_path)

    # Apply feature engineering
    df_engineered = engineer_features(df)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the result to output CSV
    df_engineered.to_csv(output_path, index=False)

    print(f"Feature engineering complete. Output saved to {output_path}")