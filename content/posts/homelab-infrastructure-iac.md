---
title: "Security & Cloud-Native Homelab Architecture (Proxmox, K3s, CrowdSec & Ansible IaC)"
date: 2026-11-09
draft: false
author: "Landon Wilmott"
image: "/images/homelab_architecture.svg"
description: "Employer-facing technical deep-dive into my production-style Security Infrastructure & Kubernetes Homelab: 3-node K3s cluster, Proxmox LXC consolidation, Ansible zero-trust hardening, distributed CrowdSec IPS, Longhorn storage with Cloudflare R2 backups, and C++ health telemetry."
tags:
  - "Security Infrastructure"
  - "Ansible IaC"
  - "Kubernetes (K3s)"
  - "Proxmox"
  - "CrowdSec IPS"
  - "Longhorn"
toc: true
weight: 5
---

## Architecture Overview

To apply enterprise **Security Infrastructure Engineering**, **DevSecOps**, and **Site Reliability Engineering (SRE)** principles hands-on, I architected and maintain a multi-node virtualized and containerized homelab environment managed through **Infrastructure as Code (IaC)**.

![Homelab Architecture Diagram](/images/homelab_architecture.svg)

### Core Infrastructure Metrics & Highlights
* **>50% Compute & Memory Footprint Reduction:** Migrated heavy full-OS virtual machines on **Proxmox VE** to lightweight, kernel-sharing **LXC containers** and a **3-node K3s Kubernetes cluster** (`i5-server`, `lenovo-server`, `pi-server`).
* **Distributed Intrusion Prevention (CrowdSec LAPI + Bouncers):** Automated the deployment of a centralized **CrowdSec Local API (LAPI) "Brain"** node (`crowdsec_lxc`) and distributed `crowdsec-firewall-bouncer-iptables` agents across Linux hosts via Ansible delegation.
* **Defense-in-Depth Host Hardening:** Engineered idempotent **Ansible** playbooks enforcing default-deny **UFW** firewall rules from inventory port definitions, **SSH `ed25519` key-only lockdown**, **Fail2Ban** jail policies, and **Tailscale** zero-trust management access.
* **High-Availability Block Storage & Offsite Cloud DR:** Deployed **Longhorn** distributed block storage across the K3s cluster with automated `RecurringJob` daily snapshots at 02:00 AM backed up off-site to **Cloudflare R2** S3-compatible storage.
* **Custom C++ Proxmox Telemetry Daemon:** Built a custom **C++** monitoring service that queries the Proxmox REST API for node CPU, memory, and storage health metrics and dispatches real-time alerts to a **Discord webhook**.

---

## 1. Automated Distributed IPS with CrowdSec & Ansible Delegation

Rather than configuring intrusion detection manually on each server, I wrote an Ansible playbook (`deploy_crowdsec_agents.yml`) that provisions a multi-node **CrowdSec** security mesh:
1. Installs `crowdsec` and `crowdsec-firewall-bouncer-iptables` on target Linux nodes.
2. Dynamically generates a 32-character cryptographic password per host and uses `delegate_to` to register each agent on the centralized **CrowdSec LAPI Brain** (`cscli machines add`).
3. Provisions a dedicated firewall bouncer API key on the LAPI server (`cscli bouncers add`) and writes locked-down (`0600`) configuration files to the agent node.
4. Disables the redundant local API on worker agents so all threat intelligence decisions flow through the central LAPI brain.

```yaml
# Excerpt from deploy_crowdsec_agents.yml
- name: Generate a random 32-char password for this host
  set_fact:
    cs_password: "{{ lookup('password', '/dev/null length=32 chars=ascii_letters,digits') }}"

- name: Provision machine on the CrowdSec LAPI Brain
  shell: "cscli machines add {{ inventory_hostname }} --password {{ cs_password }} --force"
  delegate_to: "{{ lapi_inventory_name }}"

- name: Provision Firewall Bouncer API Key on the Brain
  shell: "cscli bouncers add {{ inventory_hostname }}-bouncer -o raw"
  delegate_to: "{{ lapi_inventory_name }}"
  register: bouncer_key_output
```

---

## 2. Inventory-Driven Zero-Trust Firewall & SSH Hardening (`harden_all.yml`)

