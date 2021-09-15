import matplotlib.pyplot as plt

text1 = open("text.txt", "r")
text2 = open("plagiarism2.txt", "r")

# text1 = open("plik1.txt", "r")
# text2 = open("plik2.txt", "r")

sentences1 = text1.read().split(".")
sentences1 = sentences1[:-1]
sentences1 = [sentence.strip().replace(",", "").lower() for sentence in sentences1]

sentences2 = text2.read().split(".")
sentences2 = sentences2[:-1]
sentences2 = [sentence.strip().replace(",", "").lower() for sentence in sentences2]

if len(sentences2) < len(sentences1):
    sentences1, sentences2 = sentences2, sentences1

w = [x.split(" ") for x in sentences1]
words1 = []
for x in w:
    for y in x:
        words1.append(y)

w = [x.split(" ") for x in sentences2]
words2 = []
for x in w:
    for y in x:
        words2.append(y)


# calculates Levenshtein distance between sentence1 and sentence 2
def distance(sentence1, sentence2):
    n, m = len(sentence1), len(sentence2)
    if n > m:
        sentence1, sentence2 = sentence2, sentence1
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if sentence1[j - 1] != sentence2[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


# calculates the similarity of sentences sentence1 and sentence2
def similtarity(sentence1, sentence2):
    w1 = sentence1.split(" ")
    w2 = sentence2.split(" ")

    if len(w2) < len(w1):
        w1, w2 = w2, w1

    p = []

    for word1 in w1:
        bestL = 0
        bestW = " "
        for word2 in w2:
            d = 1/(distance(word1, word2)+1)
            if d > bestL:
                bestL = d
                bestW = word2
        p.append(bestL)
        if bestW in words2:
            w2.remove(bestW)

    return sum(p)/len(p)


resultS = []
resultW = []

for s1 in sentences1:
    bestR = 0
    bestS = " "
    for s2 in sentences2:
        r = similtarity(s1, s2)
        if r > bestR:
            bestR = r
            bestS = s2
    resultS.append(bestR)
    if bestS in sentences2:
        sentences2.remove(bestS)

for w1 in words1:
    bestQ = 0
    bestW = " "
    for w2 in words2:
        q = 1/(distance(w1, w2)+1)
        if q > bestQ:
            bestQ = q
            bestW = w2
    resultW.append(bestQ)
    if bestW in words2:
        words2.remove(bestW)


resultS = [100*percent for percent in resultS]
resultW = [100*percent for percent in resultW]

fig, axs = plt.subplots(2)
axs[0].hist(resultS, 100, facecolor='orange', alpha=0.5)
axs[1].hist(resultW, 100, facecolor='green', alpha=0.5)
axs[0].set_title('Sentence matching')
axs[1].set_title('Word matching')
axs[0].set(xlabel='Similarity(%)', ylabel='Number of sentences')
axs[1].set(xlabel='Similarity(%)', ylabel='Number of words')
fig.tight_layout(pad=1.0)
plt.show()

resultS10 = [round(r/10, 0) for r in resultS]
resultW10 = [round(r/10, 0) for r in resultW]

labelsS = []
labelsW = []
explodeS = []
explodeW = []
colorsS = []
colorsW = []

pieS = []
pieW = []


for i in range(0, 11):
    c = resultS10.count(i)
    if c > 0:
        labelsS.append(str(10*i)+"%")
        pieS.append(c)
        explodeS.append(0.2)
        colorsS.append('orange')
    c = resultW10.count(i)
    if c > 0:
        labelsW.append(str(10 * i) + "%")
        pieW.append(c)
        explodeW.append(0.2)
        colorsW.append('orange')

plt.pie(pieS, labels=labelsS, explode=explodeS, colors=colorsS, autopct='%1.1f%%', startangle=90)
plt.title('Sentence matching', pad=25)
plt.show()

plt.pie(pieW, labels=labelsW, explode=explodeW, colors=colorsW, autopct='%1.1f%%', startangle=90)
plt.title('Word matching', pad=25)
plt.show()

print("Words: ", len(words1))
print("Average sentence similarity: ", round(sum(resultS)/len(resultS), 2), "%")
print("Average word similarity: ", round(sum(resultW)/len(resultW), 2), "%")
