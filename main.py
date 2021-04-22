# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import streamlit as st
import speech_recognition as sr
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="App Audio Transcript",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",)


st.sidebar.subheader('🎵️Transcritor de áudio📜')
st.sidebar.write('App para transcrever pequenos trexos de áudios, '
                 'que podem variar entre **1 e 2 minutos** com o idoma Português - Brasil'
                 ' No momento apenas arquivos no formato **.WAV**')

st.sidebar.write('_______')
arquivo_exemplo = st.sidebar.button('Arquivo de exemplo')


def arquivo_audio_exemplo():
    with open('file_exemple/uma_lembraca.wav', "rb") as file:
        byte = file.read()
        b64 = base64.b64encode(byte).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="uma_lembraca.wav">Baixar arquivo de exemplo</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)


def file_audio():
    # Recebe o arquivo de texto do usuário
    uploaded_files = st.file_uploader("Selecione ou arraste seu arquivo: ", accept_multiple_files=True)
    if arquivo_exemplo:
        arquivo_audio_exemplo()
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.audio(bytes_data, format='audio/ogg')
            st.write('**Transcrição** ' + uploaded_file.name + '** iniciada...**')
            file_name = uploaded_file.name
            path_name = 'transcricao_' + file_name + '.txt'

            with st.spinner('Por favor aguarde...'):
                with open(file_name, "wb") as out:
                    out.write(bytes_data)

                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 300
                with sr.AudioFile(file_name) as source:
                    audio_transcript = recognizer.record(source)
                    transcripted = recognizer.recognize_google(audio_data=audio_transcript, language='pt-BR')
                    texto_lower_case = transcripted.lower()

                    with open(path_name, "w", encoding='utf-8') as file:
                        file.write(texto_lower_case)
                    download_file(path_name, texto_lower_case)


def download_file(file_name, transcripted):
    with open(file_name, "rb") as file:
        byte = file.read()
        b64 = base64.b64encode(byte).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Baixar Transcrição</a>'
        st.success('**Transcrição concluída!**')
        st.markdown(href, unsafe_allow_html=True)
        corpo_html(transcripted)

def corpo_html(txt_trasncrito):
    components.html(
        f"""
        <body> 
            <div vw class="enabled">
            <div vw-access-button class="active"></div>
            <div vw-plugin-wrapper>
              <div class="vw-plugin-top-wrapper"></div>
            </div>
            </div>
            <script src="https://vlibras.gov.br/app/vlibras-plugin.js"></script>
            <script>
                new window.VLibras.Widget('https://vlibras.gov.br/app');
            </script>
        </body>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
         integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
         integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
          crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
         integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
          crossorigin="anonymous"></script>
        <div id="accordion">
          <div class="card">
            <div class="card-header" id="headingOne">
              <h5 class="mb-0">
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne"
                 aria-expanded="true" aria-controls="collapseOne">
                Trascrição
                </button>
              </h5>
            </div>
            <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
              <div class="card-body">
                {txt_trasncrito}
              </div>
            </div>
          </div>
        </div>
        """,
        height=600,
    )


if __name__ == '__main__':
    file_audio()
