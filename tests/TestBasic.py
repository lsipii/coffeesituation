import unittest
from apps.DeviceApp.DeviceApp import DeviceApp
from apps.SlackBotApp.SlackBotApp import SlackBotApp

class TestBasic(unittest.TestCase):

    def testBasicStuff(self):
        # Device app init test
        deviceApp = DeviceApp()
        self.assertEqual(deviceApp.getAppName(), "Monitoring Device")

        # Bot app infos
        slackBotApp = SlackBotApp()
        self.assertEqual(slackBotApp.getAppName(), "Coffee Related Communication And Relations Facilitator")

if __name__ == '__main__':
    unittest.main()