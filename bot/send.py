from . import bot, connection_pool
import time
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
from log import logging
from auth import auth, authData
from concurrent.futures import ThreadPoolExecutor


# these variables were used for testing purpose
# total_get = 0
# total_return = 0


# setting up the thread pool
threadsSend = ThreadPoolExecutor(max_workers= 8)
# getting the logger
sendLog = logging.getLogger('send')

def isMovie(name, cursor):
    '''
    Returns:
        1: if name is a movies in all_records table
        0: if name is a series in all_records table
        -1: if name is not in all_records table
    cursor: connection cursor
    '''
    
    def clean_name(name):
        chars_to_remove = [' ', ':', '-', '.', ',', '_', '"', "'", ';', '?']
        for char in chars_to_remove:
            name = name.replace(char, '')
        return name


    query = '''
    SELECT isMovie FROM all_records
    WHERE name = %s
    '''
    
    # print('enter movie')
    cursor.execute(query , (name, ))
    # print('movie exe')
    
    # execution result
    result = cursor.fetchone()
    sendLog.debug(f'data fetched from the all_records table for {name}')
    # print(result)
    if result != None:
        return result[0]
    
    else:
        return -1

def searchMovies(name, cursor):
    '''
    this function searches the movie in the database and returns the list of tuples containing movie data
    '''

    
    query = '''
        SELECT sno, quality FROM moviesdata 
        WHERE name = %s
        '''
    # print(name)
    # print('search movies reached')
    cursor.execute(query , (name , ))
    # print('search movies exe')
    
    # get the execution result
    result = cursor.fetchall()
    sendLog.debug(f'data fetched from moviesData table for {name}')

    return result
    

def searchSeries(name, cursor):
    '''
    this function will search the series in the seriesData table and return the list of tuples containing the data
    '''
    
    query = '''
        SELECT sno, season FROM seriesdata 
        WHERE name = %s
        '''
    # print('series reached')
    cursor.execute(query , (name , ))
    # print('series exe')
    
    # fetching query execution result
    result = cursor.fetchall()

    sendLog.debug('data fetched from seriesData table for {name}')
    
    return result


    
def send_movie_series(message , is_rcmd = False):
    '''
    this function will send the desired movie/series to the user
    is_rmcd: its for check. True means we are in this function for the recommendation purpose, False indicates we are here because of /send <movie_name> command from the user
    '''
    # print('entered')
    
    # sending typing... gester to the user
    bot.send_chat_action(message.chat.id , 'typing')
    
    
    
    if is_rcmd == False:
        # means not for the recommendation purpose
        name = message.text[6 : ] #fetch the movie/series name
        # print('got the name')
        # print(name)
      
    else:
        # here for the recommendation purpose
        name = is_rcmd.data.split(':>')[1]
    
    # get a connection
    # global total_get
    while True:
        try:
            # print('waiting for connection')
            connection = connection_pool.get_connection()
            # total_get += 1
            # print('total get: ', total_get)
            break
        
        except Exception as e:
            sendLog.exception('connection could not be made with sql server')
            time.sleep(5)
        # print('sleeping because connection could not be made with sql server')
        
    cursor = connection.cursor()

    result = isMovie(name, cursor)
    # print(result)
    if result == 1:
        
        # print('movies section')
        moviesResult = searchMovies(name, cursor)
        # print(moviesResult)
        moviesMarkup = InlineKeyboardMarkup(row_width= 2)
    
        buttonsText = []

        for data in moviesResult:
            # using :x@x: as separator in callbacks
            # callback_data fromat = movies/series :x@x: movieName :x@x: quality
            sno = data[0]
            buttonsText.append(InlineKeyboardButton(text = data[1], callback_data= f'movies:x@x:{sno}:x@x:{data[1]}'))
        
        # print(buttonsText)
        for i in range(0, len(moviesResult), 2):
            rowButtons = buttonsText[i: i+2]

            moviesMarkup.row(*rowButtons)
        # print(moviesMarkup)
        bot.reply_to(message , f'Select the desired quality for <strong><u>{name}</u></strong> ' , reply_markup = moviesMarkup , parse_mode = 'HTML')
        
        cursor.close()
        connection.close()

      
      
    elif result == 0:
        def sortR(data):
            return int(data[1])
        
        def clean(data):
            # this function is to ensure that seasons shown in the GUI are in proper descending order
            finalData = []
            seasonsGot = []
            for i, detum in enumerate(data):
                if detum[1] not in seasonsGot:
                    finalData.append(detum)
                    seasonsGot.append(detum[1])
            return finalData
        
        seriesResult = sorted(searchSeries(name, cursor), key= sortR)
 
        seriesResult = clean(seriesResult)

        
        # sending typing... gesture
        bot.send_chat_action(message.chat.id , 'typing')
        
        seriesMarkup = InlineKeyboardMarkup()
        
        button_seasons = []

        for data in seriesResult:
            # using separator :x@x:
            # season callbacks format: seriesSeason/seriesEpisode/seriesQuality :x@x: sno in seriesData table :x@x: season/episode/quality
            button_seasons.append(InlineKeyboardButton(text = f'{data[1]}', callback_data= f'seriesSeason:x@x:{data[0]}:x@x:{data[1]}'))
            
        
            
        for i in range(0, len(button_seasons), 2):
            rowButtons = button_seasons[i: i+2]
            seriesMarkup.row(*rowButtons)
                            
          
        bot.reply_to(message , f'Select the season for <strong><u>{name}</u></strong> ' , reply_markup = seriesMarkup , parse_mode = 'HTML')
        
        cursor.close()
        connection.close()
      
    else:
        if is_rcmd == False:
            # print(message)
            bot.reply_to(message , f'Not found , make sure that you enter the correct spelling @{message.from_user.username}')
        else:
            bot.reply_to(is_rcmd.message , f'Not uploaded by the channel @{message.chat.username}')
        cursor.close()
        connection.close()



@bot.message_handler(commands=['send'])
def thread_movie_series(message):
    '''
    this function will create a new thread to send the movie/series to the user, thus improving performance
    '''
    
    # authentification
    status = auth(message.chat.id)
    if status == True:
        pass
    elif status == False:
        bot.send_message(message.chat.id, 'You are not authorized to use this bot')
        return None
    
    threadsSend.submit(send_movie_series, message)