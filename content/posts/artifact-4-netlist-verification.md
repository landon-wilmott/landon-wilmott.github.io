---
title: "Artifact 4: NGspice Netlist Verification, Capacitor Grounding Audit & Multi-Pole Revision"
date: 2026-10-08
draft: false
author: "Landon Wilmott"
image: "/images/NGspice_M1_screenshot.png"
description: "Systematic debugging and iterative netlist verification in NGspice—resolving coupling capacitor grounding errors and validating multi-stage filter topology."
tags:
  - "EC EN 340"
  - "SPICE Netlist"
  - "Verification & Debugging"
  - "Design Revision"
toc: true
mathjax: true
weight: 4
---

## The Problem
When translating complex multi-stage schematics into text-based **NGspice netlists** in EC EN 340, small node-numbering or grounding errors can silently kill an entire signal chain without throwing a syntax error. Specifically, in our optical receiver simulation, we were required to strictly preserve the starter netlist's `V1`, `I1`, and `R1` components and interconnections while integrating a rail splitter, two active bandpass op-amps, and six passive RC filter stages. A common failure mode in early drafts was inadvertently grounding series coupling capacitors (`C6`/`C7` and `C23`/`C24`) or mis-referencing the op-amp power and virtual ground nodes, which shunted the target AC signal to ground or locked the op-amp rails.

## My Contribution
I led a systematic netlist verification and topology debugging audit across the schematic and SPICE code:
1. **Node-by-Node Netlist & Capacitor Routing Audit:** I traced every netlist node between the schematic and SPICE code, verifying that series coupling and high-pass capacitors (`C6`/`C7`, `C23`–`C27`) were routed strictly inline between stages rather than tied to node `0` (ground), and confirming that shunt low-pass capacitors (`C28`–`C30`) and rail bypass capacitors (`C1`–`C4`) terminated properly at node `0`.
2. **Starter-Code Constraint Compliance (`V1`, `I1`, `R1`):** I verified that the original `V1` power source, photodiode current sources (`In1`–`In3`, `Is`), diode `D1`, and $2500\ \Omega$ sense resistor `R1` maintained their exact required node assignments while interfacing cleanly at node `in`.
3. **Iterative Bode & Transient Verification:** I used NGspice simulation outputs to iteratively tune component values across the 3-stage input HPF ($15\text{nF} / 10.6\text{k}\Omega$) and 3-stage output LPF ($1.6\text{k}\Omega / 10\text{nF}$), confirming both DC operating point stability ($\pm 1.65\text{V}$ rails) and AC passband fidelity ($1250\text{Hz}\text{–}3666\text{Hz}$).

## The Result
* Eliminated signal-shunting schematic/netlist bugs by ensuring all coupling capacitors (`C6`/`C7`, `C23`/`C24`) passed AC signals in series while shunt bypass capacitors routed high-frequency noise to ground.
* Delivered a verified, reproducible NGspice netlist and schematic that met 100% of the EC EN 340 Milestone 1 specifications and passed automated/lab verification checks.

## What This Artifact Demonstrates
* **Systematic Debugging & Root-Cause Analysis:** Diagnosing subtle circuit topology bugs (such as series vs. shunt capacitor grounding and virtual-ground reference errors) by correlating SPICE node voltages with circuit theory.
* **Verification Rigor & Constraint Adherence:** Modifying complex systems within strict interface rules (preserving legacy/starter components `V1`, `I1`, `R1`)—a critical skill in both hardware engineering and enterprise security infrastructure.
* **Feedback-Driven Engineering Iteration:** Using simulation diagnostics and instructor/TA feedback to systematically refine a design from an initial draft to a verified production netlist.

---

## Evidence of Revision (Based on Feedback)
* **Recovering & Expanding Earlier Portfolio Work:** In an earlier version of my repository (commit `7b2ba54`), my SPICE netlist analysis (*"EC EN 340 Artifact 2: SPICE Circuit Simulation"*) was overwritten when I added the Light-Following Robot Filter post. Based on portfolio review feedback requiring at least four distinct EC EN 340 artifacts and clear evidence of revision, I restored my netlist debugging and capacitor-routing work (`C6`/`C7` and `R2`/`R3` ground placement) and expanded it into this comprehensive verification artifact.

## Design Journey Note
* **What I Can Now Do That I Could Not Do at the Beginning of the Semester:** At the start of the semester, a flat SPICE netlist looked like an inscrutable list of node numbers, and when a simulation produced a flat $0\text{V}$ line, I had to guess what was wrong. Today, I can audit netlists systematically—checking DC bias points first, verifying series vs. shunt reactive components, and validating AC frequency responses stage-by-stage.

## Verified Full-System Schematic
![Verified NGspice Full System Schematic](/images/NGspice_M1_screenshot.png)
