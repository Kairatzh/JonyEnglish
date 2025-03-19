import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

questions = {
    "A0": [
        {
            "question": "I ___ John.",
            "options": ["am", "is", "are", "be"],
            "correct": "am"
        },
        {
            "question": "You ___ a student.",
            "options": ["am", "is", "are", "be"],
            "correct": "are"
        },
        {
            "question": "This ___ a cat.",
            "options": ["am", "is", "are", "be"],
            "correct": "is"
        },
        {
            "question": "He ___ my friend.",
            "options": ["am", "is", "are", "be"],
            "correct": "is"
        },
        {
            "question": "We ___ happy.",
            "options": ["am", "is", "are", "be"],
            "correct": "are"
        }
    ],
    "A1": [
        {
            "question": "What ___ your name?",
            "options": ["are", "is", "am", "be"],
            "correct": "is"
        },
        {
            "question": "She ___ TV every evening.",
            "options": ["watch", "watches", "watching", "is watch"],
            "correct": "watches"
        },
        {
            "question": "We ___ students.",
            "options": ["are", "is", "am", "be"],
            "correct": "are"
        },
        {
            "question": "They ___ from Spain.",
            "options": ["are", "is", "am", "be"],
            "correct": "are"
        },
        {
            "question": "___ you like coffee?",
            "options": ["Are", "Do", "Does", "Is"],
            "correct": "Do"
        }
    ],
    "A2": [
        {
            "question": "I ___ to the cinema last weekend.",
            "options": ["go", "went", "going", "goes"],
            "correct": "went"
        },
        {
            "question": "She ___ been to Paris.",
            "options": ["has", "have", "had", "is"],
            "correct": "has"
        },
        {
            "question": "I ___ play football tomorrow.",
            "options": ["will", "am", "going", "do"],
            "correct": "will"
        },
        {
            "question": "He's ___ than his brother.",
            "options": ["tall", "taller", "tallest", "more tall"],
            "correct": "taller"
        },
        {
            "question": "This is ___ interesting book.",
            "options": ["a", "an", "the", "—"],
            "correct": "an"
        }
    ],
    "B1": [
        {
            "question": "If I ___ rich, I would travel the world.",
            "options": ["am", "was", "were", "had been"],
            "correct": "were"
        },
        {
            "question": "By the time we arrived, the movie ___ started.",
            "options": ["has", "had", "was", "is"],
            "correct": "had"
        },
        {
            "question": "I'm not used to ___ in public.",
            "options": ["speak", "speaking", "spoke", "have spoken"],
            "correct": "speaking"
        },
        {
            "question": "The book ___ last year was very successful.",
            "options": ["published", "was published", "that published", "publishing"],
            "correct": "published"
        },
        {
            "question": "She suggested ___ for a walk.",
            "options": ["to go", "going", "go", "went"],
            "correct": "going"
        }
    ],
    "B2": [
        {
            "question": "The project ___ completed by next month.",
            "options": ["will be", "will have been", "is", "has been"],
            "correct": "will have been"
        },
        {
            "question": "I wish I ___ harder for the exam.",
            "options": ["studied", "would study", "had studied", "study"],
            "correct": "had studied"
        },
        {
            "question": "It's high time we ___ going.",
            "options": ["start", "started", "would start", "have started"],
            "correct": "started"
        },
        {
            "question": "No sooner ___ home than it started to rain.",
            "options": ["I had arrived", "had I arrived", "I arrived", "did I arrive"],
            "correct": "had I arrived"
        },
        {
            "question": "She's the kind of person ___ always helps others.",
            "options": ["who", "which", "whose", "whom"],
            "correct": "who"
        }
    ],
    "C1": [
        {
            "question": "Had I known about the problem, I ___ it earlier.",
            "options": ["would solve", "had solved", "would have solved", "solved"],
            "correct": "would have solved"
        },
        {
            "question": "Not only ___ the exam, but she also got the highest score.",
            "options": ["she passed", "did she pass", "she did pass", "passed she"],
            "correct": "did she pass"
        },
        {
            "question": "The government ___ to have misled the public.",
            "options": ["is alleged", "alleges", "is alleging", "alleged"],
            "correct": "is alleged"
        },
        {
            "question": "It's imperative that he ___ immediately.",
            "options": ["responds", "respond", "will respond", "would respond"],
            "correct": "respond"
        },
        {
            "question": "She ___ working there for ten years before she was promoted.",
            "options": ["has been", "had been", "was", "would have been"],
            "correct": "had been"
        }
    ],
    "C2": [
        {
            "question": "Seldom ___ such an impressive performance.",
            "options": ["I have seen", "have I seen", "I saw", "did I see"],
            "correct": "have I seen"
        },
        {
            "question": "The manuscript, along with the illustrations, ___ to the publisher yesterday.",
            "options": ["was sent", "were sent", "has been sent", "have been sent"],
            "correct": "was sent"
        },
        {
            "question": "Should you ___ any assistance, please do not hesitate to contact us.",
            "options": ["require", "requires", "required", "requiring"],
            "correct": "require"
        },
        {
            "question": "Only when thoroughly ___ did I realize its significance.",
            "options": ["examined the document", "examining the document", "did I examine the document",
                        "I examined the document"],
            "correct": "examining the document"
        },
        {
            "question": "He is one of those scientists who ___ dedicated to finding a cure.",
            "options": ["is", "are", "was", "were"],
            "correct": "are"
        }
    ]
}

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    user = update.effective_user
    await update.message.reply_text(
        f"Йо, {user.first_name}! ✌️ Меня зовут Jony, и я тут, чтобы проверить, насколько ты крут в английском! 🇬🇧🔥\n\n"
        "Я задам тебе несколько вопросов, и мы узнаем, где ты — абсолютный новичок (A0) или уже почти носитель (C2)! 😎\n"
        "Готов? Тогда жми /test и поехали! 🚀"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с помощью при команде /help."""
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Начать общение с ботом\n"
        "/test - Начать тест на определение уровня английского\n"
        "/help - Показать эту справку"
    )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начинает тест."""
    user_id = update.effective_user.id

    user_data[user_id] = {
        "current_level": "A0",
        "correct_answers": 0,
        "questions_asked": 0,
        "correct_per_level": {},
        "current_question_index": 0
    }

    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет вопрос пользователю."""
    user_id = update.effective_user.id

    if user_id not in user_data:
        await update.message.reply_text(
            "Для начала теста отправьте команду /test."
        )
        return

    current_level = user_data[user_id]["current_level"]
    current_question_index = user_data[user_id]["current_question_index"]

    if current_question_index >= len(questions[current_level]):
        correct_answers = user_data[user_id]["correct_answers"]
        user_data[user_id]["correct_per_level"][current_level] = correct_answers

        if correct_answers >= 3:
            next_level = get_next_level(current_level)
            if next_level:
                user_data[user_id]["current_level"] = next_level
                user_data[user_id]["correct_answers"] = 0
                user_data[user_id]["current_question_index"] = 0

                await update.effective_message.reply_text(
                    f"Вы успешно справились с уровнем {current_level}! Переходим к уровню {next_level}."
                )

                await send_question(update, context)
            else:
                await show_results(update, context)
        else:
            await show_results(update, context)
        return

    question_data = questions[current_level][current_question_index]
    question_text = f"Вопрос {current_question_index + 1}/{len(questions[current_level])} (Уровень {current_level}):\n\n{question_data['question']}"

    keyboard = []
    for option in question_data['options']:
        keyboard.append([InlineKeyboardButton(option, callback_data=f"answer_{option}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_message.reply_text(question_text, reply_markup=reply_markup)


def get_next_level(current_level):
    """Возвращает следующий уровень после текущего."""
    levels = ["A0","A1", "A2", "B1", "B2", "C1", "C2"]
    try:
        current_index = levels.index(current_level)
        if current_index < len(levels) - 1:
            return levels[current_index + 1]
    except ValueError:
        pass
    return None


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки с ответами."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_id not in user_data:
        await query.edit_message_text(
            text="Сессия истекла. Для начала нового теста отправьте команду /test."
        )
        return

    current_level = user_data[user_id]["current_level"]
    current_question_index = user_data[user_id]["current_question_index"]
    question_data = questions[current_level][current_question_index]

    user_answer = query.data.replace("answer_", "")
    correct_answer = question_data["correct"]

    if user_answer == correct_answer:
        user_data[user_id]["correct_answers"] += 1
        result_text = "✅ Правильно!"
    else:
        result_text = f"❌ Неправильно. Правильный ответ: {correct_answer}"

    await query.edit_message_text(
        text=f"{query.message.text}\n\n{result_text}"
    )

    user_data[user_id]["questions_asked"] += 1
    user_data[user_id]["current_question_index"] += 1

    await send_question(update, context)


async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает результаты теста."""
    user_id = update.effective_user.id

    if user_id not in user_data:
        await update.effective_message.reply_text(
            "У вас нет активных тестов. Для начала теста отправьте команду /test."
        )
        return

    correct_per_level = user_data[user_id]["correct_per_level"]
    user_level = "A0"

    levels = ["A0","A1", "A2", "B1", "B2", "C1", "C2"]
    for level in reversed(levels):
        if level in correct_per_level and correct_per_level[level] >= 3:
            user_level = level
            break

    level_descriptions = {
        "A0": "Нулевой уровень (Beginner)",
        "A1": "Начальный уровень (Elementary)",
        "A2": "Элементарный уровень (Pre-Intermediate)",
        "B1": "Средний уровень (Intermediate)",
        "B2": "Выше среднего (Upper-Intermediate)",
        "C1": "Продвинутый уровень (Advanced)",
        "C2": "Профессиональное владение (Proficiency)"
    }

    results_text = "📊 Результаты теста:\n\n"
    for level in levels:
        if level in correct_per_level:
            correct = correct_per_level[level]
            total = len(questions[level])
            percentage = (correct / total) * 100
            results_text += f"Уровень {level}: {correct}/{total} ({percentage:.1f}%)\n"

    results_text += f"\n🏆 Ваш уровень: {user_level} - {level_descriptions[user_level]}\n\n"

    recommendations = {
        "A0": "Бро, ну ты вообще с нуля! 😅 Не переживай, все с чего-то начинают. Главное — не сдаваться! Начни с базовых слов и простых фраз. А если хочешь легкие материалы и поддержку, залетай к нам: https://t.me/ENGFORCHAINIKIO",

        "A1": "Ну, ты уже не полный ноль, но работы еще много! 😆 Совет: подтяни грамматику (to be, present simple) и учи базовые слова. Крутые материалы и упражнения для старта ждут тебя здесь: https://t.me/ENGFORCHAINIKIO",

        "A2": "Отлично! Ты уже не чайник, но до уверенного уровня еще далеко. 📚 Совет: учи времена, расширяй словарный запас и пробуй читать простые тексты. Еще больше полезных штук — в нашем канале: https://t.me/ENGFORCHAINIKIO",

        "B1": "О, а ты уже неплох! 🚀 Теперь время работать над связной речью и письмом. Начни смотреть фильмы с субтитрами и побольше говори на английском. Лайфхаки, слова и разборы фильмов ждут тебя тут: https://t.me/ENGforCHAINIKI2",

        "B2": "Ты уже реально хорош! 💪 Теперь пора углубляться: учи идиомы, фразовые глаголы и развивай беглость речи. Прокачивай себя еще больше в нашем канале: https://t.me/ENGforCHAINIKI2",

        "C1": "Твой уровень уже впечатляет! 🔥 Если хочешь не просто учиться, а делиться знаниями, давай сотрудничать! Мы всегда открыты к новым авторам, преподавателям и просто энтузиастам. Напиши нам: https://t.me/Yul_ewq",

        "C2": "Ты уже мастер английского! 👑 Почему бы не передавать знания другим? Мы ищем людей, которые хотят создавать полезный контент, курсы и помогать другим учиться. Если интересно — пиши, обсудим сотрудничество: https://t.me/Yul_ewq"
    }

    results_text += recommendations[user_level]

    await update.effective_message.reply_text(results_text)

    # Очищаем данные пользователя
    del user_data[user_id]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает сообщения, которые не являются командами."""
    await update.message.reply_text(
        "Я понимаю только команды. Попробуйте /help для получения списка команд."
    )


def main() -> None:
    """Запускает бота."""
    # Создаем приложение и передаем ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", start_test))

    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Добавляем обработчик для остальных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()