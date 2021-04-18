# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import speech_recognition as sr
import base64


st.set_page_config(
    page_title="App Audio Transcript",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",)
st.header('App para realizar a Transcrição de arquivos de Audio para textos. ')
st.text('Somente arquivos de audio no formato .WAV com no máximo 1m:30s do idioma PT-BR')


def file_audio():
    # Recebe o arquivo de texto do usuário
    uploaded_files = st.sidebar.file_uploader("Selecione ou arraste seu arquivo: ", accept_multiple_files=True)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.audio(bytes_data, format='audio/ogg')
            st.write('**Transcrição** ' + uploaded_file.name + '** iniciada...**')
            file_name = uploaded_file.name
            path = 'transcricao_' + file_name + '.txt'

            with st.spinner('Por favor aguarde...'):
                with open(file_name, "wb") as out:
                    out.write(bytes_data)

                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 300
                with sr.AudioFile(file_name) as source:
                    audio_transcript = recognizer.record(source)
                    transcripted = recognizer.recognize_google(audio_data=audio_transcript, language='pt-BR')
                    transcript(transcripted)
                    st.success('**Transcrição concluída!**')

                    with open(path, "w", encoding='utf-8') as file:
                        file.write(transcripted)
                    download_file(path)


def download_file(file_name):
    with open(file_name, "rb") as file:
        byte = file.read()
        b64 = base64.b64encode(byte).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Baixar Transcrição</a>'
        st.markdown(href, unsafe_allow_html=True)


def transcript(transcripts):
    lowercase = transcripts.lower()
    st.write("**Resultado: **", lowercase)


if __name__ == '__main__':
    file_audio()
