---
tags: [memory]
---
# Mnemonics

Hooks for the lists that refuse to stay in your head. Say them aloud once, picture them once, then let the cards do the rest.

## Day 1

### The three layers: "Storage, Compute, Services" = **S-C-S**, bottom to top
Picture a snowflake landing on a **S**now bank, melting on a **C**ar engine, rising as **S**team. Snow at the bottom (storage), heat in the middle (compute), vapour on top (services). [[Three-Layer Architecture]]

### Hybrid architecture: "one disk, many nothings"
One shared **disk** everyone reads; many shared-**nothing** nodes that each crunch a slice. If a question asks "shared-disk or shared-nothing?", the answer is "yes". [[Three-Layer Architecture]]

### Warehouse sizes: the doubling ladder
XS **1**, S **2**, M **4**, L **8**, XL **16**, 2XL **32**, 3XL **64**, 4XL **128**, 5XL **256**, 6XL **512**. Same as RAM sticks. One extra fact rides along: **60**-second minimum per start. Say it as "one, two, four, eight, sixteen, then double the X-count and keep doubling; sixty seconds to boot". [[Warehouse Sizes and Credits]]

### Auto-suspend default: "ten minutes, six hundred"
600 seconds. Picture a warehouse clock face with the hand at 10. [[Auto-suspend and Auto-resume]]

### Up or out: "**Heavy** goes **High**, **Many** goes **wide**"
One heavy query: scale **up** (bigger size). Many queued queries: scale **out** (more clusters). [[Scaling Up vs Scaling Out]]

### Multi-cluster: "Max = Max is Maximized"
If MIN equals MAX the warehouse is **Maximized**; if MIN is less, it **auto-scales**. Policies: **Standard** starts clusters at the first sign of a queue, **Economy** waits for six minutes of work (Economy is stingy; stingy waits). Enterprise edition only: "**E**xtra clusters need **E**nterprise". [[Multi-cluster Warehouse]]

### Three caches: "**R**oof, **R**oof, **F**loor"
**R**esult cache and metadata cache are on the **roof** (Cloud Services). The **warehouse** cache is on the office **floor** and is wiped when the lights go off. Lifetimes: **24/31** for results (24 hours, extended on reuse, 31 days max), **always** for metadata, **until suspend** for the warehouse cache. [[Caching]]

### Result cache conditions: "**SAME** query"
**S**QL text identical, **A**uthorised role, **M**icro-partitions unchanged, **E**xcludes non-deterministic functions. [[Result Cache]]

### Metadata answers without compute: "**Count, Min, Max** at the front desk"
Whole-table `COUNT(*)`, `MIN`, `MAX`, plus `SHOW` and `DESCRIBE`. Anything with a WHERE walks into an office. [[Metadata Cache]]

### Editions: "**S**ome **E**ngineers **B**uy **V**aults"
**S**tandard, **E**nterprise, **B**usiness Critical, **V**PS. Time Travel climbs 1 → 90 at the **E** step; keys and private links arrive at the **B** step; **V** is a vault of your own. [[Snowflake Editions]]

### The 10 % rule: "the receptionist is free until she is a tenth of the rent"
Cloud Services are charged only above 10 % of the day's warehouse credits, and only the excess. [[Cloud Services Layer]]

### Micro-partition size: "**50 to 500**, uncompressed"
Half a hundred to five hundred megabytes, measured before compression. [[Micro-partitions]]

### Three meters on the bill: "**C**ompute, **S**torage, **T**ransfer" = **CST**
Like a time zone. Ingress free, egress paid. [[Credits and Billing]]

### Account identifier: "**org-dash-account**"
`<orgname>-<account_name>`; the locator with a region suffix is the legacy form. [[Organizations and Accounts]]

## Day 2

(added in increment 2)

## Day 3

(added in increment 3)

## Related

- [[Memory Techniques]]
- [[Cheat Sheet Day 1]]
