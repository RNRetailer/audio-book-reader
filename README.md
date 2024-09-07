# audio-book-reader
Reads text files and outputs audio one sentence at a time. Saves progress. Runs in Linux terminal.
# installation instructions:
1. clone this repo and cd into it
2. create a venv and activate it
3. run `pip3 install -r requirements.txt`
4. install mpg123. On Debian based distros, run `sudo apt install mpg123`
# usage instructions:
1. activate the venv
2. cd to the cloned repo
3. run `python3 play_audio_book.py PATH_TO_BOOK_FILE`
4. you can safely skip a line with Control + z or exit with Control + c.
5. playback will resume from the last played line if you open the same book again.
