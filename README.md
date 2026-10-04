# ⚡ UrjaMitra

### Low-cost energy intelligence for Indian small and medium-sized manufacturers

**Schneider Electric Hackathon 2026 — Smart Manufacturing: Industrial Energy & Process Efficiency**

> **Measure → Understand → Act**

UrjaMitra is a low-cost, retrofit energy-monitoring and intelligence solution designed for small and medium-sized manufacturing units that have limited automation, limited energy visibility, and limited capital for industrial monitoring systems.

**Live prototype:** https://urjamitra-9b9jjztfvmugtgjf6h2zez.streamlit.app/

---

## 🎯 The Problem

Small and medium-sized manufacturing units often have limited visibility into where and how electricity is being consumed.

Machines may continue running during non-production hours, compressors may operate unnecessarily, and abnormal energy consumption may remain unnoticed until the electricity bill arrives.

This matters because:

- Energy can represent **15–30% of production costs** in sectors such as foundries, textiles, ceramics and brick kilns.
- Many smaller units fall outside the **Perform, Achieve and Trade (PAT)** framework.
- EU **CBAM** and large buyers' **BRSR** reporting increasingly require supplier carbon data.
- Conventional industrial monitoring such as SCADA can cost **₹10 lakh or more** and can be difficult to install in plants with limited automation.

The core problem is simple:

> **The bill comes once a month. The waste happens every hour.**

---

## 💡 Our Solution

UrjaMitra brings data-driven energy management, predictive maintenance and process-efficiency insights to the factory floor without requiring a full SCADA installation.

The proposed Phase-1 architecture is:

```text
Clip-on CTs
     ↓
ESP32 Gateway
     ↓
MQTT
     ↓
Cloud Database
     ↓
Analytics
     ↓
UrjaMitra Dashboard
```

Selected machines such as furnaces, compressors and motors can be monitored without requiring production shutdown. Production quantity can be entered by an operator through a simple interface.

UrjaMitra converts raw energy measurements into information that an SME owner or operator can act on:

- Specific Energy Consumption (SEC)
- Machine-level load profiles
- Expected vs actual energy consumption
- Avoidable energy losses
- Monthly monetary impact
- Carbon emissions
- Practical recommendations

**Phase 1 is recommendation-only:** it does not modify machine settings or automatically control production equipment.

---

## 🔄 Measure → Understand → Act

### 1. Measure

Clip-on current transformers monitor selected machines such as:

- Furnaces
- Compressors
- Motors

An ESP32-based gateway collects readings. The proposed Phase-1 design uses a ready-made energy-metering module and MQTT communication.

The gateway can buffer readings during power/connectivity interruptions and send them when connectivity returns.

### 2. Understand

UrjaMitra calculates:

```text
SEC = Total energy consumed (kWh) / Units produced
```

A simple baseline model estimates expected consumption:

```text
kWh = a + b × units + c × temperature
```

The difference between expected and actual consumption can indicate possible avoidable energy losses.

### 3. Act

Explainable rules identify practical issues such as:

- Machine operation during non-production hours
- Abnormal compressor running
- Excess energy consumption relative to expected operation

Detected losses are converted into:

```text
Lost kWh → ₹ impact → CO₂ impact
```

This keeps recommendations understandable for non-technical users.

---

## 🚀 Key Features

### ⚡ Energy Monitoring

Machine-level energy visibility instead of waiting for a monthly electricity bill.

### 📊 Specific Energy Consumption

Track energy consumed per unit of production and compare baseline versus optimised operation.

### 🔎 Savings Finder

Ranks potential energy losses by estimated monthly financial impact and suggests practical actions.

### 🧠 Baseline Energy Model

Uses the explainable model:

```text
kWh = a + b × units + c × temperature
```

to estimate expected consumption and identify deviations.

### 🔧 Predictive Maintenance

The prototype demonstrates equipment-health monitoring using motor current and vibration trends to identify abnormal behaviour before a projected failure.

### 🕐 Tariff Optimisation

Evaluates movable loads and identifies opportunities to shift energy-intensive operations away from higher-tariff periods.

### 🌱 Carbon Ledger

Estimates electricity-related Scope 2 emissions and carbon intensity per product unit.

### 💰 ROI Calculator

Estimates:

- Annual energy savings
- Net savings after software/service cost
- Payback period

---

## 📈 Prototype Results

The current software prototype uses a **synthetic 30-day two-shift manufacturing plant**.

The simulated scenario demonstrates:

| Metric | Simulated result |
|---|---:|
| Baseline SEC | ~1.70 kWh/unit |
| Optimised SEC | ~1.40 kWh/unit |
| SEC reduction | ~18% |
| Simulated monthly energy-cost saving | ~₹1.02 lakh |
| Simulated CO₂e avoided | ~9.9 tCO₂e/month |
| Production throughput | Preserved |

