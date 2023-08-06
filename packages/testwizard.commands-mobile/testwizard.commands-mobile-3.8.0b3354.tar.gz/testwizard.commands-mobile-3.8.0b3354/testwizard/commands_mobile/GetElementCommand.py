import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementResult import GetElementResult


class GetElementCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetElement")

    def execute(self, selector):
        if selector is None:
            raise Exception("selector is required")

        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return GetElementResult(result, "GetElement was successful", "GetElement failed")
