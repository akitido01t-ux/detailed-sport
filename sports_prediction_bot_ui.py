import streamlit as st
import datetime
from openai import OpenAI
from serpapi import GoogleSearch

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to perform Google search using SerpAPI
def search_google(query):
    search = GoogleSearch({
        "q": query,
        "api_key": st.secrets["SERPAPI_KEY"]
    })
    results = search.get_dict()
    return results.get("organic_results", [])

# Function to get a GPT-based answer from OpenAI
def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert sports analyst. Analyze the search results and provide insightful predictions based on real-time data."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("🌍 Global Sports Prediction Bot")
st.write("Ask about any upcoming match or event and get intelligent, data-backed predictions.")

user_query = st.text_input("Enter your sports prediction query:", "Who is likely to win the next El Clasico?")

if st.button("Analyze & Predict"):
    with st.spinner("Gathering data and analyzing predictions..."):
        today = datetime.date.today().isoformat()
        search_results = search_google(user_query + f" predictions {today}")

        # Extract snippets
        snippets = [res["snippet"] for res in search_results if "snippet" in res]
        combined_snippets = "\n".join(snippets[:10]) if snippets else "No relevant results found."

        # Build prompt for OpenAI
        prompt = f"Based on the following news and predictions:\n\n{combined_snippets}\n\nWhat is your expert analysis and most likely outcome?"

        # Get AI response
        analysis = get_openai_response(prompt)

        # Display result
        st.subheader("🔍 AI Analysis & Prediction:")
        st.write(analysis)