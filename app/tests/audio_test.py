from app.generation import generate_audio


#generate_single_audio("Hello jeff, what are you up to?", "Mark")
text = ["As Alice went into the abyss he stated", 
        "Oh lord please save me from this misery",
        "As he turned around, she was suddenly face to face with a dragon. She promptly turned back around and covered her face with her hands.", 
        "If I can't see you, you can't see me. Hehe, oh shittt."]
character_names = ["Narrator", "Alice", "Narrator","Alice"]
generate_audio.generate_multiple_audio(text, character_names)