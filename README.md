# audio-book-reader
Reads text files and outputs audio one sentence at a time. Saves progress. Runs in Linux terminal.
# installation instructions:
1. clone this repo and cd into it
2. create a venv and activate it
3. run `pip3 install -r requirements.txt`
4. install ffmpeg. On Debian based distros, run `sudo apt install ffmpeg`
# usage instructions:
1. activate the venv
2. cd to the cloned repo
3. run `python3 play_audio_book.py PATH_TO_BOOK_FILE [--line LINE_TO_START_FROM] [--speed SPEED_MULTIPLIER] [--seconds-between-lines SECONDS_BETWEEN_LINES] [--language LANGUAGE] [--accent ACCENT]`
4. you can safely skip a line with Control + z or exit with Control + c.
5. playback will resume from the last played line if you open the same book again with no line index specified.
# supported accents:
American\
Australian\
Brazilian\
Canadian\
English\
French\
Indian\
Ireland\
Mexican\
Nigerian\
Portueguese\
South African\
Spanish
# supported languages:
Afrikaans\
Amharic\
Arabic\
Bulgarian\
Bengali\
Bosnian\
Catalan\
Czech\
Welsh\
Danish\
German\
Greek\
English\
Spanish\
Estonian\
Basque\
Finnish\
French\
Galician\
Gujarati\
Hausa\
Hindi\
Croatian\
Hungarian\
Indonesian\
Icelandic\
Italian\
Hebrew\
Japanese\
Javanese\
Khmer\
Kannada\
Korean\
Latin\
Lithuanian\
Latvian\
Malayalam\
Marathi\
Malay\
Myanmar (Burmese)\
Nepali\
Dutch\
Norwegian\
Punjabi (Gurmukhi)\
Polish\
Portuguese (Brazil)\
Portuguese (Portugal)\
Romanian\
Russian\
Sinhala\
Slovak\
Albanian\
Serbian\
Sundanese\
Swedish\
Swahili\
Tamil\
Telugu\
Thai\
Filipino\
Turkish\
Ukrainian\
Urdu\
Vietnamese\
Cantonese\
Chinese (Simplified)\
Chinese (Mandarin/Taiwan)\
Chinese (Mandarin)
# Demo (make sure to unmute):
https://github.com/user-attachments/assets/e9889d74-ebc7-4e61-9bbd-a967626b8003


