#  import pandas as pd
from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
from utils.helpers import DATA_simple_chat
import os
import streamlit as st
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
        return


def chat_completion(user_prompt: str):
    llm = ChatGroq(
        model_name="mixtral-8x7b-32768", api_key=os.getenv("GROQ_API_KEY")
    )
    df = SmartDataframe(
        DATA_simple_chat,
        config={"llm": llm, "response_parser": OutputParser},
        description="Dataframe containing mobility data in Spain."
        )
    return df.chat(user_prompt), df.last_code_executed


'''
print(df.chat("What is the average displacements?"))
print(f"Time taken: {time.time() - start_time} seconds")

sdf = SmartDataframe(
    connector, {"enable_cache": False},
    config={"llm": llm, "conversational": False,
    "response_parser": OutputParser}
)
'''
