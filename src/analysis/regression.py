



 ################################################################################################################
import pandas as pd
from bld.project_paths import project_paths_join as ppj
import seaborn as sns
import numpy as np
import xlsxwriter
import nltk
from openpyxl import load_workbook
import random
import pickle
from openpyxl import load_workbook
from datetime import datetime
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


# Set the file path
#filepath="C:/Users/laure/Desktop/RESEARCH/Media_Bias/code/training_2.xlsx"
# Load the excel file which was the output of the first file.
wb=load_workbook(ppj("OUT_DATA", "training.xlsx"))
sheet=wb.active
max_row=sheet.max_row

# Create a tuple containing for each article the words as an array and for each type of terrorism an indicator.
tuple = []
for row_id in range(2, max_row+1): 
    tuple.append(([x.strip() for x in str(sheet.cell(row=row_id, column=1).value).split(';')], str(sheet.cell(row=row_id, column=2).value), str(sheet.cell(row=row_id, column=3).value), str(sheet.cell(row=row_id, column=4).value), str(sheet.cell(row=row_id, column=5).value)))

# Randomise the order of the articles.
random.shuffle(tuple)

# Generate an array containing all words of all articles I classified.
all_words = []
for article in range(0, len(tuple)):
    for w in tuple[article][0]:
        all_words.append(w.lower())

# Generate a frequency distribution of those words i.e. count for each how often it occured.      
all_words = nltk.FreqDist(all_words)    
# Make a list with number of occurences for the words that occur most often up to 3000th most often.
word_features = list(all_words.keys())[:500]
    

def find_features(article_id):
    #Tell for each of the 3000 words that occur most often
    #whether it occurs in a given article or not.
    #Input: Id of an article.
    #Output: Dictionary containing as keys the 3000 words that occur most often in all articles. Values are boolean and indicate whether the given article contains the word or not (True/False)
    words = set(tuple[article_id][0])
    features = {}
    for w in word_features:
        features[w] = (w in words)        
    return features


        
# Generate a tuple consisting of a dictionary indicating which of the 3000 words
# that generally occur most often is contained in each article and one indicator
# for the kind of terrorism, for each kind of terrorism. 
feature_sets = []
for i in range(2, len(tuple)):
    feature_sets.append((find_features(i), str(sheet.cell(row=i, column=4).value)))

training_set = feature_sets[:int(len(feature_sets)/2)]
testing_set = feature_sets[int(len(feature_sets)/2):]

classifier = nltk.NaiveBayesClassifier.train(training_set)
#print("Original naive Bayes Algorithm Accuracy in percent:", (nltk.classify.accuracy(classifier, testing_set)*100))
#classifier.show_most_informative_features(10)




#filepath="C:/Users/laure/Desktop/RESEARCH/Media_Bias/code/full_sparse.xlsx"

# Load the training data.
wb=load_workbook(ppj("OUT_DATA", "all_articles.xlsx"))
sheet=wb.active
max_row=sheet.max_row


tuple = []
for row_id in range(2, max_row+1): 
    tuple.append(([x.strip() for x in str(sheet.cell(row=row_id, column=2).value).split(';')]))#, datetime.strptime(str(sheet.cell(row=row_id, column=1).value), '%Y/%m/%d')))

feature_sets = []
for i in range(0, int(len(tuple))):
    feature_sets.append((find_features(i)))


classifications_islam = classifier.classify_many(feature_sets)

#print(classifications_islam)


    
# Gte confidence for decision
#dist = classifier.prob_classify(feature_sets[200])
#list(dist.samples()) 
#dist.prob("non-islam") 



islam_year = 0
other_year = 0
year_old = 0
dict = {'year': [], "islam": []}
for row_id in range(0, max_row-4): 
    if (datetime.strptime(sheet.cell(row=row_id + 2, column=1).value, '%Y/%m/%d').year > year_old):
        year_old = datetime.strptime(sheet.cell(row=row_id + 2, column=1).value, '%Y/%m/%d').year
        dict["year"].append(year_old)
        dict["islam"].append(islam_year)      
        
    else: 
        if classifications_islam[row_id] == "islam":
            islam_year =islam_year + 1            
    
df = pd.DataFrame(data=dict)



# multiple line plot
plt.plot( 'year', 'islam', data=df, marker='', color='red', linewidth=2, linestyle='dashed', label="number of reports on islamist terrorist attacks")
#plt.plot( 'year', 'other', data=df, marker='', color='red', linewidth=2, linestyle='_ _', label="toto")
plt.legend()

plt.savefig(ppj("OUT_FIGURES", "line_chart.pdf"), delimiter=",")




