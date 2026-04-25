# Engineering Context

## Project Purpose

This document defines the engineering context used by the AI system in this project.

It is intended to support:
- understanding of the thermal risk pipeline
- future Retrieval-Augmented Generation (RAG) grounding for LLM explanations

This project explores how an LLM-based decision-support system can explain data center thermal and airflow conditions in clear engineering language.

The system is designed to translate rack-level telemetry into:
- interpretable thermal features
- risk assessment outputs
- operator-facing explanations
- recommended actions

The goal is not to automate control decisions. The goal is to support human operators by making thermal risks easier to understand and investigate.

---

## System Scope

The current system evaluates rack-level thermal and airflow conditions using synthetic telemetry.

The scope is limited to decision support. The system is designed to identify thermal risk patterns, support explanation, and recommend investigation steps.

The system does not make final operational decisions.

---

## Data Center Cooling Terms

### CRAC

CRAC stands for **Computer Room Air Conditioner**.

A CRAC unit is a data center cooling unit that typically uses compressor-based or refrigerant-based cooling to condition air in the computer room.

### CRAH

CRAH stands for **Computer Room Air Handler**.

A CRAH unit is a data center air-handling unit that typically moves air across chilled-water coils to remove heat.

### LLM Guidance

The LLM may mention CRAC or CRAH systems only as possible cooling infrastructure context.

The LLM should not claim CRAC, CRAH, or cooling equipment failure unless equipment-level data is available.

---

## Raw Telemetry Signals

The synthetic dataset represents rack-level thermal and airflow telemetry.

### `rack_id`

A unique identifier for a data center rack.

A rack is treated as a monitored thermal asset containing servers or compute equipment.

LLM guidance:
- Use `rack_id` only to identify which rack is being evaluated.
- Do not infer physical rack location, aisle position, or nearby cooling equipment unless layout data is provided.

---

### `inlet_temp`

The temperature of air entering the rack.

High inlet temperature may indicate poor cold aisle conditions, insufficient cooling supply, or recirculation of hot exhaust air.

Engineering meaning:
- High inlet temperature reduces cooling margin.
- Warm intake air makes it harder for the rack to reject heat effectively.

LLM guidance:
- If `inlet_temp` is high, explain that the rack may be receiving warmer-than-desired intake air.
- Do not claim CRAC, CRAH, or cooling equipment failure unless equipment-level data is available.

---

### `outlet_temp`

The temperature of air leaving the rack.

Outlet temperature is expected to be higher than inlet temperature because servers generate heat during operation.

Engineering meaning:
- High outlet temperature can indicate thermal stress.
- Outlet temperature should be interpreted with `load_kw`, `airflow`, and `delta_temp`.

LLM guidance:
- Use high outlet temperature as evidence of thermal stress.
- Do not treat outlet temperature alone as the root cause.

---

### `airflow`

The estimated airflow available to the rack.

Lower airflow can reduce heat removal and increase the likelihood of thermal stress.

Engineering meaning:
- Airflow supports convective heat removal.
- Low airflow may indicate airflow obstruction, fan underperformance, poor containment, or supply imbalance.
- Low airflow is more meaningful when compared against rack load.

LLM guidance:
- If airflow is low relative to load, describe insufficient cooling delivery as a likely contributor.
- Do not claim fan failure unless fan data or fault metadata supports that conclusion.

---

### `fan_speed`

A normalized representation of fan operation.

Fan speed is used as an approximate indicator of cooling effort or airflow support.

Engineering meaning:
- Higher fan speed generally suggests greater cooling effort.
- Low fan speed under high load may suggest inadequate cooling response.
- High fan speed with low airflow may suggest airflow restriction.

LLM guidance:
- Use fan speed as supporting evidence.
- Do not diagnose equipment failure based on fan speed alone.

---

### `load_kw`

The electrical or compute load associated with the rack.

Higher load generally means more heat generation.

Engineering meaning:
- Higher `load_kw` generally increases heat generation.
- High load is not automatically a fault.
- High load becomes more concerning when paired with insufficient airflow, high inlet temperature, or high temperature rise.

LLM guidance:
- Treat high load as a heat-generation driver.
- Only describe high load as risky when paired with poor cooling indicators.

---

## Engineered Features

### `delta_temp`

The temperature rise across the rack.

