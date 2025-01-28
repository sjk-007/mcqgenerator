
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utilis import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain


# loading the json file
with open(r'D:\GenerativeAI\mcqgenerator\response.json','r') as file:
    RESPONSE_JSON = json.load(file)

# create title for the app
st.title("Educational MCQ Application ")

# create a form using a st.form
with st.form("user_inputs"):
    # file upload
    uploaded_file = st.file_uploader("upload a pdf or a txt file")

    #input fields
    mcq_count = st.number_input("No.of MCQs",min_value=3,max_value=50)

    # subject
    subject = st.text_input("Insert subject",max_chars=30)

    #quiz tone
    tone =st.text_input("Complexity level of the questions",max_chars=20,placeholder="Simple")

    # add button
    button = st.form_submit_button("Create MCQs")

    # check the button and check all feilds are working

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading....."):
            try:
                text = read_file(uploaded_file)
                # count tokens and the cost of api 
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                    # st.write(response)
                
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")# input token
                print(f"Completion Tokens:{cb.completion_tokens}") # output token
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #extract the quiz data from response
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            # display the review in the text box
                            st.text_area(label="Review",value=response['review'])
                        else:
                            st.error("Error in the table data")
                        
                else:
                    st.write(response)






