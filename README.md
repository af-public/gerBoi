gerBoi
---

An automated way of training to be a GerMAN.

---
Run me from the command line to see sentences in English that you then translate into German.

Zum Beispiel:
```angular2
python -m gerboi --count 10 --gen True
```
---
##How does this work?

gerBoi reads from content files that are in the repo and randomly draws samples to construct grammatically correct (if a little asinine) sentences in English and German. 

English sentences are printed to the console where you can translate into german (verbally).  gerBoi is very honorable, so he only uses the honor system to score you.  If you got the exercise correct, type `y`, otherwise type anything else.  You'll get a chance to retry on the exercises you missed.

The content files are `goethe_a1.xlsx` and `modal_verbs.xlsx` for now - feel free to edit or add your own so long as the column and sheet names remain the same.

---

## Options:
```angular2
--count - how many examples you want generated
--gen - do you want to generate new examples?
--fid - what is the file id to load in if you don't want to generate.
```
---
## Requirements:
```angular2
python >= 3.6
pandas
numpy
click
```
---
## Notes on bois / men
gerBoi is for guys, gals, and non-binary pals.  We heart everybody regardless of gender and love a good pun!