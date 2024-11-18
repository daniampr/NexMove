from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
from pandasai.connectors import PandasConnector
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
from utils.helpers import DATA_simple_chat
import os
import streamlit as st
import json
load_dotenv()


class OutputParser(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def parse(self, result):
        if result['type'] == "dataframe":
            st.dataframe(result['value'])
        elif result['type'] == 'plot':
            st.image(result["value"])
        else:
            st.write(result['value'])
        return result['value']


with open("chatbot/config/assistant.json", "r") as f:
    model_config = json.load(f)

llm = ChatGroq(
    model_name=model_config['model_version'],
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

field_descriptions = {
    "travelers": "The number of individuals traveling between the origin and destination provinces.",
    "trips": "The total number of trips/displacements taken between the origin and destination provinces.",
    "origin_province_id": "The unique identifier for the origin province where the trip starts.",
    "origin_province_name": "The name of the origin province where the trip starts.",
    "destination_province_id": "The unique identifier for the destination province where the trip ends.",
    "destination_province_name": "The name of the destination province where the trip ends.",
    "day": "The specific date when the trip occurred, in YYYY-MM-DD format.",
    "day_of_week": "The day of the week when the trip occurred (e.g., Monday, Tuesday).",
    "origin_community": "The community or region to which the origin province belongs.",
    "destination_community": "The community or region to which the destination province belongs.",
    "distance": "The distance between the origin and destination provinces, measured in kilometers."
}


connector = PandasConnector(
    {"original_df": DATA_simple_chat},
    field_descriptions=field_descriptions
)

df = SmartDataframe(
    connector,
    config={"llm": llm, "response_parser": OutputParser, "enable_cache": False, "conversational": False},
    description="Dataframe containing daily mobility data between Spainish provinces."
)


def chat_completion(user_prompt: str):

    pandasai_response = df.chat(user_prompt)
    code_executed = df.last_code_executed
    messages = [
        ("system", model_config["system_prompt"]),
        ("user", model_config["user_prompt"].format(
            user_prompt=user_prompt,
            code_executed=code_executed,
            result=pandasai_response
        ))
    ]
    assistant_response = llm.invoke(messages)  # Get response from the model
    return assistant_response.content, code_executed
