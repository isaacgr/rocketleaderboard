import asyncio
import aiohttp
import logging
import signal
import sys
from typing import Dict, Optional

from rocketleaderboard.cmdline import parse_commandline

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%dT%H:%M:%S"
log = logging.getLogger(__name__)


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
    controller: ServerController
) -> None:
    log.error(
        'Exception caught, shutting down. Message [%s]. Exception [%s]',
        context.get('message'),
        context.get('exception')
    )
    if not loop.is_closed:
        loop.create_task(shutdown(loop, controller))


async def shutdown(
    loop: asyncio.AbstractEventLoop,
    controller: Optional[ServerController] = None,
    signal: Optional[signal.Signals] = None
) -> None:
    log.info("Received shutdown request.")
    if controller:
        log.info("Calling cleanup on objects")
        await controller.shutdown()
        log.info("Cleanup Complete.")

    tasks = [
        t for t in asyncio.all_tasks() if t is not asyncio.current_task()
    ]

    [task.cancel() for task in tasks]

    log.info("Cancelling %s outstanding tasks", len(tasks))
    await asyncio.gather(*tasks, return_exceptions=True)
    # probably not needed as start() will be cancelled with a Cancelled Error
    loop.stop()

if __name__ == '__main__':
    main()
