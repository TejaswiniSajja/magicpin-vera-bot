from rules import CATEGORY_TONES, TRIGGER_ACTIONS
from utils import safe_get


def compose_message(merchant, trigger, customer=None):
    category_slug = safe_get(merchant, "category_slug", default="restaurants")
    tone = CATEGORY_TONES.get(category_slug, CATEGORY_TONES["restaurants"])

    owner = safe_get(merchant, "identity", "owner_first_name", default="Partner")
    shop = safe_get(merchant, "identity", "name", default="your business")
    locality = safe_get(merchant, "identity", "locality", default="your area")

    views = safe_get(merchant, "performance", "views_7d", default=120)
    ctr = safe_get(merchant, "performance", "ctr_7d", default=2.0)
    delta = safe_get(merchant, "performance", "delta_7d", default=0)

    offers = safe_get(merchant, "offers", default=[])
    offer_price = offers[0].get("price", 299) if offers else 299

    trigger_kind = safe_get(trigger, "kind", default="unknown")
    payload = safe_get(trigger, "payload", default={})

    # SMART SIGNAL SELECTION
    if trigger_kind == "research_digest":
        demand = payload.get("search_volume", 100)

        message = (
            f"{owner}, {demand}+ people near {locality} are actively searching this week. "
            f"Your ₹{offer_price} offer on {shop} is visible but under-converting. "
            f"This is your highest intent window today."
        )
        cta = "Boost visibility / See audience"
        rationale = "High intent demand + active offer mismatch"

    elif trigger_kind == "performance_dip":
        message = (
            f"{owner}, your CTR dropped to {ctr}% with {abs(delta)}% dip in views. "
            f"Competitors in {locality} are running {tone['keywords'][0]} boosts right now."
        )
        cta = "Fix now / Show issue"
        rationale = "Performance drop vs local competition"

    elif trigger_kind == "spike_nearby_search":
        spike = payload.get("search_volume", 200)

        message = (
            f"{owner}, search spike detected: {spike}+ users in {locality} today. "
            f"Your listing for {shop} can capture immediate demand if boosted now."
        )
        cta = "Boost now / Miss opportunity"
        rationale = "Real-time demand spike"

    elif trigger_kind == "lapsed_customer" and customer:
        cname = safe_get(customer, "first_name", default="customer")
        gap = safe_get(customer, "last_visit_days", default=30)

        message = (
            f"{owner}, {cname} hasn't returned in {gap} days. "
            f"A simple {tone['keywords'][0]} reminder could reactivate them today."
        )
        cta = "Send reminder / Skip"
        rationale = "Customer reactivation opportunity"

    else:
        message = (
            f"{owner}, Vera detected a growth opportunity for {shop} in {locality}. "
            f"Small {tone['keywords'][0]} push can improve conversions."
        )
        cta = "Activate / Ignore"
        rationale = "Fallback growth opportunity"

    return {
        "body": message,
        "cta": cta,
        "send_as": "vera_growth_assistant",
        "suppression_key": f"{category_slug}_{trigger_kind}_{shop}",
        "rationale": rationale
    }