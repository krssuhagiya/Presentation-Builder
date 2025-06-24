import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import streamlit as st
from langchain_core.prompts import load_prompt
import regex as re

# Load env variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize model
model = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"
)

# Page config
st.set_page_config(page_title="AI Presentation Generator", page_icon="📊", layout="centered")

# Header
st.markdown("<h1 style='text-align: center; color: #4F8BF9;'>🧠 AI Presentation Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate smart, structured slide breakdowns from any topic using LangChain + Groq</p>", unsafe_allow_html=True)
st.markdown("---")

# Input form
with st.container():
    st.subheader("🔧 Customize Your Presentation")
    topic_input = st.text_input("📘 Topic", placeholder="e.g., Smart Cities, Quantum Internet")
    style_input = st.text_input("🎯 Explanation Style", placeholder="e.g., Technical, Simple, With Analogies, etc.")
    length_input = st.text_input("📏 Slide Length", placeholder="e.g., 3 slides, brief overview")

# Button
if st.button("🚀 Generate Presentation", type="primary"):
    if not topic_input or not style_input or not length_input:
        st.warning("⚠️ Please fill in all the fields before generating.")
    else:
        # Determine audience type
        audience_type = "general audience"
        if "technical" in style_input.lower():
            audience_type = "working professionals or tech students"
        elif "code" in style_input.lower():
            audience_type = "developers or engineering students"
        elif "beginner" in style_input.lower() or "simple" in style_input.lower():
            audience_type = "school or college-level audience"
        elif "analogy" in style_input.lower():
            audience_type = "general audience"

        # Load prompt template
        presentation_prompt = load_prompt('day2/template.json')

        with st.spinner("🧠 Thinking... Generating your presentation..."):
            final_prompt = presentation_prompt.format(
                topic_input=topic_input,
                audience_type=audience_type,
                explanation_style=style_input,
                slide_length=length_input
            )

            response = model.invoke(final_prompt)
            cleaned_output = re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL)

            st.success("✅ Presentation generated successfully!")
            st.markdown("---")
            st.markdown("### 📊 Slide Breakdown")
            st.markdown(cleaned_output)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9em;'>Made with ❤️ using LangChain, Groq & Streamlit</p>", unsafe_allow_html=True)
