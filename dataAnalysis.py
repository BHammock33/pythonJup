## Profital Apps Data analysis 
## Finding profitable apps from app store and google pay

import matplotlib.pyplot as plt
from csv import reader
openedFile = open('googleplaystore.csv', encoding='utf8')
readFile = reader(openedFile)
android = list(readFile)
androidHeader = android[0]
android = android[1:]

openedFile = open('AppleStore.csv', encoding='utf8')
readFile = reader(openedFile)
ios = list(readFile)
iosHeader = ios[0]
ios = ios[1:]

def explore_data(dataset, start, end, rowsAndColumns = False):
    dataSetSlice = dataset[start:end]
    for row in dataSetSlice:
        print(row)
        print('\n')
    if rowsAndColumns:
        print('Number of rows: ', len(dataset))
        print('Number of columns: ', len(dataset[0]))
        
        
def barplot(list_of_2_element_list):
    d = {ya[0]:ya[1] for ya in list_of_2_element_list}
    plt.figure(figsize=(9,15))
    axes = plt.axes()
    axes.get_xaxis().set_visible(False)

    spines = axes.spines
    spines['top'].set_visible(False)
    spines['right'].set_visible(False)
    spines['bottom'].set_visible(False)
    spines['left'].set_visible(False)
    ax = plt.barh(*zip(*d.items()), height=.5)
    plt.yticks(list(d.keys()), list(d.keys()))
    plt.xticks(range(4), range(4))
    rectangles = ax.patches
    for rectangle in rectangles:
        x_value = rectangle.get_width()
        y_value = rectangle.get_y() + rectangle.get_height() / 2
        space = 5
        ha = 'left'
        label = "{}".format(x_value)
        if x_value > 0:
            plt.annotate(
                label,
                (x_value, y_value),
                xytext=(space, 0),
                textcoords="offset points",
                va='center',
                ha=ha)

    axes.tick_params(tick1On=False)
    plt.show()
##explore_data(android, 1, 10, True)     
  
#print(android[10472])

#print(androidHeader)

#print(android[0])
#del android[10472]

#for app in android:
#    name = app[0]
#    if name == 'Instagram':
#        print(app)
del android[10472]

duplicateApps = []
uniqueApps = []
for app in android:
    name = app[0]
    if name in uniqueApps:
        duplicateApps.append(name)
    else:
        uniqueApps.append(name)
#print ('Number of duplicates: ', len(duplicateApps))
#print('number of uniques: ', len(uniqueApps))                

reviewsMax = {}
for app in android:
    name = app[0]
    nReviews = float(app[3])
    if name in reviewsMax and reviewsMax[name] < nReviews:
        reviewsMax[name] = nReviews
    elif name not in reviewsMax:
        reviewsMax[name] = nReviews
#print('expected:', len(android)-1181)
#print('actual', len(reviewsMax))        

androidClean = []
alreadyAdded = []
for app in android:
    name = app[0]
    nReviews = float(app[3])
    if(reviewsMax[name] == nReviews) and (name not in alreadyAdded):
        androidClean.append(app)
        alreadyAdded.append(name)
#explore_data(androidClean, 0, 3, True)        

def isEnglish(string):
    nonEnglish = 0
    for character in string:
        if ord(character) > 127:
            nonEnglish += 1
    if nonEnglish > 3:
        return False
    else:
        return True

AndroidEnglish = []
iosEnglish = []
for app in androidClean:
    name = app[0]
    if isEnglish(name):
        AndroidEnglish.append(app)
for app in ios:
    name = app[1]
    if isEnglish(name):
        iosEnglish.append(app)
        
#explore_data(AndroidEnglish, 0, 3, True)
#print('\n')
#explore_data(iosEnglish, 0, 3, True)     

androidFinal = []
iosFinal = []
for app in AndroidEnglish:
    price = app[7]
    if price == '0':
        androidFinal.append(app)
for app in iosEnglish:
    price = app[4]
    if price == '0.0':
        iosFinal.append(app)
#print(len(androidFinal))
#print(len(iosFinal))           

def freqTable(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    tablePercentages = {}
    for key in table:
        percentage = (table[key]/ total) * 100
        tablePercentages[key] = percentage
    return tablePercentages

def displayTable(dataset, index):
    table = freqTable(dataset, index)
    tableDisplay = []
    for key in table:
        keyTup = (table[key], key)
        tableDisplay.append(keyTup)
    tableSorted = sorted(tableDisplay, reverse= True)
    for entry in tableSorted:
        print(entry[1], ':', entry[0])


displayTable(iosFinal, -5)        
displayTable(androidFinal, 1)

genresIos = freqTable(iosFinal, -5)
for genre in genresIos:
    total = 0
    lenGenre = 0
    for app in iosFinal:
        genreApp = app[-5]
        if genreApp == genre:
            numRatings = float(app[5])
            total += numRatings
            lenGenre += 1
    avgRatings = total / lenGenre
    print(genre, avgRatings)
N = 20
data = genresIos
names = list(data.keys())
values = list(data.values())
plt.bar(range(len(data)), values, tick_label = names)
plt.gca().margins(x=0)
plt.gcf().canvas.draw()
tl = plt.gca().get_xticklabels()
maxsize = max([t.get_window_extent().width for t in tl])
m = .8
s = maxsize/plt.gcf().dpi*N+2*m
margin = m/plt.gcf().get_size_inches()[0]
plt.gcf().subplots_adjust(left=margin, right=1.-margin)
plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
plt.savefig('bar.png')

plt.show()
#barplot(genresIos)
