import logging
from logging.handlers import RotatingFileHandler
import os


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': BLUE,
    'DEBUG': WHITE,
    'CRITICAL': CYAN,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        msg = record.msg
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (
                30 + COLORS[levelname]) + levelname + RESET_SEQ
            msg_color = COLOR_SEQ % (30 + COLORS[levelname]) + msg + RESET_SEQ
            record.levelname = levelname_color
            record.msg = msg_color

        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = "[$BOLD%(name)s$RESET][%(levelname)s] $BOLD%(message)s$RESET (%(filename)s:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.INFO)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        # 创建一个handler，用于将日志输出到控制台
        console = logging.StreamHandler()

        # 创建一个handler，用于写入日志文件
        log_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs('logs', exist_ok=True)  # 设置日志输出目录
        logname = log_path + '/logs/access.log'  # 指定输出的日志文件名
        fh = logging.handlers.RotatingFileHandler(
            logname, maxBytes=1024*1024, backupCount=3)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s %(name)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s',
                                      datefmt='%b %d  %Y %H:%M:%S')

        # 格式化日志
        fh.setFormatter(formatter)
        console.setFormatter(color_formatter)

        # 给logger添加handler
        self.addHandler(fh)  # 写入文件到本地
        self.addHandler(console)  # 终端输出
        return


def log_start(module_name):
    logging.setLoggerClass(ColoredLogger)
    color_log = logging.getLogger(module_name)
    color_log.setLevel(logging.DEBUG)
    return color_log


if __name__ == '__main__':
    
    logger = log_start('log')
    logger.debug("this is a debugging message")
    logger.info("this is an informational message")
    logger.warning("this is a warning message")
    logger.error("this is an error message")
