from Stock import Stock
import numpy as np

stock = Stock(input("Whats your ticker? \n"))
#dji = Stock("^DJI")
#stock.extend(dji)

from Config import Config
best = Config(stock)


print("Calculations finished ->\n\n")
print("Finishing Accuracy: {}".format(best.score))
print("Finishing Features: {}".format(len(best.indi)))
print("Finishing Neighbors: {}".format(best.neighbors))
print(len(best.features[0]))

data = []
prediction_data = []

for i in range(len(best.indi)):
  data.append(best.features[best.indi[i]])

#print(len(data))

for i in data:
  #print(len(i))
  try:
    prediction_data.append(i[len(data) - 1])
  except:
    prediction_data.append(i)

#print(len(prediction_data))
#print(prediction_data)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split as tts
import numpy as np

knn = KNeighborsClassifier(n_neighbors=best.neighbors)

knn.fit(np.transpose(data), best.y)

#print(prediction_data)

prediction = knn.predict(np.transpose(prediction_data).reshape(1, -1))
import sys 
from termcolor import colored, cprint 
   
if prediction == 1:
  print(colored("+2% by close", 'green', attrs=['reverse', 'blink']))
elif prediction == 0:
  print(colored("+0% by close", 'yellow', attrs=['reverse', 'blink']))
else:
  print(colored("-0% by close", 'red', attrs=['reverse', 'blink']))
