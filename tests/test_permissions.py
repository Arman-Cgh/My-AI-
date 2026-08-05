# Expanded runtime test for Phase 1 permissions/usage
# Tests chat, image, vision, technical features against plan limits.

import os
import sys
from datetime import datetime

# ensure local project modules are importable
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BOTS_TG_PATH = os.path.join(BASE, 'bots', 'telegram_bot')
if BOTS_TG_PATH not in sys.path:
    sys.path.insert(0, BOTS_TG_PATH)

from database.db import add_user, get_connection, update_user_plan
from database.plans import get_user_limits
from database.usage import get_usage, add_usage
from utils.permissions import can_use_feature, increment_feature_usage

TEST_USER_ID = 999999998

print(f"\n=== Running expanded permissions runtime test for user {TEST_USER_ID} ===\n")

# Ensure test user exists and set plan to free
add_user(TEST_USER_ID, username="test_user", first_name="Test")
update_user_plan(TEST_USER_ID, 'free')

# helper: reset today's usage row for user
def reset_usage(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().date().isoformat()
    cursor.execute("DELETE FROM usage WHERE user_id=? AND date=?", (user_id, today))
    conn.commit()
    conn.close()

FEATURES = {
    'chat': ('daily_messages', 'messages'),
    'image': ('daily_images', 'images'),
    'technical': ('daily_technical_questions', 'code_requests'),
    'vision': ('daily_images', 'searches'),
}

for feat, (limit_key, usage_key) in FEATURES.items():
    print(f"--- Testing feature: {feat} ---")

    # reset
    reset_usage(TEST_USER_ID)

    limits = get_user_limits(TEST_USER_ID)
    limit = int(limits.get(limit_key, 0))
    print(f"Plan limit ({limit_key}) = {limit}")

    usage = get_usage(TEST_USER_ID)
    print("Initial usage:", usage)

    # sanity: can_use_feature should be True initially (unless limit==0)
    initial_can = can_use_feature(TEST_USER_ID, feat)
    print("can_use_feature initially:", initial_can)

    # add usage up to limit
    added = 0
    for i in range(limit):
        # before adding ensure can_use_feature is True
        before_ok = can_use_feature(TEST_USER_ID, feat)
        if not before_ok:
            print(f"Unexpected: can_use_feature returned False before reaching limit at iteration {i}")
            break
        # use add_usage directly
        add_usage(TEST_USER_ID, feat)
        added += 1

    usage_after = get_usage(TEST_USER_ID)
    print(f"Usage after adding {added} times:", usage_after)

    # now should be at or above limit; can_use_feature should be False
    can_now = can_use_feature(TEST_USER_ID, feat)
    print("can_use_feature after reaching limit:", can_now)

    # try increment_feature_usage wrapper once more and ensure usage increases if allowed
    wrapped_inc = increment_feature_usage(TEST_USER_ID, feat)
    usage_after_wrap = get_usage(TEST_USER_ID)
    print("increment_feature_usage returned:", wrapped_inc)
    print("usage after wrapper call:", usage_after_wrap)

    print('\n')

print("=== Expanded test complete ===\n")
