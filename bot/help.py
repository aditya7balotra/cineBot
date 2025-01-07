from . import bot
from auth import auth, authData


@bot.message_handler(commands=['help', 'info'])
def send_welcome(message):
    '''
    Provide instructions or information to the user.
    '''
    # Sending typing... gesture
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Authentication
    status = auth(message.chat.id)
    if status:
        pass
    else:
        bot.send_message(message.chat.id, "You are not authenticated")
        return None
    
    # Handling the /help command
    if message.text == '/help':
        bot.send_message(
            message.chat.id, 
            '''
<i>🎬 Movie & Series Assistant Bot 🎥</i>

<i>This Telegram bot helps you find movies and web series directly from our database.</i>

<i><b>✨ Features:</b></i>
<i>1. 📂 <code><b>/send &lt;movie/series name&gt;</b></code>: Instantly get the movie or series if available.</i>
   <i>Example usage:</i>
   <i><b><code>/send Inception</code></b></i>
   <i><b><code>/send The Office</code></b></i>
<i>2. 🤖 <b><code>/help</code></b>: Get guidance on how to use the bot.</i>
<i>3. 💬 <b><code>/c &lt;text&gt;</code></b>: Chat with the bot powered by advanced AI (Gemini).</i>
<i>4. 📝 <b><code>/info</code></b>: Learn how to correctly format movie or series names when using <b><code>/send</code></b>.</i>
<i>5. 🤖 <b><code>/intention</code></b>: intention of this project.</i>
<i>6. 💡 Feel free to inform admin in case you encounter a bug or problem.</i>

<i>Made with &#10084;&#65039;</i>
            ''',
            parse_mode='HTML'
        )
    
    # Handling the /info command
    elif message.text == '/info':
        bot.send_message(
            message.chat.id,
            '''
<i><b>📝 Instructions for Using <code><b>/send</b></code> Command:</b></i>

<i>When sending a movie or series name with <code><b>/send</b></code>, please follow these guidelines:</i>

<i><b>1. Case does not matter:</b></i> 
   <i>You can write in lowercase or uppercase.</i>
   <i>Example:</i> 
   <i><b><code>/send inception</code></b></i>  
   <i><b><code>/send INCEPTION</code></b></i>  
   <i><b><code>/send InCePtIoN</code></b></i>  

<i><b>2. Spaces do not matter:</b></i> 
   <i>The number of spaces between words or letters does not matter.</i>
   <i>Example:</i> 
   <i><b><code>/send theoffice</code></b></i>  
   <i><b><code>/send the office</code></b></i>  
   <i><b><code>/send  the   office</code></b></i>  

<i><b>3. Avoid special signs:</b></i> 
   <i>Do not use special characters like :, ., ', "", @, etc.</i>
   <i>Example:</i> 
   <i>Instead of: <b><code>/send Harry Potter: The Sorcerer's Stone</code></b></i>  
   <i>Use: <b><code>/send Harry Potter The Sorcerers Stone</code></b></i>  

<i><b>4. Use base forms of special characters essential to the title:</b></i> 
   <i>Replace symbols like "&" with their word form "and".</i>
   <i>Example:</i> 
   <i>Instead of: <b><code>/send Fast & Furious</code></b></i>  
   <i>Use: <b><code>/send Fast and Furious</code></b></i>  

<i><b>5. Spellings matter:</b></i> 
   <i>Ensure the spelling of the movie or series name is accurate.</i>
   <i>Example:</i> 
   <i>Correct: <b><code>/send Breaking Bad</code></b></i>  
   <i>Incorrect: <b><code>/send Braking Bad</code></b></i>  

<i>Follow these instructions to ensure the bot can find the movie or series you’re searching for.</i>

<i>Happy exploring! 🎬</i>
            ''',
            parse_mode='HTML'
        )


@bot.message_handler(commands=['intention'])
def send_intention(message):
    '''
    Send the creator's intention and disclaimer for making this bot
    '''
    # sending typing... gesture
    bot.send_chat_action(message.chat.id, 'typing')
    # print(message)
    
    # authentication
    status = auth(message.chat.id)
    if status:
        pass
    else:
        bot.send_message(message.chat.id, "You are not authenticated")
        return None
    
    bot.send_message(
        message.chat.id, 
        '''
<b>📜 Disclaimer:</b>

This project, was created solely for personal learning and educational purposes. The creator does not endorse or encourage the use of this bot to access or distribute copyrighted material unlawfully.

<b>⚠️ Users are fully responsible for how they use this bot.</b> Any misuse of this project for infringing copyright laws is entirely at the user's own risk, and the creator will not be held liable for such actions.
        ''',
        parse_mode='HTML'
    )
