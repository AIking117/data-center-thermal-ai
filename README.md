# Data Center Thermal Digital Twin

## Overview

A synthetic data center thermal digital twin project that uses physics-inspired telemetry, feature engineering, machine learning, and reinforcement learning to model rack-level thermal behavior and evaluate cooling control strategies.

This project began as an LLM-based thermal risk explainer, but has been reframed into a predictive modeling and control project. The original rule-based thermal risk pipeline is preserved as a baseline, while the new direction adds a surrogate machine learning model and a reinforcement learning control agent.

The goal is to demonstrate practical AI/ML applied to a mechanical and infrastructure engineering problem: keeping data center racks within acceptable thermal conditions while minimizing unnecessary cooling energy use.

---

## Why This Project Was Reframed

The original architecture followed this path:

```text
telemetry → engineered features → rule-based risk score → RAG context → LLM explanation
```

That was useful, but it made this project too similar to a general RAG-based question-answering system.

The revised architecture adds a stronger technical core:

```text
telemetry → engineered features → baseline risk assessment → surrogate ML model → RL control agent
```

This makes the project more distinct, more engineering-focused, and better aligned with digital twin, thermal systems, and control-oriented AI work.

The LLM explanation layer is now optional v2 polish rather than the backbone of the project.

---

## Problem Statement

Data centers must manage rack-level heat generation, airflow delivery, and cooling energy use. Operators need to avoid thermal risk, but simply running cooling at maximum capacity wastes energy.

A useful AI system should not only identify risky thermal conditions, but also help evaluate control strategies that balance:

- Rack thermal safety
- Airflow and cooling response
- Energy cost
- Operational constraints
- Human review before action

This project uses synthetic rack-level telemetry to build and test that decision-making workflow.

---

## Objective

The goal of this project is to design a synthetic data center thermal digital twin that:

1. Generates physics-inspired rack thermal telemetry
2. Engineers meaningful thermal and airflow features
3. Uses rule-based risk assessment as a baseline
4. Trains a surrogate ML model to predict thermal risk or future temperature behavior
5. Builds a simple reinforcement learning agent to choose cooling actions
6. Compares the RL agent against a naive always-max-cooling baseline
7. Documents results with reproducible scripts and clear evaluation metrics

---

## Revised System Architecture

The project follows this modular pipeline:

### 1. Synthetic Data Generation

- Generates rack-level telemetry
- Includes inlet temperature, outlet temperature, airflow, fan speed, and load
- Simulates normal and elevated-risk conditions

### 2. Feature Engineering

Derived engineering metrics include:

- Temperature differential (`delta_temp`)
- Cooling efficiency / thermal rise per kW
- Airflow per unit load
- Fan speed per unit load
- Thermal risk flag

### 3. Rule-Based Risk Assessment

The current baseline system produces:

- Risk scores
- Risk levels
- Contributing factors
- Primary risk drivers
- Recommended operator actions

This rule-based system is preserved as the baseline for later ML comparison.

### 4. Surrogate ML Model

Planned next major module.

The surrogate model will learn to predict rack thermal behavior from engineered features, such as:

- `outlet_temp`
- `delta_temp`
- `risk_score`
- or `risk_level`

This becomes the digital twin core: a learned approximation of thermal behavior.

### 5. Reinforcement Learning Control Agent

Planned after the surrogate model.

The RL agent will operate in a synthetic environment and choose simple cooling actions, such as increasing or decreasing fan speed or cooling intensity.

The agent’s objective will be to:

- Reduce thermal risk
- Avoid excessive energy use
- Stay within predefined safety bounds

### 6. Optional LLM Explanation Layer

The LLM explanation layer is now considered optional v2 work.

If added later, it will explain the model or RL agent’s recommended action in engineering language, but the project should stand on its own without requiring an LLM.

---

## Current Project Direction

The project now focuses on:

- Generating synthetic rack-level thermal telemetry
- Engineering thermal and airflow features
- Assessing thermal risk using a rule-based baseline
- Training a surrogate ML model to predict rack thermal behavior
- Building a simple reinforcement learning agent to balance cooling energy use against thermal risk
- Optionally adding an LLM explanation layer as a later v2 feature

---

## Data Strategy

This project uses synthetic data generation to simulate realistic rack-level data center conditions.

This approach enables:

- Controlled experimentation
- Reproducibility
- Safe testing of control logic
- Clear comparison between baselines and learned models
- No dependency on proprietary facility data

All data is synthetic and intended for demonstration purposes only.

---

## Technologies

- Python
- Pandas / NumPy
- Scikit-learn
- Reinforcement learning methods
- GitHub
- VS Code
- Optional later: OpenAI API / LLM explanation layer
- Optional later: Streamlit UI

---

## Project Status

### Completed

- Repository initialized
- Synthetic data generation module implemented (`src/data_generation.py`)
- Feature engineering module implemented (`src/feature_engineering.py`)
- Rule-based thermal risk assessment module implemented (`src/risk_assessment.py`)
- Structured prompt template created for optional future LLM layer (`src/prompt_templates.py`)
- Project scope reframed as a digital twin / ML control project (`docs/Scope.md`)
- Engineering context documentation moved into `docs/engineering_context.md`

### Current Outputs

The current pipeline produces:

- Engineered thermal features
- Risk scores
- Risk levels
- Contributing factors
- Primary risk drivers
- Recommended operator actions

### In Progress

- README update for digital twin direction
- Preparing the project for surrogate ML model development

### Next Steps

- Add a one-command pipeline runner
- Build `src/surrogate_model.py`
- Define baseline metrics before model training
- Train and evaluate the surrogate model
- Build a simple synthetic thermal control environment
- Add a reinforcement learning control agent
- Compare RL performance against a naive cooling baseline

---

## Acceptance Criteria for v1

The v1 project will be considered complete when:

1. A surrogate model is trained and evaluated against a rule-based baseline
2. Evaluation metrics are defined before training
3. The RL agent is evaluated across simulated episodes
4. The RL agent achieves lower average energy cost than a naive always-max-cooling baseline while keeping thermal risk within acceptable limits
5. Results are reproducible from documented scripts or notebooks
6. README and documentation clearly explain the architecture, scope, and limitations

---

## Key Skills Demonstrated

- Synthetic data generation
- Feature engineering for thermal systems
- Rule-based baseline modeling
- Supervised machine learning
- Digital twin architecture
- Reinforcement learning for control decisions
- Mechanical engineering reasoning applied to AI/ML
- Reproducible project structure
- Git/GitHub version control

---

## Future Work

- Improve the synthetic thermal environment
- Add surrogate regression and classification models
- Add reinforcement learning control policies
- Add model evaluation plots and metrics
- Add a simple dashboard or UI
- Add optional LLM explanations for model or RL decisions
- Explore more advanced digital twin modeling
- Explore physics-informed ML or simulation-informed learning

---

## Disclaimer

This project uses synthetic data only. It is intended for learning, demonstration, and portfolio development.

It is not connected to a real building management system, data center control system, SCADA system, or production facility. It does not make live operational control decisions.

---

## Design Philosophy

This project emphasizes practical AI/ML for engineering systems. The focus is not only on model complexity, but on building a believable workflow that connects thermal reasoning, prediction, control, evaluation, and human oversight.

