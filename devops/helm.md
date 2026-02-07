========================================================
HELM — FROM ZERO TO MASTER (PRODUCTION-GRADE SUMMARY)
========================================================

Audience:
Senior backend / platform / security engineers.

Goal:
Understand WHAT Helm is, WHY it exists, HOW it works internally,
and HOW to use it correctly in production.

--------------------------------------------------------
1. WHAT HELM IS (PRECISE, NO MARKETING)
--------------------------------------------------------

Helm is:
- A package manager for Kubernetes
- A templating engine for Kubernetes YAML
- A release/version manager for Kubernetes resources

Helm does NOT:
- Run containers
- Replace Kubernetes controllers
- Add new runtime behavior

Helm ONLY:
- Renders Kubernetes manifests
- Sends them to the Kubernetes API
- Tracks what it sent (history, versions)

Think of Helm as:
"Git + templating + rollback" for Kubernetes manifests.

--------------------------------------------------------
2. WHY HELM EXISTS (THE REAL PROBLEMS)
--------------------------------------------------------

Plain Kubernetes YAML has no built-in solution for:

- Environment differences (dev / staging / prod)
- Feature flags
- Versioned releases
- Rollbacks
- Diff before apply
- Reuse of manifests
- Safe upgrades

Without Helm:
- YAML duplication
- Manual edits
- No atomic rollback
- Human error in prod

Helm exists to solve exactly these problems.

--------------------------------------------------------
3. CORE HELM CONCEPTS (MUST KNOW)
--------------------------------------------------------

Helm has 4 core concepts:

1) Chart
2) Values
3) Templates
4) Release

Understand these → you understand Helm.

--------------------------------------------------------
4. HELM CHART (WHAT IT IS)
--------------------------------------------------------

A Helm Chart is:
- A directory
- That describes how to deploy an application to Kubernetes

Minimal chart structure:

my-chart/
  Chart.yaml
  values.yaml
  templates/

Chart = reusable deployment package.

--------------------------------------------------------
5. Chart.yaml (METADATA ONLY)
--------------------------------------------------------

Example:

apiVersion: v2
name: miggo-agent
description: Miggo runtime security agent
type: application
version: 0.3.0
appVersion: "1.9.4"

Meaning:
- version     → chart version (Helm package)
- appVersion  → application version (informational)

Chart.yaml does NOT affect runtime behavior.

--------------------------------------------------------
6. VALUES (CONFIGURATION LAYER)
--------------------------------------------------------

values.yaml contains:
- Defaults
- Feature flags
- Resource tuning
- Image versions
- Environment-specific config

Example:

image:
  repository: miggo/runtime
  tag: "1.9.4"

runtime:
  enabled: true
  profiler:
    enabled: false
    enabledTracers: []

Values are NOT Kubernetes objects.
They exist only at Helm render time.

--------------------------------------------------------
7. TEMPLATES (THE ACTUAL K8S MANIFESTS)
--------------------------------------------------------

Everything under templates/ becomes Kubernetes YAML.

Templates are:
- Normal Kubernetes manifests
- With Go-template variables

Example template:

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: {{ .Release.Name }}-runtime
spec:
  template:
    spec:
      containers:
        - name: agent
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"

After rendering:
- Helm sends pure YAML to Kubernetes
- Kubernetes does not know Helm exists

IMPORTANT:
Templates = the Kubernetes resources you are creating.

--------------------------------------------------------
8. RELEASE (THE MOST IMPORTANT CONCEPT)
--------------------------------------------------------

A Release is:
- One installation of a chart
- With a specific set of values
- In a specific namespace

Created by:

helm install <release-name> <chart>

Example:

helm install miggo ./miggo-agent

This creates:
.Release.Name = "miggo"

Release metadata is stored in the cluster
(as Secrets or ConfigMaps).

--------------------------------------------------------
9. WHERE .Release.Name COMES FROM
--------------------------------------------------------

.Release.Name comes from the Helm CLI:

helm install miggo ./miggo-agent
             ↑
        Release name

Used to:
- Name resources
- Track versions
- Enable rollback

Multiple releases can exist:

helm install miggo-prod ./chart
helm install miggo-staging ./chart

--------------------------------------------------------
10. HOW HELM ACTUALLY WORKS (INTERNAL FLOW)
--------------------------------------------------------

Helm workflow:

1) Load chart
2) Merge values.yaml + user overrides
3) Render templates
4) Send YAML to Kubernetes API
5) Store release metadata
6) Exit

Helm does NOT stay running.
Helm is not a controller.

--------------------------------------------------------
11. CORE HELM COMMANDS (PARETO)
--------------------------------------------------------

You need ~6 commands in real life:

helm install
helm upgrade
helm upgrade --install
helm rollback
helm history
helm template

Everything else is secondary.

--------------------------------------------------------
12. ROLLBACKS (WHY HELM IS VALUABLE)
--------------------------------------------------------

Helm tracks every install/upgrade as a revision.

helm history miggo

Rollback:

helm rollback miggo 6

What happens:
- Helm re-applies the YAML from revision 6
- Kubernetes reconciles state
- Controllers perform rollbacks

Rollback is deterministic and fast.

--------------------------------------------------------
13. HELM VS KUSTOMIZE (SHORT, HONEST)
--------------------------------------------------------

Kustomize:
- Patch-based
- No release history
- No rollback
- No atomic upgrades

Helm:
- Value-based
- Release history
- Rollbacks
- Upgrade safety

If you need lifecycle management → Helm.

--------------------------------------------------------
14. HELM + OPERATORS (HOW THEY FIT)
--------------------------------------------------------

Two valid models:

A) Helm deploys native K8s resources directly
B) Helm deploys an Operator (+ CRDs),
   then users apply Custom Resources

Helm manages installation.
Operator manages runtime behavior.

They are complementary, not competing.

--------------------------------------------------------
15. FINAL HELM MENTAL MODEL (MASTER LEVEL)
--------------------------------------------------------

Helm is:
- A compiler (values → YAML)
- A package manager (charts)
- A release manager (history + rollback)

Helm is NOT:
- Kubernetes
- A runtime
- A controller

Golden rule:
Helm manages intent versions.
Kubernetes executes intent.
