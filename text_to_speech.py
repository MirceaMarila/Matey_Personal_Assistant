#import library
import pyttsx3
#engine setup
engine = pyttsx3.init()
#converting text to speech
engine.say("""Late at night, guards on the battlements of Denmark's Elsinore castle are met by Horatio, Prince Hamlet's friend from school. The guards describe a ghost they have seen that resembles Hamlet's father, the recently-deceased king. At that moment, the Ghost reappears, and the guards and Horatio decide to tell Hamlet.

Claudius, Hamlet's uncle, married Hamlet's recently-widowed mother, becoming the new King of Denmark. Hamlet continues to mourn for his father's death and laments his mother's lack of loyalty. When Hamlet hears of the Ghost from Horatio, he wants to see it for himself.

Elsewhere, the royal attendant Polonius says farewell to his son Laertes, who is departing for France. Laertes warns his sister, Ophelia, away from Hamlet and thinking too much of his attentions towards her. """)
engine.runAndWait()


# import pyttsx3
# engine = pyttsx3.init()
#
# """Setting Volumn"""
# #get current volumn level
# volume = engine.getProperty('volume')
# print (volume)
#
# #setting volumn
# engine.setProperty('volume',1)
# engine.say("""Late at night, guards on the battlements of Denmark's Elsinore castle are met by Horatio, Prince Hamlet's friend from school. The guards describe a ghost they have seen that resembles Hamlet's father, the recently-deceased king. At that moment, the Ghost reappears, and the guards and Horatio decide to tell Hamlet.
#
# Claudius, Hamlet's uncle, married Hamlet's recently-widowed mother, becoming the new King of Denmark. Hamlet continues to mourn for his father's death and laments his mother's lack of loyalty. When Hamlet hears of the Ghost from Horatio, he wants to see it for himself.
#
# Elsewhere, the royal attendant Polonius says farewell to his son Laertes, who is departing for France. Laertes warns his sister, Ophelia, away from Hamlet and thinking too much of his attentions towards her. """)
# engine.runAndWait()


