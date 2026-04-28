"""
Prompt templates for the Data Center Thermal AI project.

This module builds structured prompts for the future LLM explanation layer.
The goal is to ensure explanations are consistent, conservative, and grounded
in engineering context.
"""


def build_thermal_explanation_prompt(record, retrieved_context):
    """
    Build a structured prompt for explaining one rack-level thermal risk record.

    Args:
        record (dict): A dictionary containing telemetry, engineered features,
            and risk assessment outputs for one rack.
        retrieved_context (str): Engineering context retrieved from project
            documentation, such as docs/engineering_context.md.

    Returns:
        str: A formatted prompt string for the LLM.
    """

    prompt = f"""
You are a data center thermal decision-support assistant.

Your task is to explain the thermal risk condition for one data center rack
using the provided rack data, risk assessment outputs, and engineering context.

Use conservative engineering language.
Do not invent data.
Do not claim confirmed equipment failure.
Do not recommend automatic control actions.
Do not describe the risk_score as a validated probability of failure.
Keep the explanation human-in-the-loop.

ENGINEERING CONTEXT:
{retrieved_context}

RACK DATA:
rack_id: {record.get("rack_id")}
inlet_temp: {record.get("inlet_temp")}
outlet_temp: {record.get("outlet_temp")}
airflow: {record.get("airflow")}
fan_speed: {record.get("fan_speed")}
load_kw: {record.get("load_kw")}

ENGINEERED FEATURES:
delta_temp: {record.get("delta_temp")}
cooling_efficiency: {record.get("cooling_efficiency")}
airflow_per_kw: {record.get("airflow_per_kw")}
fan_speed_per_kw: {record.get("fan_speed_per_kw")}
thermal_risk_flag: {record.get("thermal_risk_flag")}

RISK ASSESSMENT OUTPUTS:
risk_score: {record.get("risk_score")}
risk_level: {record.get("risk_level")}
contributing_factors: {record.get("contributing_factors")}
primary_driver: {record.get("primary_driver")}
recommended_action: {record.get("recommended_action")}

OUTPUT FORMAT:
1. Risk Summary
2. Primary Driver
3. Supporting Evidence
4. Cause-and-Effect Explanation
5. Recommended Action
6. Uncertainty / Boundaries
7. Human-in-the-Loop Note\n
"""
    return prompt.strip()


if __name__ == "__main__":
    sample_record = {
        "rack_id": "R12",
        "inlet_temp": 28.4,
        "outlet_temp": 48.9,
        "airflow": 650,
        "fan_speed": 0.62,
        "load_kw": 9.5,
        "delta_temp": 20.5,
        "cooling_efficiency": 2.16,
        "airflow_per_kw": 68.42,
        "fan_speed_per_kw": 0.065,
        "thermal_risk_flag": 1,
        "risk_score": 80,
        "risk_level": "Critical",
        "contributing_factors": [
            "Excessive temperature rise",
            "Insufficient airflow per loadzzzz"
        ],
        "primary_driver": "Insufficient airflow per load",
        "recommended_action": "Inspect fans, air pathways, and airflow management for this rack."
    }

    sample_context = """

Low airflow per kW suggests insufficient cooling delivery relative to heat generation.
High delta temperature means the air is gaining significant heat across the rack.
The system should recommend investigation, not automatic control action.
"""

    print(build_thermal_explanation_prompt(sample_record, sample_context))