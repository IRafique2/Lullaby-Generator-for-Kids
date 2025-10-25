from pypdf import PdfReader
import pandas as pd
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain 
from langchain.chains import SequentialChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

#import model
model = OllamaLLM(model="gemma3:1b", temperature=0.7)

from langchain.prompts import PromptTemplate

def generate_lullaby(name, location, language):
    template = """
        As a children's book writer, please come up with a simple and short lullaby based on
        the location {location} and the main character {name}.

        STORY:

    """
    prompt_template = PromptTemplate(
        input_variables=["location", "name"],
        template=template
    )

    chain_story = LLMChain(llm=model, prompt=prompt_template,output_key="story")

    template_update="""


    Translate the {story} into {language}. Make sure

    the Language is simple and fun.

    TRANSLATION:

    """


    prompt_translate=PromptTemplate(
        input_variables=["story", "language"],
        template=template_update
    )

    chain_translate=LLMChain(llm=model, prompt=prompt_translate, output_key="translation")

    overall_chain=SequentialChain(
        chains=[chain_story, chain_translate],
        input_variables=["location", "name", "language"],
        output_variables=["story", "translation"],
        verbose=True)

    response=overall_chain.invoke({"location":location,
                                "name":name,
                                "language":language})
    return response

def main():
    st.set_page_config(page_title="Lullaby Generator", page_icon=":books:", layout="centered")
    st.title("Lullaby Generator for Kids :books:")
    st.header("Create personalized lullabies for your little ones!")
    
    # Inputs for location, main character name, and language
    location_input = st.text_input(label="Where is the story set?")
    main_character_input = st.text_input(label="What's the main character's name?")
    language_input = st.text_input(label="Translate the story into (language)")

    submit_button = st.button("Submit")

    if location_input and main_character_input and language_input:
        if submit_button:
            with st.spinner("Generating lullaby..."):
                response = generate_lullaby(
                    location=location_input,
                    name=main_character_input,
                    language=language_input
                )

            # Show the generated lullaby story and translation in respective sections
            st.success("Lullaby Successfully Generated!")

            with st.expander("English Version"):
                st.write(response['story'])

            with st.expander(f"{language_input} Version"):
                st.write(response['translation'])

# Run the main function
if __name__ == "__main__":
    main()