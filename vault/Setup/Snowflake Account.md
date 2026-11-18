---
tags: [setup]
---
# Snowflake Account

You need an account where you can create warehouses, roles and grants, because Day 2 and Day 3 do exactly that. Never practise on a production account.

> [!warning] Not yet executed by the author
> The author of these notes had no Snowflake account while writing. The steps follow the official docs; if anything differs on your screen, note it and tell me.

## Which account

Log in to the team account in Snowsight, open a worksheet, and run:

```sql
SHOW GRANTS TO USER <your_user>;
SELECT CURRENT_ACCOUNT_NAME(), CURRENT_REGION(), CURRENT_ROLE();
```

Use the team account for the exercises only if **both** are true:

- it is a non-production account (a dev or sandbox account, not the one the business reads from), and
- the grants list `ACCOUNTADMIN`, or both `SYSADMIN` and `SECURITYADMIN`.

Otherwise create a personal trial. It costs nothing, lasts 30 days, and you hold `ACCOUNTADMIN`.

## Trial account

1. Go to signup.snowflake.com.
2. Choose the **Enterprise** edition (so you can see multi-cluster warehouses and 90-day Time Travel, see [[Snowflake Editions]]).
3. Pick the cloud and region closest to the team (see [[Cloud Providers and Regions]]).
4. Verify your email and set a username and password.
5. Save the account identifier, shown as `<orgname>-<account_name>`; you need it for every tool login (see [[Organizations and Accounts]]).
6. Log in to [[Snowsight]].
7. Create your practice warehouse:

```sql
CREATE WAREHOUSE WH_LEARN_XS
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Personal learning warehouse';
```

The name is a shortened form of the standard you will meet on [[Day 3]], `WH_<TEAM>_<PURPOSE>_<SIZE>`, with the purpose dropped because this personal warehouse has only one.

## Related

- [[00 Home]]
- [[Day 1]]