### Important distinction

The ~18% reduction is **simulation output, not a field-validated saving**.

For planning and pilot deployment, UrjaMitra assumes **5–10% savings**. Real savings would be measured by comparing post-intervention consumption against expected consumption from a pre-intervention baseline, with uncertainty bounds.

> **UrjaMitra claims only what can be measured.**

---

## 🏗️ Proposed System Architecture

```text
┌─────────────────────────────────────┐
│            FACTORY FLOOR            │
│                                     │
│  Furnace    Compressor     Motor    │
│     │           │           │       │
│     └────── Clip-on CTs ────┘       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│          ESP32 EDGE GATEWAY          │
│                                     │
│  • Reads energy measurements        │
│  • Buffers during interruptions     │
│  • Sends readings using MQTT        │
└────────────────┬────────────────────┘
                 │ MQTT
                 ▼
┌─────────────────────────────────────┐
│           CLOUD / DATABASE          │
│                                     │
│  • Energy data                      │
│  • Production data                  │
│  • Temperature                      │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│           ANALYTICS LAYER           │
│                                     │
│  • SEC calculation                  │
│  • Baseline model                   │
│  • Rule-based loss detection        │
│  • ₹ impact                         │
│  • CO₂e calculation                 │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│          URJAMITRA DASHBOARD        │
│                                     │
│  Owner → Savings / ROI              │
│  Operator → Alerts / Actions        │
│  Exporter → Carbon data             │
└─────────────────────────────────────┘
```

### Data flow

The Phase-1 architecture is deliberately one-way:

**Factory → Gateway → Cloud → Analytics → Dashboard**

Phase 1 does **not** write control commands back to machinery.

---

## 🧮 Four Simple Models

### 1. SEC

```text
SEC = Total kWh / Units produced
```

SEC shows how much electricity is required for each unit of output.

### 2. Baseline

```text
Expected kWh = a + b × units + c × temperature
```

The model is fitted on a reference period. Expected versus actual consumption is then used to identify possible avoidable loss.

### 3. Rule Checks

Simple rules identify:

- Idle running
- Abnormal compressor operation
- Other avoidable loads

Potential financial impact is calculated as:

```text
Lost kWh × Tariff = ₹ per month
```

### 4. Carbon Ledger

```text
Scope 2 CO₂e = Electricity consumption × Applicable grid factor
```

The applicable grid emission factor should be used when deployed. The prototype uses a planning value rather than claiming a universal or latest official factor.

---

## 👷 Designed for the Shop Floor

UrjaMitra focuses on usability for non-technical SME users.

### Clip on, no shutdown

Sensors can be installed around selected conductors while production continues, subject to appropriate electrical safety procedures.

### Log output with a tap

Operators can enter production quantity through a simple interface.

### Every finding in rupees

Losses appear as estimated monthly rupees rather than only technical energy units.

### SEC without SCADA

Energy efficiency can be tracked without requiring a large SCADA infrastructure investment.

### Survives power cuts

The proposed gateway buffers readings and sends them when power/connectivity returns.

### Models you can explain

The analytics use straightforward arithmetic, rules and a simple fitted model rather than opaque black-box predictions.

> **If the owner cannot understand it, the owner will not use it.**

---

## 🔬 How We Will Prove It

UrjaMitra follows a staged validation approach.

### Phase 1 — Laboratory

- Perform controlled laboratory measurements.
- Compare sensor readings against a reference meter.
- Report measurement error.

### Phase 2 — Simulated Plant

- Use 30-day simulated plant data.
- Demonstrate SEC calculation and loss detection.
- Validate the software workflow.

### Phase 3 — Pilot

- Deploy on selected equipment at a partner unit.
- Establish a pre-intervention baseline.
- Use owner consent and qualified electrical personnel.

### Phase 4 — Measured Saving

Compare actual post-intervention consumption with expected consumption from the pre-intervention baseline.

Real savings will be reported with uncertainty bounds.

---

## 💰 Business Case

The planning case assumes:

- **Annual energy bill:** ₹30 lakh
- **Installation cost:** approximately ₹1.5 lakh
- **Service/software cost:** ₹3,000/month
- **Planning savings:** 5–10%

Indicative payback:

| Assumed saving | Approx. payback |
|---:|---:|
| 5% | 16 months |
| 7% | 10 months |
| 10% | 7 months |

These are **planning assumptions**, not guaranteed commercial returns. Installation costs and savings would be confirmed through quotations and pilot measurements.

### Potential business model

UrjaMitra can be offered through:

- One-time retrofit installation
- Monthly SaaS/monitoring fee
- Shared-savings model
- Scaled deployment across SME industrial clusters

---

## 🎯 Target Users

UrjaMitra is designed for small and medium-sized manufacturing units with limited automation and energy visibility.

Potential segments include:

