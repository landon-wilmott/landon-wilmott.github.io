# Landon Wilmott — Security Infrastructure & Computer Engineering Portfolio

[![Deploy Hugo to Pages](https://github.com/landon-wilmott/landon-wilmott.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/landon-wilmott/landon-wilmott.github.io/actions/workflows/deploy.yml)

**Live Site:** [https://landon-wilmott.github.io/](https://landon-wilmott.github.io/)

Personal engineering resume and portfolio built with **Hugo**, featuring:
* **Professional Experience & Certifications:** Endpoint Engineering & Security Manager at BYU Life Sciences IT (1,200+ endpoints, 8 student technicians) and **CompTIA Security+, Network+, and A+** certifications.
* **Enterprise Security & K3s Homelab (IaC):** Architecture and sanitized playbooks for a multi-node **Proxmox VE** & **3-node K3s Kubernetes** cluster automated with **Ansible**, **CrowdSec Distributed IPS**, **Longhorn** distributed storage with **Cloudflare R2** disaster recovery, and a custom **C++ Proxmox health telemetry daemon**.
* **BYU EC EN 340 Engineering Portfolio:** Four selected analog circuit design and **NGspice** simulation artifacts (Power Supply Rail Splitter, $120\text{dB}$ Dual Op-Amp Bandpass Filter, Single-Supply Light-Following Robot Filter, and Netlist Verification), plus documented design revisions, semester Design Journey reflections, and alignment with the [Aims of a BYU Education](https://aims.byu.edu/).

---

## CI/CD Pipeline & Automated Verification

Every push and pull request to `main` runs the automated build, linting, and DevSecOps verification pipeline in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) and [`scripts/verify_site.py`](scripts/verify_site.py):

1. **Strict Hugo Compilation (`hugo --minify --panicOnWarning --printPathWarnings`):** Fails the pipeline on any template error, deprecated configuration key, or duplicate path conflict.
2. **TOML & Front Matter Linting:** Validates `hugo.toml` syntax and ensures all Markdown files in `content/` contain valid YAML front matter and non-draft status.
3. **DevSecOps Secret & Private-IP Leak Prevention:** Scans source and built artifacts to block accidental leaks of private RFC1918 LAN IPs (`192.168.x.x`), Tailscale IPs, Argon2id password hashes, or cloud storage secret keys before deployment.
4. **Internal Link & Asset Integrity Check:** Verifies all 1,500+ internal `href` and `src` references across every generated HTML page to guarantee zero broken links or missing schematic images.
5. **Required Section & Page Verification:** Confirms all resume sections, Homelab IaC documentation, and EC EN 340 portfolio artifacts are present in the final build.

---

## Local Development & Verification

```bash
# 1. Start local development server with live reload
hugo server -D

# 2. Run strict production build and CI verification suite locally
hugo --cleanDestinationDir --minify --panicOnWarning --printPathWarnings
rm -rf public/fontawesome-6/svgs && touch public/.nojekyll
python3 scripts/verify_site.py
```

## Disclaimer
The source code for this website is licensed under the MIT License. All website content, including text, resume details, and images, is Copyright © 2026 Landon Wilmott. All Rights Reserved.

