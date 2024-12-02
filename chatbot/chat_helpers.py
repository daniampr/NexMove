# chatbot/chat_helpers.py
import json
import streamlit as st
from pandasai import Agent
from pandasai.responses.response_parser import ResponseParser
from pandasai.connectors import PandasConnector
from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI
import plotly.graph_objects as go
from utils.helpers import load_dataset_chat


class OutputParser(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def parse(self, result):
        if result['type'] == "dataframe":
            st.dataframe(result['value'])

        elif isinstance(result['value'], go.Figure):
            st.plotly_chart(result['value'])

        elif result['type'] == 'plot':
            st.image(result["value"])

        else:
            st.write(result['value'])
        return result['value']


# Load configuration from JSON and TOML files
with open("chatbot/config/assistant.json", "r") as f:
    model_config = json.load(f)

api_keys = st.secrets

field_descriptions = {
    "trips": "The total number of trips/displacements taken between the origin and destination provinces.",
    "origin_province_id": "The unique identifier for the origin province where the trip starts.",
    "origin_province_name": "The name of the origin province where the trip starts.",
    "destination_province_id": "The unique identifier for the destination province where the trip ends.",
    "destination_province_name": "The name of the destination province where the trip ends.",
    "day": "The specific date when the trip occurred, in YYYY-MM-DD format.",
    "day_of_week": "The day of the week when the trip occurred (e.g., Monday, Tuesday).",
    "origin_community": "The Spanin autonomic community which the origin province belongs.",
    "destination_community": "The Spanin autonomic community which the destination province belongs.",
    "distance": "The distance between the origin and destination provinces, measured in kilometers."
}


@st.cache_resource
def setup_llm_client(model: str):
    if 'gpt' in model:
        llm = ChatOpenAI(
            model=model,
            temperature=model_config['temperature'],
            max_tokens=model_config['max_tokens'],
            max_retries=2,
            api_key=api_keys['OPENAI_API_KEY'],
        )
    else:
        llm = ChatGroq(
            model=model,
            api_key=api_keys["GROQ_API_KEY"],
            temperature=model_config['temperature'],
            max_tokens=model_config['max_tokens']
        )
    DATA_simple_chat = load_dataset_chat()
    connector = PandasConnector(
        {"original_df": DATA_simple_chat},
        field_descriptions=field_descriptions
    )

    # df = SmartDataframe(
    #     connector,
    #     config={
    #         "llm": llm,
    #         "response_parser": OutputParser,
    #         "enable_cache": False,
    #         "conversational": False
    #     },
    #     description="Dataframe containing daily mobility data between Spanish provinces. If you are asked to plot something, use the plotly library to create it in case no module is specified."
    # )

    agent = Agent(
        connector,
        description="Act as a data analyst. You will have to perform queries about a dataframe containing daily mobility data between Spanish provinces. Every time I ask you a question related to plotting sothing, you should provide the code to visualize the answer using plotly as a plotly graphical object, import required libraries. Do not save images. If you are asked for somethings not related to performing a query, return None.",
        config={
            "llm": llm,
            "response_parser": OutputParser,
            "enable_cache": False,
            "conversational": False,
            "custom_whitelisted_dependencies": ["plotly", "pydeck"]
        },
    )
    return llm, agent


def chat_completion(user_prompt: str, model: str):
    llm, df = setup_llm_client(model)
    pandasai_response = df.chat(user_prompt)
    code_executed = df.last_code_executed
    messages = [
        {"role": "system", "content": model_config["system_prompt"]},
        {"role": "user", "content": model_config["user_prompt"].format(
            user_prompt=user_prompt,
            code_executed=code_executed,
            result=pandasai_response
        )}
    ]
    assistant_response = llm.invoke(messages)  # Get response from the model
    return assistant_response.content, code_executed
