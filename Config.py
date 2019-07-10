class Config:
  def __init__(self, stock):

    #Transferring the data from the stock to the config file
    self.name = stock.name
    self.features = stock.features
    self.y = stock.y
    self.score = 0
    self.neighbors = 0
    
    self.counter = 0
    self.shuffles = 3
    self.threshold = 80
    self.best_features = []

    self.indi = []
    self.recurse(self.features)


  #These 3 functions remove the [0], [1], [2] index respectively and returns the new list
  def rLeft(self, info):
    return info[1:]
  
  def rMid(self, info):
    a = []
    a.extend(info[0])
    a.extend(info[2:])
    return a
  def rRight(self, info):
    a = []
    a.extend(info[0:2])
    a.extend(info[3:])
    return a

  #Basic KNN Prediction - where if the data (features) don't exist, the function exits.
  
  def predict(self, data, answers):
    (print(f"Best Score: {self.score} - Iteration: {self.counter}", end="\r"))
    indexing_data = data
    self.counter += 1
    #print(self.counter)

    #print("Making a prediction")

    import copy
    cpy = copy.copy(data)

    
    if self.threshold >= self.score:
      #print("Threshold " + str(self.threshold) + " : Score " + str(self.score))

      """
      if self.counter >= 1000 and self.shuffles != 0:
        self.shuffles -= 1
        self.counter = 0
        data = self.shuffle(data)
        print("Shuffle!")
      """

      if self.score >= self.threshold:
        print("HIJANGA")

      else:
        for i in range(1, 20):
          self.counter += 1
          #print(self.counter)

          from sklearn.neighbors import KNeighborsClassifier
          from sklearn.model_selection import train_test_split as tts

          import numpy as np
          knn = KNeighborsClassifier(n_neighbors=i)
          xTrain, xTest, yTrain, yTest = tts(np.array(data).T, answers)
          knn.fit(xTrain, yTrain)
          
          score = round(knn.score(xTest, yTest) * 100, 2)

          #print("Attempt Score {}".format(score))
          if score >= self.score:
            self.score = score
            self.neighbors = i
            self.best_features = data
            self.counter = 0

            self.indi = []
            for i in range(len(self.features)):
              for ii in data:
                if ii is self.features[i]:
                  self.indi.append(i)

            
    return


  def recurse(self, data):

    temp_len = len(data)
    perm_len = len(self.features)

    if temp_len > perm_len or temp_len == 0 or self.score > self.threshold:
      return
    
    self.predict(data, self.y)
    
    if len(data) > 0:
      self.recurse(self.rLeft(data))
    if len(data) > 1:
      self.recurse(self.rMid(data))
    if len(data) > 2:
      self.recurse(self.rRight(data))

  def shuffle(self, unshuffled):
    import random
    for i in range(len(unshuffled)):
      num = random.randrange(0, len(unshuffled))
      a = unshuffled[i]
      b = unshuffled[num]

      unshuffled[i] = b
      unshuffled[num] = a
    return unshuffled