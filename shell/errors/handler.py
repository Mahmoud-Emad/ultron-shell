class ErrorHandler:
    @staticmethod
    def no_color_found(color, end: str = ""):
        """Just prints the error message"""
        from shell.logger.logging import Logger
        Logger.error_log(message="There is no color named {}")
    
    @staticmethod
    def command_not_found(command: str):
        from shell.logger.logging import Logger
        Logger.log(message="Faild to get command: ", color="error", emoji="error", end="")
        Logger.log(message="command ", color="doc", end="")
        Logger.log(message=f"`{command}` ", color="header", end="")
        Logger.log(message="not found.", color="doc", end="\n\n")
        Logger.log(message=f"Try to run ", color="doc", emoji="header",end="")
        Logger.log(message='ultron [-h, --help] ', color='warning', end='')
        Logger.log(message=f"to get more help.", color="doc", end='\n')
        return