This is calculated as:

```text
delta_temp = outlet_temp - inlet_temp
```

A larger temperature rise may indicate that the rack is producing significant heat or that cooling is not keeping up with the load.

Engineering meaning:
- High `delta_temp` may indicate high heat load, insufficient airflow, or both.
- `delta_temp` should be interpreted with `load_kw` and `airflow_per_kw`.

LLM guidance:
- If `delta_temp` is high, explain that the rack air is gaining significant heat.
- If `delta_temp` is high and airflow is low, explain that insufficient airflow may be contributing to poor heat removal.
- If `delta_temp` is high and load is high, explain that elevated heat generation may be a contributing factor.

---

### `airflow_per_kw`

The amount of airflow available per unit of rack load.

This is calculated as:

```text
airflow_per_kw = airflow / load_kw
```

Low airflow per kW suggests that the rack may not have enough cooling capacity relative to its heat generation.

Engineering meaning:
- Low `airflow_per_kw` indicates insufficient cooling delivery relative to load.
- This is one of the clearest indicators of airflow-related thermal risk.

LLM guidance:
- If `airflow_per_kw` is low, identify insufficient airflow relative to load as a likely contributor.
- Prefer this explanation over simply saying “airflow is low.”

---

### `cooling_efficiency`

In the current version of this project, this feature represents temperature rise per kW of load.

This is calculated as:

```text
cooling_efficiency = delta_temp / load_kw
```

A higher value indicates more temperature rise for each unit of load, which may suggest higher thermal stress.

Important naming note:
- This is not true thermodynamic efficiency.
- This name may be refined in a future version to something clearer, such as `thermal_rise_per_kw`.

LLM guidance:
- If `cooling_efficiency` is high, explain that the rack is experiencing high thermal rise relative to load.
- Do not describe this feature as formal thermodynamic efficiency.

---

### `fan_speed_per_kw`

The fan speed value normalized by rack load.

This is calculated as:

```text
fan_speed_per_kw = fan_speed / load_kw
```

This feature gives a simple indication of cooling effort relative to the thermal load.

Engineering meaning:
- Low `fan_speed_per_kw` may suggest fan response is not keeping pace with heat generation.
- This is a simplified proxy, not a validated equipment-health metric.

LLM guidance:
- Use this feature only as supporting evidence.
- Do not make direct equipment failure claims based only on this feature.

---

### `thermal_risk_flag`

A basic rule-based indicator that flags elevated thermal risk conditions.

It is triggered when:
- inlet temperature is greater than 27°C, or
- temperature rise across the rack is greater than 20°C

This is an early-stage risk signal, not a final diagnosis.

LLM guidance:
- Treat this flag as a signal that additional explanation is needed.
- Do not present this flag as proof of failure.

---

## Basic Thermal Reasoning

Data center racks generate heat as electrical load increases.

Cooling performance depends on whether enough cool air reaches the rack and whether heat is removed effectively.

Important relationships include:

- Higher `load_kw` generally increases heat generation.
- Lower `airflow` reduces heat removal.
- Higher `inlet_temp` reduces the available cooling margin.
- Higher `delta_temp` may indicate increased thermal stress.
- Low `airflow_per_kw` may suggest insufficient airflow relative to load.
- High `cooling_efficiency` in this project means high thermal rise per kW, not formal thermodynamic efficiency.

The project uses these relationships to support risk assessment and later LLM-based explanations.

---

## Risk Assessment Context

The current risk assessment module converts engineered features into:

- `risk_score`
- `risk_level`
- `contributing_factors`
- `primary_driver`
- `recommended_action`

These outputs provide structured context for the future LLM explanation layer.

Instead of asking the LLM to interpret raw numbers alone, the system provides intermediate engineering reasoning first.

This improves:
- consistency
- explainability
- operator trust
- control over LLM responses

---

## Risk Assessment Outputs

### `risk_score`

A numeric rule-based score representing estimated thermal concern.

LLM guidance:
- Use `risk_score` to describe relative severity.
- Do not describe it as a validated probability of failure.

---

### `risk_level`

A categorical severity level derived from `risk_score`.

Expected values may include:
- Low
- Medium
- High
- Critical

LLM guidance:
- Use `risk_level` to set tone and urgency.
- For High or Critical risk, recommend investigation, not automatic shutdown.

