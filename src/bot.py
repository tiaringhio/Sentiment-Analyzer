from functools import wraps
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters, ConversationHandler)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ChatAction)
import requests
import re
import pickle
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string
from statistics import mode
import logging
import time
import yaml
from live_classifier import (additional_stop_words, remove_noise, sentiment,
                             getSentiment, getPolarity, getConfidence)

# Importing token
with open('.\\token.yaml', 'r') as file:
    txt = yaml.load(file, Loader=yaml.FullLoader)
token = txt['telegram']['token']


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# Initaliz logger
logger = logging.getLogger(__name__)

# The states used by ConversationHandlers
PREDICTION, WORDCLOUD = range(2)

# Italian stopwords used for wordcloud oprations
stop_words = stopwords.words('italian')

# Italian Stemmer use for wordcloud operations
stemmer = SnowballStemmer('italian')


# Enables the 'typing...' animation in the Telagram header
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


# Enables the 'uploading photo...' animation in the Telagram header
def send_uploading_action(func):
    """Sends uploading photo action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO)
        return func(update, context,  *args, **kwargs)

    return command_func


# The initial state, it tells the user the bot is active
def start(update, context):
    update.message.reply_text(
        'Ehilà! Sono un bot che analizza i sentimenti!\n'
        'Se mi mandi un messaggio ti dirò se è negativo o positivo.\n'
        'Se vuoi mandare messaggi senza che il bot li analizza, '
        'metti la parola ignore a inizio messaggio.\n'
        'Per smettere di parlare premi /cancel.\n\n')

    return PREDICTION


# This function is on by default, it will output a prediction based on the user's message
# saying if the message is positive or negative, with which degree of certainty (there are four)
# and outputting the polarity, so the user can see the degreen of precision.
# The decorator is used to enable the typing animation
@send_typing_action
def predict(update, context):
    # Ignores the text if the message starts with this word
    if update.message.text.startswith('ignore'):
        return PREDICTION
    # Detects the /cancel command in both private chats and groups
    if update.message.text == '/cancel' or update.message.text == '/cancel@covid_sentiment_bot':
        return cancel(update, context)
    # Detects the /wordcloud command in both private chats and groups
    elif update.message.text == '/wordcloud' or update.message.text == '/wordcloud@covid_sentiment_bot':
        update.message.reply_text(
            'Mandami un messaggo bello lungo, è più divertente!\n')
        return wordcloud(update, context)
    # Detects the /start command in both private chats and groups
    elif update.message.text == '/start' or update.message.text == '/start@covid_sentiment_bot':
        update.message.reply_text(
            'Il bot è già attivo, mandami il messaggio da analizzare!')
        return PREDICTION
    # Detects the /predict command in both private chats and groups
    elif update.message.text == '/predict' or update.message.text == '/predict@covid_sentiment_bot':
        update.message.reply_text(
            'Il bot è già attivo, ti ascolto')
        return PREDICTION
    else:
        # Will send 'typing' action while processing the request.
        pass
        tweet = update.message.text
        # Sends the user message to the sentiment function
        result = sentiment(tweet)
        if(result != None):
            # Gets the prediction from the live_classifier
            prediction = getSentiment(result)
            # Gets polarity from the live_classifier
            polarity = getPolarity(result)
            pol_rounded = round(polarity, 3)
            # gets confidence from the live_classifier
            confidence = getConfidence(result)
            if(polarity > 0.25):
                emoji = '✅'
            elif polarity >= 0 and polarity < 0.25:
                emoji = '⚠'
            elif polarity < 0 and polarity >= -0.25:
                emoji = '⚠'
            else:
                emoji = '❌'
            # Sends the user the results
            update.message.reply_text('Fammi pensare...\n'
                                      'Il tuo input sembra essere {} {}!\n'
                                      '{}'
                                      'Questa è la polarità: {}, in caso volessi più precisione.'.format(
                                          prediction.upper(), emoji, confidence, pol_rounded))

    return PREDICTION


# This function will output a wordcloud using the message sent by the user, it gets activated
# with the /wordcloud command.
# The decorator is used to enable the uploading phot animation
@send_uploading_action
def wordcloud(update, context):
    # Ignores the text if the message starts with this word
    if update.message.text.startswith('ignore'):
        return WORDCLOUD
    # Detects the /cancel command in both private chats and groups
    if update.message.text == '/cancel' or update.message.text == '/cancel@covid_sentiment_bot':
        return cancel(update, context)
    # Detects the /start command in both private chats and groups
    elif update.message.text == '/start' or update.message.text == '/start@covid_sentiment_bot':
        update.message.reply_text(
            'Il bot è già attivo, mandami il messaggio da analizzare!\n'
            'In alternativa premi /predict per passare ad analizzare il testo')
        return WORDCLOUD
    # Detects the /wordcloud command in both private chats and groups
    elif update.message.text == '/wordcloud' or update.message.text == '/wordcloud@covid_sentiment_bot':
        update.message.reply_text(
            'Ti ascolto, manda pure!')
    # Detects the /predict command in both private chats and groups
    elif update.message.text == '/predict' or update.message.text == '/predict@covid_sentiment_bot':
        update.message.reply_text(
            'Mandami il messaggio da analizzare!')
        return PREDICTION
    else:
        # Will send 'uploading photo' action while processing the request.
        pass
        cid = str(update.message.chat_id)
        uid = int(update.message.from_user.id)
        text = update.message.text
        # Creates wordcloud based on user's message
        cloud = WordCloud(width=500, height=500, collocations=False,
                          stopwords=stop_words).generate(text)
        image = cloud.to_image()
        image.save('.\\Resources\\wc.png', 'PNG')
        # Sends the genarated image to the user
        context.bot.send_photo(cid, photo=open('.\\Resources\\wc.png', 'rb'), reply_to_message_id=update.message.message_id,
                               caption='Ecco la tua WordCloud %s' % (update.message.from_user.first_name))
    return WORDCLOUD


# Stops te bot from analyzing the messages
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Speriamo i nostri cammini si incrocino di nuovo!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


# Sends the user a message saying that the timeout has expired
def timeout(update, context):
    update.message.reply_text(
        'Vado a dormire, se hai ancora bisogno di me premi /start')
    return ConversationHandler.END


# Logs errors
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Logs errors
    logger.info("Starting bot")

    # Uses the bot token
    updater = Updater(token, use_context=True)

    # The dispatcher is use to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        conversation_timeout=60,
        states={
            PREDICTION: [MessageHandler(Filters.text, predict),
                         CommandHandler('predict', predict)],
            WORDCLOUD: [MessageHandler(Filters.text, wordcloud),
                        CommandHandler('wordcloud', wordcloud)],
            ConversationHandler.TIMEOUT: [
                MessageHandler(Filters.text, timeout)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # This is standard
    dispatcher.add_handler(conv_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # The bot will run until you stop it in the terminal by pressing ctrl + c
    # or after 5 minutes, via ConversationHandler.TIMEOUT (above), after which it
    # will send the user a message notifying of the state
    updater.idle()


if __name__ == '__main__':
    main()
