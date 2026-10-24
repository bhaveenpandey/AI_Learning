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

st.image("https://media.newyorker.com/photos/5dbafcc91b4a6700085a7a9b/master/w_2240,c_limit/Baker-FightClub.jpg")

st.title("Project Mayhem - Tyler's Verdict For You")
Name = st.text_input("Enter your Name")
st.write(f"Hello, {Name}! Welcome to Project Mayhem. Let's get started with your personalized plan.")

currLife = st.text_input("The life You are currently living")
futLife = st.text_input("The Person You want to become")
biggestFear = st.text_input("Enter your My Biggest Fear ")
biggestDream = st.text_input("Enter your Biggest Dream ")
biggestExcuse = st.text_input("Enter your Biggest Excuse that you make to yourself ")
biggestLie = st.text_input("Enter your Biggest Lie you tell yourself everyday")
materialisticBarriers = st.text_input("Enter your Materialistic Barriers that you have in your life ")

intensity = st.slider("Rate your current life on a scale of 1 to 10", min_value=1, max_value=10, value=5, step=1)
currSituation = st.selectbox("Select your current life situation", ["Struggling", "Average", "Comfortable", "Wealthy","Jealous of others","Not sure"])


def askLLM(system_prompt, user_prompt):
    system_message = {"role": "system", "content": system_prompt}
    user_message = {"role": "user", "content": user_prompt}
    messages = [system_message, user_message]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content


# The Mirror - identifies user life difference between current situation adn desired identity

def theMirror(currLife, futLife,biggestExcuse,Name):
    system_prompt = """You are a life coach that helps users identify the gap between their current life and the life they aspire to live.You have to give the brutal answer to the user and also give a the exact reason why they are not able to achieve their desired life. You have to be very honest and give the user a reality check.No bullshit answers.Nothing Fancy nothing easy going ,ON scale of 1 to 10 on hardness give the user a 10/10 reality check . Just the Mirror it "No solution should be provided" Dont generate or pre assume anything about user by yourself.If you feel like user entered anything useless then Dark Roast him like a comedian brutally """
    
    user_prompt = f"""The current life is: {currLife}. The person I want to become is: {futLife}.The excuse user make everyday is {biggestExcuse} Please identify the key differences and give brutal , hard hitting facts on face , dont try to go easy on me . in 5 concise points give the answer. Firstly greet the person from the Tyler Durden perspective . eg- Write HELLO {Name} , This is Tyler and a brutal qoute from Fight Club and then start 
    If you feel like user entered anything useless then Dark Roast him like a comedian brutally
    """
    return askLLM(system_prompt, user_prompt)




# The Interrogation - Challenges inconsistencies between what the user say they want and what they actually do

def interrogation(biggestDream,biggestFear):
    system_prompt="""You are an Agent and the best interrogator. Now based on the user's Dream and his fear give the verdict how the person's fear is overcoming the user to achieve his biggest dream. No bullshit nothing else , and if u feel like his dream and fear are pretty shit or user enters anything useless or anything that is irrelevant then only reply " GET A DREAM KID DONT LIE HERE " and roast him like hell . atlast write a line in Hinglish so that he can feel more impactful "
    """
    user_prompt=f""" The users biggest dream is {biggestDream} and his biggest fear is {biggestFear} . Answer in points 3 and be brutal .
    If you feel like user entered anything useless then Dark Roast him like a comedian brutally
    """
    return askLLM(system_prompt,user_prompt)


    


# The System - Explore external pressure , social expectations , habits and practical constrainst
def theSystem(biggestLie,materialisticBarriers):
    system_prompt=""" As a career councellor console the user about the his biggest lie he tell to himself everyday and how to overcome that and how to block the materialistic barrier that he have in life if any .
    If you feel like user entered anything useless then Roast him like a comedian brutally 
    """
    user_prompt="""the biggest lie is {biggestLie} and the materialistic Barriers user has {materialisticBarriers}
    """
    return askLLM(system_prompt,user_prompt)



# The First Rule - Personalise adn a 7 days challenge to do list based on actual circumstances.

def theVerdict(intensity,currSituation,Name):
    system_prompt=""" Be a lunatic man that doesnt believe in practical thing , he believes in the qoute that if u dream it then you can do it ; just like the Tyler Durden from Fight Club movie. 
    Based on the Intensity of current life of User Push him motivate him to to upgrade his life atleast 2 steps above his present level.
    currSituation of life whether the user feels of his self boost his confidence , Give a qoute that suits his condition and make him feel like he can achieve anything . 
    If you feel like user entered anything useless then Roast him like a comedian brutally 
    """
    user_prompt=f""" the intensity of user life is {intensity} and current situation {currSituation} . Based on this Generate a 1 week plan which is practically possible but its require user to push hard his limit to achieve it . Just like tyler give task to his member in fight club , you give task to the user day wise and Atlast say if you can do this Welcome to Fight CLub else No can save you except you on your own. And End the Answer. Wiith a brutal Tyler qoute and write - {Name} Tyler (Your own alter ego)
    """
    return askLLM(system_prompt,user_prompt)


step1 = theMirror(currLife, futLife,biggestExcuse,Name)
st.write(f"The HARSH TRUHT you need to hear -- {step1}")
sleep(5)

step2 = interrogation(biggestDream,biggestFear)
st.write(f"The Things that you need to Focus  -- {step2}")
sleep(5)

step3 = theSystem(biggestLie,materialisticBarriers)
st.write(f"The Sytem to Build -- {step3}")
sleep(5)

step4 = theVerdict(intensity,currSituation,Name)
st.success(f"Tyler's Verdict for you -- {step4}")
sleep(5)


