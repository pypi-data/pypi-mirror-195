class TestObject:
  def __init__(self) -> None:
    self.one_param = 0
    self.bool_param = 0
    self.list_param = 0
    self.dict_param = 0

  def with_only_one_param(self, param1):
    self.one_param += 1

  def with_bool_param(self):
    self.bool_param += 1

  def with_list_param(self, param1, param2):
    self.list_param += 1

  def with_object_param(self, param1 = None, param2 = None, param3 = None):
    if param1 and param2 and param3:
      self.dict_param += 1
