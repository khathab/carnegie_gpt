from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from app.database import db
from app.generation.generate_characters import generate_characters_settings

model_turbo = ChatOpenAI(model="gpt-3.5-turbo",max_tokens=100,model_kwargs={"stop": ["\n"]})
model_gpt4 = ChatOpenAI(model="gpt-4",max_tokens=100,model_kwargs={"stop": ["\n"]})

scenario_text = """This is a conversation between our user {user_name} and a character named {character_name}. The goal of the conversation is to practice the principles
of how to win friends and influence others by dale carnegie. The conversation should be normal with the implicit goal to practice the specific principle below.

Ex.
Principle:
Talk in terms of the other person’s interests: Find out what the other person is passionate about.

Given the following information about the character and location setting, create that would be natural but would allow the user {user_name} to practice the principle above.
Lily Bio: Lily, a dedicated social worker, has spent years advocating for children's rights.
Lily Age: middle_aged
Lily Gender: female
Scenario setting: Underground Subway

Come up with a unique scenario given the above setting, so that the user {user_name} can practice the principle above.
Scenario (2-3 sentences):
{user_name} is waiting for a train in the underground subway when they notice Lily, a middle-aged woman, looking at a poster about a local children's charity event. Recognizing her from a community meeting, {user_name} approaches her to strike up a conversation. This setting provides a natural opportunity for {user_name} to talk with Lily about her interest in children's rights and welfare.

Principle:
{principle}

Given the following information about the character and location setting, create that would be natural but would allow the user {user_name} to practice the principle above.
{character_name} Bio: {bio}
{character_name} Age: {age}
{character_name} Gender: {gender}
Scenario setting: {setting}

Come up with a unique scenario given the above setting, so that the user {user_name} can practice the principle above.
Scenario (2-3 sentences):
"""

scenario_prompt = ChatPromptTemplate.from_template(scenario_text)
scenario_chain = scenario_prompt | model_turbo | StrOutputParser()

narration_text = """Given the following scenario, write a narration of the scenario.
Text:
{scenario}

Narrators text only (2-3 sentences):
"""

narration_prompt = ChatPromptTemplate.from_template(narration_text)

narration_chain = narration_prompt | model_turbo | StrOutputParser()

speech_text = """This is a conversation between our user {user_name} and a character named {character_name}. The goal of the conversation is to practice the principles
of how to win friends and influence others by dale carnegie. The conversation should be normal with the implicit goal to practice the specific principle below.

Principle:
{principle}

Character information:
{character_name} Bio: {bio}
{character_name} Age: {age}
{character_name} Gender: {gender}

Scenario setting: 
{setting}

Scenario:
{scenario}

Write the intial start of the conversation by {character_name} to {user_name} for the given scenario:
{character_name}: """

speech_prompt = ChatPromptTemplate.from_template(speech_text)
speech_chain = speech_prompt | model_turbo | StrOutputParser()

conversation_text = """This is a conversation between our user {user_name} and a character named {character_name}. The goal of the conversation is to practice the principles
of how to win friends and influence others by dale carnegie. The conversation should be normal with the implicit goal to practice the specific principle below.

Principle:
{principle}

Character information:
{character_name} Bio: {bio}
{character_name} Age: {age}
{character_name} Gender: {gender}

Scenario setting: 
{setting}

Scenario:
{scenario}

Write the generate the response to {user_name} in the following conversation.
{history}
{character_name}: """

response_prompt = ChatPromptTemplate.from_template(conversation_text)
response_chain = response_prompt | model_turbo | StrOutputParser()

