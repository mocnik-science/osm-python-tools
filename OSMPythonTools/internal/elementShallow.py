class ElementShallow:
  def type(self):
    return None
  def id(self):
    return None
  def typeId(self):
      return self.type() + '/' + str(self.id()) if self.type() != None and self.id() != None else None
  def typeIdShort(self):
      return self.type()[0] + str(self.id()) if self.type() != None and self.id() != None else None
  def areaId(self):
      if self.type() == 'way':
          return self.id() + 2400000000
      elif self.type() == 'relation':
          return self.id() + 3600000000
      else:
          return None
