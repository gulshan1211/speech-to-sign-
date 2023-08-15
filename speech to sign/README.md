# A2SL-Translator
### Sign language is a way of communicating using hand gestures and movements, body language and facial expressions, instead of spoken words. This project describes a sign language translator for the deaf. 
![image](https://user-images.githubusercontent.com/76841315/162028693-7aa2e6af-3a7f-4f07-a088-e30628ec754b.png)




The interface works in phases,

1. First recognizes Audio input on the platform using Python Speech Recognition module.
2. Conversion of audio to text using Google Speech API.
3. Dependency parser for analysing grammatical structure of the sentence and establishing relationship between words.
4. ISL Generator: ISL of input sentence using ISL grammar rules.
5. Generation of Sign language with concating videos.

### Requirements:
1. streamlit==1.8.1
2. opencv-python==4.4.0.44
3. moviepy==1.0.3
4. numpy==1.21.5
5. SpeechRecognition==3.8.1
6. nltk==3.7
