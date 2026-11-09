---
title: "EC EN 340 Engineering Portfolio & Resume Overview"
date: 2026-11-09
draft: false
author: "Landon Wilmott"
description: "Complete EC EN 340 engineering portfolio for Landon Wilmott, featuring a professional introduction and target role, organized Table of Contents, four selected EC EN 340 artifacts, evidence of revision, a semester Design Journey note, and connection to the Aims of a BYU Education."
tags:
  - "EC EN 340"
  - "Portfolio"
  - "Computer Engineering"
  - "Cybersecurity"
  - "BYU Aims"
toc: true
mathjax: true
---

## 1. Professional Introduction & Target Role

**Target Role:** **Security Infrastructure Engineer / DevSecOps & Data Center Systems Engineer**

I am **Landon Wilmott**, a Computer Engineering student at **Brigham Young University (GPA: 3.88)** with a minor in **Cybersecurity** (and an A.S. from Weber State University). Alongside my engineering coursework, I serve as **Endpoint Engineering and Security Manager** at **BYU Life Sciences IT**, where I directly manage and mentor a team of **8 student technicians** and track/remediate security vulnerabilities across **1,200+ endpoints** (after previously reducing vulnerability exposure by 20% across 200+ endpoints as an IT Specialist).

I hold **CompTIA A+, Network+, and Security+** certifications and maintain an enterprise-grade **[Proxmox VE & 3-Node K3s Kubernetes Homelab](/posts/homelab-infrastructure-iac/)** automated with **Ansible**, **CrowdSec Distributed IPS**, **Longhorn + Cloudflare R2** disaster recovery, and a **custom C++ health monitoring daemon**.

---

## 2. Organized Table of Contents

