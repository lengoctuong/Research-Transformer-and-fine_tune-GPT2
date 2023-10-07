import streamlit as st
from transformers import pipeline
import re
from datetime import datetime
st.title('GPT-2')
# streamlit run c:\Users\MyPC\Downloads\HTK\webapp.py

if 'history' not in st.session_state:
    st.session_state['history'] = ''

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'max_length' not in st.session_state:
    st.session_state['max_length'] = 50

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
        time = message['time']
        if message['role'] == 'user':
            st.markdown(f'<div style="position: absolute; top: 100; right: 0;">{time}</div>', unsafe_allow_html = True)
        else:
            st.markdown(f'<div style="position: absolute; top: 100; right: 15px;">{time}</div>', unsafe_allow_html = True)

def RemoveSpecialCharacters(sequence, replacements):
    for char in replacements:
        if char in sequence:
            sequence = sequence.replace(char, '')
    return sequence

def ResetConversation():
    st.session_state['messages'] = []

seed = st.chat_input('Say something')

if seed:
    current_time = datetime.now().strftime("%H:%M")
    with st.chat_message('user'):
        st.markdown(seed)
        st.markdown(f'<div style="position: absolute; top: 100; right: 0;">{current_time}</div>', unsafe_allow_html = True)
    st.session_state['messages'].append({'role': 'user', 'content': seed, 'time': current_time})
    try:
        generator = pipeline("text-generation", model = "lengoctuong/gpt2-finetuned-wikitext2", max_length = st.session_state['max_length'])
        output = generator(seed)

        st.session_state['history'] += '[' + current_time + '] User: ' + seed + '\n\n'
        str_seq = output[0]['generated_text']
        str_seq = str_seq.strip()
        removes = [' @', '@ ', ' =', '= ']
        str_seq = RemoveSpecialCharacters(str_seq, removes)
        if re.search(r'^((.|\n)*[.?!]) [A-Z]+', str_seq) == None and str_seq[-1] not in ['.', '?', '!']:
            str_seq = str_seq + "."
        else:
            str_seq = re.search(r'^((.|\n)*[.?!]) [A-Z]+', str_seq).group(1)
        st.session_state['history'] += '[' + current_time + '] Bot: ' + str_seq + '\n\n'
        with st.chat_message('assistant'):
            st.markdown(str_seq)
            st.markdown(f'<div style="position: absolute; top: 100; right: 15px;">{current_time}</div>', unsafe_allow_html = True)
        st.session_state['messages'].append({'role': 'assistant', 'content': str_seq, 'time': current_time})

    except Exception as e:
        st.exception("Exception: %s\n" % e)

with st.sidebar:
    st.image("https://images.pexels.com/photos/861449/pexels-photo-861449.jpeg?auto=compress&cs=tinysrgb&w=1600")
    st.title('Options')
    st.session_state['max_length'] = st.slider('Choose generated sequence\'s maximum length', 30, 300, 50, step = 20)
    st.button('Clear chat', on_click = ResetConversation)
    current_date = datetime.now().strftime("%d%m%Y")
    st.download_button('Download chat history', st.session_state['history'], file_name = 'chat_history_' + current_date + '.txt')