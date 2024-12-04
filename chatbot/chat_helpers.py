# chatbot/chat_helpers.py
import json
import streamlit as st
from pandasai import Agent
from pandasai.responses.response_parser import ResponseParser
from pandasai.connectors import PandasConnector
from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI
import plotly.graph_objects as go
from pydantic import BaseModel, Field
from utils.helpers import load_dataset_chat

DATA_simple_chat = load_dataset_chat()


class ChitchatChecker(BaseModel):
    '''
    Class to check if the response is a chitchat message or a usecase message.
    '''
    is_chitchat: bool = Field(..., description="Indicates true if the response is a chitchat message. False if it is a usecase message related with a query about some dataframe.")


class OutputParser(ResponseParser):
    '''
    Class used to parse the output of the model and display it in the Streamlit app.
    '''
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
    '''
    Setup the client for the language model.
    Parameters:
        model (str): The name of the language model to use.
    Returns:
        llm (ChatOpenAI): The client for the language model.
    '''
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
            temperature=model_config['temperature'],
            max_tokens=model_config['max_tokens'],
            max_retries=2,
            api_key=api_keys['GROQ_API_KEY'],
        )

    return llm

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


@st.cache_resource
def setup_pandasai_agent(_llm):
    '''
    Setup the PandasAI agent for the chatbot for performing data analysis tasks.
    Parameters:
        _llm (ChatOpenAI): The client for the language model.
    Returns:
        agent (Agent): The PandasAI agent for the chatbot.
    '''
    #  DATA_simple_chat = load_dataset_chat()
    connector = PandasConnector(
        {"original_df": DATA_simple_chat},
        field_descriptions=field_descriptions
    )
    agent = Agent(
        connector,
        description="Act as a data analyst. You will have to perform queries about a dataframe containing daily mobility data between Spanish provinces. Every time I ask you a question related to plotting sothing, you should provide the code to visualize the answer using plotly as a plotly graphical object, import required libraries. Do not save images.",
        config={
            "llm": _llm,
            "response_parser": OutputParser,
            "enable_cache": False,
            "conversational": False,
            "custom_whitelisted_dependencies": ["plotly", "pydeck"]
        },
    )
    return agent


def chat_completion_usecase(user_prompt: str, model: str, llm=None):
    '''
    Chat completion function for the use case messages, when the user prompt is related to a query about the dataframe. It performs a query to the dataframe and returns the Natural language response from the model.
    Parameters:
        user_prompt (str): The user prompt to send to the model.
        model (str): The name of the language model to use.
        llm (Any): The client for the language model.
    Returns:
        assistant_response (str): The response from the model.
        code_executed (str): The code executed by the PandasAI agent.
        messages (list): The list of messages to send to the model.
    '''
    if llm is None:
        llm = setup_llm_client(model)
    df = setup_pandasai_agent(llm)
    # Perform the query to the dataframe. Result will be displayed in the app
    pandasai_response = df.chat(user_prompt)
    code_executed = df.last_code_executed

    # Obtain a Natural Language analysis of the query result
    messages = [
        {"role": "system", "content": model_config["system_prompt_2"]},
        {"role": "user", "content": model_config["user_prompt"].format(
            user_prompt=user_prompt,
            code_executed=code_executed,
            result=pandasai_response
        )}
    ]
    assistant_response = llm.invoke(messages).content  # Get response from the model
    messages.append({"role": "assistant", "content": assistant_response})
    return assistant_response, code_executed, messages


def chat_completion(user_prompt: str, model: str, messages=None):
    '''
    Main function of the RAG. It receives the user prompt and the model to use, performs a query to the dataframe if the user prompt follows the use case, and returns the response from the model.
    Parameters:
        user_prompt (str): The user prompt to send to the model.
        model (str): The name of the language model to use.
        messages (list): The list of messages in the conversation history.
    Returns:
        response (str): The response from the model.
        code_executed (str): The code executed by the PandasAI agent, if any.
    '''
    llm = setup_llm_client(model)
    structured_output = llm.with_structured_output(ChitchatChecker)
    if messages is None:
        messages = [
            {"role": "system", "content": model_config["system_prompt_0"]},
            {"role": "user", "content": user_prompt}
        ]
    # Boolean value to check if the response is a chitchat message or a usecase message
    prompt_type = structured_output.invoke(messages)

    # Debug print statements
    st.write(structured_output)
    st.write(type(structured_output.is_chitchat))
    if prompt_type.chitchat is False:
        st.write("entered in here!!")
        # Call the function to perform the query to the dataframe and get the NL response
        return chat_completion_usecase(user_prompt, model, llm)

    # If the response is a chitchat message, return the response from the model
    messages = [
        {"role": "system", "content": model_config["system_prompt_1"]},
        {"role": "user", "content": user_prompt}
    ]
    response = llm.invoke(messages)
    chitchat_response = response.content
    st.write(messages)
    return chitchat_response, None
