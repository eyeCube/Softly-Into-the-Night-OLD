


class EntityDialogue:
    def __init__(self):
        pass

class Topics:
    topics = {
        "rumors",
        "advice",
        "places",
        "people",
        "weather",
    }

class Advice:
    pass
    

ent.dialogue = EntityDialogue()
ent.dialogue.add_topic(TPC_)


'''
You: Hello, Aorus.
Aorus: Hello, You. Are you interested in hearing some rumors?
>>people
Which person?
>>$NPCname
You: Do you know $NPCname?
Aorus: What do you want to know about $pronoun?
>>location
You: Where is $pronoun?
Aorus: I don't know, sorry.
>>bye
You: Goodbye.
Aorus: 'Til next we meet.
'''


