# anki-fretboard-generator

Generate Anki flashcards for guitar/bass fretboard memorization.

Uses `pipenv`. Run `pipenv install` to install dependencies.

After that, run this for standard guitar tuning:

```bash
pipenv run python main.py --name="Guitar fretboard" --output-path=guitar.apkg --tuning=E,A,D,G,B,E --widths=3,2.5,2,1.5,1,1
```

Or for standard bass guitar tuning:

```bash
pipenv run python main.py --name="Bass fretboard" --output-path=bass.apkg --tuning=E,A,D,G --widths=4,3.5,3,2.5
```
