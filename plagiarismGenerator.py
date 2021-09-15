import random

basicText = open("text.txt", "r")
wordBank = open("randomWordBank.txt", "r")

newText1 = open("plagiarism1.txt", "a")  # created with the first function
newText2 = open("plagiarism2.txt", "a")  # created with the second function


###
# The new text represents p% of the randomly selected and mixed sentences from old text.
# The remaining (100-p)% are random sentences. All sentences are randomly mixed.
###
def fun1(basicFile, additionalWordsFile, resultFile, p):
    sentences = basicFile.read().split(".")
    sentences = sentences[:-1]
    sentences = [sentence.strip() for sentence in sentences]

    newSentences = additionalWordsFile.read().split(".")
    newSentences = newSentences[:-1]
    newSentences = [sentence.strip() for sentence in newSentences]

    result = []
    resultFile.truncate(0)

    length = len(sentences)

    # sentences from old text
    for i in range(0, int(length * p * 0.01)):
        s = random.choice(sentences)
        sentences.remove(s)
        result.append(s + ". ")

    # new sentences
    for i in range(0, int(length * (100 - p) * 0.01)):
        s = random.choice(newSentences)
        newSentences.remove(s)
        result.append(s + ". ")

    random.shuffle(result)

    for s in result:
        resultFile.write(s)


###
# The new text represents p% of the randomly selected and mixed words from old text.
# The remaining (100-p)% are random words. All words are randomly mixed.
###
def fun2(basicFile, additionalWordsFile, resultFile, p):
    sentences = basicFile.read().split(".")
    sentences = sentences[:-1]
    sentences = [sentence.strip() for sentence in sentences]
    w = [x.split(" ") for x in sentences]
    words = []
    for x in w:
        for y in x:
            words.append(y.lower())

    newSentences = additionalWordsFile.read().split(".")
    newSentences = newSentences[:-1]
    newSentences = [sentence.strip() for sentence in newSentences]
    w = [x.split(" ") for x in newSentences]
    newWords = []
    for x in w:
        for y in x:
            if y[-1] == ",":
                newWords.append(y[:-1].lower())
            else:
                newWords.append(y.lower())

    result = []
    resultFile.truncate(0)

    length = len(words)

    # words from old text
    for i in range(0, int(length * p * 0.01)):
        s = random.choice(words)
        words.remove(s)
        result.append(s)

    # new words
    for i in range(0, int(length * (100 - p) * 0.01)):
        s = random.choice(newWords)
        newWords.remove(s)
        result.append(s)

    random.shuffle(result)

    nextSentence = True
    point = False
    for s in result:
        if nextSentence:
            resultFile.write(s.title())
            nextSentence = False
        else:
            resultFile.write(s)

        q = random.random()
        if q < 0.15:
            resultFile.write(". ")
            nextSentence = True
            point = True
        elif q < 0.2:
            resultFile.write(", ")
            point = False
        else:
            resultFile.write(" ")
            point = False

    if not point:
        resultFile.write(".")


# fun1(basicText, wordBank, newText1, 70)
fun2(basicText, wordBank, newText2, 65)

basicText.close()
wordBank.close()
newText1.close()
newText2.close()
