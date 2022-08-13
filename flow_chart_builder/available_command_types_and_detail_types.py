AVAILABLE_COMMAND_TYPES = "start stop operation decision connection delete delete-all title box font connector".split()

DETAIL_TYPES_FOR_COMMANDS = dict()
DETAIL_TYPES_FOR_COMMANDS["start"] = ("name", "placement", "autostart", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["stop"] = DETAIL_TYPES_FOR_COMMANDS["start"]
DETAIL_TYPES_FOR_COMMANDS["operation"] = ("name", "text", "placement", "autostart", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["decision"] = DETAIL_TYPES_FOR_COMMANDS["operation"]
DETAIL_TYPES_FOR_COMMANDS["connection"] = ("start", "end", "points", "autostart",
                                           "label", "label-dx", "label-dy", "label-color")
DETAIL_TYPES_FOR_COMMANDS["delete"] = ("name", "autostart")
DETAIL_TYPES_FOR_COMMANDS["delete-all"] = ("autostart",)
DETAIL_TYPES_FOR_COMMANDS["title"] = ("text", "autostart")
DETAIL_TYPES_FOR_COMMANDS["box"] = ("width", "autostart")
DETAIL_TYPES_FOR_COMMANDS["font"] = ("size", "weight", "autostart")
DETAIL_TYPES_FOR_COMMANDS["connector"] = ("width", "autostart")
