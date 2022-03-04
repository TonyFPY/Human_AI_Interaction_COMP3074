
from question_ansering import answer_Q
from name_management import name_change
from name_management import check_name_change
from name_management import name_response
from small_talk import talk_response
from util import time_response
from util import emotion
from util import correct

#######################################################################################
########## PLEASE REMOVE THE COMMENT IF THE LIBRARIES ARE ALREADY DOWNLOADED ##########
#######################################################################################
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
       
if __name__ == "__main__":

    user_name = '(Unknown)'

    flag = True
    print(">> Jarvis: I'm Jarvis. Yeah, you heard me right. I am working with Tony Stark.")
    print("           Please Enter 'bye' if you want to say good bye.")
    print("           May I have ur name? %s" %emotion())
    print('>> %s: ' %user_name, end=" ")
    user_input = input()
    if user_input == 'bye':
        flag = False
    else:
        user_name = name_change(user_input)
        if user_name.lower() == 'tony stark':
            print(">> Jarvis: Oh, u r my boss! I love u three thousand! %s" %emotion())
        else:
            print(">> Jarvis: Hi, %s, glad to know u! %s" %(user_name, emotion()))

    while(flag == True):
        print('>> %s: '%user_name, end=" ")
        user_input = input()
        # user_input = user_input.lower()
        user_input = [correct(i) for i in user_input.split(' ')]
        user_input = (' ').join(user_input)
        if(user_input != 'bye'):

            # name management
            response = name_response(user_input, threshold = 0.9)
            if response != 'NOT FOUND':
                print(">> Jarvis: I have a good memory. YOU ARE %s %s" %(user_name,emotion()))
                continue

            if check_name_change(user_input):
                user_name = name_change(user_input)
                print(">> Jarvis: Hi, %s! %s" %(user_name, emotion()))
                continue
            
            # time and data -- a part of the small talk
            if 'time' in user_input:
                time_response('time')
                continue

            if  'today' in user_input:
                time_response('today')
                continue

            # small talk
            response = talk_response(user_input, threshold = 0.9)
            if response != 'NOT FOUND':
                print(">> Jarvis: " + response + ' ' + emotion())
                continue

            # Question Answering
            response = answer_Q(user_input, threshold = 0.1)
            if response != 'NOT FOUND':
                print(">> Jarvis: " + response + ' ' + emotion())
            else:
                print(">> Jarvis: I'm sorry. I don't know. STACK OVERFLOW %s"%emotion())

        else:
            flag = False
    print(">> Jarvis: Bye! Take care..")
