import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from langchain.llms import OpenAI
from youtube_utils import *
from langchain_utils import *

load_dotenv()
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model_name='text-davinci-003', openai_api_key=OPENAI_API_KEY)

st.title('YouTube Top Video Summarization')

search_term = st.text_input("Enter a search term:")
num_weeks = st.number_input("Enter number of past weeks to search in:", min_value=1, value=3, step=1)
num_results = st.number_input("How many results do you want to see:", min_value=1, value=3, max_value=20, step=1)

if st.button('Search'):
    if search_term and num_weeks and num_results:

        videos = get_top_videos(search_term, num_weeks, num_results, DEVELOPER_KEY)

        st.write("Video info acquired")
        st.write("Generating summaries...")
        
        for video in videos:
            video_id = video['Id']
            transcript = get_transcript_from_video_id(video_id)

            if transcript is None:
                summary = 'No transcript available.'
            else:
                summary = get_summary_from_transcript(transcript, llm=llm)
            del video['Id']
            video['Summary'] = summary

        # Create a dataframe and show it in the app
        df = pd.DataFrame(videos)
        st.table(df)