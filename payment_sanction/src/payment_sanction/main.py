#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.Payment_Sanction_Crew.PaymentSanctionCrew import PaymentSanctionCrew
from crewai_tools import SerperDevTool

import agentops
import os
# tool = SerperDevTool(
#     search_url="https://google.serper.dev/scholar",
#     n_results=2,
# )

# print(tool.run(search_query="ChatGPT"))


class PaymentSanctionState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class PaymentSanctionFlow(Flow[PaymentSanctionState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        print("Generating poem")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated", result.raw)
        self.state.poem = result.raw



def kickoff():
    session = agentops.init(api_keys=os.getenv("AGENTOPS_API_KEY"))
    payment_sanction_flow = PaymentSanctionFlow()
    payment_sanction_flow.kickoff()
    session.end_session()


def plot():
    payment_sanction_flow = PaymentSanctionFlow()
    payment_sanction_flow.plot()


if __name__ == "__main__":
    kickoff()
