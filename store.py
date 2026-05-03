merchant_contexts = {}
customer_contexts = {}
trigger_contexts = {}
category_contexts = {}
conversation_states = {}


def store_context(scope, context_id, version, payload):
    target = None

    if scope == "merchant":
        target = merchant_contexts
    elif scope == "customer":
        target = customer_contexts
    elif scope == "trigger":
        target = trigger_contexts
    elif scope == "category":
        target = category_contexts

    if target is None:
        return False

    old = target.get(context_id)

    if old and old["version"] >= version:
        return False

    target[context_id] = {
        "version": version,
        "payload": payload
    }
    return True


def get_merchant(context_id):
    return merchant_contexts.get(context_id, {}).get("payload", {})


def get_customer(context_id):
    return customer_contexts.get(context_id, {}).get("payload", {})


def get_trigger(context_id):
    return trigger_contexts.get(context_id, {}).get("payload", {"kind": "unknown", "payload": {}})

def get_category(context_id):
    return category_contexts.get(context_id, {}).get("payload", {})


def save_conversation_state(key, value):
    conversation_states[key] = value


def get_conversation_state(key):
    return conversation_states.get(key)