import argparse
from rocketleaderboard.version import version


def build_parser(
    version: str,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Host a GraphQL server for the Rocket League Leaderboard',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    server_group = parser.add_argument_group('Server')
    server_group.add_argument(
        '--host',
        default='127.0.0.1',
        help='IP address to host API on',
    )
    server_group.add_argument(
        '--port',
        default=3475,
        help='Port to host API on',
    )

    config_group = parser.add_argument_group('Config')
    config_group.add_argument(
        '--config',
        default='/var/lib/rocketleaderboard/config.ini',
        help='Location of the config.ini file'
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
