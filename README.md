# Static Routing using SDN Controller

## Problem Statement

This project demonstrates **Software-Defined Networking (SDN)** concepts using **Mininet** and the **POX OpenFlow Controller**. The goal is to implement static flow rules to control packet forwarding in a simple network.

### Key Objectives:

1. Demonstrate controller-switch interaction using OpenFlow
2. Install static flow rules (match-action rules)
3. Verify forwarding behavior through testing
4. Compare:

   * Normal forwarding
   * Failure detection using port status

---

## Architecture & Design

### Topology

```
Single-switch topology:
  h1 --- s1 --- h2

Node Details:
- h1: 10.0.0.1
- h2: 10.0.0.2
- s1: OpenFlow Switch
```

---

### Flow Rules (Match-Action)

#### Scenario 1: Normal Controller (static_routing)

| Priority | Match     | Action   | Purpose |
| -------- | --------- | -------- | ------- |
| 100      | in_port=1 | output=2 | h1 → h2 |
| 100      | in_port=2 | output=1 | h2 → h1 |

---

#### Scenario 2: Failure Controller (wrong_routing)

| Event     | Action    | Purpose                       |
| --------- | --------- | ----------------------------- |
| Port DOWN | log.error | Detect link failure           |
| Port UP   | log.info  | Detect recovery               |
| in_port=1 | output=2  | Forward traffic (when active) |
| in_port=2 | output=1  | Forward traffic (when active) |

---

### Controller Logic

Both controllers:

* Use `_handle_ConnectionUp()` to install flow rules
* Use OpenFlow events for control

Failure controller additionally:

* Uses `_handle_PortStatus()` to detect link state changes

---

## Setup & Installation

### Prerequisites

* Linux (Ubuntu recommended)
* Python 2.7/3.x
* Mininet
* POX Controller

---

## Execution Steps

### Scenario 1: Normal Routing

#### Terminal 1 (Controller)

```bash
cd pox
python3 pox.py log.level --DEBUG openflow.of_01 static_routing
```

---

#### Terminal 2 (Mininet)

```bash
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6633
```

---

#### Test

```bash
mininet> h1 ping -c 4 h2
```

✅ Expected:

* 0% packet loss
* Successful communication

---

### Scenario 2: Failure Detection

#### Terminal 1 (Controller)

```bash
cd pox
python3 pox.py log.level --DEBUG openflow.of_01 wrong_routing
```

---

#### Terminal 2 (Mininet)

```bash
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6633
```

---

#### Simulate Failure

```bash
mininet> link h1 s1 down
mininet> h1 ping -c 4 h2
mininet> link h1 s1 up
```

---

### Expected Behavior

#### When link is DOWN:

* Controller logs error
* Packets are dropped

#### When link is UP:

* Controller logs recovery
* Communication resumes

---

## Code Structure

```
StaticRouting-SDN/
├── static_routing.py      # Normal forwarding controller
├── wrong_routing.py       # Failure detection controller
├── README.md
└── screenshots/
```

---

## Key Findings

### Scenario 1:

* Successful bidirectional communication
* Static flow rules handle all traffic

### Scenario 2:

* Link failure detected using PortStatus
* Logs clearly indicate network state
* Traffic stops when link is down

---

## References

* POX Documentation
* OpenFlow 1.0 Specification
* Mininet Walkthrough

---

## Author

**Student Name:** Manav Dewangan
**Date:** April 2026
**Course:** SDN
**Institution:** PES University

---

## License

For educational use only.
