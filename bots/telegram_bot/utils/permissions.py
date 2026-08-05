import logging
from database.plans import get_user_limits
from database.usage import get_usage, add_usage, check_and_increment_usage

logger = logging.getLogger(__name__)

# Map logical feature names to plan limit keys and usage keys
# This mapping only maps names of keys; no numeric values are stored here.
FEATURE_CONFIG = {
    "chat": {"limit_key": "daily_messages", "usage_key": "messages"},
    "image": {"limit_key": "daily_images", "usage_key": "images"},
    "technical": {"limit_key": "daily_technical_questions", "usage_key": "code_requests"},
    # vision falls back to image usage by default
    "vision": {"limit_key": "daily_images", "usage_key": "searches"}
}


def can_use_feature(user_id, feature_name):
    """Return True if user can use the feature according to current plan limits.

    Behavior:
    - All numeric limits are read from database.plans.get_user_limits(user_id).
    - If the expected limit key is missing or invalid, a warning is logged and the feature is
      treated as "unlimited" (allowed). This avoids silently blocking users when admin
      hasn't configured a key yet.
    """
    cfg = FEATURE_CONFIG.get(feature_name)
    if not cfg:
        logger.warning("Feature mapping missing for '%s'", feature_name)
        # No mapping => assume feature is allowed (fallback unlimited) but cannot increment usage safely
        return True

    limits = get_user_limits(user_id)
    usage = get_usage(user_id)

    limit_key = cfg.get("limit_key")
    usage_key = cfg.get("usage_key")

    if limit_key not in limits:
        logger.warning("Plan limit key '%s' not found for user %s (plan limits: %s)", limit_key, user_id, list(limits.keys()))
        return True

    limit_val = limits.get(limit_key)
    used = usage.get(usage_key, 0)

    try:
        if limit_val is None:
            logger.warning("Plan limit '%s' is None for user %s", limit_key, user_id)
            return True
        # attempt to coerce to int; if fails, log and allow (unlimited)
        limit_int = int(limit_val)
        return used < limit_int
    except Exception as e:
        logger.warning("Invalid plan limit value for key '%s' for user %s: %s (error: %s)", limit_key, user_id, limit_val, e)
        return True


def increment_feature_usage(user_id, feature_name, amount=1):
    """Increment stored usage for a feature. Returns True on success.

    This function performs storage only; permission checks should be done via can_use_feature
    before calling increment_feature_usage if strict enforcement is desired.
    """
    if feature_name not in FEATURE_CONFIG:
        logger.warning("Attempted to increment unknown feature '%s' for user %s", feature_name, user_id)
        return False

    try:
        add_usage(user_id, feature_name, amount)
        return True
    except Exception as e:
        logger.exception("Failed to increment usage for feature '%s' for user %s: %s", feature_name, user_id, e)
        return False


def check_and_consume_feature(user_id, feature_name, amount=1):
    """Check plan limit and attempt to atomically consume usage.

    Returns True if consumption succeeded (usage incremented), False otherwise.
    """
    cfg = FEATURE_CONFIG.get(feature_name)
    if not cfg:
        logger.warning("Feature mapping missing for '%s'", feature_name)
        return True

    limits = get_user_limits(user_id)
    limit_key = cfg.get("limit_key")
    usage_key = cfg.get("usage_key")

    if limit_key not in limits:
        logger.warning("Plan limit key '%s' not found for user %s (plan limits: %s)", limit_key, user_id, list(limits.keys()))
        return True

    limit_val = limits.get(limit_key)
    try:
        if limit_val is None:
            logger.warning("Plan limit '%s' is None for user %s", limit_key, user_id)
            return True
        limit_int = int(limit_val)
    except Exception as e:
        logger.warning("Invalid plan limit value for key '%s' for user %s: %s (error: %s)", limit_key, user_id, limit_val, e)
        return True

    # Delegate atomic check+increment to database layer
    try:
        return check_and_increment_usage(user_id, feature_name, limit_int, amount=amount)
    except Exception as e:
        logger.exception("Error while attempting check_and_consume_feature for %s user %s: %s", feature_name, user_id, e)
        # fallback allow to avoid accidental blocking
        return True
