# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

import json
from genlayer import *


class UniversalPredictionMarket(gl.Contract):
    has_resolved: bool
    outcome: u256
    question: str
    category: str
    resolution_url: str
    deadline: str

    def __init__(self, question: str, category: str, resolution_url: str, deadline: str):
        self.has_resolved = False
        self.outcome = u256(0)
        self.question = question
        self.category = category
        self.resolution_url = resolution_url
        self.deadline = deadline

    @gl.public.write
    def resolve(self) -> str:
        if self.has_resolved:
            return "Already resolved"

        def nondet() -> str:
            response = gl.nondet.web.get(self.resolution_url)
            web_data = response.body.decode("utf-8")

            task = f"""In the following web page, find information to answer this prediction market question:
            Question: {self.question}

            Web page content:
            {web_data[:3000]}
            End of web page data.

            If the event in the question has clearly happened based on the web page, set occurred to 1.
            If the event has NOT happened yet or is unclear, set occurred to 0.

            Respond with the following JSON format:
            {{
                "occurred": int, // 1 if event happened, 0 if not yet or unclear
                "explanation": str // brief explanation of your decision
            }}
            It is mandatory that you respond only using the JSON format above,
            nothing else. Don't include any other words or characters,
            your output must be only JSON without any formatting prefix or suffix.
            This result should be perfectly parsable by a JSON parser without errors.
            """
            result = gl.nondet.exec_prompt(task).replace("```json", "").replace("```", "")
            return json.dumps(json.loads(result), sort_keys=True)

        result_json = json.loads(gl.eq_principle.strict_eq(nondet))

        self.has_resolved = True
        self.outcome = u256(result_json["occurred"])

        return json.dumps(result_json)

    @gl.public.view
    def get_outcome(self) -> str:
        if not self.has_resolved:
            return "Pending. Call resolve() to determine the outcome."
        if int(self.outcome) == 1:
            return "YES. The event has occurred."
        return "NO. The event has not occurred yet."

    @gl.public.view
    def is_resolved(self) -> bool:
        return self.has_resolved

       
