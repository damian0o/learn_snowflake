---
tags: [concept, day1, platform]
docs: https://docs.snowflake.com/en/user-guide/organizations
---
# Organizations and Accounts

**In one sentence:** An organization is the top-level container that links all of a company's Snowflake accounts; each account is a separate Snowflake environment with its own region, edition, users and data.

**Why it matters:** Your team account is one of possibly many in the company organization. Knowing the hierarchy tells you what crosses account boundaries (almost nothing without replication or sharing) and who can create new accounts.

**Coming from Hadoop:** Cloudera Manager could run several clusters, each with its own HDFS and users; the organization is the Manager, an account is one cluster. The analogy breaks because Snowflake accounts can share data without copying it (secure data sharing, Day 2) and replicate databases to each other with one command (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```
Organization  (one per company; name chosen by Snowflake with you)
 └── Account  (one region, one cloud, one edition)
      ├── Users, Roles, Warehouses, Resource monitors, Integrations   (account-level objects)
      └── Database
           └── Schema
                └── Tables, Views, Stages, Pipes, Streams, Tasks, Functions ...   (Day 2)
```

- **Organization.** Groups accounts for billing, administration and cross-account features (replication, failover, listings). Organization-level work is done with the `ORGADMIN` role, which can create accounts, list them and enable replication. Newer multi-account organizations use an *organization account* with the `GLOBALORGADMIN` role; `ORGADMIN` is being phased out for them, so expect to see both names.
- **Account.** The unit you log in to. It has an identifier `<orgname>-<account_name>` (see [[Cloud Providers and Regions]]), an [[Snowflake Editions|edition]], and its own complete set of users, roles and data. Nothing is visible across accounts unless shared or replicated.
- **Why several accounts.** Typical reasons: environment separation (a sandbox account next to production), different regions or clouds, business units with separate billing.

Many teams instead keep one account and separate environments by **database** (`ANALYTICS_DEV`, `ANALYTICS_PROD`). The Day 3 naming standard takes that route; it is cheaper to operate and lets you clone production into development in seconds.

## Gotchas / exam traps

- Account names must be unique only within the organization; they cannot contain hyphens.
- ORGADMIN is the organization role; ACCOUNTADMIN is the top role inside one account. They are different.
- Users, roles and warehouses belong to an account. Databases contain schemas; schemas contain tables.

## Related

- [[Cloud Providers and Regions]]
- [[Snowflake Editions]]
- [[Snowflake Account]]
- [[What Snowflake Is]]
- [[Snowsight]]

## Explain it to a teammate (fill in yourself)

> 
