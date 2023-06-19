import re


def main():
    txt = input("Text: ")

    l = letter_count(txt)
    # print(f"Letters: {l}")
    w = word_count(txt)
    # print(f"words: {w}")
    s = sentence_count(txt)
    # print(f"Sentences: {s}")

    # Calculates index using formula
    index = round(0.0588 * l / w * 100 - 0.296 * s / w * 100 - 15.8)

    # Prints grade
    if index > 0 and index < 17:
        print(f"Grade {index}")
    elif index <= 0:
        print("Before Grade 1")
    else:
        print("Grade 16+")


def letter_count(txt):
    letters = re.findall("[a-zA-Z]", txt)
    return len(letters)


def word_count(txt):
    words = re.split(" ", txt)
    return len(words)


def sentence_count(txt):
    sentences = re.split("[.?!]", txt)
    return len(sentences) - 1


if __name__ == "__main__":
    main()