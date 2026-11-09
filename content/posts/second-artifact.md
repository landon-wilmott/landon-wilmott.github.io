---
title: "Artifact 3: Single-Supply Light-Following Robot Filter & Virtual Ground Biasing"
date: 2026-10-08
draft: false
author: "Landon Wilmott"
image: "/images/NGspice_project_2.png"
description: "Designing a 9V single-supply AC-coupled transimpedance/inverting amplifier with a +4.5V virtual ground bias for an autonomous light-following robot."
tags:
  - "EC EN 340"
  - "Single-Supply Op-Amp"
  - "Light-Following Robot"
  - "Analog Interfacing"
toc: true
mathjax: true
weight: 3
---

## The Problem
The objective of this **EC EN 340** circuit was to condition the optical sensor signal for an autonomous light-following robot. In a mobile robotics platform, only a single $9\text{V}$ battery (`V1 = 9V`) and $0\text{V}$ ground are available—there is no negative voltage supply rail. Furthermore, static ambient room lighting creates a large DC photodiode offset, while the robot needs to track a modulated $1\text{kHz}$ target light beacon (`I1 = 0.1 mA`). Without proper DC blocking and mid-rail biasing, the negative half-cycle of the AC signal immediately clips against the $0\text{V}$ ground rail.

## My Contribution
I designed a single-supply, AC-coupled inverting amplifier and signal-conditioning stage in NGspice:
1. **Sensor Transducer & Input AC Coupling:** Converted the $0.1\text{mA}$, $1\text{kHz}$ photodiode current (`I1`) into a voltage across sense resistor $R_1 = 1\text{k}\Omega$, and placed a series coupling capacitor $C_1 = 1\ \mu\text{F}$ ahead of input resistor $R_4 = 10\text{M}\Omega$ to block ambient DC room light.
2. **Mid-Rail Virtual Ground Biasing ($+4.5\text{V}$):** Configured op-amp `X1` with its supply rails at $9\text{V}$ (`vp`) and $0\text{V}$ (`GND`), and constructed a matched $100\text{k}\Omega$ voltage divider ($R_7 = 100\text{k}\Omega$, $R_8 = 100\text{k}\Omega$) to bias the non-inverting input (`+`) at exactly **$+4.5\text{V}$** ($\frac{1}{2}V_{CC}$).
3. **High-Impedance Gain & Output DC Restoration:** Set the feedback resistor to $R_5 = 50\text{M}\Omega$ over $R_4 = 10\text{M}\Omega$ for an inverting voltage gain of $|A_v| = \frac{50\text{M}\Omega}{10\text{M}\Omega} = 5\text{ V/V}$, and added an output high-pass AC-coupling stage ($C_2 = 1\ \mu\text{F}$, $R_9 = 1\text{M}\Omega$) to remove the $+4.5\text{V}$ DC bias so the final `out` signal swings cleanly around $0\text{V}$.

## The Result
* Eliminated single-supply rail clipping by centering the internal op-amp signal swing at $+4.5\text{V}$, allowing maximum peak-to-peak headroom between $0\text{V}$ and $9\text{V}$.
* Rejected steady-state ambient room lighting via dual AC-coupling capacitors ($C_1, C_2$) while delivering an amplified, unclipped $1\text{kHz}$ output signal (`out`) ready for downstream robot detection circuitry.

## What This Artifact Demonstrates
* **Single-Supply Analog Engineering:** Designing op-amp circuits that operate reliably from a single $9\text{V}$ battery using a $\frac{1}{2}V_{CC}$ virtual ground reference.
* **Input & Output AC Coupling:** Using series blocking capacitors ($C_1, C_2$) to isolate DC operating points between sensor, amplifier, and load stages.
* **Practical Embedded Sensor Interfacing:** Translating real-world robotics hardware constraints (battery power + ambient room light interference) into a working analog front-end.

---

## Evidence of Revision (Based on Feedback)
* **Circuit Design Revision:** During initial testing, attempting to amplify the photodiode signal without the output RC restoration network ($C_2 = 1\ \mu\text{F}$, $R_9 = 1\text{M}\Omega$) left the output riding on a $+4.5\text{V}$ DC offset. Based on lab feedback, I added the output coupling stage so downstream stages receive a true $0\text{V}$-centered AC waveform, and verified that $R_7/R_8$ ($100\text{k}\Omega$) held the virtual ground stable under load.
* **Portfolio Narrative Revision:** I revised this artifact write-up to explicitly separate **The Problem**, **My Contribution**, **The Result**, and **What This Artifact Demonstrates**, and added quantitative analysis of thegain ($R_5/R_4 = 50\text{M}\Omega/10\text{M}\Omega = 5\text{ V/V}$) and biasing network.

## Design Journey Note
* **What I Can Now Do That I Could Not Do at the Beginning of the Semester:** At the start of the semester, I did not know how an op-amp could amplify an AC signal swinging positive and negative when powered only by a $9\text{V}$ battery and $0\text{V}$ ground. I can now establish a stable mid-rail virtual ground ($+4.5\text{V}$), select biasing resistors that prevent loading, and use AC coupling to interface single-supply analog filters with embedded robotics hardware.

## Circuit Schematic
![Single-Supply Light Following Robot Filter Schematic](/images/NGspice_project_2.png)
