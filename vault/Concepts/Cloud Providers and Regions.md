---
tags: [concept, day1, platform]
docs: https://docs.snowflake.com/en/user-guide/intro-regions
---
# Cloud Providers and Regions

**In one sentence:** Each Snowflake account lives in exactly one region of one cloud provider, AWS, Microsoft Azure or Google Cloud, and talks to other regions and clouds only through replication and sharing.

**Why it matters:** The region decides latency to your sources and consumers, which features and warehouse sizes are available, data residency, and whether moving data costs egress fees.

**Coming from Hadoop:** Your Cloudera cluster lived in one data centre, and so did its data. Same idea, but now the choice is a dropdown at sign-up, and the cloud provider's object storage replaces your racks. The analogy breaks because Snowflake can replicate a database to another region or another cloud with one command, something a second Hadoop cluster never made easy (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

- **Providers:** Amazon Web Services, Microsoft Azure, Google Cloud Platform. You choose one per account. The Snowflake experience is the same on all three; a few features and the largest warehouse sizes (5X-Large, 6X-Large) are AWS and Azure only.
- **Region:** one per account, chosen at creation (for example AWS `eu-central-1` Frankfurt). Storage and compute for that account stay in that region. Regions do not limit who can log in, only where data sits.
- **Account identifier:** `<orgname>-<account_name>`, used in URLs (`https://<orgname>-<account_name>.snowflakecomputing.com`) and in every driver and tool login. The legacy *account locator* (for example `xy12345.eu-central-1`) still works but is not recommended. See [[Organizations and Accounts]].
- **Cross-region and cross-cloud:** databases can be replicated to accounts in other regions or clouds, and data can be shared across them. Both move bytes between regions, which incurs data transfer (egress) charges (see [[Credits and Billing]]).

For a team feeding external platforms, put the account in the region closest to the bulk of the sources and consumers, and expect to pay egress for anything that leaves the region.

## Gotchas / exam traps

- One account, one cloud, one region. Multi-region means multiple accounts linked by replication.
- Ingress (loading data into Snowflake) is free; egress out of the region is charged.
- Account identifiers use the organisation name and account name; the locator is legacy.

## Related

- [[Organizations and Accounts]]
- [[Credits and Billing]]
- [[What Snowflake Is]]
- [[Snowflake Editions]]
- [[Snowflake Account]]

## Explain it to a teammate (fill in yourself)

> 
