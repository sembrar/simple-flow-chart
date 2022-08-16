AVAILABLE_COMMAND_TYPES = "start stop operation decision connection delete delete-all title box font connector".split()

DETAIL_TYPES_FOR_COMMANDS = dict()
DETAIL_TYPES_FOR_COMMANDS["start"] = ("name", "placement", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["stop"] = DETAIL_TYPES_FOR_COMMANDS["start"]
DETAIL_TYPES_FOR_COMMANDS["operation"] = ("name", "text", "placement", "dx", "dy")
DETAIL_TYPES_FOR_COMMANDS["decision"] = tuple(list(DETAIL_TYPES_FOR_COMMANDS["operation"]) + ["angle"])
DETAIL_TYPES_FOR_COMMANDS["connection"] = ("start", "end", "points",
                                           "label", "label-dx", "label-dy", "label-color")
DETAIL_TYPES_FOR_COMMANDS["delete"] = ("name",)
DETAIL_TYPES_FOR_COMMANDS["delete-all"] = ()
DETAIL_TYPES_FOR_COMMANDS["title"] = ("text",)
DETAIL_TYPES_FOR_COMMANDS["box"] = ("width",)
DETAIL_TYPES_FOR_COMMANDS["font"] = ("size", "weight")
DETAIL_TYPES_FOR_COMMANDS["connector"] = ("width",)
