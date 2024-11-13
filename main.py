from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Define a dictionary to store songs and playlists
songs = {}
playlists = {}

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a song to save it. You can also create playlists.')

# Save song handler
def save_song(update: Update, context: CallbackContext) -> None:
    if update.message.audio:
        file_id = update.message.audio.file_id
        file_name = update.message.audio.file_name
        songs[file_name] = file_id
        update.message.reply_text(f'Saved song: {file_name}')
    else:
        update.message.reply_text('Please upload an audio file.')

# Create playlist handler
def create_playlist(update: Update, context: CallbackContext) -> None:
    playlist_name = ' '.join(context.args)
    if playlist_name:
        playlists[playlist_name] = []
        update.message.reply_text(f'Playlist {playlist_name} created.')
    else:
        update.message.reply_text('Please provide a name for the playlist.')

# Add song to playlist handler
def add_to_playlist(update: Update, context: CallbackContext) -> None:
    args = context.args
    if len(args) < 2:
        update.message.reply_text('Please provide the playlist name and song name.')
        return

    playlist_name = args[0]
    song_name = ' '.join(args[1:])

    if playlist_name in playlists and song_name in songs:
        playlists[playlist_name].append(song_name)
        update.message.reply_text(f'Added {song_name} to {playlist_name}.')
    else:
        update.message.reply_text('Playlist or song not found.')

# Play song handler
def play_song(update: Update, context: CallbackContext) -> None:
    song_name = ' '.join(context.args)
    if song_name in songs:
        file_id = songs[song_name]
        update.message.reply_audio(InputFile(file_id))
    else:
        update.message.reply_text('Song not found.')

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your bot token
    updater = Updater('YOUR_TOKEN_HERE')

    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_playlist", create_playlist))
    dispatcher.add_handler(CommandHandler("add_to_playlist", add_to_playlist))
    dispatcher.add_handler(CommandHandler("play_song", play_song))
    dispatcher.add_handler(MessageHandler(Filters.audio, save_song))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
