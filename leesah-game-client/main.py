from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA
import base64
from datetime import datetime

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
        self.beholdning = 0
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        #raise NotImplementedError("Her må du implementere håndtering av spørsmål 😎")
        #if question.category == "team-registration":
        #    self.handle_register_team(question)
        #if question.category == "ping-pong":
        #    self.handle_ping_pong(question)
        #if question.category == "arithmetic":
        #    self.handle_arithmetic(question)
        #if question.category == "NAV":
        #    self.handle_nav(question)
        #if question.category == "is-a-prime":
        #    self.handle_prime(question)
        #if question.category == "transactions":
        #    self.handle_transactions(question)
        #if question.category == "base64":
        #    self.handle_base64(question)
        if question.category == "grunnbelop":
            self.handle_grunnbelop(question)
        if question.category == "min-max":
            self.handle_minmax(question)
    
    def handle_assessment(self, assessment: quiz_rapid.Assessment):
        pass

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

    def handle_base64(self, question: quiz_rapid.Question):
        q = question.question.split(" ")[-1]
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=base64.b64decode(q).decode("utf-8")
        )

    def handle_nav(self, question: quiz_rapid.Question):
        q = question.question
        answer = "IDK"
        if "applikasjonsplattformen" in q:
            answer = "NAIS"
        if "hvilken nettside" in q:
            answer = "detsombetyrnoe.no"
        if "Hva heter NAV" in q:
            answer = "Hans Christian Holte"
        if "kontor" in q:
            answer = "Fyrstikkalléen 1"
        if "designsystem" in q:
            answer = "Aksel"
        if "1G" in q:
            answer = 118620
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=answer
        )

    def handle_prime(self, question: quiz_rapid.Question):
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=is_prime(int(question.question.split(" ")[-1]))
        )
    
    def handle_grunnbelop(self, question: quiz_rapid.Question):
        dato = question.question.split(" ")[-1]
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=finn_belop(dato))
    
    def handle_minmax(self, question: quiz_rapid.Question):
        # HOYESTE i [23, 63, 48, 17, 67, 19, 81, 70, 68, 94, 91, 34, 24, 69, 91, 36, 9, 13, 18, 78]
        parts = question.question.replace("[", "").replace("]", "").replace(",", "").split(" ")
        ismax = parts[0] == "HOYESTE"
        arr = [int(x) for x in parts[2:]]
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=max(arr) if ismax else min(arr))

    def handle_transactions(self, question: quiz_rapid.Question):
        parts = question.question.split(" ")
        if parts[0]=="INNSKUDD":
            self.beholdning += int(parts[1])
        if parts[0]=="UTTREKK":
            self.beholdning -= int(parts[1])    
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=self.beholdning
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

def is_prime(n):
    if n == 1:
        return False
    if n == 2:
        return True
    for i in range(2,int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def finn_belop(self, date):
    dato_til_belop= {
        "2023-5-1": 118620,
        "2022-5-1": 111477,
        "2021-5-1": 106399,
        "2020-5-1": 101351,
        "2019-5-1": 99858,
        "2018-5-1": 96883,
        "2017-5-1": 93634,
        "2016-5-1": 92576,
        "2015-5-1": 90068,
        "2014-5-1": 88370,
        "2013-5-1": 85245,
        "2012-5-1": 82122,
        "2011-5-1": 79216,
        "2010-5-1": 75641,
        "2009-5-1": 72881,
        "2008-5-1": 70256,
        "2007-5-1": 66812,
        "2006-5-1": 62892,
        "2005-5-1": 60699,
        "2004-5-1": 58778,
        "2003-5-1": 56861,
        "2002-5-1": 54170,
        "2001-5-1": 51360,
        "2000-5-1": 49090,
        "1999-5-1": 46950,
        "1998-5-1": 45370,
        "1997-5-1": 42500,
        "1996-5-1": 41000,
        "1995-5-1": 39230,
        "1994-5-1": 38080,
        "1993-5-1": 37300,
        "1992-5-1": 36500,
        "1991-5-1": 35500,
        "1990-12-1": 34100,
        "1990-5-1": 34000,
        "1989-4-1": 32700,
        "1988-4-1": 31000,
        "1988-1-1": 30400,
        "1987-5-1": 29900,
        "1986-5-1": 28000,
        "1986-1-1": 26300,
        "1985-5-1": 25900,
        "1984-5-1": 24200,
        "1983-5-1": 22600,
        "1983-1-1": 21800,
        "1982-5-1": 21200,
        "1981-1-10": 19600,
        "1981-5-1": 19100,
        "1981-1-1": 17400,
        "1980-5-1": 16900,
        "1980-1-1": 16100,
        "1979-1-1": 15200,
        "1978-7-1": 14700,
        "1977-12-1": 14400,
        "1977-5-1": 13400,
        "1977-1-1": 13100,
        "1976-5-1": 12100,
        "1976-1-1": 11800,
        "1975-5-1": 11000,
        "1975-1-1": 10400,
        "1974-5-1": 9700,
        "1974-1-1": 9200,
        "1973-1-1": 8500,
        "1972-1-1": 7900,
        "1971-5-1": 7500,
        "1971-1-1": 7200,
        "1970-1-1": 6800,
        "1969-1-1": 6400,
        "1968-1-1": 5900,
        "1967-1-1": 5400,
    }
    indate = datetime.strptime(date, "%Y-%m-%d").date()
    for datadate, amount in dato_til_belop.items():
        datadateobj = datetime.strptime(datadate, "%Y-%m-%d").date()
        if indate > datadateobj:
            return amount

def get_chat_gpt_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "{question}"}
        ]
    )
