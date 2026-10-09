---
title: "Light Following Robot Filter"
date: 2026-10-08
draft: false
---

## Context
The objective of this circuit was to process the signal for a light-following robot. Specifically, the system needed a reliable way to filter out ambient room lighting interference so the robot could accurately track its target light source.

## My Contribution
I designed a circuit that allows the rails of the op-amp to rest at 9V and 0V while biasing the positive input to 4.5V. Establishing this virtual ground made it possible to correctly filter the signal using a single voltage source.

## What This Demonstrates
* **Circuit Analysis:** Applying voltage division and operational amplifier analysis to physical designs.
* **Troubleshooting:** Identifying and resolving design constraints imposed by single voltage source limitations.

---

## Design Journey Note
* **What I learned:** Biasing an op-amp with a single supply requires careful resistor selection to ensure the virtual ground remains stable under load, otherwise the signal clips against the rails.
* **Next steps:** This biasing and filtering design pattern will serve as a foundational template for future embedded projects involving optical sensors and signal processing.

## Photo
![NGspice circuit image](/images/NGspice_project_2.png)
