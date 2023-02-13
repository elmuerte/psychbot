# PsychBot

Mastodon bot posting quotes from Psychonauts. The script to post quotes is quite simple, see `psychbot.py`. The actual complexity is in creating the quote database.

This script is repsonsible for the quotes posted at https://botsin.space/@psychonauts

## Generating the quote database

To generate the quote database from the game files (the PC release) you first need to use the the GNU "strings" utility on the localization files. From the directory `Psychonauts/WorkResource/Localization/English`

```
strings -eS *.lub > strings_en.txt
```

The generated file is fed to `extract-quotes.py` script, which will generate the `quotes.db` file that is used by `psychbot.py`.

```
./extract-quotes.py strings_en.txt
```

The strings command simply extracts all C-style strings from the compiled lua files.
This includes some garbage, but that will be filtered out by the `extract-quotes.py` script.

Every quote starts with a 9 character long identifier, followed by a single line of text.
The identifier looks like this: `ASBV005RA`.
The first 4 characters are a level, area, or cinematic identifier. Followed by 3 digit number. Which all are not really interesting.
The last 2 characters however are interesting. They identify the speaker, this is probably used to show a portrait next to the text.
There is no lookup table for the 2 character speaker ID to the full name, a lookup table for this was created in the `extract-quotes.py` script.
