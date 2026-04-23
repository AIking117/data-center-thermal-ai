import pandas as pd
import os

def assess_risk(df):
    """
    Assesses thermal risk for datacenter racks based on engineered features.

    Args:
        df (pd.DataFrame): DataFrame with engineered features from feature_engineering.py.

    Returns:
        pd.DataFrame: DataFrame with additional risk assessment columns:
            - risk_score (0-100 scale)
            - risk_level (Low/Medium/High/Critical)
            - contributing_factors (list of contributing factors)
            - primary_driver (most important contributing factor)
            - recommended_action (operator guidance)

    Note:
        In this early version, `cooling_efficiency` represents temperature rise per kW.
        Higher values indicate higher thermal stress. Later this feature can be
        renamed to `thermal_rise_per_kw` for clarity.
    """
    # Calculate risk score based on multiple factors
    # Weights: thermal_risk_flag (40%), cooling_efficiency (30%), delta_temp (20%), airflow_per_kw (10%)
    # Note: cooling_efficiency is currently defined as delta_temp / load_kw.
    # A higher value means more temperature rise per kW, which is worse.
    df['risk_score'] = (
        df['thermal_risk_flag'] * 40 +
        (df['cooling_efficiency'] > 0.5).astype(int) * 30 +
        (df['delta_temp'] > 15).astype(int) * 20 +
        (df['airflow_per_kw'] < 100).astype(int) * 10
    ).clip(0, 100)

    # Classify risk level
    df['risk_level'] = pd.cut(
        df['risk_score'],
        bins=[-1, 25, 50, 75, 100],
        labels=['Low', 'Medium', 'High', 'Critical'],
        include_lowest=True
    )

    # Identify contributing factors
    def get_contributing_factors(row):
        factors = []
        if row['thermal_risk_flag'] == 1:
            factors.append('High inlet temperature or large delta temperature')
        if row['cooling_efficiency'] > 0.5:
            factors.append('High thermal rise per kW')
        if row['delta_temp'] > 15:
            factors.append('Excessive temperature rise')
        if row['airflow_per_kw'] < 100:
            factors.append('Insufficient airflow per load')
        return factors

    df['contributing_factors'] = df.apply(get_contributing_factors, axis=1)

    def choose_primary_driver(factors):
        if not factors:
            return 'No elevated thermal risk detected'
        priority = [
            'High inlet temperature or large delta temperature',
            'Excessive temperature rise',
            'High thermal rise per kW',
            'Insufficient airflow per load'
        ]
        for driver in priority:
            if driver in factors:
                return driver
        return factors[0]

    df['primary_driver'] = df['contributing_factors'].apply(choose_primary_driver)

    def choose_recommended_action(driver):
        if driver == 'No elevated thermal risk detected':
            return 'Continue normal monitoring.'
        if driver == 'High inlet temperature or large delta temperature':
            return 'Inspect inlet air conditions and verify rack intake cooling.'
        if driver == 'Excessive temperature rise':
            return 'Check rack heat load and cooling delivery for the affected rack.'
        if driver == 'High thermal rise per kW':
            return 'Review cooling efficiency and consider increasing airflow or reducing load.'
        if driver == 'Insufficient airflow per load':
            return 'Inspect fans, air pathways, and airflow management for this rack.'
        return 'Review rack thermal metrics and investigate anomalies.'

    df['recommended_action'] = df['primary_driver'].apply(choose_recommended_action)

    return df

if __name__ == "__main__":
    # Define file paths
    input_path = os.path.join('data', 'processed', 'rack_features.csv')
    output_path = os.path.join('data', 'processed', 'rack_risks.csv')

    # Read the input CSV
    df = pd.read_csv(input_path)

    # Apply risk assessment
    df_assessed = assess_risk(df)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the result to output CSV
    df_assessed.to_csv(output_path, index=False)

    print(f"Risk assessment complete. Output saved to {output_path}")
    print(f"Sample critical racks: {df_assessed[df_assessed['risk_level'] == 'Critical'].shape[0]} found")