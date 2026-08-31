from __future__ import annotations
from typing import Literal, TypedDict

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate


class GraderInput(TypedDict):
    """The variables the prompt below expects."""
    schema_ddl: str
    nl_question: str
    gold_sql: str
    submission_sql: str


class Verdict(BaseModel):
    label: Literal["correct", "incorrect_syntax", "incorrect_semantic"] = Field(
        description="correct: semantically equivalent to gold. "
                    "incorrect_syntax: would fail to parse/execute. "
                    "incorrect_semantic: parses but returns wrong results.")
    reason: str = Field(
        description="Concise account of the specific problem, or why it is correct.")


SYSTEM = (
    "You grade a student's SQL answer to a natural-language question against a "
    "reference (gold) query. Assign exactly one label:\n"
    "- incorrect_syntax: the query would fail to parse or execute (bad grammar, "
    "unknown table/column, type error).\n"
    "- incorrect_semantic: it parses and runs, but does not correctly answer the "
    "question -- wrong join, filter, aggregation, grouping, projection, or ordering.\n"
    "- correct: it is semantically equivalent to the gold query.\n\n"
    "Judge equivalence by MEANING, not by text. A query written very differently "
    "from the gold -- different aliases, join order, subquery vs join, extra "
    "parentheses -- is still CORRECT if it returns the same result for the "
    "question. Do not penalize style. Point to the specific offending clause when "
    "there is a fault. Base your verdict only on the information given."
)

HUMAN = (
    "Schema (with PK/FK constraints):\n{schema_ddl}\n\n"
    "Question:\n{nl_question}\n\n"
    "Gold SQL:\n{gold_sql}\n\n"
    "Student SQL:\n{submission_sql}"
)


PROMPT = ChatPromptTemplate.from_messages([("system", SYSTEM), ("human", HUMAN)])


def build_grader(model: str = "gpt-5.6",
                 provider: str = "openai",
                 temperature: float | None = None):
    kwargs = {} if temperature is None else {"temperature": temperature}
    llm = init_chat_model(model, model_provider=provider, **kwargs)
    return PROMPT | llm.with_structured_output(Verdict)
