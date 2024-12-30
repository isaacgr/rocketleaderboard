from typing import List
import asyncio
import logging

log = logging.getLogger('util.subprocess')

COMMAND_TIMEOUT = 300


async def run_subprocess(cmd_list: List[str]) -> str:
    proc = await asyncio.create_subprocess_exec(
        *cmd_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        outs, errs = await asyncio.wait_for(
            proc.communicate(),
            timeout=COMMAND_TIMEOUT,
        )
        if proc.returncode != 0:
            raise Exception(
                f'Got errors. Errors [{errs.decode("utf-8").strip()}]. '
                f'Return Code [{proc.returncode}].'
            )
        return outs.decode('utf-8').strip()
    except asyncio.TimeoutError:
        log.error('Command timed out.')
        proc.terminate()
        return ''
