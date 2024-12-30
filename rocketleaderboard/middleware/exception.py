import logging
import json
from typing import Any, Callable
from aiohttp import web


log = logging.getLogger('middleware.exception')


def json_error(
    request: web.Request,
    status_code: int,
    exception: Exception,
) -> web.Response:
    """
    Returns a Response from an exception.
    Used for error middleware.
    :param status_code:
    :param exception:
    :return:
    """
    log.warning(
        'Error processing request. '
        f'Request [{request}]. Error [{exception}].',
    )
    return web.Response(
        status=status_code,
        body=json.dumps({
            'error': exception.__class__.__name__,
            'status': status_code,
            'detail': str(exception),
        }).encode('utf-8'),
        content_type='application/json'
    )


@web.middleware
async def error_middleware(
    request: web.Request,
    handler: Callable[['web.Request'], Any],
):
    """
    Handles exceptions received from views or previous middleware
    """
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return json_error(request, ex.status, ex)
    except Exception as e:
        return json_error(request, 500, e)
