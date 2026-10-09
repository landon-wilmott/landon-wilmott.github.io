---
title: "OpAmp Noise Filter"
date: 2026-10-08
draft: false
---

## Context
This project involved using a maximum of two op-amps to filter out noise coming from different sources, including two photodiodes at 100Hz and 20kHz, and a 1481Hz power source. This design ensures that only the target frequencies of 1250Hz to 3666Hz make it through the circuit.

## My Contribution
I designed a circuit using two op-amps with multiple filters, setting the lower corner frequency to 1000Hz and the upper corner frequency to 10kHz. These corner frequencies were specifically chosen to create a bandpass window that allows the 1250Hz–3666Hz range to pass while severely attenuating all other environmental noise.

## What This Demonstrates
* **Circuit Analysis:** Translating physical constraints into SPICE syntax.
* **Troubleshooting:** Identifying and resolving corner frequency constraints.

---

## Design Journey Note
* **What I learned:** I learned how to calculate corner frequencies to ensure there is proper gain within the desired frequency range while mitigating all other frequencies.
* **Next steps:** Now that the NGspice simulation is complete the next step is to build the real circuit with the same specifications.

## Photos
![NGspice circuit image](/images/NGspice_M1_screenshot.png)
