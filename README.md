# Data Center Thermal AI

## Overview
An LLM-based decision support system using Retrieval-Augmented Generation (RAG) to provide **explainable thermal analysis for data center operations**.

The system translates raw sensor telemetry into **clear, engineering-level explanations** that help operators understand:
- What is happening  
- Why it is happening  
- What actions should be taken  

The focus is not just prediction, but **explainability, operational trust, and actionable insight**.

---

## Problem Statement
Modern data centers generate large volumes of telemetry data (temperature, airflow, load, etc.). While monitoring systems can detect anomalies, they often fail to provide:

- Root cause explanations  
- Contextual interpretation  
- Actionable recommendations  

As a result, operators must manually interpret alerts, leading to:
- Delayed responses  
- Misdiagnosis  
- Reduced trust in automated systems  

---

## Objective
The goal of this project is to design an AI system that:

1. Processes data center thermal telemetry  
2. Identifies potential issues  
3. Uses an LLM to generate **causal, structured explanations**  
4. Provides **clear operational recommendations**  
5. Communicates **uncertainty and limitations**  

---

## System Architecture

The system follows a modular pipeline:

### 1. Data Generation
- Synthetic, physics-inspired rack-level telemetry  
- Includes fault scenarios (e.g., airflow blockage, overload)  

### 2. Feature Engineering
- Derived engineering metrics such as:
  - Temperature differential (`ΔT`)
  - Airflow per unit load  
  - Cooling efficiency indicators  

### 3. Risk Assessment
- Identifies abnormal conditions  
- Produces:
  - Risk scores  
  - Severity classification  
  - Key contributing factors  

### 4. Context Layer (RAG)
- Stores domain knowledge:
  - Thermal management principles  
  - Operational rules  
  - Known failure patterns  

### 5. LLM Explanation Layer
Generates structured outputs:
- Primary cause  
- Secondary contributors  
- Cause–effect chain  
- Recommended action  
- Confidence and limitations  

### 6. Evaluation
- Human-in-the-loop feedback  
- Basic validation checks  

### 7. User Interface (Planned)
Displays:
- System explanations  
- Latency  
- Estimated cost per query  

---

## Example Output

**Input (simplified):**
- High outlet temperature  
- Low airflow  
- Increased load  

**LLM Output:**
> The elevated temperature is primarily driven by reduced airflow relative to the current load.  
> This suggests insufficient convective cooling, likely due to airflow restriction or degraded fan performance.  
> It is recommended to inspect airflow pathways and verify fan operation.  
> Confidence is moderate due to potential sensor variability.

---

## Data Strategy
This project uses **synthetic data generation** to simulate realistic data center conditions, including:
- Thermal behavior  
- Airflow variation  
- Operational faults  

This approach enables:
- Controlled experimentation  
- Reproducibility  
- Focus on system design  

---

## Technologies
- Python (data processing and pipeline)  
- Pandas / NumPy  
- LLM APIs (e.g., OpenAI)  
- Retrieval-Augmented Generation (RAG)  
- GitHub (version control)  
- VS Code with Copilot (development environment)  
- Streamlit (planned UI)  

---

## Project Status

### Completed
- Repository initialized  
- Data generation module implemented (`src/data_generation.py`)  
- System architecture defined  

### In Progress
- Feature engineering  
- Risk assessment logic  
- LLM prompt design  

---

## Key Skills Demonstrated
- AI system design (end-to-end)  
- Integration of LLMs into engineering workflows  
- Feature engineering based on physical systems  
- Explainable AI (XAI) principles  
- Retrieval-Augmented Generation (RAG)  
- Human-in-the-loop evaluation design  

---

## Future Work
- Real-world dataset integration  
- Advanced anomaly detection models  
- Enhanced evaluation metrics (e.g., RAGAS)  
- Expanded UI and visualization  
- Latency and cost optimization  

---

## Disclaimer
All data used in this project is synthetic and intended for demonstration purposes only.

---

## Design Philosophy
This project emphasizes **practical deployment of AI in engineering systems**, focusing on usability, interpretability, and real-world constraints rather than model complexity alone.
