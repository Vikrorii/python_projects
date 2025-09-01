from customtkinter import *
import re
import random


#Змінна, коли виявлений бот
correct_response_counter = 0



#Функція для вирахування і виявлення ймовірності відповіді(response)
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):

    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty +=1
    #Рахує процент розпізнаних слів в повідомлені
    percentage = float(message_certainty)/float(len(recognised_words))


    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0




#Перевірка повідомлення, на знайомі слова, для спілкування
def check_all_messages(message):
    global correct_response_counter
    highest_prob_list = {}

    #Функція відповіді, яка має бути від бота, які мають бути слова від користувача
    def response(bot_responses, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[random.choice(bot_responses)] = message_probability(
            message, list_of_words, single_response, required_words
        )


#Response ____________________________________________________________________________________________
    response(["Як ви?","Як у вас справи?",], ["привіт!","привіт"], single_response=True)
    response(["Чудово, коли ви здасте проект?","Ясно, коли я побачу вашу роботу?","Зрозуміло, через скільки часу буде ваша робота?"], ["погано","добре","нормально","гірше","ок","у","мене", "чудово"])
    response(["Я вашу роботу не бачив з початку семестра, що ви робили?","Ви затягнули занадто сильно, що сталось?"], ["сьогодні", "завтра", "післязавтра","через тиждень"])
    response(["Який жах, ну добре, відповісте на моє питання, і ви можете на цей раз запобігти відрахуванню. Відповідайте чітко цифрою до 5, на питання:\nСкільки у вас хвостів по предмету?", "Ужас, ну добре, відповісте на моє питання, і ви можете на цей раз запобігти відрахуванню. Відповідайте чітко цифрою до 5 на питання:\n Скільки у вас хвостів по предмету?", "Дуже безвідповідально з вашого боку, ну добре, відповісте на моє питання, і ви можете на цей раз запобігти відрахуванню. Відповідайте чітко цифрою до 5 на питання:\n Скільки у вас хвостів по предмету?"], ["я", "пив", "випивав", "відпочивав", "забив", "працював", "гуляв", "нічого"])
    response(["Правильно,ви вільні, ідіть робіть проект далі.", "Вірно,можете йти.", "Хто б сумнівався, ви знаєте, добре, ви продовжуєте навчання"],["5"])
    response(["Я казав цифрою, не словами"], ["нуль", "один", "два", "три", "чотири", "п'ять"])
    response(["Ні.", "Ви пам'ятаєте мою фамілію?",
              "Невірно, на повторний курс."],
             ["4", "3", "2", "1"])
    response(["АХАХАХХАХАХАХАХАХАХАХХА", "Ахахахахахахахахахахах",
              "АХахаХАХАахахХАХах"],
             ["0"])

    response(R_EATING, ["я", "хочу", "їсти", "зголоднів","голодний"])



    best_match=max(highest_prob_list, key=highest_prob_list.get)


#Тест на бота
    if highest_prob_list.get(best_match, 0) > 0:  # Якщо відповідь правильна, збільшуємо лічильник
        correct_response_counter += 1
    return unknown() if highest_prob_list[best_match] < 1 else best_match


#Просто альтернативний спосіб написання, якщо відповідей бота занадто багато, їх можна відправити в інший файл
R_EATING = ["Пішли в їдальню", "Я б тоже сирник заточав", "Я чув, що недалеко тут шаурма є"]






#Функція виклику фраз, коли бот не розуміє користувача/виявляється ботом
def unknown():
    response = ["...(",
                "Напишіть інше питання",
                "Перепишіть повідомлення, будь ласка",
                "Я вас не розумію",
                "Напишіть щось інше"
                ][random.randrange(5)]
    return response




#Бере текст, і розділяє його на слова. Приймає рядок і повертає відповідь
def get_response(user_input):
    split_message=re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response= check_all_messages(split_message)
    return response




#Список слів для виходу з додатку
exit_words = [ "вихід","exit", "quit", "bye","допобачення","гарного дня","пішли"]





#Зміна параметра віджета(Змінює значення, коли бот виявляється)
def update_fail_counter():
    counter_label.configure(text=f"Лічильник НЕ виявлення бота: {correct_response_counter}")





#function for interface

def send_message():
    user_text=user_input.get().split()

    if any(word in exit_words for word in user_text):
        window.destroy()  # Закриваємо програму
        return

    if user_text:
        add_message(f"Ви: {user_input.get()}", sender="user")
        bot_response = get_response(user_input.get())
        add_message(f"Bot: {bot_response}", sender="bot")
        update_fail_counter()
        user_input.delete(0, END) #очищуємо строку від надісланого вже тексту





#Виводить текст в гарний інтерфейс
def add_message(text, sender="bot"):
    color = "lightblue" if sender == "bot" else "white"
    message_label = CTkLabel(chat_frame, text=text,text_color="black", wraplength=380, fg_color=color
                             ,corner_radius=10, padx=5, pady=5, justify="left", anchor="w", font=("Arial", 15))
    message_label.pack( pady=2, padx=5, fill=X)


    # Автопрокрутка вниз
    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1)







#Створення інтерфейсу додатку
window=CTk()
window.title("Комп'ютерний практикум 1")
set_appearance_mode("dark")
window.geometry("500x600")
window.resizable(False, False)



counter_label = CTkLabel(window, text=f"Лічильник НЕ виявлення бота: {correct_response_counter}", font=("Arial", 20))
counter_label.pack(pady=10)



#Інтерфейс чату
chat_frame=CTkScrollableFrame(window,fg_color="#526f80")
chat_frame.pack(padx=15, pady=10, fill=BOTH, expand=True)


#Підложка для СТРОКИ
input_frame = CTkFrame(window)
input_frame.pack(fill=X, padx=10, pady=10)


#Вводна строка
user_input = CTkEntry(input_frame, placeholder_text="Введіть ваше повідомлення...", width=330, height=40, font=("Arial", 15))
user_input.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)


#Кнопка
button = CTkButton(input_frame, text="Відправити",command=send_message, corner_radius=20, fg_color="#00a6ff", font=("Arial", 15), width=55, height=35)
button.pack(side=RIGHT, padx=5, pady=5)


add_message("Bot: Привіт!", sender="bot")

window.mainloop()
