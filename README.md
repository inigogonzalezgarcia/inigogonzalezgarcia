### Hi, I'm Iñigo 👋

IT Operations & End User Services leader with 11+ years of experience in financial services, healthcare, manufacturing and luxury retail. I lead distributed IT teams across countries and time zones, and I stay hands-on with infrastructure, endpoints and service delivery.

This GitHub is where I turn lessons from that work into small, practical tools.

**Website:** [inigogonzalezgarcia.github.io](https://inigogonzalezgarcia.github.io): career, toolkit, an interactive map and all my projects (ES/EN).

**Focus areas:** IT operations in critical environments · Modern Workplace · ITSM and service delivery · Security and resilience · Automation and FinOps

**Stack:** Python · pandas · Streamlit · PowerShell · Microsoft Graph · AWS · Microsoft 365 · ServiceNow

**Labs:** cloud and Kubernetes networking (Ingress, DNS, private connectivity), Terraform, SRE practice (SLOs, error budgets, incident reviews) and day 2 operations for GPU clusters. Projects 06–16 are hands-on labs that take my infrastructure and operations experience into these areas.

---

### Projects

Each project starts from a real problem I have dealt with. All of them are built from scratch with synthetic data: no employer code, data or systems.

| # | Project | Problem it tackles | Status |
|---|---|---|---|
| 01 | [FinOps Cloud Cost Dashboard](https://github.com/inigogonzalezgarcia/01-finops-cloud-cost-dashboard) | Cloud cost drift and anomalies across AWS and Azure | ✅ Live |
| 02 | [Intune Device Compliance Report](https://github.com/inigogonzalezgarcia/02-intune-compliance-report) | Endpoint compliance visibility for IT and management | ✅ Live |
| 03 | [Entra ID Identity Hygiene Audit](https://github.com/inigogonzalezgarcia/03-entra-id-hygiene-audit) | Inactive accounts, stale guests and users without MFA | ✅ Live |
| 04 | [ITSM Service Desk KPI Dashboard](https://github.com/inigogonzalezgarcia/04-itsm-kpi-dashboard) | MTTR, SLA and backlog tracking for service desks | ✅ Live |
| 05 | [IT Ops Console](https://github.com/inigogonzalezgarcia/05-it-ops-console) | One view for on-site IT operations, invite-only with MFA | ✅ Live |
| 06 | [Kubernetes Ingress Lab](https://github.com/inigogonzalezgarcia/06-kubernetes-ingress-lab) | Ingress, DNS and network policies with Cilium, Envoy Gateway and external-dns | ✅ Live |
| 07 | [AWS Private Connectivity](https://github.com/inigogonzalezgarcia/07-aws-private-connectivity) | PrivateLink, private DNS and security controls as code (Terraform) | ✅ Live |
| 08 | [Edge Health & SLO Monitor](https://github.com/inigogonzalezgarcia/08-edge-health-slo-monitor) | DNS, TLS and HTTP probes with SLOs, burn-rate alerts and incident reviews | ✅ Live |
| 09 | [GPU Node Remediation](https://github.com/inigogonzalezgarcia/09-gpu-node-remediation) | Kubernetes controller that drains, repairs, validates or quarantines unhealthy GPU nodes (Go, kind e2e) | ✅ Live |
| 10 | [GPU Fleet Observability](https://github.com/inigogonzalezgarcia/10-gpu-fleet-observability) | dcgm-exporter metrics, alerts with runbooks and promtool tests, Alertmanager routing, Grafana and a fleet report | ✅ Live |
| 11 | [GPU Fleet Lifecycle](https://github.com/inigogonzalezgarcia/11-gpu-fleet-lifecycle) | Driver rollouts across a GPU fleet: canary, approval, batches, validation, soak and automatic rollback | ✅ Live |
| 12 | [GPU Goodput and MTBI](https://github.com/inigogonzalezgarcia/12-gpu-goodput-mtbi) | Where a large training job's GPU-hours go: interruption simulator, goodput and MTBI, Young/Daly checkpoints, goodput SLO | ✅ Live |
| 13 | [GPU Cluster Acceptance and Burn-in](https://github.com/inigogonzalezgarcia/13-cluster-acceptance-burnin) | Handover to sign-off: staged DCGM/NCCL validation, burn-in, agreed criteria, punch list and customer report | ✅ Live |
| 14 | [Slurm GPU Operations](https://github.com/inigogonzalezgarcia/14-slurm-gpu-ops) | Slurm cluster in Docker Compose: XID health check that drains and requeues, validation in a maintenance reservation, goodput from sacct | ✅ Live |
| 15 | [Multi-tenant GPU Scheduling](https://github.com/inigogonzalezgarcia/15-multi-tenant-gpu-scheduling) | One GPU agreement for three teams, enforced by Kueue and KAI Scheduler on kind with simulated GPUs: borrowing, reclaim, priorities, gang scheduling, GPU sharing; KubeVirt under software emulation | ✅ Live |
| 16 | [GitOps GPU Fleet](https://github.com/inigogonzalezgarcia/16-gitops-gpu-fleet) | GPU Operator and Network Operator releases promoted with Flux across kind clusters (staging → prod H100 → prod A100): versions pinned per node pool, `helm template` + kubeconform in CI, approvals in Git, rollout plan for repo 11 generated from the same file | ✅ Live |
| 17 | [Teams Rooms Fleet Health](https://github.com/inigogonzalezgarcia/17-teams-rooms-fleet-health) | Which meeting rooms will fail today: Teams Rooms health from Microsoft Graph, room register and bookings turned into an ordered morning check, firmware drift and a daily trend | ✅ Live |
| 18 | [MECM + Intune Co-management Tracker](https://github.com/inigogonzalezgarcia/18-mecm-intune-comanagement-tracker) | Real co-management state, workload authority against the plan, Windows 11 waves and go/no-go gates for the next slider move | ✅ Live |
| 19 | [AD Infrastructure Health Check](https://github.com/inigogonzalezgarcia/19-ad-infra-health-check) | Weekly Active Directory check from one read-only export: DC services, clock and disk, replication links and tombstone risk, DHCP scopes, GPO hygiene, privileged groups and krbtgt age, compared with last week | ✅ Live |
| 20 | [Entra SSO App Audit](https://github.com/inigogonzalezgarcia/20-entra-sso-app-audit) | Monthly review of enterprise apps and app registrations: SAML certificates and secrets about to expire, owners, assignment and MFA coverage, risky permissions and consents, SCIM provisioning, with a renewal calendar | ✅ Live |
| 21 | [Apple Fleet Audit](https://github.com/inigogonzalezgarcia/21-apple-fleet-audit) | Weekly review of a Jamf Pro Apple fleet: APNs, ADE and Apps and Books tokens, OS currency, FileVault, SIP and bootstrap token, passcodes, stale check-ins, storage and warranty, VIP devices first | ✅ Live |
| 22 | [DEX Experience Score](https://github.com/inigogonzalezgarcia/22-dex-experience-score) | Lab: endpoint telemetry (boot, crashes, Wi-Fi, Teams calls, VPN, battery) turned into a 0-10 experience score per device, site and department, with a weekly trend and the top fixes | ✅ Live |
| 23 | [IT Vendor Contract Tracker](https://github.com/inigogonzalezgarcia/23-it-vendor-contract-tracker) | Monthly review of the contract register: notice deadlines and contracts that renew by themselves, unused and over-deployed licences, budget forecast, missed SLAs and service credits, single-supplier risk, with a renewal calendar to import | ✅ Live |
| 24 | [Hospitality IT Pre-opening](https://github.com/inigogonzalezgarcia/24-hospitality-it-preopening) | Will IT be ready before the hotel opens: task network with vendor lead times, critical path, gates from T-90 to T-1, blocked and start-now work, risks and a go-live checklist | ✅ Live |
| 25 | [Security Controls Evidence](https://github.com/inigogonzalezgarcia/25-security-controls-evidence) | One control register mapped to ISO 27001, NIS2 and GDPR: missing, late or failing evidence, controls claimed without proof, expired exceptions, readiness per framework, an audit pack and an evidence calendar | ✅ Live |
| 26 | [OT Segmentation Lab](https://github.com/inigogonzalezgarcia/26-ot-segmentation-lab) | A plant network checked against the Purdue model and IEC 62443 zones and conduits: paths that bypass the DMZ, controller protocols from IT, remote access that skips the jump host, the safety system reachable from control, and a tighter rule set from observed traffic | ✅ Live |
| 27 | [M365 Tenant Governance Review](https://github.com/inigogonzalezgarcia/27-m365-tenant-governance-review) | A monthly review of a Microsoft 365 tenant: standing admin roles and PIM, emergency accounts, Conditional Access basics, settings drift, licences to reclaim, and admin changes matched to change tickets, including the provider's | ✅ Live |
| 28 | [EUC Provider Service Review](https://github.com/inigogonzalezgarcia/28-euc-provider-service-review) | Monthly service review of a provider-run end-user computing service from a ticket export: SLA scorecard with the breach list, backlog and ageing, escalations and the OLAs the internal teams owe, out-of-hours coverage, quality signals a compliance figure hides, and the service credits due | ✅ Live |
| 29 | [Tenant Separation Cutover Planner](https://github.com/inigogonzalezgarcia/29-tenant-separation-cutover-planner) | Readiness review for a Microsoft 365 tenant separation from the source tenant's exports: devices that cannot be reset into the target (Autopilot, BitLocker, Windows 11 hardware), users who will fail on day 1, applications without a decision, and a go / no-go per wave with the reason | ✅ Live |
| 30 | [Jira & Confluence Admin Kit](https://github.com/inigogonzalezgarcia/30-jira-confluence-admin-kit) | Monthly admin review of a Jira, JSM and Confluence Cloud site from its own exports: licences to reclaim with the saving, admins, external users and service accounts without an owner, projects, spaces and custom fields to clean up, and the agile health of every Scrum board (carry-over, scope added, say/do, idle boards) | ✅ Live |
| 31 | [Dealer Systems Health](https://github.com/inigogonzalezgarcia/31-dealer-systems-health) | Weekly review of a car brand's dealer systems from the network's own exports: DMS feeds that stopped or send nothing, warranty claims about to miss the deadline and why they are rejected, the parts catalogue and price file each dealer really uses, and dealers opening or leaving, per dealer in red, amber or green | ✅ Live |
| 32 | [Backup Restore Test Tracker](https://github.com/inigogonzalezgarcia/32-backup-restore-test-tracker) | Monthly review of whether backups would actually bring systems back: RPO from the last good backup, offsite and immutable copies that really ran, restore tests against the plan and the RTO, and DR exercises with their actions, per system and tier | ✅ Live |
| 33 | [Executive Meeting Readiness](https://github.com/inigogonzalezgarcia/33-executive-meeting-readiness) | Readiness check of board, committee and executive meetings: the tech check, the Teams Room and its peripherals, updates inside the freeze, VIP devices and the support engineer, with a ready / attention / at-risk verdict per meeting | ✅ Live |
| 34 | [Venue Service Readiness](https://github.com/inigogonzalezgarcia/34-venue-service-readiness) | Morning check of a hospitality venue before each service: enough working tills and handhelds, kitchen printers, card terminals and cash machines, the internet failover and Wi-Fi, the PMS and IPTV, and vendor tickets past their SLA, with a ready / attention / at-risk verdict per service | ✅ Live |
| 35 | [Private Cloud Capacity Review](https://github.com/inigogonzalezgarcia/35-private-cloud-capacity-review) | Monthly capacity and availability review of a private cloud (vSphere and Nutanix): headroom after a host failure, the month each cluster crosses its N+1 limit with the approved projects, the reclaim list that buys time, datastores, availability, and when to order hosts | ✅ Live |
| 36 | [Major Incident Command Kit](https://github.com/inigogonzalezgarcia/36-major-incident-command-kit) | Running and reviewing P1/P2 incidents: detection gaps and monitoring blind spots, MTTA and MTTR against target, stakeholder update gaps, changes in the 72 hours before, overdue actions and repeats, with a timeline and a draft post-incident review per incident | ✅ Live |

---

### Where the ideas come from

| Period | Role | Environment |
|---|---|---|
| 2021 – now | IT Site Leader / Senior Engineer | Financial services, trading floor, multi-site team |
| 2019 – 2021 | IT Manager | Manufacturing, Spain / Italy / Turkey |
| 2018 – 2019 | IT Systems Engineer | Healthcare IT, regulated environments |
| 2016 – 2018 | IT Support / Systems Engineer | Luxury retail, multinational |
| 2015 – 2016 | IT Support Engineer | Technology consultancy |

### Customisation and contact

Want one of these tools adapted to your environment? Use the contact form on [my website](https://inigogonzalezgarcia.github.io/about.html#contacto) or reach out on [LinkedIn](https://www.linkedin.com/in/igonzalez93).
