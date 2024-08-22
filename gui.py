# Streamlit Interface (streamlit_app.py)

import streamlit as st

from squat_wise import SquatWise  # Import your SquatWise class


def main():
    model = init_model()
    st.title("SquatWise AI Assistant")

    st.write("""
    Welcome to the SquatWise AI Assistant! This AI is trained on Squat University content
    and can answer your questions about squatting, mobility, and related topics.
    """)

# Create a text input for the user's query
    user_query = st.text_input("Enter your question here:")

    if st.button("Ask SquatWise"):
        if user_query:
            st.session_state.query = user_query
            st.write(f"Query: {st.session_state.query}")
            st.markdown("---")
            #try:
            # Get the response from the model
            response = model.ask(user_query)
            
            # Display the response
            st.write("SquatWise says:")
            st.write(response)
            #except Exception as e:
            #    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question before clicking 'Ask SquatWise'.")

    st.markdown("---")
    st.write("Powered by Squat University content and AI technology.")

def init_model():
# Initialize the SquatWise model
    return SquatWise()

if __name__ == "__main__":
    st.session_state.query = ""
    main()

