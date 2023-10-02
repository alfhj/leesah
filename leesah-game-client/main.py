from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA

# LEESAH QUIZ GAME CLIENT

# 1. Set `TEAM_NAME` to your preferred team name
# 2. Set `HEX_CODE` to your preferred team color
# 3. Set `QUIZ_TOPIC` to the topic name provided by the course administrators
# 4. Make sure you have downloaded and unpacked the credential files in the certs/ dir

# Config ##########################################################################################################

TEAM_NAME = "1 til 5"
HEX_CODE = "003D3D"
QUIZ_TOPIC = "leesah-quiz-abakus-1"
CONSUMER_GROUP_ID = f"cg-leesah-team-${TEAM_NAME}-1"


# ##################################################################################################################


class MyParticipant(quiz_rapid.QuizParticipant):
    def __init__(self):
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        #raise NotImplementedError("Her må du implementere håndtering av spørsmål 😎")
        if question.category == "team-registration":
            self.handle_register_team(question)
        if question.category == "ping-pong":
            self.handle_ping_pong(question)
        if question.category == "arithmetic":
            self.handle_arithmetic(question)

    # ---------------------------------------------------------------------------- Question handlers

    def handle_register_team(self, question: quiz_rapid.Question):
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=HEX_CODE
        )
    
    def handle_ping_pong(self, question: quiz_rapid.Question):
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer="pong"
        )

    def handle_arithmetic(self, question: quiz_rapid.Question):
        parts = question.question.split(" ")[:3]
        if parts[1] == "+":
            answer = int(parts[0]) + int(parts[2])
        if parts[1] == "-":
            answer = int(parts[0]) - int(parts[2])
        if parts[1] == "/":
            answer = int(float(parts[0]) / float(parts[2]))
        if parts[1] == "*":
            answer = int(parts[0]) * int(parts[2])
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=answer
        )


def main():
    rapid = quiz_rapid.QuizRapid(
        team_name=TEAM_NAME,
        topic=QUIZ_TOPIC,
        bootstrap_servers=HOSTED_KAFKA,
        consumer_group_id=CONSUMER_GROUP_ID,
        auto_commit=False,  # Bare skru på denne om du vet hva du driver med :)
        logg_questions=True,  # Logg spørsmålene appen mottar
        logg_answers=True,  # Logg svarene appen sender
        short_log_line=False,  # Logg bare en forkortet versjon av meldingene
        log_ignore_list=[]  # Liste med spørsmålskategorier loggingen skal ignorere
    )
    return MyParticipant(), rapid

def get_chat_gpt_response(question):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "{question}"}
    ]
)
