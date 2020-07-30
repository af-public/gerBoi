"""
This is a silly script that is designed to help me practice german.

For now it only has one exercise that will later be refactored

Deutsch ist schwer, deshalb ich brauche hilfe!
"""

import pandas as pd
import numpy as np
from datetime import datetime
import click


def modal_sampler(num_records):
    """
    Dumb sampler - this grabs random rows from each of the datasets then makes a sentence out of them.
    """
    ## Read in data here:
    modal_verbs_df = pd.read_excel("modal_verbs.xlsx")
    nouns_df = pd.read_excel("goethe_a1.xlsx", sheet_name="noun")
    regular_verbs_df = pd.read_excel("goethe_a1.xlsx", sheet_name="verb")

    # check inputs
    if num_records > len(nouns_df):
        print("WARNING: Num records inputted is greater than max.")
        print("Value inputted: {}".format(num_records))
        print("New value: {}".format(len(nouns_df)))
        num_records = len(nouns_df)

    # article mapping
    artikel = {"m": "Der", "w": "Die", "n": "Das"}

    # Templates
    english_sentence_template = "The {SUBJECT} {MODAL} {VERB}"
    deutscher_satzvorlage = "{ARTIKEL} {SUBJECT} {MODAL} {VERB}"

    # Get your samples:
    working_nouns = nouns_df.sample(frac=num_records / len(nouns_df)).reset_index(drop=True)
    working_verbs = regular_verbs_df.sample(frac=num_records / len(regular_verbs_df), replace=True).reset_index(
        drop=True)
    working_modal = modal_verbs_df.sample(frac=num_records / len(modal_verbs_df), replace=True).reset_index(drop=True)

    sentences = []
    saetze = []

    for ii in range(num_records):
        de_a = artikel[working_nouns.loc[ii, "gender"]]
        de_s = working_nouns.loc[ii, "base"]
        de_m = working_modal.loc[ii, "er-sie-es"]
        de_v = working_verbs.loc[ii, "inf"]

        en_s = working_nouns.loc[ii, "english"]
        en_m = working_modal.loc[ii, "english"]
        if en_m == "like" or en_m == "want":
            en_m = en_m + "s to"

        en_v = working_verbs.loc[ii, "english"]

        satz = deutscher_satzvorlage.format(
            ARTIKEL=de_a,
            SUBJECT=de_s,
            MODAL=de_m,
            VERB=de_v
        )

        sentence = english_sentence_template.format(
            SUBJECT=en_s,
            MODAL=en_m,
            VERB=en_v
        )
        saetze.append(satz)
        sentences.append(sentence)

    return sentences, saetze


class beispiel():
    def __init__(self, frage, loesung):
        self.frage = frage
        self.loesung = loesung


@click.command()
@click.option("--count", default=10, help="Number of exercises")
@click.option("--gen", default=False, help="Generate new exercises")
@click.option("--fid", default="missed_last_time.csv", help="File ID")
def main(count, gen, fid):
    time_stamp = datetime.strftime(datetime.now(), "%d-%m-%y_%H:%M")
    exercise_fid = "modal_verbs_" + time_stamp + ".csv"

    if gen:
        en, de = modal_sampler(count)
        df = pd.DataFrame({
            "en":en,
            "de":de
        })

    else:
        df = pd.read_csv(fid)
        en = df["en"].values
        de = df["de"].values

    fragen = [beispiel(x[0], x[1]) for x in zip(en, de)]

    de_missed = []
    en_missed = []
    c = 0
    retry = "y"

    while retry == "y":
        print("\n**************************************")
        print("\nAlright gerBoi, let's do this!!\n")

        if len(fragen) == 0:
            print("\nWhy are you playing around gerBoi? Yer already a gerMAN!!")
            break

        for e in fragen:
            c+=1
            print("{} / {}".format(c, len(fragen)))
            input(e.frage)
            print(e.loesung)
            good = input("did you get it?")

            if good != "y":
                en_missed.append(e.frage)
                de_missed.append(e.loesung)

        print("missed last time:")
        [print(x) for x in de_missed]

        missed = pd.DataFrame({
                "en":en_missed,
                "de":de_missed
            })

        erfolg = np.round(100 * (c - len(missed)) / c, 2)
        print("\n{}% success!".format(erfolg))

        missed.to_csv("missed_last_time.csv")

        retry = input("\nTry again?")
        fragen = [beispiel(x[0], x[1]) for x in zip(en_missed, de_missed)]
        de_missed = []
        en_missed = []
        c = 0

    print("\n**************************************")
    if erfolg > 95.:
        print("\nGood work gerBoi, yer on yer way to being a GerMAN!")
    else:
        print("\nWe'll get 'em next time gerBoi, you'll be a GerMAN some day...")


if __name__ == "__main__":
    main()