---

### `contributing_factors`

A list of detected factors that contributed to the risk score.

Examples:
- high inlet temperature
- excessive temperature rise
- high thermal rise per kW
- insufficient airflow per load

LLM guidance:
- Use these as explanation evidence.
- Do not invent additional contributing factors not present in the data or retrieved context.

---

### `primary_driver`

The highest-priority detected contributor to the risk condition.

LLM guidance:
- Use this as the main explanation anchor.
- Explain secondary contributors separately if available.

---

### `recommended_action`

A conservative operator-facing recommendation generated by the rule-based system.

LLM guidance:
- The LLM may rephrase the recommendation for clarity.
- The LLM must not escalate the recommendation into automatic control action.
- The LLM should preserve the human-in-the-loop principle.

---

## Thermal Reasoning Rules

### Rule 1: Load increases heat generation

Higher `load_kw` generally increases heat generation.

Correct explanation:
- “The rack load is elevated, which may increase heat output.”

Avoid:
- “The high load means the rack is failing.”

---

### Rule 2: Airflow supports heat removal

Lower airflow reduces convective heat removal.

Correct explanation:
- “Airflow appears insufficient relative to load, reducing heat removal capacity.”

Avoid:
- “The fan has failed.”

---

### Rule 3: High inlet temperature reduces cooling margin

Warmer intake air reduces the rack’s ability to reject heat.

Correct explanation:
- “The rack is receiving warmer intake air, reducing cooling margin.”

Avoid:
- “The cooling unit is broken.”

---

### Rule 4: High delta temperature indicates thermal rise

A high `delta_temp` means the air is gaining significant heat across the rack.

Correct explanation:
- “The rack shows elevated temperature rise across the inlet-to-outlet path.”

Avoid:
- “The rack is definitely overheating due to one specific cause.”

---

### Rule 5: Explanations must include uncertainty

Because the system uses synthetic data and simplified thresholds, explanations must remain conservative.

Correct explanation:
- “The likely contributor is insufficient airflow relative to load.”

Avoid:
- “This is confirmed equipment failure.”

---

## Assumptions

This project currently assumes:
- Data is synthetic and generated for demonstration purposes.
- Each row represents a rack-level operating condition.
- Higher rack load increases heat generation.
- Reduced airflow can increase thermal risk.
- High inlet temperature reduces cooling margin.
- Rule-based thresholds are simplified and not production-grade.
- Recommended actions are advisory only.

---

## System Boundaries
This project does not currently include:
- real data center telemetry
- live BMS or SCADA integration
- CFD simulation
- real-time control logic
- validated production thresholds
- automated control actions
- confirmed equipment failure diagnosis

This project is a prototype for learning and demonstrating rack-level decision support for data center thermal analysis.

This prototype can be further explored and advanced toward industry deployment.

---

## LLM Explanation Requirements

When generating an operator-facing explanation, the LLM should include:

1. **Risk Summary**
   - State the rack condition and risk level.

2. **Primary Driver**
   - Identify the main risk driver.

3. **Supporting Evidence**
   - Reference relevant telemetry and engineered features.

4. **Cause-and-Effect Chain**
   - Explain how the signals relate physically.

5. **Recommended Action**
   - Provide a conservative next step.

6. **Uncertainty / Limitations**
   - State what cannot be confirmed from the available data.

7. **Human-in-the-Loop Statement**
   - Remind that operators should validate conditions before action.

---

## LLM Behavior Constraints

The LLM should not:
- claim confirmed equipment failure
- recommend automatic control changes
- invent sensor readings
- invent rack location or layout details
- invent cooling equipment status
- treat synthetic thresholds as production-grade
- describe `risk_score` as a validated probability of failure
- ignore uncertainty
- override human operator judgment

The LLM should:
- use engineering language
- remain conservative
- explain cause and effect clearly
- distinguish evidence from assumptions
- recommend inspection or review when uncertainty exists
- keep humans responsible for operational decisions

---

## Human-in-the-Loop Principle

The LLM explanation layer should support human judgment, not replace it.

Operators should remain responsible for:
- validating system conditions
- confirming sensor reliability
- checking site conditions
- confirming equipment status
- deciding whether action is required
- approving maintenance or operational changes

The system should explain, recommend, and communicate uncertainty clearly.
