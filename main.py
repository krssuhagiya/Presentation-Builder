import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import load_prompt
import regex as re

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    groq_api_key = groq_api_key,
    model_name = "llama3-8b-8192"
)
 

st.header("Presentation Tool")

topic_input = st.text_input("📘 Enter the Topic (e.g., Smart Cities, Quantum Internet, etc.)")

style_input = st.text_input("🎯 Enter Explanation Style (e.g., Technical, Simple, With Analogies, Code-Based, etc.)")

length_input = st.text_input("📏 Enter Slide Length Preference (e.g., 3 slides, brief overview, 5-7 slides, etc.)")


presentation_prompt = load_prompt('day2/template.json')
audience_type = "general audience"
if "technical" in style_input.lower():
    audience_type = "working professionals or tech students"
elif "code" in style_input.lower():
    audience_type = "developers or engineering students"
elif "beginner" in style_input.lower() or "simple" in style_input.lower():
    audience_type = "school or college-level audience"
elif "analogy" in style_input.lower():
    audience_type = "general audience"

if topic_input and style_input and length_input:
    st.subheader("📝 Your Selections")
    st.markdown(f"- **Topic:** {topic_input}")
    st.markdown(f"- **Explanation Style:** {style_input}")
    st.markdown(f"- **Explanation Length:** {length_input}")

    if st.button("🚀 Generate Presentation"):
        with st.spinner("Generating slide breakdown..."): 
            final_prompt = presentation_prompt.format(
                topic_input=topic_input,
                audience_type=audience_type,
                explanation_style=style_input,
                slide_length=length_input
            )

            print(final_prompt) 
            response = model.invoke(final_prompt)
            cleaned_output = re.sub(r"<think>.*?</think>","",response.content,flags=re.DOTALL)
 
            st.success("🎉 Presentation generated successfully!")
            st.markdown("---")
            st.markdown(cleaned_output)