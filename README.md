# 🚀 Privacy-First Classroom Quiz Pipeline

A real-time, self-hosted classroom formative assessment system connecting physical **BBC micro:bit** student nodes to a Dockerized **Home Assistant** dashboard and **Google Sheets** — engineered with student data privacy at the core and zero reliance on third-party quiz platforms.

Designed for **Informatics / Computer Science** classes as well as **any K–12 school subject** (math, languages, history, sciences) where teachers need instant, distraction-free feedback on student understanding.

---

## 🏗️ System Architecture

```text
[Student micro:bit Nodes 1–5] 
       │  (Radio Group - Buttons A / B)
       ▼
[Receiver micro:bit Gateway] 
       │  (USB Serial - 115200 baud)
       ▼
[Python Edge Bridge] ──┬──► [Home Assistant (Docker / Tailscale)] ──► Live Teacher Dashboard
                       │
                       └──► [Google Apps Script Webhook (doPost)] ──► Google Sheets ("QandA")
                                                                            │
[Home Assistant REST Sensor] ◄── (GET Active Question via doGet) ───────────┘
