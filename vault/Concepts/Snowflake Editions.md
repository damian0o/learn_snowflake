---
tags: [concept, day1, platform]
docs: https://docs.snowflake.com/en/user-guide/intro-editions
---
# Snowflake Editions

**In one sentence:** Snowflake comes in four editions, Standard, Enterprise, Business Critical and Virtual Private Snowflake, each adding features and compliance on top of the previous one, at a higher price per credit.

**Why it matters:** Several features your team will want (multi-cluster warehouses, 90-day Time Travel, masking policies) exist only from Enterprise up, and your account's edition decides what the exercises in these notes can show.

**Coming from Hadoop:** Cloudera's licence tiers (Express, Enterprise, Data Platform) gated support and some tooling. The analogy breaks because Snowflake's edition changes behaviour inside SQL: on Standard a `MAX_CLUSTER_COUNT = 3` is simply refused (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

| Edition | Adds | Typical reason to pick it |
|---------|------|---------------------------|
| **Standard** | the full platform: SQL, warehouses, Time Travel up to 1 day, Fail-safe 7 days, secure data sharing, database replication | small teams, cost first |
| **Enterprise** | [[Multi-cluster Warehouse]]; extended Time Travel up to **90 days**; materialized views; search optimization; column-level security (masking policies) and row access policies; periodic rekeying of encrypted data; query acceleration | most production teams; this is what the exercises assume |
| **Business Critical** | compliance support for HIPAA, HITRUST, PCI DSS; Tri-Secret Secure (customer-managed keys); private connectivity (AWS PrivateLink, Azure Private Link, Google Private Service Connect); account failover/failback and client redirect | regulated data, strict networking |
| **Virtual Private Snowflake (VPS)** | a completely separate Snowflake environment isolated from all other accounts | the highest isolation requirement |

Each edition includes everything below it. The price per credit rises with the edition; the credit *consumption* of a warehouse does not.

The edition is chosen per account and can be upgraded. The trial sign-up lets you pick Enterprise, which these notes assume (see [[Snowflake Account]]).

## Gotchas / exam traps

- Time Travel: Standard up to 1 day, Enterprise and above up to 90 days. Fail-safe is 7 days on all editions.
- Multi-cluster warehouses, materialized views and masking policies start at Enterprise.
- Tri-Secret Secure, PrivateLink-style connectivity and failover start at Business Critical. Business Critical was once called Enterprise for Sensitive Data (ESD).

## Related

- [[What Snowflake Is]]
- [[Multi-cluster Warehouse]]
- [[Credits and Billing]]
- [[Snowflake Account]]
- [[Organizations and Accounts]]

## Explain it to a teammate (fill in yourself)

> 
