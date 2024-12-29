import streamlit as st
import chatbot
import re

if 'buttonState' not in st.session_state:
    st.session_state.buttonState = False

if 'summary' not in st.session_state:
    st.session_state.summary = ''

st.title("Youtube Video Summarizer")
if not st.session_state.summary:
    if youtube_link := st.text_input("Enter the youtube video link: ",):
        regex = r"(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^\"&?/\s]{11})"
        if not re.match(regex, youtube_link):
            st.error("Please enter a valid youtube link")
            st.stop()
        else:
            match = re.search(regex,youtube_link)
            video_id = match.group(1)

def onClick():
    summary = chatbot.extract_transcript_details(video_id) if video_id else None
    st.session_state.summary = summary
    st.session_state.buttonState = summary is not None

if st.session_state.buttonState:
    st.markdown("### Summary:")
    st.write(st.session_state.summary)

else:
    st.button("Summarize", on_click=onClick)
 
if st.session_state.buttonState:
    if prompt := st.chat_input("Say something"):
        chat = chatbot.start_conversation(prompt)
        for messages in chat[2:]:
            with st.chat_message( "user" if messages.role == "user" else "assistant"):
                st.write(messages.parts[0].text)

