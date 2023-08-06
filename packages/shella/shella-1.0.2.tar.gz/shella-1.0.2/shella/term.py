import asyncio
import aiofiles
import termios
import sys
import os

LOCAL_FLAG = 3  # [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]


class Console:
    def __init__(self, cmd_cb):
        self.s = ""
        self.history = []
        self.hp = len(self.history)  # history pointer
        self.commands = []
        self.cursor_pos = 0

        self.cmd_cb = cmd_cb
        self.temp_s = None
        self.prompt = "shella$ "
        self.debug = False
        self.update_line()
        sys.stdout.flush()

    async def read_input_stream(self):
        fd = sys.stdin.fileno()
        previous_flags = termios.tcgetattr(fd)
        all_flags = termios.tcgetattr(fd)

        all_flags[LOCAL_FLAG] &= ~termios.ECHO
        all_flags[LOCAL_FLAG] &= ~termios.ICANON

        termios.tcsetattr(fd, termios.TCSANOW, all_flags)
        try:
            async with aiofiles.open(os.ttyname(fd), mode='r') as f:
                while True:
                    c = await f.read(1)
                    if c == '\x1b':
                        char = c

                        """
                        We just want to receive the whole escaped character, so lets check when it ends, 
                        i.e. when the command character such as 'A' for up arrow
                        """
                        for i in range(20):  # Dont get stuck if we screw up
                            c = await f.read(1)
                            char += c
                            if c.isnumeric() or c in [';', '[', '?', '=']:
                                continue
                            else:
                                break
                        c = char
                    await self.on_input_character(c)
        except (KeyboardInterrupt, asyncio.exceptions.CancelledError):
            pass
        except:
            import traceback
            traceback.print_exc()

        finally:
            termios.tcsetattr(fd, termios.TCSANOW, previous_flags)

    def stdout(self, c, flush=False):
        sys.stdout.write(c)
        if flush:
            sys.stdout.flush()

    def update_line(self):
        self.stdout('\x1b[2K\033[1G')
        self.print_prompt()
        self.stdout(self.s)
        for i in range(len(self.s)-self.cursor_pos):
            self.stdout('\x1b[D')

    def print_prompt(self):
        # self.stdout(f"\033[92m PROMPT [{self.cursor_pos:2}\t{self.hp}/{len(self.history)}]$ \033[0m")
        if self.debug:
            self.stdout(
                f"\033[92m{self.prompt} [{self.cursor_pos:2}\t{self.hp}/{len(self.history)}]$ \033[0m")
        else:
            self.stdout(f"\033[92m{self.prompt}\033[0m")

    def print_hist(self, dir_):

        if len(self.history) == 0:
            return
        # Note addidtion of extra empty slot at end of history
        max_len = len(self.history)

        self.hp += dir_
        if self.hp <= 0:
            self.hp = 0

        if self.hp >= max_len:
            self.hp = max_len

        self.s = (self.history+[self.temp_s])[self.hp]
        self.cursor_pos = len(self.s)

        self.update_line()

    async def on_input_character(self, x):
        if x == '\x7f':
            if (len(self.s) != 0) and (self.cursor_pos > 0):
                self.s = self.s[0:self.cursor_pos-1]+self.s[self.cursor_pos:]
                self.cursor_pos = len(self.s[0:self.cursor_pos-1])
                self.update_line()
        elif x == '\x1b[3~':  # delete
            if (len(self.s) != 0) and (self.cursor_pos >= 0):
                self.s = self.s[0:self.cursor_pos]+self.s[self.cursor_pos+1:]
                self.update_line()
        elif x in ['\x03', '\x1a']:
            return
        elif x == '\x1b[A':  # up
            self.print_hist(-1)
        elif x == '\x1b[B':  # down
            self.print_hist(1)
        elif x == '\x1b[D':  # left
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
                self.stdout(x)
        elif x == '\x1b[C':  # right
            if self.cursor_pos < len(self.s):
                self.cursor_pos += 1
                self.stdout(x)
            pass

        elif x == '\n':
            if len(self.s) > 0:
                print()
                await self.cmd_cb(self.s.split())
            else:
                print("")
            valid_for_history = True
            if len(self.history) > 0:
                if self.s == self.history[-1]:
                    valid_for_history = False

            if len(self.s) > 0 and valid_for_history:
                self.history.append(self.s)
            self.temp_s = ""

            self.hp = len(self.history)
            self.s = ""
            self.cursor_pos = 0
            self.print_prompt()
        elif x == '\t':
            L = len(self.s)
            hits = 0
            options = []
            for c in self.commands:
                if self.s == c[0:L]:
                    hits += 1
                    autocomplete = c[L:]
                    options.append(c)

            if hits == 1:

                self.stdout(autocomplete)
                self.s += autocomplete
                self.cursor_pos = len(self.s)
            elif hits != 0:
                print('\033[2K\033[1G'+",".join(options))
                self.print_prompt()
                self.stdout(self.s)
                self.cursor_pos = len(self.s)
        else:

            if x.isprintable():
                self.s = self.s[0:self.cursor_pos]+x+self.s[self.cursor_pos:]
                self.temp_s = self.s
                self.cursor_pos += 1
                self.update_line()

        sys.stdout.flush()

    def set_prompt(self, prompt):
        self.prompt = prompt
        self.update_line()
