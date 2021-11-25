from mir import MirManual
import curses

def log(string, line, screen):
    screen.addstr(line, 0, string)
    screen.clrtoeol()
    screen.refresh()


def start_controlling(mir, screen):
    mir.callManualMode()
    mir.subToSafetyInfo()
    # waiting for data from mir
    while not hasattr(mir, 'safetyInfo'):
        pass

    log("Press blue button on robot to unlock manual mode.", 0, screen)
    # waiting for button press
    while mir.safetyInfo['is_manual_mode_restart_required']:
        pass
    log("Now use the arrowkeys to move robot. Press 'q' to quit.", 0, screen)

    x = 0
    z = 0

    while True:
        arrow_key = curses.initscr().getch()

        if arrow_key == ord('q'):
            break

        if arrow_key == curses.KEY_UP:
            x = 0.3
        elif arrow_key == curses.KEY_DOWN:
            x = -0.3
        else: x = 0

        if arrow_key == curses.KEY_RIGHT:
            z = -0.3
        elif arrow_key == curses.KEY_LEFT:
            z = 0.3
        else: z = 0

        log(f"X: {str(x)} Y:{str(z)}", 1, screen)
        mir.move(x, z)

def end_controlling(mir, screen):
    # Close websocket connectin to mir
    mir.callPauseMode()
    mir.terminate()

    # Restore terminal
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def main():
    session_id = '03bdbug5tprmn0q7l00b742vh7'  # extracted from web-interace
    sdt_host = "mir.com"

    print(f"Enter mir's network-address: (hit enter to use '{sdt_host}')")
    usr_host = input()
    print("OK, Trying to connect to MiR...")

    # Connecting to MiR
    host = usr_host if len(usr_host) > 0 else sdt_host
    mir = MirManual(host, 9090, session_id)

    try:
        mir.connect()
    except:
        print("Cloud not connect to mir! Leaving...")
        return

    print("Connected!")
    print("Starting user interface for manual control...\n")

    # Setting up user-interface
    screen = curses.initscr()
    screen.keypad(True)
    curses.noecho()
    curses.cbreak()

    try:
        start_controlling(mir, screen)
    finally:
        # Making sure the connection to MIR is always closed savely
        end_controlling(mir, screen)
        print("Back to terminal and closed connection to mir safely.")

main()
