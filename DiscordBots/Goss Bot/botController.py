import argparse

import KesselBot
import PrinTee

if __name__ == '__main__':
    # Start our tee
    PrinTee.start_printee_logging()

    #   Set up argument parser for command line
    parser = argparse.ArgumentParser(description="Kessel Bot")

    parser.add_argument('--version', action='version', version=f'%(prog)s {KesselBot.VERSION}')
    parser.add_argument('--cfgpath', dest='configPath', metavar='<path>',\
        help='Path to configuration files (defaults to %(prog)s folder if not specified).')
    parser.add_argument('--secretcfg', dest='secret', metavar='<filename>',\
        default='secretConfig.json', help='Filename of secret config with token data (default: %(default)s).')
    parser.add_argument('--config', dest='config', metavar='<filename>', default='botConfig.json',\
        help='Filename of bot config with general data (default: %(default)s).')
    parser.add_argument('--debug', dest='debug', action='store_true',\
        help='Fall out bottom of program to allow access with interactive console. LAUNCH CONSOLE WITH -i PARAMETER')
    parser.add_argument('--restart', dest='restart', nargs='?', type=int, const=-1, default=0,\
        help='Number of times to restart bot if it exits (no value represents indefinite restarts).')

    args = parser.parse_args()

    if not args.debug:
        #   Bot restart manager
        counter = 0
        while True: #   Make a "do-while" loop
            if args.restart < 0:
                lives = float("inf")
            else:
                lives = args.restart - counter
            botInstance = KesselBot.KesselBot(configPath=args.configPath, config=args.config, secret=args.secret, lives=lives)
            botInstance.start(block=True)
            counter += 1
            if (counter > args.restart and args.restart >= 0) or botInstance.do_not_revive:
                break
    else:
        botInstance = KesselBot.KesselBot(configPath=args.configPath, config=args.config, secret=args.secret)
        botInstance.start()