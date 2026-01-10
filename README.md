<div align="center">

# 🧠 CortexCare
### A Sanctuary of Calm in the Age of AI

**An ethical, empathetic, and responsible emotional support platform.**

[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=activity)](https://github.com/shivam-prajapat/CortexCare)
[![Ethical AI](https://img.shields.io/badge/AI-Ethical-blue?style=for-the-badge&logo=openai)](https://github.com/shivam-prajapat/CortexCare)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://github.com/shivam-prajapat/CortexCare)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

<br />

<p align="center">
  <a href="#-philosophy"><strong>Philosophy</strong></a> •
  <a href="#-features"><strong>Features</strong></a> •
  <a href="#-architecture"><strong>Architecture</strong></a> •
  <a href="#-tech-stack"><strong>Tech Stack</strong></a> •
  <a href="#-getting-started"><strong>Getting Started</strong></a>
</p>

</div>

<br />

---

### 🌱 Philosophy

**CortexCare** is not just a chatbot; it is a safe harbor. Built on the belief that AI should support rather than replace human connection, it provides a judgment-free zone for users experiencing emotional distress.

> *"To listen without judging, to support without overtaking, and to guide toward help when it matters most."*

<div align="center" style="background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; border: 1px solid #ffeeba;">
  <b>⚠️ Important Disclaimer:</b> CortexCare does <b>not</b> diagnose medical conditions or replace professional therapy. It is a supportive first step.
</div>

<br />

---

### ✨ Features

| Feature | Description |
| :--- | :--- |
| **🧠 Medical-Grade AI** | Powered by **MedGemma (4B)** to ensure responses are grounded, empathetic, and context-aware. |
| **🚨 Crisis Intervention** | Intelligently detects intent related to self-harm or crisis, switching immediately to a safety-first protocol. |
| **🛡️ Privacy First** | No user data is stored. Conversations are ephemeral to ensure complete confidentiality. |
| **❤️ Empathetic Tone** | Trained to use grounding techniques and calming language rather than robotic answers. |

<br />

---

### 🏗 Architecture

CortexCare bridges the gap between simple chat interfaces and complex medical LLMs using a secure, logic-driven backend.

```mermaid
graph TD
    User([👤 User]) -->|Input| UI[🖥️ Streamlit Frontend]
    UI -->|API Request| API[⚡ FastAPI Backend]
    
    subgraph "Logic Core"
    API -->|Prompt Engineering| LLM[🧠 Ollama / MedGemma]
    LLM -->|Empathetic Response| API
    end
    
    subgraph "Safety Layer"
    API -->|Check Intent| Guard[🛡️ Crisis Detector]
    Guard -- Safe --> LLM
    Guard -- Danger --> Protocol[🚨 Safety Protocol]
    end
    
    Protocol --> UI
    API --> UI

