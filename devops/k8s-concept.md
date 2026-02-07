=====================================================
KUBERNETES, HELM & CRDs — SENIOR / PARETO SUMMARY
=====================================================

Audience:
Senior backend / platform / security engineers who want a
correct mental model (not slogans).

-----------------------------------------------------
0. THE CORE IDEA (READ THIS FIRST)
-----------------------------------------------------

Kubernetes is NOT a runtime.
Kubernetes is NOT an orchestrator in the traditional sense.

Kubernetes is a **declarative control system**.

You describe desired state.
Controllers reconcile the system until reality matches it.
Actual execution happens on nodes, outside the API.

-----------------------------------------------------
1. WHAT IS A KUBERNETES RESOURCE (PRECISE)
-----------------------------------------------------

A Kubernetes Resource is:
- An **API object**
- Stored in **etcd**
- Served by **kube-apiserver**
- Defined by `apiVersion`, `kind`, `metadata`

Examples:
- Pod
- Deployment
- DaemonSet
- Service
- ConfigMap
- Secret
- Namespace
- Node
- CRD
- Role / RoleBinding

If you can:
  kubectl get <thing>

It is an API object.

---

IMPORTANT CLARIFICATION:

Not everything in the system is an API object.

These are NOT API objects:
- Containers
- Processes
- Threads
- Network packets
- cgroups
- iptables rules
- mounted volumes

Those belong to the **execution layer** (kubelet + kernel).

Correct statement:
Kubernetes stores *intent* as API objects and delegates execution
to node-level agents.

-----------------------------------------------------
2. API VERSION, API GROUPS, AND KIND
-----------------------------------------------------

apiVersion = API contract (schema + behavior)
kind       = which controller logic applies

Format:
  <api-group>/<version>

Examples:
- v1 → core primitives (Pod, Service, ConfigMap, Secret)
- apps/v1 → workload controllers (Deployment, DaemonSet, StatefulSet)
- batch/v1 → Job, CronJob
- rbac.authorization.k8s.io/v1 → RBAC
- apiextensions.k8s.io/v1 → CRDs

`kind` selects the controller.
`apiVersion` selects the API rules that controller obeys.

-----------------------------------------------------
3. POD VS CONTROLLERS (WHY POD IS NOT IN apps/)
-----------------------------------------------------

Pod:
- Smallest schedulable unit
- One execution attempt
- No self-healing
- No scaling
- No lifecycle guarantees

Controllers:
- Create and manage Pods
- Enforce availability
- Replace failures
- Scale replicas

Examples:
- Deployment
- DaemonSet
- StatefulSet
- Job

Design rule:
Pods are execution primitives.
apps/v1 objects are execution managers.

-----------------------------------------------------
4. WHAT CONTROLLERS ACTUALLY DO (VERY IMPORTANT)
-----------------------------------------------------

A controller is a reconciliation loop:

  watch API objects
  compare desired vs actual state
  mutate API objects to reduce drift
  repeat forever

Controllers DO NOT:
- Run containers
- Schedule Pods
- Execute binaries

Controllers ONLY:
- Read from kube-apiserver
- Write back to kube-apiserver

---

WHAT CONTROLLERS CAN CREATE OR MODIFY:

Controllers can create/update/delete **ANY Kubernetes API object**
they have RBAC permissions for.

Examples:
- Pods
- ReplicaSets
- Deployments
- DaemonSets
- StatefulSets
- ConfigMaps
- Secrets
- Services
- PersistentVolumeClaims
- RBAC objects
- CR status fields

Pods are just the *most common* side effect.

---

IMPORTANT CHAIN EXAMPLE (Deployment):

Deployment controller:
- Creates ReplicaSet

ReplicaSet controller:
- Creates Pods

The Deployment controller NEVER creates Pods directly.

-----------------------------------------------------
5. THE 3-LAYER KUBERNETES MENTAL MODEL (USE THIS)
-----------------------------------------------------

LAYER 1 — INTENT (API OBJECTS)
--------------------------------
- Stored in etcd
- Declarative
- Versioned
- Auditable

Examples:
- Deployment: "I want 3 replicas"
- Service: "I want stable networking"
- CRD object: "I want runtime security enabled"

Nothing runs here.

---

LAYER 2 — CONTROL (CONTROLLERS)
--------------------------------
- Control loops
- Policy enforcement
- State reconciliation

Examples:
- Deployment controller
- DaemonSet controller
- Operator controller

They translate intent into more intent (API mutations).

