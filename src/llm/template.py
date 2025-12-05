def generate_commentary(event):
    etype = event.get("event_type")
    batsman = event.get("batsman", "the batsman")

    if etype == "boundary":
        return f"{batsman} smashes it to the boundary!"
    if etype == "wicket":
        return f"OUT! Huge moment in the match!"
    return "A good delivery."
