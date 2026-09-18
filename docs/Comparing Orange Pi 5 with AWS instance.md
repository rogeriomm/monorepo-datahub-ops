# Orange Pi 5 vs AWS EC2 Equivalent

## Orange Pi 5

- **CPU:** Rockchip RK3588S
  - 4× Cortex-A76 up to 2.4 GHz
  - 4× Cortex-A55 up to 1.8 GHz
- **Architecture:** ARM64
- **RAM:** 16 GB
- **Storage:** 256 GB NVMe SSD
- **NVMe interface:** PCIe 2.0 ×1
- **Typical sequential storage performance:** ~400–420 MB/s
- **OS:** Linux ARM64

---

## Closest AWS Hardware Match: `m7gd.xlarge`

The AWS EC2 instance that most closely resembles the Orange Pi 5 configuration is:

**`m7gd.xlarge`**

| Feature | Orange Pi 5 | AWS `m7gd.xlarge` |
|---|---|---|
| Architecture | ARM64 | ARM64 |
| CPU | RK3588S | AWS Graviton3 |
| CPU cores/vCPU | 8 heterogeneous cores | 4 vCPU |
| RAM | 16 GB | 16 GiB |
| Local NVMe | 256 GB | 237 GB |
| Storage | Local NVMe SSD | Local NVMe instance store |
| OS | Linux ARM64 | Linux ARM64 |

### CPU Performance

Approximate Geekbench 6 performance:

| Benchmark | Orange Pi 5 | Graviton3 |
|---|---:|---:|
| Single-core | ~750–850 | ~1,500 |
| Multi-core | ~2,900–3,100 | ~4,900 |

The `m7gd.xlarge` is significantly faster than the Orange Pi 5, especially for single-threaded workloads.

A rough practical estimate is:

> **AWS `m7gd.xlarge` may provide approximately 1.5–2× the CPU performance of an Orange Pi 5.**

### Storage

The Orange Pi 5 NVMe slot is limited by PCIe 2.0 ×1, so practical sequential throughput is usually around:

```text
400–420 MB/s
```

The `m7gd.xlarge` includes:

```text
1 × 237 GB local NVMe SSD
```

This makes it unusually close to the Orange Pi 5 hardware configuration.

However, AWS local NVMe instance storage is **ephemeral**.

Data may be lost when the instance is stopped or terminated.

---

# Practical Persistent AWS Equivalent

For a server where storage must survive instance stops and restarts, a better functional equivalent is:

## `t4g.xlarge` + 256 GB gp3

Configuration:

```text
EC2: t4g.xlarge

CPU:
4 ARM Graviton2 vCPU

RAM:
16 GiB

Storage:
256 GiB EBS gp3

Architecture:
ARM64

OS:
Linux ARM64
```

To make the EBS storage performance closer to the Orange Pi NVMe:

```text
Volume type: gp3
Size: 256 GiB
IOPS: 5,000–8,000
Throughput: ~500 MiB/s
```

The resulting configuration would be:

```text
AWS t4g.xlarge
├── 4 ARM vCPU
├── 16 GiB RAM
├── 256 GiB gp3 SSD
├── ~500 MiB/s storage throughput
└── Linux ARM64
```

---

# Comparison

```text
Orange Pi 5
RK3588S
16 GB RAM
256 GB NVMe
~400 MB/s disk
        │
        ├── Closest hardware specification
        │   └── AWS m7gd.xlarge
        │       ├── 4 Graviton3 vCPU
        │       ├── 16 GiB RAM
        │       └── 237 GB local NVMe
        │           └── Ephemeral storage
        │
        └── Closest practical persistent server
            └── AWS t4g.xlarge
                ├── 4 Graviton2 vCPU
                ├── 16 GiB RAM
                └── 256 GB gp3
                    └── ~500 MiB/s
```

---

# Summary

For a direct hardware comparison:

> **Orange Pi 5 ≈ AWS `m7gd.xlarge`, although the AWS CPU is considerably faster.**

For a practical cloud replacement:

> **Orange Pi 5 ≈ AWS `t4g.xlarge` + 256 GB gp3**

For lighter Docker, MCP, infrastructure automation, monitoring, reverse proxy, and similar workloads, an AWS `t4g.large` may already provide enough performance.