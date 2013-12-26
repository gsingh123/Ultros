# coding=utf-8
__author__ = 'Gareth Coles'

from threading import Lock

from system.command_manager import CommandManager
from system.event_manager import EventManager
from system.events.general import MessageReceived
from system.plugin import PluginObject
from system.protocols.generic.channel import Channel
from system.protocols.generic.user import User
from utils.config import YamlConfig


class BridgePlugin(PluginObject):

    config = None
    events = None
    commands = None

    rules = {}

    mutex = Lock()

    def setup(self):
        self.logger.debug("Entered setup method.")
        try:
            self.config = YamlConfig("plugins/bridge.yml")
        except Exception:
            self.logger.exception("Error loading configuration!")
            self.logger.error("Disabling..")
            self._disable_self()
            return
        if not self.config.exists:
            self.logger.error("Unable to find config/plugins/bridge.yml")
            self.logger.error("Disabling..")
            self._disable_self()
            return

        self.commands = CommandManager.instance()
        self.events = EventManager.instance()

        self.rules = self.config["rules"]

        self.events.add_callback("MessageReceived", self, self.handle_msg,
                                 0)

    def handle_msg(self, event=MessageReceived):
        msg = event.message
        caller = event.caller
        source = event.source
        target = event.target

        if not caller:
            return
        if not source:
            return
        if not target:
            return

        c_name = caller.name.lower()  # Protocol
        s_name = source.nickname  # User
        if isinstance(target, Channel):
            t_name = target.name  # Channel
        else:
            t_name = target.nickname

        for rule, data in self.rules.items():
            self.logger.debug("Checking rule: %s - %s" % (rule, data))
            from_ = data["from"]
            to_ = data["to"]

            if c_name != from_["protocol"].lower():
                self.logger.debug("Protocol doesn't match.")
                continue

            if not self.factory_manager.get_protocol(to_["protocol"]):
                self.logger.debug("Targer protocol doesn't exist.")
                continue

            if isinstance(target, User):
                # We ignore the source name since there can only ever be one
                #     user: us.
                if from_["source-type"].lower() != "user":
                    self.logger.debug("Target type isn't a user.")
                    continue
            elif isinstance(target, Channel):
                if from_["source-type"].lower() != "channel":
                    self.logger.debug("Target type isn't a user.")
                    continue
                if from_["source"].lower() != t_name.lower():
                    self.logger.debug("Target name doesn't match the source.")
                    continue
            else:
                self.logger.debug("Target isn't a known type.")
                continue

            # If we get this far, we've matched the incoming rule.

            format_string = data["format-string"]
            format_string = format_string.replace("{MESSAGE}", msg)
            format_string = format_string.replace("{USER}", s_name)
            format_string = format_string.replace("{TARGET}", t_name)
            format_string = format_string.replace("{PROTOCOL}", caller.name)

            prot = self.factory_manager.get_protocol(to_["protocol"])
            prot.send_msg(to_["target"], format_string,
                          target_type=to_["target-type"])
