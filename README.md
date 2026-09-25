# 📡 Smart Scan — Adaptive RF Spectrum Simulation & AI Engine

A modular, real-time Radio Frequency (RF) spectrum simulation and autonomous scanning system. The project models synthetic RF environments with various emitter behaviors, evaluates autonomous scanning agents over WebSocket streams, and tracks live performance metrics (POD and PFA) through an interactive web visualizer.

---

## 🚀 Features

* **Synthetic RF Physics Engine:** Simulates a 100-band RF spectrum with dynamic signal generation, thermal Gaussian noise, and ground-truth tracking.
* **5 Distinct Emitter Behaviors:**
  * `STATIC` — Constant signal transmission.
  * `PERIODIC` — Regular on/off duty cycle.
  * `INTERMITTENT` — Variable active and idle intervals.
  * `BURST` — Short, unpredictable high-power spikes.
  * `FREQUENCY_AGILE` — Dynamic frequency-hopping across spectrum bands.
* **Virtual Receiver Bridge:** Decouples the environment physics from the scanning brain, enforcing observation and action contracts.
* **Asynchronous FastAPI Engine:** Real-time bi-directional streaming over WebSockets (`ws://127.0.0.1:8000/ws/scan`).
* **Adaptive AI Agent:** Dynamic decision-making engine that adjusts dwell times and target selection based on detection confidence.
* **Live Analytics & Visualization:** Interactive frontend rendering spectrum power levels, hit feeds, and real-time **POD** (Probability of Detection) and **PFA** (Probability of False Alarm) metrics.

---

## 🏗 System Architecture

```text
 ┌──────────────────────┐                     ┌──────────────────────┐
 │   Frontend / Client  │  ─── Action ────►   │   FastAPI Server     │
 │  (HTML UI / AI Agent)│                     │   (WebSocket Engine) │
 │                      │  ◄── Observation ── │                      │
 └──────────────────────┘                     └──────────┬───────────┘
                                                         │
                                                         ▼
                                              ┌──────────────────────┐
                                              │   Receiver Bridge    │
                                              └──────────┬───────────┘
                                                         │
                                                         ▼
                                              ┌──────────────────────┐
                                              │  Synthetic RF World  │
                                              │   (5 Emitter Types)  │
                                              └──────────────────────┘


$env:PYTHONPATH="." ; uvicorn backend.main:app --reload
