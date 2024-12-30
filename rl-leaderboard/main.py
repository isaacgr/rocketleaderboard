import asyncio
import aiohttp
import argparse
import logging
import signal
import sys
from typing import Dict, Optional

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%dT%H:%M:%S"
log = logging.getLogger(__name__)


def parse_commandline():
    parser = argparse.ArgumentParser(
        description='Host API server for rl-leaderboard',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    serverGroup = parser.add_argument_group('HTTP Server')
    serverGroup.add_argument(
        '--host',
        default='127.0.0.1',
        help='IP address to host http server',
    )
    serverGroup.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to host http server',
    )
    parser.add_argument('--log-file', help='File for logging')
    return parser.parse_args()


def main():
    options = parse_commandline()
    if options.log_file:
        logfile = options.log_file
        logging.basicConfig(
            filename=logfile,
            level=logging.INFO,
            format=FORMAT,
            datefmt=datefmt,
        )
    else:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.INFO,
            format=FORMAT,
            datefmt=datefmt,
        )

    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for sig in signals:
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(loop, s))
        )
    loop.set_exception_handler(handle_exception)

    # TODO: add retries etc.
    # should probably handle each of these seperately beyond logging
    try:
        loop.run_until_complete(start_server(
            app,
            host=options.host,
            port=options.port,
        ))
    except (
        aiohttp.client_exceptions.ClientConnectorError,
        ConnectionResetError,
    ) as e:
        log.error(e)
    except aiohttp.client_exceptions.ServerDisconnectedError as e:
        log.error(e)
    except aiohttp.client_exceptions.ContentTypeError as e:
        log.error('Invalid response type [%s]' % e)
    except asyncio.CancelledError:
        pass


def handle_exception(
    loop: asyncio.AbstractEventLoop,
    context: Dict[str, str],
):
    log.error(
        'Exception caught. Shutting down. Message [%s]' % context.get('message'))
    asyncio.create_task(shutdown(loop))


async def shutdown(
    loop: asyncio.AbstractEventLoop,
    signal: Optional[bool] = None,
) -> None:
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logging.info(f"Received exit signal {signal.name}")
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    logging.info(f"Flushing metrics")
    loop.stop()

if __name__ == '__main__':
    main()
