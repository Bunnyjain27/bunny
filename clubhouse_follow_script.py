#!/usr/bin/env python3
"""
Clubhouse Follow Script

This script demonstrates how to create a follow relationship between two IDs
using a token from a third ID for authorization.

Usage:
    python3 clubhouse_follow_script.py

Example scenario:
    - User A wants to follow User B
    - Admin has a token that allows creating relationships
    - User A follows User B via Admin's authorization token
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eosclubhouse.id_manager import (
    create_clubhouse_id, create_token_link, follow_via_token,
    get_id_manager, verify_token_link, IDType
)
import time


def main():
    """Main script demonstrating the follow functionality."""
    print("=== Clubhouse Follow Script ===")
    print("Demonstrating: One ID follows another ID via token of another ID\n")
    
    # Step 1: Create the IDs
    print("Step 1: Creating IDs...")
    
    # Create admin ID (has permissions to authorize relationships)
    admin_id = create_clubhouse_id(
        id_type=IDType.USER,
        metadata={"username": "admin", "role": "administrator", "permissions": ["create_relationships"]}
    )
    print(f"Created Admin ID: {admin_id.id_value}")
    
    # Create user A (follower)
    user_a_id = create_clubhouse_id(
        id_type=IDType.USER,
        metadata={"username": "alice", "role": "user"}
    )
    print(f"Created User A ID: {user_a_id.id_value}")
    
    # Create user B (to be followed)
    user_b_id = create_clubhouse_id(
        id_type=IDType.USER,
        metadata={"username": "bob", "role": "user"}
    )
    print(f"Created User B ID: {user_b_id.id_value}")
    
    # Step 2: Create admin authorization token
    print("\nStep 2: Creating admin authorization token...")
    
    # Admin creates a token that can be used to authorize follow relationships
    admin_token = create_token_link(
        source_id=admin_id.id_value,
        target_id=admin_id.id_value,  # Self-referential for permission token
        expires_in=7200,  # 2 hours
        relationship_type="authorization",
        metadata={"permission": "create_follow_relationships", "scope": "all_users"}
    )
    print(f"Created Admin Token: {admin_token.token_value}")
    
    # Step 3: User A follows User B via Admin's token
    print("\nStep 3: User A follows User B via Admin's authorization token...")
    
    follow_token = follow_via_token(
        follower_id=user_a_id.id_value,
        followee_id=user_b_id.id_value,
        authorizer_token=admin_token.token_value
    )
    
    if follow_token:
        print(f"✓ Success! Follow relationship created.")
        print(f"Follow Token: {follow_token.token_value}")
        print(f"Authorized by: {follow_token.metadata.get('authorized_by')}")
        print(f"Authorized at: {time.ctime(follow_token.metadata.get('authorized_at'))}")
    else:
        print("✗ Failed to create follow relationship.")
        return
    
    # Step 4: Verify the relationships
    print("\nStep 4: Verifying relationships...")
    
    manager = get_id_manager()
    
    # Check who User A is following
    user_a_following = manager.get_linked_ids(user_a_id.id_value)
    print(f"User A is following: {len(user_a_following)} users")
    for followed_id in user_a_following:
        followed_user = manager.get_id(followed_id)
        if followed_user:
            print(f"  - {followed_user.get_metadata('username')} ({followed_id})")
    
    # Check who is following User B
    user_b_followers = manager.get_reverse_linked_ids(user_b_id.id_value)
    print(f"User B has {len(user_b_followers)} followers")
    for follower_id in user_b_followers:
        follower_user = manager.get_id(follower_id)
        if follower_user:
            print(f"  - {follower_user.get_metadata('username')} ({follower_id})")
    
    # Step 5: Show follow relationships
    print("\nStep 5: All follow relationships in the system...")
    
    follow_relationships = manager.get_relationships("follow")
    print(f"Total follow relationships: {len(follow_relationships)}")
    
    for relationship in follow_relationships:
        follower = manager.get_id(relationship.source_id)
        followee = manager.get_id(relationship.target_id)
        if follower and followee:
            print(f"  - {follower.get_metadata('username')} follows {followee.get_metadata('username')}")
            print(f"    Authorized by: {relationship.metadata.get('authorized_by')}")
            print(f"    Status: {relationship.status.value}")
            print(f"    Expires: {time.ctime(relationship.expires_at) if relationship.expires_at else 'Never'}")
    
    # Step 6: System statistics
    print("\nStep 6: System statistics...")
    
    stats = manager.get_statistics()
    print(f"Total IDs: {stats['total_ids']}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"Active tokens: {stats['active_tokens']}")
    print(f"Expired tokens: {stats['expired_tokens']}")
    print(f"Revoked tokens: {stats['revoked_tokens']}")
    
    # Step 7: Demonstrate token verification
    print("\nStep 7: Token verification...")
    
    print(f"Admin token valid: {verify_token_link(admin_token.token_value)}")
    print(f"Follow token valid: {verify_token_link(follow_token.token_value)}")
    
    print("\n=== Script completed successfully! ===")


def demo_advanced_scenario():
    """Demonstrate a more advanced scenario with multiple users and relationships."""
    print("\n=== Advanced Scenario: Multiple Users ===")
    
    # Create multiple users
    users = []
    for i, username in enumerate(["charlie", "diana", "eve", "frank"]):
        user = create_clubhouse_id(
            id_type=IDType.USER,
            metadata={"username": username, "role": "user", "level": i + 1}
        )
        users.append(user)
        print(f"Created user: {username} ({user.id_value})")
    
    # Create moderator with authorization powers
    moderator = create_clubhouse_id(
        id_type=IDType.USER,
        metadata={"username": "moderator", "role": "moderator", "permissions": ["manage_relationships"]}
    )
    print(f"Created moderator: {moderator.id_value}")
    
    # Create moderator authorization token
    mod_token = create_token_link(
        source_id=moderator.id_value,
        target_id=moderator.id_value,
        expires_in=3600,
        relationship_type="authorization",
        metadata={"permission": "batch_follow", "scope": "all_users"}
    )
    
    # Create multiple follow relationships
    print("\nCreating multiple follow relationships...")
    follow_count = 0
    
    for i, follower in enumerate(users):
        for j, followee in enumerate(users):
            if i != j:  # Don't follow yourself
                follow_token = follow_via_token(
                    follower_id=follower.id_value,
                    followee_id=followee.id_value,
                    authorizer_token=mod_token.token_value
                )
                if follow_token:
                    follow_count += 1
                    print(f"  {follower.get_metadata('username')} → {followee.get_metadata('username')}")
    
    print(f"\nCreated {follow_count} follow relationships")
    
    # Show network statistics
    manager = get_id_manager()
    stats = manager.get_statistics()
    print(f"System now has {stats['total_ids']} IDs and {stats['active_tokens']} active tokens")


if __name__ == "__main__":
    try:
        main()
        
        # Uncomment the line below to run the advanced scenario
        # demo_advanced_scenario()
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()