principles = [
    "Don’t criticize, condemn or complain. This is straight forward in its emphasis in keeping negativity away from your interactions. People don't like feeling devalued or the sensation that they are being complained about. Instead of pointing out weaknesses, focus on strengths and opportunities for improvement. If something is not right, address it in a manner that creates solutions, not just highlighting problems - this is far more inspiring and constructive.",
    "Give honest and sincere appreciation: When you appreciate people, it shows that you value their contribution. Acknowledge their efforts, validate their feelings and praise their achievements. People can differentiate between a genuine compliment and a fake one, thus, always be real. For example, when someone does a good job, don't just say “good job”, be specific about what you liked about his/her work.",
    "Arouse in the other person an eager want: This is about motivating others to take action. Understand what drives the other person, what their needs or desires are, and show them how they can achieve what they crave or need. This principle can be applied in negotiations or when seeking alliance with someone. Pledge benefits that they would derive from the arrangement.",
    "Become genuinely interested in other people: Show interest in people's stories, their experiences, and aspirations. Ask open-ended questions and get to know them better. People will pick up on your sincerity, and will be more likely to trust and engage with you.",
    "Smile: A simple smile can make others feel comfortable around you. It creates a positive and welcoming energy around you that others will gravitate towards. But just like appreciation, the smile should be genuine.",
    "Say their name: When you use a person's name during a conversation, it sends a message that you see them as a unique individual. It creates a level of personal connection and draws their attention making them more receptive to what you have to say.",
    "Be a good listener: Good listening is about fully focusing on the other person when they are talking and resisting the urge to interrupt. Make sure to give feedback, ask follow-up questions, and do your best to understand their perspective. A good listener can gain a lot of trust and respect.",
    "Talk in terms of the other person’s interests: Find out what the other person is passionate about, and ask them about it or look for ways to relate it back to the topic of conversation. If you know a colleague enjoys golf, for example, you might discuss a recent golf tournament. This makes the conversation more interesting to them and helps you build a stronger relationship."
]

def generate_scenario(principle_state: int, user_id: int):
    character, setting = generate_characters_settings()
    principle_text = principles[principle_state]
    db.reset_message(user_id)
    user = db.get_user(user_id)

    user_name = user.full_name

    scenario = scenario_chain.invoke({
        "principle": principle_text,
        "character_name": character.name,
        "user_name": user_name,
        "bio": character.bio,
        "age": character.age,
        "gender": character.gender,
        "setting": setting

    })

    narrator_speech = narration_chain.invoke({"scenario":scenario})
    character_speech = speech_chain.invoke({
        "principle": principle_text,
        "character_name": character.name,
        "user_name": user_name,
        "bio": character.bio,
        "age": character.age,
        "gender": character.gender,
        "setting": setting,
        "scenario": scenario
    })

    db.set_principle(user_id, principle_state=principle_state)
    db.set_character(user_id, character)
    db.set_scenario(user_id, scenario)
    db.set_setting(user_id, setting)

    formatted_message = f"{character.name}: {character_speech}"
    db.add_bot_message(user_id,formatted_message)

    return narrator_speech, character_speech

def generate_response(user_id: int, user_message: str):
    user = db.get_user(user_id)
    principle_text = principles[user.principle_state]
    formatted_message = f"{user.full_name}: {user_message}"
    db.add_user_message(user_id,formatted_message)
    message_history = get_messsage_history(user_id)

    character_speech = response_chain.invoke({
        "principle": principle_text,
        "character_name": user.current_character.name,
        "user_name": user.full_name,
        "bio": user.current_character.bio,
        "age": user.current_character.age,
        "gender": user.current_character.gender,
        "setting": user.setting,
        "scenario": user.scenario,
        "history": message_history
    })
    formatted_message = f"{user.current_character.name}: {character_speech}"
    db.add_bot_message(user_id,formatted_message)
    return character_speech

def get_messsage_history(user_id: int, latest_n=10):
    messages_history = db.get_messages(user_id)
    message_list = [message.text for message in messages_history]
    # Reverse the messages to have them in order from oldest to newest
    reversed_messages = message_list[::-1]
    # Select the latest_n messages
    selected_messages = reversed_messages[-latest_n:]
    return "\n".join(selected_messages)