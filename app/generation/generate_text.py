from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

model = ChatOpenAI(model="gpt-3.5-turbo",max_tokens=100)

prompt1_text = """The following is an application used to improve a user's people skills, 
by following the principles of how to win friends and influence others by dale carnegie.

The user has selected the following principle to practice: {principle}

Generate a scenario in which the user can practice this principle by first the character saying something to them. Then the user has the chance to respond.
The scenario should have one character the user is dealing with and be extremely creative in terms of scenarios.
"""

prompt1 = ChatPromptTemplate.from_template(prompt1_text)

prompt2_text = """Select a name from the followng list that can be used for the character in the scenario.

Character list:
Myra, Alice, Bria, Tony, Kate, Jessica, John, Mark, Drew

Scenario:
{scenario}

Select one name:
"""

prompt2 = ChatPromptTemplate.from_template(prompt2_text)

prompt3_text = """The following is an application used to improve a user's people skills, 
by following the principles of how to win friends and influence others by dale carnegie.

Given the following scenario created to practice the principle {principle}.
Generate the narration of what the scenario is, said by a narraor. And the stuff the character will say.

Example:

Scenario:
Myra, a co-worker who is known for her meticulous approach to projects but sometimes misses deadlines.

Narrator: "You're in a team meeting, and the discussion shifts to the recent project delay. Everyone knows Alex was responsible for the hold-up. She looks visibly stressed. As a team member who values Carnegie's principles, it's your turn to speak."

Alex: "I know I missed the deadline, and I feel terrible about it. There were so many unexpected issues, and I just couldn't get everything done on time."


Scenario:
{scenario}

Narrator:"""

prompt3 = ChatPromptTemplate.from_template(prompt3_text)

prompt4_text = """Given the following speech extract only the Narrator's text without any quotations.
Text:
{speech}

Narrators text only:"""

prompt5_text = """Given the following speech extract only other character's text without any quotations. Not the narrator, the other character.
Text:
{speech}

Other character text only:"""

prompt4 = ChatPromptTemplate.from_template(prompt4_text)
prompt5 = ChatPromptTemplate.from_template(prompt5_text)

chain1 = prompt1 | model | StrOutputParser()
chain2 = prompt2 | model | StrOutputParser()
chain3 = prompt3 | model | StrOutputParser()
chain4 = prompt4 | model | StrOutputParser()
chain5 = prompt5 | model | StrOutputParser()

principles = [
"Don’t criticize, condemn or complain",
"Give honest and sincere appreciation",
"Arouse in the other person an eager want",
"Become genuinely interested in other people",
"Smile",
"Say their name",
"Be a good listener",
"Talk in terms of the other person’s interests",
]

def generate_scenario(principle: int):

    principle_text = principles[principle]
    scenario = chain1.invoke({"principle":principle_text})
    speech = chain3.invoke({"principle": principle_text,"scenario":scenario})
    narrator_speech = chain4.invoke({"speech":speech})
    character_speech = chain5.invoke({"speech":speech})

    return narrator_speech, character_speech

def generate_character(principle: int):
    principle_text = principles[principle]
    character_name = chain2.invoke({"scenario":principle_text})
    return character_name