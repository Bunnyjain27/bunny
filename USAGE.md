# Clubhouse Follow Script Usage Guide

## Overview

This script demonstrates how to create follow relationships between Clubhouse IDs using token-based authorization from a third party.

## What It Does

The script implements the scenario: **"One ID follows another ID via token of another ID"**

### Key Components:

1. **Three IDs**: Admin, User A (follower), User B (followee)
2. **Authorization Token**: Admin creates a token that grants permission to create follow relationships
3. **Follow Relationship**: User A follows User B using the Admin's authorization token

## How to Run

```bash
# Make sure you have Python 3 installed
python3 clubhouse_follow_script.py
```

## Script Flow

### Step 1: Create IDs
- Creates an Admin ID with permissions to authorize relationships
- Creates User A ID (the follower)
- Creates User B ID (the one to be followed)

### Step 2: Create Authorization Token
- Admin creates a token that can authorize follow relationships
- Token expires in 2 hours for security

### Step 3: Follow via Token
- User A follows User B using the Admin's authorization token
- The system verifies the token before creating the relationship

### Step 4-7: Verification and Statistics
- Shows who is following whom
- Displays all follow relationships in the system
- Shows system statistics (total IDs, tokens, etc.)
- Verifies that tokens are still valid

## Example Output

```
=== Clubhouse Follow Script ===
Demonstrating: One ID follows another ID via token of another ID

Step 1: Creating IDs...
Created Admin ID: ed6d63c3-66a3-4d33-a4c2-8dccee26faea
Created User A ID: 9fab8ebe-f588-4df9-ad5c-74bfde01dc70
Created User B ID: 6ceb0eba-07cc-4529-a28d-3ef5d395f487

Step 2: Creating admin authorization token...
Created Admin Token: 2588bc86-8704-433a-b880-8f60d48146e0

Step 3: User A follows User B via Admin's authorization token...
✓ Success! Follow relationship created.
Follow Token: 696f4d5a-2bb4-434a-bc2e-59a7427b0272
Authorized by: ed6d63c3-66a3-4d33-a4c2-8dccee26faea
Authorized at: Sat Jul 12 08:06:37 2025

Step 4: Verifying relationships...
User A is following: 1 users
  - bob (6ceb0eba-07cc-4529-a28d-3ef5d395f487)
User B has 1 followers
  - alice (9fab8ebe-f588-4df9-ad5c-74bfde01dc70)

Step 5: All follow relationships in the system...
Total follow relationships: 1
  - alice follows bob
    Authorized by: ed6d63c3-66a3-4d33-a4c2-8dccee26faea
    Status: active
    Expires: Sun Jul 13 08:06:37 2025

Step 6: System statistics...
Total IDs: 3
Total tokens: 2
Active tokens: 2
Expired tokens: 0
Revoked tokens: 0

Step 7: Token verification...
Admin token valid: True
Follow token valid: True

=== Script completed successfully! ===
```

## Advanced Usage

To run the advanced scenario with multiple users, uncomment this line in the script:
```python
# demo_advanced_scenario()
```

This will create 4 additional users and demonstrate batch follow operations.

## Security Features

- **Token Expiration**: All tokens have expiration times
- **Token Verification**: Tokens are validated before use
- **Authorization Tracking**: All relationships track who authorized them
- **Status Management**: Tokens can be active, expired, or revoked

## Files Structure

```
/workspace/
├── clubhouse_follow_script.py      # Main script
├── eosclubhouse/
│   ├── __init__.py                 # Package init
│   └── id_manager.py               # Core ID management system
├── requirements.txt                # Dependencies
├── USAGE.md                        # This file
└── README.md                       # Project documentation
```

## Dependencies

- Python 3.6+
- PyGObject (for GObject integration)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Use Cases

This script is useful for:
- Social media platforms implementing follow functionality
- Permission-based relationship management
- Token-based authorization systems
- Multi-user applications requiring secure relationship creation