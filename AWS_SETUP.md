# AWS Setup Documentation

## Overview

The Shongwe Restaurant Ordering System uses Amazon RDS MySQL (AWS Free Tier) hosted in the `af-south-1` (Cape Town) region as its cloud database.

## RDS Instance

| Setting | Value |
|---|---|
| Engine | MySQL 8.x |
| Instance class | db.t3.micro (Free Tier) |
| Region | af-south-1 (Cape Town) |
| Database name | shongwe_ordering |
| Port | 3306 |
| Multi-AZ | No (Free Tier) |
| Automated backups | Enabled (7-day retention) |
| Deletion protection | Enabled |

## Databases

| Database | Purpose |
|---|---|
| `shongwe_ordering` | Production data |
| `shongwe_ordering_test` | Automated test data (never contains real data) |

## Security Group

The RDS instance is attached to a security group with the following inbound rule:

| Type | Protocol | Port | Source |
|---|---|---|---|
| MySQL/Aurora | TCP | 3306 | Your IP address only |

**Only your IP address should be allowed inbound on port 3306. Never use `0.0.0.0/0`.**

To update your IP if it changes:
1. Go to AWS Console → EC2 → Security Groups
2. Find the security group attached to your RDS instance
3. Edit inbound rules → update the source IP to your current IP

## SSL Connection

All connections to RDS use SSL with certificate verification.

The AWS global certificate bundle (`global-bundle.pem`) is required and must be downloaded from:
```
https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

Place it in the project root and add it to `.gitignore`. It is never committed to version control.

## Environment Variables

All credentials are stored in a `.env` file in the project root. This file is gitignored and never committed.

```
DB_HOST=<your-rds-endpoint>
DB_PORT=3306
DB_USER=<your-db-username>
DB_PASSWORD=<your-db-password>
DB_NAME=shongwe_ordering
DB_SSL_CA=./global-bundle.pem
TEST_DB_NAME=shongwe_ordering_test
TEST_MODE=
```

`TEST_MODE` is set to `1` only inside test files. It is left empty in `.env` so the app always uses the production database.

## Schema

Apply the schema to a new database using:
```
mysql -h <DB_HOST> -u <DB_USER> -p --ssl-ca=global-bundle.pem shongwe_ordering < schema.sql
```

Or run the migration script for the test database:
```
python create_test_db.py
```

## Security Controls

- Passwords are hashed with bcrypt (cost factor 12) before storage
- Plain text passwords are never stored or logged
- All SQL queries use parameterised statements — no string interpolation
- Database credentials are stored in environment variables only
- SSL certificate verification is enforced on every connection (`ssl_verify_cert=True`)
- RDS access is restricted to authorised IP addresses via security group rules
- Employee and admin roles are enforced at the application layer
- Login is limited to 3 attempts before returning to the main menu
- Usernames must be alphanumeric and at least 3 characters
- Passwords must be at least 8 characters

## Backups

Automated backups are enabled on the RDS instance with a 7-day retention window. Backups run during the configured maintenance window and can be restored from the AWS RDS console.

## Free Tier Limits

| Resource | Free Tier Allowance |
|---|---|
| RDS instance hours | 750 hours/month (db.t3.micro) |
| Storage | 20 GB |
| Backup storage | 20 GB |

Monitor usage in AWS Console → Billing → Free Tier to avoid unexpected charges.
