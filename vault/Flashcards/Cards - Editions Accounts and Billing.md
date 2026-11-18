---
tags: [flashcards/day1, cards]
---
# Cards - Editions Accounts and Billing

Cards for: [[Snowflake Editions]], [[Cloud Providers and Regions]], [[Organizations and Accounts]], [[Snowsight]], [[Credits and Billing]]

Name the four Snowflake editions in order.::Standard, Enterprise, Business Critical, Virtual Private Snowflake (VPS). [[Snowflake Editions]]

Time Travel limits by edition?::Standard up to 1 day; Enterprise and above up to 90 days. Fail-safe is 7 days on all editions. [[Snowflake Editions]]

Name four features that start at Enterprise edition.
?
Multi-cluster warehouses, extended Time Travel (90 days), materialized views, search optimization, column-level security (masking policies) and row access policies. [[Snowflake Editions]]

Name three features that start at Business Critical.::Tri-Secret Secure (customer-managed keys), private connectivity (AWS PrivateLink, Azure Private Link, Google Private Service Connect), account failover/failback; plus HIPAA, HITRUST and PCI DSS support. [[Snowflake Editions]]

What is Virtual Private Snowflake?::A completely separate Snowflake environment isolated from all other accounts; the highest isolation level. [[Snowflake Editions]]

Which cloud providers can host a Snowflake account?::AWS, Microsoft Azure, Google Cloud. One provider and one region per account. [[Cloud Providers and Regions]]

How does data get from one region to another in Snowflake?::Database replication or cross-region data sharing between accounts. Both incur egress charges. [[Cloud Providers and Regions]]

Preferred account identifier format?::`<orgname>-<account_name>`. The account locator (`xy12345.eu-central-1`) is legacy and not recommended. [[Cloud Providers and Regions]]

What is an organization in Snowflake?::The top-level container linking all of a company's accounts, for billing, administration, replication and listings. [[Organizations and Accounts]]

ORGADMIN versus ACCOUNTADMIN?::ORGADMIN manages the organization (create and list accounts, enable replication). ACCOUNTADMIN is the top role inside one account. [[Organizations and Accounts]]

Where do users, roles and warehouses live in the object hierarchy?::At the account level. Databases contain schemas; schemas contain tables, views, stages and the rest. [[Organizations and Accounts]]

Where in Snowsight do you open Query Profile?::Monitoring → Query History → click a query → Query Profile tab. [[Snowsight]]

What are the three cost categories on a Snowflake bill?::Compute (credits), storage (per compressed TB per month), data transfer (egress). [[Credits and Billing]]

Compute credits come from three sources. Name them.::Virtual warehouses, serverless features (Snowpipe, Automatic Clustering, serverless tasks, search optimization), and cloud services above the 10 % threshold. [[Credits and Billing]]

How is storage billed?::A flat rate per terabyte per month on the average daily on-disk (compressed) bytes, including Time Travel and Fail-safe history. [[Credits and Billing]]

Is loading data into Snowflake charged as data transfer?::No. Ingress is free; egress out of the region is charged. [[Credits and Billing]]
