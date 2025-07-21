from .gemmini import gemmini_prompt

# Field order and their questions
field_order = ["description", "mood", "instruments", "tempo", "genre"]
field_questions = {
    "description": "📝 What's your music idea?",
    "mood": "🎭 What mood should the track have?",
    "instruments": "🎸 Which instruments should be included?",
    "tempo": "⏱️ What tempo do you prefer?",
    "genre": "🎶 What genre would you like?",
}

def refine_prompt(conversation_history, user_message):
    conversation_history.append({"user": user_message, "assistant": ""})

    # Initialize state
    fields = {key: None for key in field_order}

    # Fill fields sequentially with user inputs
    user_responses = [msg["user"].strip() for msg in conversation_history if msg["user"].strip()]
    for i, field in enumerate(field_order):
        if i < len(user_responses):
            fields[field] = user_responses[i]

    # Determine the next field to ask
    next_field = None
    for field in field_order:
        if fields[field] is None:
            next_field = field
            break

    if len(conversation_history) == 1:
        assistant_response = (
            "🎉 Welcome to the AI Music Generator! Let's create your perfect track.\n\n"
            + field_questions["description"]
        )
    elif next_field:
        assistant_response = field_questions[next_field]
    else:
        assistant_response = "✅ Great! Click Finalize to get your complete prompt."

    # Add assistant reply
    conversation_history[-1]["assistant"] = assistant_response

    # Generate conversation text
    chat_text = "\n".join([
        f"User: {msg['user']}\nAssistant: {msg['assistant']}"
        for msg in conversation_history
    ])
    return conversation_history, chat_text

def finalize_prompt(conversation_history):
    user_responses = [msg["user"].strip() for msg in conversation_history if msg["user"].strip()]
    prompt_data = dict(zip(field_order, user_responses))
    combined_text = " ".join(user_responses)
    final_prompt = gemmini_prompt(combined_text)
    return final_prompt
