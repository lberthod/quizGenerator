# based on this github : https://github.com/nicknochnack/Langchain-Crash-Course
# Bring in deps
import os 

import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
    
os.environ['OPENAI_API_KEY'] = st.secrets["auth"]

# App framework
st.set_page_config(
   page_title="quizForge",
   page_icon="🧊",
)

st.title('🔗💬 Quiz FORGE')

st.write('🔗💬 GÉNÉRATEUR DE QUIZ')
st.write("QuizForge est un outil d'IA conçu pour aider les enseignants à créer des questionnaires pertinents pour leurs cours.")
st.info("QuizForge demande les informations ci-dessous afin de générer le contenu le plus précis possible pour vous. Toutes les informations sont facultatives et contribuent à améliorer la précision de la sortie générée.")

st.title('Décrivez votre cours')
st.info("Dans cette zone de saisie, vous pouvez fournir des informations sur votre cours et votre matière pour aider QuizForge à générer un questionnaire précis pour vous.")
prompt_title = st.text_input('Thématique de cours') 



# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template = "En tant qu'expert en enseignement et en pédagogie, vous êtes chargé(e) de concevoir cinq questions à choix multiple pour évaluer la compréhension d'un sujet spécifique. Pour chaque question, veuillez fournir uniquement la question elle-même, sans les réponses ni les propositions de réponses. Voici la thématique : \n\n1. {topic}"

)

# Prompt templates
question_template = PromptTemplate(
    input_variables = ['list_question', 'number'], 
  template = "À partir de la liste de questions suivante : {list_question}, reprenez la question {number}, reformulez-la et proposez quatre réponses possibles. Indiquez laquelle parmi ces réponses est la correcte. Veuillez énumérer les réponses une par une, en sautant une ligne entre chacune, et fournir une explication détaillée pour la réponse correcte."

)


# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
listq_memory = ConversationBufferMemory(input_key='list_question', memory_key='list_question_history')

# Llms
llm = OpenAI(temperature=0.9, model_name="gpt-3.5-turbo-16k")
 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='list_question', memory=title_memory)
question_chain = LLMChain(llm=llm, prompt=question_template, verbose=True, output_key='question', memory=listq_memory)

# Show stuff to the screen if there's a prompt
if st.button('Générer les questions'):

    list_question = title_chain.run(prompt_title)
    st.info('Liste des questions : \n' +  list_question)
    number = 1
    question = question_chain.run(list_question=list_question, number=number )
    st.info('Question 1 : \n' +  question)

    number = 2
    question = question_chain.run(list_question=list_question, number=number )
    st.info('Question 2 : \n' +  question)

    number = 3
    question = question_chain.run(list_question=list_question, number=number )
    st.info('Question 3 : \n' +  question)

    number = 4
    question = question_chain.run(list_question=list_question, number=number )
    st.info('Question 4 : \n' +  question)

    number = 5
    question = question_chain.run(list_question=list_question, number=number )
    st.info('Question 5 : \n' +  question)
