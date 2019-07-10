class Stock:
  def __init__(self, ticker):
    from yahoo_historical import Fetcher

    import datetime
    now = datetime.datetime.now()

    raw = Fetcher(ticker, [2018,1,1], [now.year,now.month,now.day])
    self.data = raw.getHistorical()
    self.name = ticker
    

    self.features = []

    #The data -- raw and unpruned. Needed for passing data into functions
    self.r_opens = self.data['Open']
    self.r_highs = self.data['High']
    self.r_lows = self.data['Low']
    self.r_closes = self.data['Close']
    self.r_adj_close = self.data['Adj Close']
    self.r_volumes = self.data['Volume']

    self.m_opens = self.data['Open'][2:-1]
    self.m_highs = self.data['High'][2:-1]
    self.m_lows = self.data['Low'][2:-1]
    self.m_closes = self.data['Close'][2:-1]
    self.m_adj_close = self.data['Adj Close'][2:-1]
    self.m_volumes = self.data['Volume'][2:-1]

    self.pc_open_close = self.percentChange(self.r_opens, self.r_closes)

    self.pc_high_low = self.percentChange(self.r_lows, self.r_highs)

    self.rv_opens = self.relVelocity(self.r_opens)
    self.rv_highs = self.relVelocity(self.r_highs)
    self.rv_lows = self.relVelocity(self.r_lows)
    self.rv_closes = self.relVelocity(self.r_closes)
    self.rv_adj_closes = self.relVelocity(self.r_adj_close)
    self.rv_volumes = self.relVelocity(self.r_volumes)

    self.rp_opens = self.relPos(self.r_opens)
    self.rp_highs = self.relPos(self.r_highs)
    self.rp_lows = self.relPos(self.r_lows)
    self.rp_closes = self.relPos(self.r_closes)
    self.rp_adj_closes = self.relPos(self.r_adj_close)
    self.rp_volumes = self.relPos(self.r_volumes)


    
    self.features.append(self.m_adj_close)
    self.features.append(self.m_closes)
    self.features.append(self.m_highs)
    self.features.append(self.m_lows)
    self.features.append(self.m_opens)
    self.features.append(self.m_volumes)

    self.y = self.percentChangeY(self.r_closes, self.r_closes)#r_opens

  def relPos(self, a):
    iems = []
    for i in range(2, len(a) - 1):
      if a[i+1] < a[i] > a[i-1]:
        iems.append(1)
      elif a[i+1] > a[i] < a[i-1]:
        iems.append(-1)
      else:
        iems.append(0)

    self.features.append(iems)

    return iems


  def relVelocity(self, a):
    iems = []
    for i in range(2, len(a) - 1):
      if a[i] >= a[i-1] >= a[i-1] >= a[i-2]:
        iems.append(1)
      elif a[i] <= a[i-1] <= a[i-2]:
        iems.append(-1)
      else:
        #print(a)
        iems.append(0)

    self.features.append(iems)
    
    return iems

  def percentChange(self, a, b):
    iems = []
    for i in range(len(a[2:-1])):
      iems.append(round((((b[i] - a[i])/ a[i])) * 100, 2))
    
    self.features.append(iems)

    return iems
  
  def percentChangeY(self, a, b):
    iems = []
    for i in range(len(a[2:-1])):
      perc = round((((b[i+1] - a[i])/ a[i])) * 100, 2)
      if perc >= 2:
        iems.append(1)
      elif perc >= 0:
        iems.append(0)
      else:
        iems.append(-1)
    return iems

  def extend(self, a):
    self.features.extend(a.features)

  