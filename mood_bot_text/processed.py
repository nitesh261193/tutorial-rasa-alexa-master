from collections import defaultdict
import text2emotion as te

emotion_effect = {"Surprise": "<amazon:emotion name =" + "'excited'" + " " + "intensity = " + "'high'" + "> text "
                                                                                                         "</amazon"
                                                                                                         ":emotion> ",
                  "Sad": "<amazon:emotion name =" + "'disappointed'" + " " + "intensity = " + "'high'" + "> text "
                                                                                                         "</amazon"
                                                                                                         ":emotion>",
                  "Happy": "<amazon:emotion name =" + "'excited'" + " " + "intensity = " + "'medium'" + "> text "
                                                                                                        "</amazon"
                                                                                                        ":emotion>",
                  "Fear": "<amazon:effect  name = " + "'whispered'" + "> text </amazon:effect>",
                  "Angry": "<voice name=" + "'Kendra'" + ">text</voice>",
                  }


def sentiment_for_each_sentence(response):
    emotion_with_word = defaultdict(list)
    emotion = te.get_emotion(response)
    max_key = max(emotion, key=emotion.get)
    print(max_key)
    for word in response.split(" "):
        word_emotion = te.get_emotion(word)
        max_key_word = max(word_emotion, key=word_emotion.get)
        if max_key == max_key_word:
            emotion_with_word[word] = max_key_word
            response = response.replace(word, word+" <break time="+"'1s'"+"/>")
    if max_key in emotion_effect.keys():
        response = "<speak>" + emotion_effect[max_key].replace("text", response) + "</speak>"
    return response

