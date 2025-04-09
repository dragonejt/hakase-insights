from langchain_core.runnables import RunnableLambda

from app.agents import date_time_agent


def date_time_runnable() -> RunnableLambda:
    def invoke_date_time_agent(question: str):
        return date_time_agent().invoke(
            {
                "instructions": "Using any tools and retrievals you have, answer the question.",
                "input": question,
            }
        )

    return RunnableLambda(name="date_time_runnable", func=invoke_date_time_agent)
