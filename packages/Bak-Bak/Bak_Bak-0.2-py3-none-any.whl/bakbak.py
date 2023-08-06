import win32com.client as wincl

def speak(str):
    from win32com.client import Dispatch
    n = 1
    speaker_number = n
    speak = wincl.Dispatch("SAPI.SpVoice")
    vcs = speak.GetVoices()
    SVSFlag = 11
    speak.SetVoice(vcs.Item(speaker_number))
    print(f"AI : {str}")
    speak.Speak(str)
