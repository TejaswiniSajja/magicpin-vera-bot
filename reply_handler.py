def handle_reply(user_reply, last_message):
    text = user_reply.lower()

    # 🔴 AUTO-REPLY DETECTION
    if any(p in text for p in [
        "thank you for contacting",
        "we will get back",
        "our team will respond"
    ]):
        return {"action": "end"}

    # 🔴 HOSTILE HANDLING
    if any(p in text for p in [
        "stop messaging",
        "spam",
        "useless",
        "don't message"
    ]):
        return {
            "action": "end",
            "body": "Sorry about that. We’ll stop here."
        }

    # 🔴 INTENT / COMMITMENT
    if any(p in text for p in [
        "ok", "yes", "send", "do it",
        "lets do it", "let's do it",
        "whats next", "what's next"
    ]):
        return {
            "action": "send",
            "body": "Great — I’ll set this up for you. Sending a draft now. Confirm once ready.",
            "cta": "Confirm",
            "send_as": "vera_growth_assistant"
        }

    # 🔵 EXPLANATION
    if "why" in text or "explain" in text:
        return {
            "action": "send",
            "body": "This was triggered by real-time demand, performance drop, and local competition activity.",
            "cta": "Proceed / Skip",
            "send_as": "vera_growth_assistant"
        }

    # 🟡 DECLINE
    if any(w in text for w in ["no", "skip", "later"]):
        return {
            "action": "end",
            "body": "Got it. Vera will wait for a stronger conversion window.",
            "send_as": "vera_growth_assistant"
        }

    # ⚪ FALLBACK
    return {
        "action": "send",
        "body": "I can activate this opportunity or explain expected impact in one line.",
        "cta": "Activate / Explain",
        "send_as": "vera_growth_assistant"
    }