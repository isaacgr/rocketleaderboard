import asyncio
import logging
import signal
import sys
from typing import Dict, Optional

from rocketleaderboard.config.ini import parse_ini_configuration
from rocketleaderboard.controller import ServerController
from rocketleaderboard.cmdline import parse_commandline
from rocketleaderboard.typedefs import T_CONTROL_ADDRESS

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%dT%H:%M:%S"
log = logging.getLogger(__name__)


async def start():
    options = parse_commandline()
    log_level = logging.INFO if not options.debug else logging.DEBUG
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format=FORMAT,
        datefmt=datefmt,
    )

    config = parse_ini_configuration(options.config)
    host = options.host
    port = options.port

    server_host: T_CONTROL_ADDRESS = {'host': host, 'port': port}

    controller = ServerController.from_config(
        server_host,
        config,
    )
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(
        lambda loop, context: handle_exception(loop, context, controller)
    )
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for sig in signals:
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(
                shutdown(
                    loop,
                    controller,
                    signal=s
                )
            )
        )
    controller.start()

    # TODO determine the best approach for running this method forever
    while True:
        await asyncio.sleep(1)


def main():
    try:
        asyncio.run(start())
    except asyncio.CancelledError:
        log.info('Event loop closed')


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
