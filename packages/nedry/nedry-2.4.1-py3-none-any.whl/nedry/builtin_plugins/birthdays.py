import logging

from nedry.plugin import PluginModule


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Birthdays(PluginModule):
    """
    Plugin for wishing discord users a happy birthday
    """
    plugin_name = "birthdays"
    plugin_version = "1.0.0"
    plugin_short_description = "Wish discord users a happy birthday"
    plugin_long_description = """
    """

    def open(self):
        """
        Enables plugin operation; subscribe to events and/or initialize things here
        """
        self.discord_bot.add_command("mock", mock_command_handler, False, MOCK_HELPTEXT)
        self.discord_bot.add_command("apologize", apologize_command_handler, False, APOLOGIZE_HELPTEXT)
        self.discord_bot.add_command("apologise", apologize_command_handler, False, APOLOGIZE_HELPTEXT)

    def close(self):
        """
        Disables plugin operation; unsubscribe from events and/or tear down things here
        """
        self.discord_bot.remove_command("mock")
        self.discord_bot.remove_command("apologize")
        self.discord_bot.remove_command("apologise")
