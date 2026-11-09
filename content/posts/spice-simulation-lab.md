---
title: "Artifact 2: Dual Op-Amp Cascaded Bandpass Noise Filter (1.25 kHz – 3.67 kHz)"
date: 2026-10-08
draft: false
author: "Landon Wilmott"
image: "/images/artifact2_bandpass_chain.png"
description: "Designing a 120 dB hybrid active-passive bandpass filter chain using two op-amps to isolate a 1 pA, 2 kHz photodiode signal from heavy out-of-band interference."
tags:
  - "EC EN 340"
  - "Active Filters"
  - "Op-Amp Design"
  - "Signal Processing"
toc: true
mathjax: true
weight: 2
---

## The Problem
This **EC EN 340** design challenge required isolating an ultra-weak $1\text{pA}$ ($2000\text{Hz}$) optical signal (`Is`) from severe multi-source interference using **at most two operational amplifiers**. Specifically, the photodiode sensing node (`in`) was simultaneously driven by:
* A $1\text{mA}$ DC ambient light offset (`In1`),
* A $400\text{nA}$ low-frequency interference source at $100\text{Hz}$ (`In2`),
* A $400\text{nA}$ high-frequency interference source at $20\text{kHz}$ (`In3`), and
* A $1481\text{Hz}$ power-supply ripple source (`V1`).

Because the interfering currents were $400{,}000\times$ to $10^9\times$ larger than the $1\text{pA}$ target current, the circuit had to provide massive in-band amplification across the target **$1250\text{Hz}$ to $3666\text{Hz}$** frequency window while aggressively rejecting all out-of-band frequencies.

## My Contribution
I architected a multi-stage hybrid passive-and-active bandpass filter chain centered on the **$1000\text{Hz}$ to $10\text{kHz}$** corner window:
1. **3-Stage Input Passive RC High-Pass Filter:** Configured three cascaded high-pass poles ($C_{27}, C_{26}, C_{25} = 15\text{nF}$ and $R_{29}, R_{28}, R_{27} = 10.6\text{k}\Omega$) with a corner frequency of $f_L = \frac{1}{2\pi (10.6\text{k}\Omega)(15\text{nF})} \approx 1001\text{Hz}$ to completely block the $1\text{mA}$ DC current and sharply attenuate the $100\text{Hz}$ photodiode hum before amplification.
2. **Two Cascaded High-Gain Inverting Active Bandpass Op-Amp Stages (`X1`, `X2`):** Designed each op-amp stage with an input series network ($R_{25}, R_{26} = 1\text{k}\Omega$ and $C_{23}, C_{24} = 159\text{nF}$, $f_L \approx 1001\text{Hz}$) and a parallel RC feedback loop ($R_{30}, R_{31} = 1\text{M}\Omega$ and $C_{31}, C_{32} = 15.9\text{pF}$, $f_H \approx 10.01\text{kHz}$). Each stage delivers an mid-band gain magnitude of $|A_v| = \frac{1\text{M}\Omega}{1\text{k}\Omega} = 1000\text{ V/V}$ ($60\text{dB}$), yielding **$120\text{dB}$ ($10^6\text{ V/V}$) total passband gain**.
3. **3-Stage Output Passive RC Low-Pass Filter:** Added three cascaded low-pass poles ($R_{32}, R_{33}, R_{34} = 1.6\text{k}\Omega$ and $C_{28}, C_{29}, C_{30} = 10\text{nF}$) at $f_H = \frac{1}{2\pi (1.6\text{k}\Omega)(10\text{nF})} \approx 9947\text{Hz}$ to strip out the $20\text{kHz}$ photodiode noise at the output (`out`).

## The Result
* Successfully amplified the $1\text{pA}$ ($2000\text{Hz}$) signal across the required **$1250\text{Hz}\text{–}3666\text{Hz}$** passband into a clean, measurable output voltage waveform.
* Achieved steep 4th-order high-pass and 4th-order low-pass roll-off per active/passive cascade, suppressing the $0\text{Hz}$ DC offset, $100\text{Hz}$ hum, and $20\text{kHz}$ interference without saturating either op-amp against the $\pm 1.65\text{V}$ rails.

## What This Artifact Demonstrates
* **Multi-Pole Filter Synthesis & Bode Analysis:** Selecting exact standard resistor and capacitor values to place lower ($1\text{kHz}$) and upper ($10\text{kHz}$) poles symmetrically around a target passband.
* **High-Gain Cascaded Amplifier Staging:** Distributing $120\text{dB}$ of gain across two inverting bandpass op-amps while stripping DC and out-of-band energy prior to the first gain stage to avoid rail saturation.
* **SPICE AC Sweep & Signal-to-Noise Verification:** Translating physical photodiode interference constraints into an end-to-end verified NGspice topology.

---

## Evidence of Revision (Based on Feedback)
* **Technical Filter Revision:** My earliest design relied primarily on the op-amps' single-pole feedback networks, which did not provide a steep enough roll-off to suppress the $400\text{nA}$ noise sources at $100\text{Hz}$ and $20\text{kHz}$ ($54\text{dB}$ stronger than the $1\text{pA}$ signal). Based on simulation feedback, I added the 3-stage passive RC high-pass cascade at the input and the 3-stage passive RC low-pass cascade at the output, dramatically sharpening the passband skirts.
* **Portfolio Communication Revision:** Based on portfolio feedback, I expanded my original two-sentence summary into a full engineering breakdown detailing the exact component values ($15\text{nF}/10.6\text{k}\Omega$, $1\text{M}\Omega/15.9\text{pF}$, $1.6\text{k}\Omega/10\text{nF}$), gain calculations ($60\text{dB}$ per stage), and quantitative results.

## Design Journey Note
* **What I Can Now Do That I Could Not Do at the Beginning of the Semester:** At the start of the semester, I could not design a multi-stage filter to recover a picowatt signal buried in noise, nor did I understand why high-pass filtering *must* precede high-gain amplification. I can now calculate corner frequencies across multiple cascaded stages, prevent DC offset saturation, and transition seamlessly from NGspice simulation to physical breadboard implementation.

## Circuit Schematics
### Cascaded Bandpass Filter Chain (`in` to `out`)
![Cascaded Bandpass Filter Chain](/images/artifact2_bandpass_chain.png)

### Complete Milestone 1 System Schematic
![Complete NGspice Milestone 1 Schematic](/images/NGspice_M1_screenshot.png)