Every LXC container and bare-metal node is hardened automatically via Ansible (`harden_all.yml` & `harden_media.yml`):
* **Default-Deny Ingress:** Resets UFW to deny all incoming traffic by default while permitting outbound traffic.
* **Management Plane Safety Lock:** Explicitly restricts port `22` (SSH) to the designated **Tailscale** management IP (`100.x.x.x`) before enabling the firewall so automation never locks out the operator.
* **Dynamic Inventory Port Whitelisting:** Reads each host's `allowed_ports` variable from `hosts.yml` and opens only the exact TCP/UDP ports required for that workload (e.g., UDP `53` only on `pihole` group members).
* **SSH & Brute-Force Hardening:** Enforces `PasswordAuthentication no`, `PermitRootLogin prohibit-password`, `MaxAuthTries 3`, and configures an active **Fail2Ban** `[sshd]` jail (`maxretry = 3`, `bantime = 1h`).

```yaml
# Excerpt from harden_all.yml
- name: Set Default Firewall Policies
  community.general.ufw:
    direction: "{{ item.dir }}"
    policy: "{{ item.pol }}"
  loop:
    - { dir: 'incoming', pol: 'deny' }
    - { dir: 'outgoing', pol: 'allow' }

- name: Allow TCP Ports Dynamically from Host Inventory
  community.general.ufw:
    rule: allow
    port: "{{ item | trim }}"
    proto: tcp
  loop: "{{ (allowed_ports | default('')).split(',') }}"
  when: allowed_ports is defined and allowed_ports | length > 0
```

---

## 3. 3-Node K3s Kubernetes Cluster, Longhorn Storage & Cloudflare R2 Backups

To move beyond single-host Docker containers, I built a declarative **3-node K3s cluster** (`i5-server`, `lenovo-server`, `pi-server`) backed by **Longhorn** distributed block storage:
* **Automated Node Preparation (`prep_nodes_longhorn.yml`):** Uses Ansible to install `open-iscsi`, `nfs-common`, and `util-linux` and enable the `iscsid` systemd daemon across all K3s worker nodes.
* **Automated Offsite Disaster Recovery (`longhorn-backup-job.yaml`):** Configured a Kubernetes `RecurringJob` in the `longhorn-system` namespace that snapshots persistent volumes labeled `recurring-job.longhorn.io/cloud-backup-daily: "enabled"` every night at 2:00 AM (`cron: "0 2 * * *"`) with a 7-day rolling retention policy backed by **Cloudflare R2** S3 storage.
* **Zero-Trust Ingress & Automated TLS (`traefik-config.yaml` & `tunnel.yaml`):** Configured **Traefik** via `HelmChartConfig` to automatically provision wildcard/domain TLS certificates from Let's Encrypt using the **Cloudflare ACME DNS-01 challenge** (`CF_DNS_API_TOKEN` injected via K8s `secretKeyRef`), alongside **Cloudflare Tunnels (`cloudflared`)** so public-facing web services require zero open inbound WAN firewall ports.

```yaml
# Excerpt from longhorn-backup-job.yaml
apiVersion: longhorn.io/v1beta2
kind: RecurringJob
metadata:
  name: cloud-backup-daily
  namespace: longhorn-system
spec:
  cron: "0 2 * * *" # Automated nightly offsite backup at 2:00 AM
  task: "backup"
  retain: 7
  concurrency: 2
```

---

## 4. Self-Hosted Production Services & C++ Telemetry

Across the Proxmox LXC fleet and K3s cluster, I maintain and monitor production services for identity management, DNS security, observability, and documentation:
* **Identity & Secrets Management:** **Vaultwarden** (Bitwarden-compatible server with Argon2id admin hashing and persistent volume claims).
* **Network & DNS Sinkhole:** **Pi-hole** (network-wide DNS ad/tracker blocking and local split-DNS resolution for internal ingress domains).
* **Observability & Fleet Management:** **Custom C++ Proxmox Health Monitor** (polling the Proxmox API and alerting via Discord webhooks), **Uptime Kuma**, **Portainer** + **Portainer Agents** (`bootstrap_node.yml`), and **Homarr**.
* **Application Workloads:** **Wiki.js** (internal operational runbooks), **Immich** (distributed photo/ML backend with Redis & Postgres), **Ghost + MySQL** (backed by Longhorn PVCs and Cloudflare Tunnels), **Jellyfin**, and **Stirling-PDF**.
