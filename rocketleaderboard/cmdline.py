import argparse
from rocketleaderboard.version import version


def build_parser(
    version: str,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Host API server for the Rocket League Leaderboard',
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

    debug_group = parser.add_argument_group('Debug')
    debug_group.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s: ' + str(version)
    )
    debug_group.add_argument(
        '-D',
        '--debug',
        action='store_true',
    )

    return parser


def parse_commandline() -> argparse.Namespace:
    parser = build_parser(version)
    options = parser.parse_args()
    return options
