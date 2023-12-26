from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot import TeleBot
from ugc.models import Profile
from ugc.models import Message

class DirectionBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.questions = [
            "",
            "1. Хотите объединить знания в области бизнеса и информационных технологий?",
            "2. Хотите стать востребованным юристом и защищать права и интересы людей?",
            "3. Хотите разобраться в социальных явлениях общества и исследовать его тенденции?",
            "4. Хотите разобраться в экономических процессах и принимать весомые управленческие решения?",
            "5. Вас интересует использование технологий для оптимизации бизнес-процессов и улучшения управления?",
            "6. Мечтаете о карьере в судебной системе или в адвокатуре?",
            "7. Интересуетесь вопросами социальной справедливости и равенства?",
            "8. Мечтаете о стабильном и перспективном профессиональном росте?",
            "9.  Хотите стать лидером и успешно управлять командой?",
            "10. Интересуетесь разработкой стратегий и оптимизацией бизнес-процессов?"
        ]
        self.current_question = 0

        self.directions = {
            'Бизнес-информатика': "Рекомендуем вам обратить внимание на направление Бизнес-информатика!",
            'Юриспруденция': "Рекомендуем вам обратить внимание на направление Юриспруденция!",
            'Социология': "Рекомендуем вам обратить внимание на направление Социология!",
            'Экономика': "Рекомендуем вам обратить внимание на направление Экономика!",
            'Менеджмент': "Рекомендуем вам обратить внимание на направление Менеджмент!"
        }

        self.user_responses = {}

    def restart(self, message):
        self.current_question = 0
        self.user_responses = {}
        self.start(message)

    def start(self, message):
        self.bot.send_message(message.chat.id, "Привет, я бот помогающий выбрать направление в вузе, ответь на пару вопросов и я помогу тебе, хочешь начать?")

    def ask_question(self, message):
        user_response = message.text.lower()
        if user_response == 'да' or user_response == 'нет':
            # Сохраняем ответ пользователя
            self.user_responses[self.current_question] = user_response

            self.current_question += 1

            if self.current_question < len(self.questions):
                self.bot.send_message(message.chat.id, self.questions[self.current_question])
            else:
                self.calculate_direction(message)
        else:
            self.bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def calculate_direction(self, message):
    # Подсчет количества ответов "Да" для каждого направления
        directions_count = {direction: 0 for direction in self.directions}

        for question_num, answer in self.user_responses.items():
            if answer == 'да':
                for direction, question_numbers in settings.DIRECTIONS_QUESTIONS.items():
                    if question_num in question_numbers:
                        directions_count[direction] += 1

    # Выбор направления с максимальным количеством ответов "Да"
        max_count = max(directions_count.values())
        global recommended_direction
        recommended_directions = [direction for direction, count in directions_count.items() if count == max_count]

        if len(recommended_directions) == 1:
            recommended_direction = recommended_directions[0]
            response_text = self.directions.get(recommended_direction)
            self.bot.send_message(message.chat.id, response_text)
        else:
            self.bot.send_message(message.chat.id, "Мы не можем подобрать направление для вас.")

        additional_question = "Хотели бы вы получать интересную информацию о поступлении в вуз?"
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.row('Да', 'Нет')
        self.bot.send_message(message.chat.id, additional_question, reply_markup=markup)   

    def handle_additional_question(self, message):
        user_response = message.text.lower()
        if user_response == 'да':
            self.bot.send_message(message.chat.id, "Отлично! Буду стараться радовать тебя информацией.")
            chat_id = message.chat.id
            p, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                defaults={'name': message.from_user.username}
            )
            Message(
                profile =p,
                text = recommended_direction,
                send = user_response,
            ).save()
            self.restart(message)
        elif user_response == 'нет':
            self.bot.send_message(message.chat.id, "Хорошо! Удачного поступления в вуз.")
            chat_id = message.chat.id
            p, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                defaults={'name': message.from_user.username}
            )
            Message(
                profile =p,
                text = recommended_direction,
                send = user_response,
            ).save()
            self.restart(message)
        else:
            self.bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_messages(message):
            if self.current_question < len(self.questions):
                self.ask_question(message)
            else:
                self.handle_additional_question(message)

        self.bot.polling()

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        bot = TeleBot(settings.TOKEN, threaded=False)
        direction_bot = DirectionBot(settings.TOKEN)
        direction_bot.run()