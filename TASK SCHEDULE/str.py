import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from time import sleep
import streamlit as st


load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")   


client = Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

st.title("AI Daily Planner")

# Tasks = """ Workout ; Research Paper study ; Ai Engineering Learn ; Youtube Video make 4 and each video take 1 hrs each ; talk to gf  
# """

# Schedule = """ I wake up at 730 hours ; and sleep around 2330 hours and running in morning  These things are non negotiable . Slots should be minimum 2 hrs and maximum 3 hrs for each task .Lunch at 1300 hours and followed by some rest . Bath 30 mins adjust in morning only.
# """

# Exercises = """ Running ; Stretching   """
Name = st.text_input("Enter your Name")
Tasks = st.text_input("Enter your Tasks")
Schedule = st.text_input("Enter your Schedule")
Exercises = st.text_input("Enter your Exercises")


def llmReply(systemPrompt, userPrompt):
    system_message = { "role": "system", "content": systemPrompt}
    user_message = { "role": "user", "content": userPrompt}
    messages = [system_message, user_message]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


def step1_taskAnalysis(Tasks):
    systemPrompt = """You are an AI assistant that helps users plan their daily tasks and schedule. You will be given a list of tasks now you have to arrange them in a logical order and also consider the time required for each task and also have some margin for extended task. Have priority list for study more and workout is non negotiatable . Just give the task name in list format nothing else """
    userPrompt = f"""Given the following tasks: {Tasks} give the task name in bullets points and nothing else """
    return llmReply(systemPrompt, userPrompt)


def step2_workoutPlanner(Exercises):
    systemPrompt = """You are an Gym coach or a fitness expert.Based on running for beginner provide me things"""
    userPrompt = f"""Given the following Exercises: {Exercises}  just give the exercise name in bullets points and nothing else  Format ; Monday : 1. exercise name ; 2. exercise name ; 3. exercise name ; thats it and if  it is tuesday then give tuesday and so on . Do not include any irrelevant information. If irrelevant information is given then reply with "I am sorry, I can only answer technical questions.progressive overload is important for genuine queries """
    return llmReply(systemPrompt, userPrompt)
    
def step3_schedulePlanner(Schedule,Tasks):
    systemPrompt = """You are an AI assistant that helps users plan their daily tasks in time blocking manners. You will be given a list of tasks now you have to arrange them in a logical order and also consider the time required for each task and also have some margin for extended task. Have priority list for study more and workout is non negotiatable"""
    userPrompt = f"""Given the following Schedule: {Schedule} Give it in time --> task {Tasks} wise manner only and firstly write date and day and then give the time and task in bullets points and nothing else. Give it in 24 hours format only. Do not include any irrelevant information.My Name is {Name} write at top """
    return llmReply(systemPrompt, userPrompt)


taskAnalysis = step1_taskAnalysis(Tasks)
# print("Task Analysis:", taskAnalysis)
st.write(f"Task Analysis: {taskAnalysis}")
sleep(5)  # Adding a delay to avoid hitting rate limits


ExercisePlan = step2_workoutPlanner(Exercises)
# print("Exercise Plan:", ExercisePlan)
st.write(f"Exercise Plan: {ExercisePlan}")
sleep(5)  # Adding a delay to avoid hitting rate limits


SchedulePlan = step3_schedulePlanner(Schedule,Tasks)
# print("Schedule Plan:", SchedulePlan)
st.success(f"Schedule Plan: {SchedulePlan}")