---

LAYER 3 — EXECUTION (NODES)
--------------------------------
- Scheduler assigns Pods to nodes
- kubelet runs containers
- kernel executes processes

This layer:
- Does not understand Deployments
- Does not understand CRDs
- Does not care about namespaces

It only executes instructions.

-----------------------------------------------------
6. WORKLOAD TYPES (PARETO)
-----------------------------------------------------

Deployment:
- Stateless apps
- Interchangeable Pods
- Parallel scaling
- No identity

DaemonSet:
- One Pod per node
- Node-local responsibility
- Logging, monitoring, security agents

StatefulSet:
- Stable Pod identity
- Ordered creation/deletion
- Persistent storage per Pod
- Databases, brokers, consensus systems

Ordered Pods means:
- Stable names (db-0, db-1, db-2)
- Sequential lifecycle
- Identity matters

-----------------------------------------------------
7. DATA LIVES IN APP VS DATA LIVES IN NODE
-----------------------------------------------------

Data lives in app:
- stdout logs
- HTTP metrics
- business logic
- request handling
→ Deployment

Data lives in node:
- container log files
- kernel/syscall events
- node metrics
- runtime profiling
→ DaemonSet

Rule:
If it must be physically present → DaemonSet
If it can be load-balanced → Deployment

-----------------------------------------------------
8. SERVICES & DNS (CORE NETWORKING)
-----------------------------------------------------

Service provides:
- Stable virtual IP
- Stable DNS name
- Load-balancing to Pods

Default DNS:
<service>.<namespace>.svc.cluster.local

In practice:
- Use service name only (same namespace)

Service gives identity.
Pods remain ephemeral.

-----------------------------------------------------
9. NAMESPACES VS NODES
-----------------------------------------------------

Namespaces:
- Logical isolation
- Names, RBAC, config, quotas

Nodes:
- Physical compute
- Run Pods from many namespaces

A single node commonly runs:
- prod Pods
- monitoring Pods
- security Pods
- system Pods

Namespaces do NOT isolate CPU, memory, or kernel.

-----------------------------------------------------
10. HELM — WHY IT EXISTS
-----------------------------------------------------

Problems Helm solves:
- Environment-specific config
- Feature flags
- Versioned releases
- Rollbacks
- Diffs before apply
- Reuse

Helm:
- Renders Kubernetes YAML
- Tracks release state
- Enables rollback

Helm does NOT run workloads.
Kubernetes does.

Rule:
Helm decides WHAT.
Kubernetes decides HOW.

-----------------------------------------------------
11. FEATURE FLAGS & ROLLBACKS WITHOUT HELM
-----------------------------------------------------

Without Helm:
- Duplicated YAMLs
- kubectl edit / set (imperative, unsafe)
- Kustomize overlays (manual values system)
- Rollbacks require Git archaeology
- No atomic rollback across resources

Kustomize base/overlay:
- base = shared truth
- overlays = env-specific patches

This recreates Helm concepts manually, without release safety.

-----------------------------------------------------
12. CRDs — WHAT THEY REALLY ARE
-----------------------------------------------------

CRD:
- Adds a new resource type to Kubernetes
- Defines schema + validation
- Stored in etcd
- No behavior by itself

CRD = vocabulary, not execution.

-----------------------------------------------------
13. CRD + CONTROLLER = OPERATOR
-----------------------------------------------------

CRD defines intent.
Controller interprets intent.

Operator:
- Runs as a Pod (usually Deployment)
- Watches CRDs
- Creates/updates Kubernetes resources
- May call external APIs

Without controller:
- CRs exist
- Nothing happens

-----------------------------------------------------
14. DATADOG / VENDOR PATTERN
-----------------------------------------------------

Datadog installs:
- CRDs (DatadogAgent, etc.)
- Operator Deployment

Flow:
CR created
→ operator sees it
→ operator creates DaemonSet, Deployment, ConfigMaps, RBAC
→ Kubernetes runs workloads

Operator must exist BEFORE CRs have meaning.

-----------------------------------------------------
15. FINAL SENIOR TRUTHS
-----------------------------------------------------

- Kubernetes is an API-driven control plane
- API objects store intent, not execution
- Controllers reconcile state via API mutations
- Controllers can create ANY K8s resource
- Pods are execution units, not managers
- CRDs extend the language, operators give meaning
- Helm manages versions of intent, not runtime

-----------------------------------------------------
END OF FILE
-----------------------------------------------------