import json
import pandas as pd
import emoji

def contractions():
    with open('contractions.json') as f:
        contrac = json.load(f)
    return contrac

def replace_contraction(string):
    contractions_dict=contractions()
    string=string.lower()
    for s in string.split(' '):
        if s in contractions_dict.keys():
            string=string.replace(s,contractions_dict[s])
    return string

def abbreviations():
    with open('abbreviations.json') as f:
        abb= json.load(f)
    return abb

def replace_abbreviations(string):
    abbreviations_dict=abbreviations()
    string=string.lower()
    for s in string.split(' '):
        if s in abbreviations_dict.keys():
            string=string.replace(s,abbreviations_dict[s])
    return string

def remove_emoji(string):
    emoji_list=[c for c in string if c in emoji.EMOJI_DATA]
    for e in emoji_list:
        string=string.replace(e,'')
    return string

def replace_emoji(string):
    emoji_list=[c for c in string if c in emoji.EMOJI_DATA]
    df=pd.read_csv('emoji_emotion.csv')
    for e in emoji_list:
        if e in list(df['Emoji']):
            emotion=list(df[df['Emoji']==e]['Emotion'])[0]
            string=string.replace(e,' '+emotion+' ')
        else:
            string=string.replace(e,'')
    return string