import unittest
import selenium_loader
import tests.common as common

from unittest.mock import Mock, mock_open
from selenium.webdriver.remote.webdriver import WebDriver



class ActionExecutorTest(unittest.TestCase):
  def setUp(self):
    self._driver_mock = Mock(spec=WebDriver)
    self._driver_mock.__enter__ = lambda self: self
    self._driver_mock.__exit__ = lambda self, exc_type, exc_val, exc_tb: None

    self._config_mock = Mock(spec=selenium_loader.Config)


  def test_call_method_dynamically_with_none_object(self):
    try:
      selenium_loader.ActionExecutor.call_method_dynamically(None, "test")
    except Exception as e:
      assert str(e) == "Imposible call method on None object"


  def test_call_method_dynamically_with_object_has_not_method(self):
    test_object = common.TestObject()

    try:
      selenium_loader.ActionExecutor.call_method_dynamically(test_object, "test")
    except Exception as e:
      assert str(e) == "Object {} has no method {}".format(test_object.__class__.__name__, "test")


  def test_call_method_dynamically_with_object_with_different_kind_of_method_and_parameters(self):
    test_object = common.TestObject()
    selenium_loader.ActionExecutor.call_method_dynamically(test_object, "with_only_one_param", 1)
    selenium_loader.ActionExecutor.call_method_dynamically(test_object, "with_bool_param")
    selenium_loader.ActionExecutor.call_method_dynamically(test_object, "with_list_param", [1, 2])
    selenium_loader.ActionExecutor.call_method_dynamically(test_object, "with_object_param", {"param1": 1, "param2": 2, "param3": 3})

    assert test_object.one_param == 1
    assert test_object.bool_param == 1
    assert test_object.list_param == 1
    assert test_object.dict_param == 1


  def test_run_with_no_steps(self):
    self._config_mock.get.return_value = []

    action_executor = selenium_loader.ActionExecutor(self._driver_mock, self._config_mock)
    action_executor.run()

    self._config_mock.assert_not_called()


  def test_run_with_one_invalid_step(self):
    self._config_mock.get = Mock(args=("steps", []), return_value=[])

    action_executor = selenium_loader.ActionExecutor(self._driver_mock, self._config_mock)
    action_executor.run()


if __name__ == '__main__':
  unittest.main()
