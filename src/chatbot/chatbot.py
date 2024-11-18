from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
from pandasai.connectors import PandasConnector
from langchain_groq.chat_models import ChatGroq
from pandasai.llm import OpenAI
import openai
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

client = openai.OpenAI(api_key="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")

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


def chat_completion(user_prompt: str, model: str):

    if model == "gpt-4o":
        llm = OpenAI(api_token="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")
        connector = PandasConnector(
            {"original_df": DATA_simple_chat},
            field_descriptions=field_descriptions
        )

        df = SmartDataframe(
            connector,
            config={"llm": llm, "response_parser": OutputParser, "enable_cache": False, "conversational": False},
            description="Dataframe containing daily mobility data between Spainish provinces."
        )

        pandasai_response = df.chat(user_prompt)
        code_executed = df.last_code_executed
        assistant_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": model_config["system_prompt"]},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0
        )

    if model == "mixtral-8x7b-32768":
        llm = ChatGroq(
            model_name=model_config['model_version'],
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.0
        )
        messages = [
            ("system", model_config["system_prompt"]),
            ("user", model_config["user_prompt"].format(
                user_prompt=user_prompt,
                code_executed=code_executed,
                result=pandasai_response
            ))
        ]
        assistant_response = llm.invoke(messages)  # Get response from the model
    return assistant_response.choices[0].message.content, code_executed
