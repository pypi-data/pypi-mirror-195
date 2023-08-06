from colorlog import logger

import numpy as np
# from .colorlog import Color
# from .colorlog import LOG_LEVEL
from colorlog.utils import *

from humanfriendly.tables import format_pretty_table



''' tests '''

def test_pretty_print():
    dict_ = dict(
        id=42,
        name=dict(first_name='Jimmy',
                    last_name='Deng'),
        sexual='male',
        age=30,
        info='Hello world!',
        email=dict(main="121dengpeng@163.com", aux='xx@qq.com')
    )
    logger.debug('int:', 42, True)
    logger.debug('dict:', dict_)


# def test_pretty_print():
#     args = dict(
#         id=42,
#         name=dict(first_name='Jimmy',
#                     last_name='Deng'),
#         sexual='male',
#         age=30,
#         info='Hello world!',
#         arr=np.array([[1, 2], [3, 4]]),
#         email=dict(a=['xxx', 'yyys', 'zzz'], b='bbb')
#     )
#     logger.debug('int:', 42, True)
#     logger.debug('args:', args)


def test_format_pretty_table():
    column_names = ['Version', 'Uploaded on', 'Downloads']

    humanfriendly_releases = [
        ['1.23', '2015-05-25', '218'],
        ['1.23.1', '2015-05-26', '1354'],
        ['1.24', '2015-05-26', '223'],
        ['1.25', '2015-05-26', '4319'],
        ['1.25.1', '2015-06-02', '197'],
    ]
    print(format_pretty_table(humanfriendly_releases, column_names))



if __name__ == "__main__":
    # test_debug_log_functions()
    # test_get_space_dim()
    # test_pretty_print()
    # test_format_pretty_table()
    # logger.log("dada", color="green")
    # logger.set_level("SUCCESS")
    # logger.set_level("WARNING")
    your_args = 'your args...'
    # s = """
    # hjdlahldkjakldhalkdh,
    # djlajdajldjl,
    # dadkladkldjdakl
    # """
    # logger.debug("prompt", args)
    # logger.set_type_hinting(False)
    # logger.debug("prompt", args)
    # # logger.info("prompt", args)
    # # logger.warning("prompt", args)
    # # logger.success("prompt", args)
    # logger.error("prompt", args)

    # logger.debug("dict", {'key': 42})

    # test_pretty_print()

    # print(LOG_LEVEL.SUCCESS == LOG_LEVEL.DEBUG)
    # print(type(LOG_LEVEL.DEBUG.value))

    logger.debug("prompt:", your_args)
    logger.info("prompt:", your_args)
    logger.warning("prompt:", your_args)
    logger.success("prompt:", your_args)
    logger.error("prompt:", your_args)