- Foundries
- Textile manufacturing
- Ceramics
- Food processing
- Chemicals
- Brick kilns
- Other energy-intensive SME manufacturing units

The initial deployment concept is suited to semi-urban industrial clusters where expensive industrial automation infrastructure may be difficult to justify.

---

## 🌱 Decarbonisation Impact

UrjaMitra connects energy efficiency with carbon visibility:

```text
Energy use
    ↓
SEC
    ↓
CO₂e intensity
    ↓
Product-level carbon information
```

This can help SMEs understand their Scope 2 emissions and provide useful carbon information to customers and exporters.

An illustrative scaling scenario in the project proposal estimates that if 10,000 units each achieved 10% savings, the resulting national impact could be approximately:

- **950 GWh energy saved**
- **0.67 million tonnes CO₂e avoided annually**

This is an **illustrative projection, not a forecast**.

---

## 🛡️ Safety & Risk Approach

| Risk | Mitigation |
|---|---|
| Sensor measurement error | Calibrate against a reference meter |
| Missing production data | Operator input; fall back to energy per shift |
| Wi-Fi or power interruption | Gateway buffering |
| Electrical safety | Enclosed installation, fuse protection and qualified electrician |
| Savings lower than simulation | Plan around 5–10% and validate against baseline |
| Unsafe automation | Phase 1 does not control machinery |

---

## 🧰 Technology Stack

### Current software prototype

- Python
- Streamlit
- NumPy
- Pandas
- Plotly

### Proposed Phase-1 hardware / connectivity

- Clip-on current transformers
- ESP32
- PZEM-004T or suitable energy-metering module
- MQTT
- Cloud database

### Analytics

- Specific Energy Consumption
- Linear baseline model
- Rule-based loss detection
- Predictive maintenance trends
- Tariff analysis
- Scope 2 carbon calculation
- ROI/payback analysis

---

## 🖥️ Live Prototype

### Try UrjaMitra

**https://urjamitra-9b9jjztfvmugtgjf6h2zez.streamlit.app/**

The deployed Streamlit prototype demonstrates the analytics and dashboard layer using synthetic manufacturing data.

---

## ⚠️ Prototype & Data Disclaimer

This repository contains a **hackathon prototype**.

The current Streamlit application uses **synthetic plant data** to demonstrate the UrjaMitra workflow.

The following are proposed deployment components rather than claims of current field deployment:

- Physical CT sensor installation
- ESP32 gateway
- MQTT telemetry
- Cloud database
- Mobile/Tamil operator interface
- Live industrial equipment integration

The simulated savings shown by the prototype should **not** be interpreted as guaranteed real-world savings.

Actual performance would be established through calibrated measurements, a pre-intervention baseline, pilot deployment and uncertainty-aware evaluation.

---

## 📂 Project Structure

```text
urjamitra/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ Run Locally

Clone the repository:

```bash
git clone https://github.com/ritvikr-codes/urjamitra.git
cd urjamitra
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📋 Schneider Electric Challenge Alignment

| Challenge objective | UrjaMitra response |
|---|---|
| Reduce specific energy consumption | SEC baseline vs optimised analysis |
| Enable real-time visibility | Machine-level energy monitoring architecture |
| Support decarbonisation | Scope 2 carbon ledger and carbon intensity |
| Strengthen SME competitiveness | Low-cost retrofit + savings + ROI |
| Predictive maintenance | Motor current and vibration trend analysis |
| Process optimisation | Idle-load and tariff-shifting recommendations |
| Quantified improvement | Simulated SEC and cost/emissions impact |
| Deployment plan | Retrofit architecture + pilot roadmap |
| Business viability | Installation, service cost and payback model |

---

## 🔮 Future Scope

After successful Phase-1 validation, UrjaMitra can expand toward:

- Additional machine-level sensors
- Automated production-data integration
- ERP integration
- More advanced equipment-health models
- Renewable-energy integration
- Fuel and Scope 1 tracking
- Multi-site industrial-cluster dashboards
- Automated mobile alerts
- Optional closed-loop control after appropriate safety validation

The principle remains:

> **Measure → Understand → Act — without making the system unnecessarily complex.**

---

## 👥 Team

- **Gowtham V**
- **Ritvik R**
- **Kailesh S**

---

## 📚 Abbreviations

| Term | Meaning |
|---|---|
| SEC | Specific Energy Consumption |
| SCADA | Supervisory Control and Data Acquisition |
| PAT | Perform, Achieve and Trade |
| EU | European Union |
| CBAM | Carbon Border Adjustment Mechanism |
| BRSR | Business Responsibility and Sustainability Report |
| CT | Current Transformer |
| MQTT | Message Queuing Telemetry Transport |
| ESP32 | Low-cost microcontroller platform |

---

## ⚡ UrjaMitra

**Making energy waste visible, understandable and actionable for small manufacturers.**
