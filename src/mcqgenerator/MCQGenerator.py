import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utilis import read_file,get_table_data
from src.mcqgenerator.logger import logging


#importing necessary packages packages from langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables with os.environ
key =os.getenv("openai_api_key")

llm = ChatOpenAI(openai_api_key = key,model_name ="gpt-4o-mini",temperature = 0.8)

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template = TEMPLATE
)

quiz_chain = LLMChain(llm=llm,prompt = quiz_generation_prompt,output_key = 'quiz',verbose = True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=['subject','quiz'],
    template = TEMPLATE2
)

quiz_review_chain = LLMChain(llm=llm,prompt =quiz_evaluation_prompt,output_key = 'review',verbose = True)



generate_evaluate_chain = SequentialChain(chains=[quiz_chain,quiz_review_chain],input_variables = ['text','number','subject','tone','response_json'],
                                          output_variables= ['quiz','review'],verbose = True)

