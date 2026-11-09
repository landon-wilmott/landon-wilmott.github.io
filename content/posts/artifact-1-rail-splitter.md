---
title: "Artifact 1: Power Supply Rail Splitter & 3-Stage Ripple Decoupling Network"
date: 2026-10-08
draft: false
author: "Landon Wilmott"
image: "/images/artifact1_rail_splitter.png"
description: "Designing a 3-stage RC low-pass power decoupling network and symmetric ±1.65V virtual-ground rail splitter from a noisy 3.3V supply in NGspice."
tags:
  - "EC EN 340"
  - "NGspice"
  - "Power Integrity"
  - "Virtual Ground"
toc: true
mathjax: true
weight: 1
---

## The Problem
In precision analog optical receivers, noise on the DC power rails couples directly into high-gain operational amplifier stages and corrupts microvolt-level sensor signals. For this **EC EN 340** milestone, our circuit was powered by a single $3.3\text{V}$ DC voltage source (`V1`) contaminated with a $30\text{mV}$ AC ripple at $1481\text{Hz}$—sitting right inside our target $1250\text{Hz}\text{–}3666\text{Hz}$ signal passband. Furthermore, the dual-rail operational amplifiers required clean, symmetric $+1.65\text{V}$ (`vp`) and $-1.65\text{V}$ (`vn`) supply rails while strictly preserving the starter netlist's `V1`, `I1`, and `R1` components.

## My Contribution
I designed and implemented a two-part power conditioning and rail-splitting architecture in NGspice:
1. **3-Stage Cascaded RC Low-Pass Ripple Filter:** Ahead of the voltage divider, I placed three low-impedance series resistors ($R_{24} = 10\ \Omega$, $R_{11} = 10\ \Omega$, $R_4 = 10\ \Omega$) paired with large shunt decoupling capacitors ($C_{22} = 159\ \mu\text{F}$ and $C_9 = 159\ \mu\text{F}$). With an individual stage corner frequency of $f_c = \frac{1}{2\pi (10\ \Omega)(159\ \mu\text{F})} \approx 100\text{Hz}$, this cascade heavily attenuates the $1481\text{Hz}$ power-supply ripple before it reaches the rail splitter.
2. **Symmetric Virtual-Ground Rail Splitter & Multi-Decade Bypassing:** I constructed a balanced $100\text{k}\Omega$ voltage divider ($R_2 = 100\text{k}\Omega$, $R_3 = 100\text{k}\Omega$) and strategically placed the system reference ground (`0V`) directly between $R_2$ and $R_3$. I stabilized both the positive (`vp`) and negative (`vn`) rails using parallel bulk ($C_1, C_2 = 1\text{mF}$) and high-frequency ($C_3, C_4 = 1\ \mu\text{F}$) bypass capacitors to ground.

## The Result
* Generated rock-solid, symmetric **$v_p = +1.65\text{V}$** and **$v_n = -1.65\text{V}$** supply rails from the single $3.3\text{V}$ source with minimal static current draw.
* Eliminated the $30\text{mV}$, $1481\text{Hz}$ power-line ripple from the op-amp power pins, preventing in-band power supply modulation from masking the $1\text{pA}$ photodiode signal.

## What This Artifact Demonstrates
* **Power Integrity & Decoupling Design:** Combining low-pass RC filtering with multi-decade capacitor bypassing ($1\text{mF}$ and $1\ \mu\text{F}$) to suppress in-band supply noise.
* **Reference Node & Virtual Ground Synthesis:** Establishing dual bipolar supply rails ($\pm 1.65\text{V}$) from a unipolar source by strategically defining the circuit ground node.
* **Constraint-Driven SPICE Modeling:** Extending a constrained starter netlist (`V1`, `I1`, `R1`) without introducing floating nodes or DC path errors.

---

## Evidence of Revision (Based on Feedback)
* **Initial Draft vs. Revised Design:** In my initial schematic layout, the $3.3\text{V}$ supply divider lacked multi-stage series RC decoupling ahead of `R2`/`R3`, allowing the $1481\text{Hz}$ ripple on `V1` to modulate `vp` and `vn`. Based on simulation diagnostics and lab feedback, I added the 3-stage $10\ \Omega / 159\ \mu\text{F}$ low-pass filter cascade and paired the $1\text{mF}$ bulk capacitors with $1\ \mu\text{F}$ bypass capacitors.
* **Portfolio Documentation Revision:** Earlier versions of my portfolio merged this rail-splitter work into a short paragraph inside Artifact 2 without explaining *why* the $1481\text{Hz}$ ripple was so dangerous (it lies directly inside the $1250\text{Hz}\text{–}3666\text{Hz}$ passband). I revised this into a standalone artifact with explicit *Problem*, *Contribution*, *Result*, and *Demonstrated Competency* sections.

## Design Journey Note
* **Start of Semester vs. Now:** At the beginning of the semester, I treated voltage sources in circuit diagrams as ideal, noiseless batteries. Through this project, I learned how real-world power supplies inject in-band ripple into sensitive analog front-ends—and I can now design multi-stage RC decoupling networks and split-rail virtual grounds from scratch.

## Circuit Schematic
![Power Supply Rail Splitter and 3-Stage RC Decoupling Network](/images/artifact1_rail_splitter.png)
