from pdb import Pdb


class Powerdb(Pdb):
    def precmd(self, line):
        if not isinstance(line, str): return line
        return super().precmd(line)

    def onecmd(self, line):
        self.prompt = '--> '
        # print('line:', line)
        if line == ':r':
            self.message('%-15s' % '[Step Out....]')
            return self.do_return(None)
        if line == ':s':
            self.message('%-15s' % '[Step Into...]')
            return self.do_step(None)
        if line == ':n':
            self.message('%-15s' % '[Step Next...]')
            return self.do_next(None)
        if line == ':c':
            self.message('%-15s' % '[Continue....]')
            return self.do_continue(None)
        if line == ':u':
            return self.do_up(None)
        if line == ':d':
            return self.do_down(None)
        if line == ':l':
            return self.do_list(None)
        if line == ':w':
            return self.do_where(None)
        if line == ':q':
            self.message('%-15s' % '[Step Debug..]')
            return self.do_quit(None)
        if line == ':m':
            return self.refresh_bpmark(None)
        if isinstance(line, tuple):
            method, name = line
            # if method == 'locals':
            #     self.message((get_locals(self.curframe_locals, name), True))
            #     self.prompt = None
            if method == 'breakpoint':
                self.clear_all_breaks()
                for file, line in name:
                    self.set_break(file, line)
                self.message(('breakpoint', True))
                if self.first:
                    self.first, self.prompt = False, None
                    return
                self.message('%-15s' % '[Set BreakPoint...]\n')
            return 0
        _, self.message = self.message, print
        self.default(line)
        self.message = _

    def user_call(self, frame, argument_list):
        if self._wait_for_mainpyfile: return
        if self.stop_here(frame):
            self.interaction(frame, None)

    def user_return(self, frame, return_value):
        pass

    def print_stack_entry(self, frame_lineno, prompt_prefix=''):
        frame, lineno = frame_lineno
        import linecache
        filename = self.canonic(frame.f_code.co_filename)
        line = linecache.getline(filename, lineno, frame.f_globals)
        {'path': filename, 'no': lineno, 'line': line}
        self.message(({'path': filename, 'no': lineno, 'line': line.rstrip()}, True))
        if self.first: self.message('--> %-15s' % '[Debugging...]')
        self.message('%-15s ln:%-4d || %s' % (
            filename.split('\\')[-1], lineno, line))

    def debug(self, filename, globals=None, locals=None):
        import os, os.path as osp, sys
        os.chdir(osp.split(filename)[0])
        sys.path.append(osp.split(filename)[0])
        self.prompt, self.first = '--> ', True
        # import __main__
        # __main__.__dict__.clear()
        # __main__.__dict__.update({"__name__": "__main__",
        #                           "__file__": filename, "__builtins__": __builtins__, })
        # self._wait_for_mainpyfile = True
        # self.mainpyfile = self.canonic(filename)
        # self._user_requested_quit = False

        with open(filename, "rb") as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % (fp.read(), self.mainpyfile)
        self.set_break(file_path, 7, temporary=False)
        # self.run(statement, globals, locals)
        # self.run('python3 -u '+file_path, globals, locals)
        self._runscript(file_path)
        # self.message(({'path': 'end', 'no': 0, 'line': ''}, False))
        # self.message(({'path': 'end', 'no': 0, 'line': ''}, False))
        # self.message('Debug Completed...\n')


db = Powerdb()
# db.message = self.write
file_path = '/home/hzy/Documents/Developing/Python/pyminer_dist_debian_deepin/pyminer/pmtoolbox/debug/test2.py'
db.debug(file_path)