1. [Professional Introduction & Target Role](#1-professional-introduction--target-role)
2. [Organized Table of Contents](#2-organized-table-of-contents)
3. [Selected EC EN 340 Artifacts (4 Artifacts)](#3-selected-ec-en-340-artifacts)
   - [Artifact 1: Power Supply Rail Splitter & 3-Stage Ripple Decoupling Network](#artifact-1-power-supply-rail-splitter--3-stage-ripple-decoupling-network)
   - [Artifact 2: Dual Op-Amp Cascaded Bandpass Noise Filter (1.25 kHz – 3.67 kHz)](#artifact-2-dual-op-amp-cascaded-bandpass-noise-filter-125-khz--367-khz)
   - [Artifact 3: Single-Supply Light-Following Robot Filter & Virtual Ground Biasing](#artifact-3-single-supply-light-following-robot-filter--virtual-ground-biasing)
   - [Artifact 4: NGspice Netlist Verification, Capacitor Grounding Audit & Multi-Pole Revision](#artifact-4-ngspice-netlist-verification-capacitor-grounding-audit--multi-pole-revision)
4. [Evidence of Revision Based on Feedback](#4-evidence-of-revision-based-on-feedback)
5. [Design Journey Note: Start of Semester vs. Now](#5-design-journey-note-start-of-semester-vs-now)
6. [Connection to BYU Aims (aims.byu.edu)](#6-connection-to-byu-aims)
7. [Security & K3s Homelab Architecture (Proxmox, Ansible & CrowdSec)](/posts/homelab-infrastructure-iac/)

---

## 3. Selected EC EN 340 Artifacts

Below are four selected engineering artifacts from **EC EN 340 (Electronic Circuit Design 1)**, each structured to highlight **The Problem**, **My Contribution**, **The Result**, and **What This Artifact Demonstrates**.

---

### Artifact 1: Power Supply Rail Splitter & 3-Stage Ripple Decoupling Network

* **Standalone Write-Up:** [Open Artifact 1 Full Page →](/posts/artifact-1-rail-splitter/)
* **The Problem:** Our optical receiver circuit was powered by a single $3.3\text{V}$ DC supply (`V1`) contaminated with a $30\text{mV}$ AC ripple at $1481\text{Hz}$—directly inside our $1250\text{Hz}\text{–}3666\text{Hz}$ passband—while the operational amplifiers required clean, symmetric $+1.65\text{V}$ (`vp`) and $-1.65\text{V}$ (`vn`) dual rails.
* **My Contribution:** I designed a 3-stage cascaded RC low-pass decoupling filter ($R_{24}, R_{11}, R_4 = 10\ \Omega$ and $C_{22}, C_9 = 159\ \mu\text{F}$, with stage corner frequency $f_c \approx 100\text{Hz}$) feeding a matched $100\text{k}\Omega$ voltage divider ($R_2, R_3$). To establish symmetric bipolar rails, I placed the system reference ground (`0V`) directly between $R_2$ and $R_3$ and added parallel multi-decade bypass capacitors ($1\text{mF}$ bulk + $1\ \mu\text{F}$ high-frequency) on both rails.
* **The Result:** Produced stable **$v_p = +1.65\text{V}$** and **$v_n = -1.65\text{V}$** supply rails while heavily attenuating the $1481\text{Hz}$ power-line ripple before it could modulate the high-gain amplifier stages.
* **What This Artifact Demonstrates:** Power integrity engineering, virtual ground synthesis, multi-decade capacitor bypassing, and constraint-driven SPICE modeling.

![Artifact 1 Schematic: Rail Splitter and Ripple Filter](/images/artifact1_rail_splitter.png)

---

### Artifact 2: Dual Op-Amp Cascaded Bandpass Noise Filter (1.25 kHz – 3.67 kHz)

* **Standalone Write-Up:** [Open Artifact 2 Full Page →](/posts/spice-simulation-lab/)
* **The Problem:** Using a maximum of two operational amplifiers, isolate an ultra-weak $1\text{pA}$ ($2000\text{Hz}$) photodiode signal (`Is`) from a $1\text{mA}$ DC offset (`In1`), two $400\text{nA}$ photodiode noise sources at $100\text{Hz}$ (`In2`) and $20\text{kHz}$ (`In3`), and a $1481\text{Hz}$ power supply ripple so that only the **$1250\text{Hz}\text{–}3666\text{Hz}$** target band passes through.
* **My Contribution:** I designed a hybrid passive-active bandpass chain with lower corner frequency $f_L = 1000\text{Hz}$ and upper corner frequency $f_H = 10\text{kHz}$. This combined a 3-stage passive RC high-pass input filter ($C = 15\text{nF}, R = 10.6\text{k}\Omega$), two cascaded inverting active bandpass op-amps ($R_{in} = 1\text{k}\Omega, C_{in} = 159\text{nF}, R_f = 1\text{M}\Omega, C_f = 15.9\text{pF}$ providing $60\text{dB}$ gain per stage / $120\text{dB}$ total), and a 3-stage passive RC low-pass output filter ($R = 1.6\text{k}\Omega, C = 10\text{nF}$).
* **The Result:** Cleanly extracted and amplified the $1250\text{Hz}\text{–}3666\text{Hz}$ signal window with $120\text{dB}$ mid-band gain while sharply attenuating DC, $100\text{Hz}$, and $20\text{kHz}$ interference without saturating the op-amp outputs.
* **What This Artifact Demonstrates:** Multi-pole active/passive filter synthesis, Bode corner-frequency design, high-gain amplifier staging, and signal-to-noise optimization.

![Artifact 2 Schematic: Cascaded Bandpass Filter Chain](/images/artifact2_bandpass_chain.png)

---

### Artifact 3: Single-Supply Light-Following Robot Filter & Virtual Ground Biasing

* **Standalone Write-Up:** [Open Artifact 3 Full Page →](/posts/second-artifact/)
* **The Problem:** Process a $1\text{kHz}$ pulsed optical signal (`I1 = 0.1 mA`) for a light-following robot operating from a single $9\text{V}$ battery (`V1 = 9V`) and $0\text{V}$ ground, while rejecting steady-state ambient room lighting that would otherwise saturate or clip the signal against the $0\text{V}$ rail.
* **My Contribution:** I designed an AC-coupled inverting op-amp stage ($R_4 = 10\text{M}\Omega, R_5 = 50\text{M}\Omega$, voltage gain $|A_v| = 5\text{ V/V}$) where the op-amp rails sit at $9\text{V}$ and $0\text{V}$ while a matched $100\text{k}\Omega$ divider ($R_7, R_8$) biases the non-inverting input (`+`) to a $+4.5\text{V}$ virtual ground. I paired this with input ($C_1 = 1\ \mu\text{F}$) and output ($C_2 = 1\ \mu\text{F}, R_9 = 1\text{M}\Omega$) AC-coupling networks.
* **The Result:** Enabled full symmetric AC signal swing centered at $+4.5\text{V}$ inside the op-amp without rail clipping, and delivered a clean, $0\text{V}$-referenced output signal (`out`) completely free of ambient DC room-light interference.
* **What This Artifact Demonstrates:** Single-supply op-amp biasing, DC blocking / AC restoration, high-impedance optical sensor conditioning, and practical robotics hardware design.

![Artifact 3 Schematic: Single-Supply Light Following Robot Filter](/images/NGspice_project_2.png)

---

### Artifact 4: NGspice Netlist Verification, Capacitor Grounding Audit & Multi-Pole Revision

* **Standalone Write-Up:** [Open Artifact 4 Full Page →](/posts/artifact-4-netlist-verification/)
* **The Problem:** Early iterations of the optical receiver netlist and schematic risked shunting AC signals or locking op-amp rails due to mis-grounded coupling capacitors (`C6`/`C7` and `C23`/`C24`) and strict requirements to preserve starter components (`V1`, `I1`, and `R1`) without modification.
* **My Contribution:** I performed a comprehensive node-by-node audit between the schematic and NGspice netlist—confirming that all series coupling capacitors were routed inline without grounding them, verifying that shunt bypass/low-pass capacitors terminated properly at ground (`0`), and upgrading single-pole sections into 3-stage RC cascades based on simulation diagnostics.
* **The Result:** Eliminated schematic-to-netlist topology discrepancies, achieved steep 4th-order roll-off on both sides of the passband, and produced a verified netlist that passed all Milestone 1 simulation benchmarks.
* **What This Artifact Demonstrates:** Systematic hardware/simulation troubleshooting, SPICE netlist fluency, strict interface compliance, and feedback-driven iterative engineering.

![Artifact 4 Schematic: Complete Verified System Topology](/images/NGspice_M1_screenshot.png)

---

## 4. Evidence of Revision Based on Feedback

This portfolio and the underlying circuit designs incorporate direct revisions from instructor, TA, and peer feedback:

1. **Portfolio Structure, Target Role & Navigation Revision:**
   * *Before:* My initial Hugo site used a minimal blog list with only two visible posts, lacked an explicit target role banner and table of contents, and used inconsistent section headings (such as *"Context"* and *"Procedure"*).
   * *After (Revised):* I adapted the portfolio into a structured engineering resume & showcase featuring an explicit **Target Role (Security Infrastructure & Data Center Hardware Engineer)**, a sticky navigation bar and **Organized Table of Contents**, and four complete EC EN 340 artifacts standardized around **The Problem**, **My Contribution**, **The Result**, and **What This Artifact Demonstrates**.
2. **Restoring & Expanding Overwritten Netlist Artifact (`commit 7b2ba54` → Artifact 1 & Artifact 4):**
   * *Before:* My earlier SPICE netlist write-up (*"EC EN 340 Artifact 2: SPICE Circuit Simulation"*, explaining the $v_p = +1.65\text{V} / v_n = -1.65\text{V}$ ground placement between `R2` and `R3` and proper routing of `C6` and `C7`) had been overwritten when `second-artifact.md` was replaced with the Light-Following Robot Filter.
   * *After (Revised):* I recovered that technical analysis from version control and expanded it into **Artifact 1** (Rail Splitter & Ripple Decoupling) and **Artifact 4** (Netlist Verification & Capacitor Routing Audit), complete with cropped and full-system schematics.
3. **Technical Circuit Revisions in NGspice:**
   * Added the 3-stage $10\ \Omega / 159\ \mu\text{F}$ RC ripple filter ahead of the `R2`/`R3` rail splitter to suppress the $1481\text{Hz}$ supply ripple.
   * Expanded the input high-pass and output low-pass filters into 3-stage passive RC cascades ($15\text{nF}/10.6\text{k}\Omega$ and $1.6\text{k}\Omega/10\text{nF}$) to sharpen out-of-band noise rejection at $100\text{Hz}$ and $20\text{kHz}$.
   * Added the output AC-coupling restoration network ($C_2 = 1\ \mu\text{F}, R_9 = 1\text{M}\Omega$) on the $9\text{V}$ single-supply robot filter so the output swings around $0\text{V}$ instead of riding on $+4.5\text{V}$ DC.

---

## 5. Design Journey Note: Start of Semester vs. Now

> **What I can now do that I could not do at the beginning of the semester:**

At the beginning of the semester in **EC EN 340**, I could solve basic textbook resistor networks and ideal op-amp equations on paper, but I could not design a multi-stage analog front-end that survived real-world physical imperfections like single-supply rail limits, power-line ripple, and overwhelming ambient optical interference.

**Specifically, I can now:**
1. **Design Multi-Stage Active & Passive Bandpass Filters to Exact Specifications:** I can calculate RC pole and zero frequencies ($f_c = \frac{1}{2\pi RC}$), cascade multiple passive and active stages, and distribute $120\text{dB}$ of gain across dual op-amps to recover a $1\text{pA}$ signal inside a strict $1250\text{Hz}\text{–}3666\text{Hz}$ window while rejecting interferences $10^6\times$ larger.
2. **Engineer Single-Supply Virtual Grounds & Power Integrity Networks:** Rather than relying on ideal $\pm V_{CC}$ bench supplies, I can bias single-supply op-amps ($9\text{V}$ or $3.3\text{V}$) to a stable mid-rail virtual ground ($+4.5\text{V}$ or $\pm 1.65\text{V}$), decouple noisy power rails with multi-stage RC filters and dual-decade bypass capacitors, and AC-couple inputs and outputs to prevent rail clipping.
3. **Debug & Verify Complex Topologies in NGspice Before Building Hardware:** I can translate schematic constraints into SPICE netlists, diagnose subtle node-grounding bugs, and use simulation data to iteratively refine a circuit before committing to a physical breadboard or PCB.

---

## 6. Connection to BYU Aims

My engineering work in **EC EN 340** and my broader preparation as a **Computer Engineering & Cybersecurity** student directly connect to the **[Aims of a BYU Education (https://aims.byu.edu/)](https://aims.byu.edu/)**:

* **[Intellectually Enlarging](https://aims.byu.edu/):** BYU emphasizes uniting rigorous academic theory with practical competence. In EC EN 340, bridging mathematical transfer functions and Bode plots with real-world non-idealities—such as filtering out a $1481\text{Hz}$ power-supply ripple or preventing single-supply op-amp saturation—taught me how to think across levels of abstraction. As a future **Security Infrastructure Engineer**, this ability to connect physical-layer hardware realities (power integrity, signal noise, hardware diagnostics) with higher-level network virtualization and security architecture is essential.
* **[Lifelong Learning and Service](https://aims.byu.edu/) & [Character Building](https://aims.byu.edu/):** Engineering is ultimately a stewardship of trust. Whether I am mentoring and supervising student IT technicians on campus, methodically auditing an NGspice netlist so a circuit operates safely and reliably, or securing enterprise server infrastructure using principles from my CompTIA Security+ and Network+ training, I strive to practice disciplined verification, continuous learning, and dependable service to others.
