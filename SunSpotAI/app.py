import streamlit as st
import requests
import json

# App Title
st.set_page_config(page_title="SunWatch Finder", page_icon="🌅")
st.title("🌅 SunWatch Finder")
st.write("Find the best local spots to catch the first or last light of the day.")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("This app uses GPT-4o to find scenic locations.")

# User Input
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("Enter your City (e.g., San Francisco, Paris)", "")
with col2:
    category = st.radio("What are you looking for?", ["Sunrise", "Sunset"])

if st.button("Find Best Spots"):
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not city:
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Searching for the best {category} spots in {city}..."):
            try:
                # API Call Setup
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                prompt = (
                    f"List 3 to 5 specific, high-quality locations to watch the {category} in {city}. "
                    "For each place, provide the name, why it is good, and a brief tip (e.g., parking or best time to arrive). "
                    "Format the response as a clear list."
                )

                data = {
                    "model": "gpt-4o",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }

                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    
                    st.subheader(f"📍 Top {category} Spots in {city}")
                    st.markdown(result)
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Simple Footer
st.divider()
st.caption("Keep in mind that peak times change daily. Check your local weather app for exact timing!")