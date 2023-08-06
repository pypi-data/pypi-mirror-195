from __future__ import annotations

import inspect
from typing import Callable

from ..exceptions import MissingArgument, Async, ClientException
from .rule import CommandRule, DEFAULT_RULE, _dfr

class _str:
    def __matmul__(self, other):
        return str

String = _str()

VALID_TYPES = [int, float, bool, str]

class Cog:
    name = "UnnamedCog"
    show_not_found_log = False # whether to show the not found log or not.
    
    def __init__(self):
        self._ll_CONSTRUCTED = True

    def __init_subclass__(cls, prefix: str = None) -> None:
        """
        Initialize a subclass.

        :param str prefix: Command prefix.
        """
        # ll => linelib
        cls._ll_commands: list = []
        cls._ll_CONSTRUCTED: bool = False
        cls.PREFIX: str = prefix or ""
        [cls._ll_commands.append(getattr(cls, i)) if (not i.startswith('__')) and (isinstance(getattr(cls, i), CogCommandWrapper)) else None for i in dir(cls)]

        for item in dir(cls):
          if not item.startswith('__'):
            actual: type = getattr(cls, item) # actual content
            if (
              isinstance(actual, CogCommandWrapper)
              or
              isinstance(actual, CogListenerWrapper)
            ):
              actual.PREFIX = cls.PREFIX
              cls._ll_commands.append(actual)


    async def emit(self, ctx: type):
        gathered = []

        for cmd in self._ll_commands:
            res = await cmd.emit(self, ctx)
            gathered.append(res)

        if all(i == 'no' for i in gathered):
            await self.not_found(ctx, ctx.content.strip().split(' ')[0])
            return 'all-nf' # all not found

    def get_events(self):
      return [
        # handler: str
        # get actual content:
        # getattr(self, handler)
        getattr(self, handler)
        for handler in dir(self)
        if isinstance(getattr(self, handler), CogListenerWrapper)
      ]

    async def emit_events(self, EVENT_TYPE: str, ctx: type):
      for item in self.get_events():
        if item.event == EVENT_TYPE:
          await item.emit(self, ctx)

    async def not_found(self, ctx, command: str):
        """
        Do something when a command was not found.
        """
        pass # default

class CogCommandWrapper:
    """
    Represents a cog command.
    """
    ann: list

    def __init__(self, cmd_name: str, func, rule: CommandRule | _dfr = DEFAULT_RULE, aliases: list[str] = []):
        parameters = inspect.signature(func).parameters

        self.ann = []
        self.rule = rule.emit

        self.aliases = aliases # setup aliases

        keywordOnlyAlreadyFound = False
        cur = 0 # current state

        for name, param in parameters.items():
            cur += 1
            if cur < 3: # meaning that (1, 2) will both be ignored
                continue # ignore

            if (not param.annotation in VALID_TYPES) and (not param.annotation is inspect._empty):
                raise TypeError(f'The type \'{param.annotation.__name__}\' could not be recognized as a valid type.\nLinelib only accepts the following:\nint, float, bool, str')

            if param.kind == inspect.Parameter.KEYWORD_ONLY:
                if keywordOnlyAlreadyFound:
                    raise TypeError('\n\nThe keyword (*) should only be used once in function arguments. This represents that rest of the string that\'s sent from the user will all be passed into this parameter.\n\n')
                else:
                    keywordOnlyAlreadyFound = True
                    # str(name) == parameter name.
                    self.ann.append(('*', str(name)))
            else:
                ann = param.annotation if (not param.annotation is inspect._empty is inspect._empty) else str # empty annotation? then str.

                self.ann.append((ann,))

        self.func: type = func
        self.name = cmd_name
    
    async def emit(self, o: Cog, ctx: type):
        """Emits the command."""

        msg = ctx.content.strip()

        if not msg.startswith(self.PREFIX):
            return "unaccepted-prefix"

        splitted = msg.split(' ')
        
        args = splitted[1:]

        if splitted[0] in [self.name, *self.aliases]:
            should = self.rule(ctx)
            if not should: # not allowed
                await self._RULE_REJECT(o, ctx)
                return
            _PASS = [] # arguments that will be passed in. (*)
            _NAMED = {} # named arguments. (**)

            for i in range(len(args)):
                if (i + 1) > len(self.ann):
                    break # end this
                if self.ann[i][0] != '*':
                    try:
                        _PASS.append(self.ann[i][0](args[i])) # annotations (type)
                    except Exception as err:
                        await self._LL_ERR(o, ctx, err)
                else: # *
                    _NAMED[self.ann[i][1]] = ' '.join(args[i:])
            try:
              await self.func(o, ctx, *_PASS, **_NAMED)
            except Exception as err:
                ERROR = MissingArgument(str(err)) if (isinstance(err, TypeError) and "missing" in str(err)) else err
                await self._LL_ERR(o, ctx, ERROR)

        return 'no'

    def on_error(self, function: Callable) -> Callable:
        if not inspect.iscoroutinefunction(function):
            raise Async("Async Function", f"The function '{function.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")

        self._LL_ERR = function
        return function

    def rule_reject(self, function: Callable) -> Callable:
        if not inspect.iscoroutinefunction(function):
            raise Async("Async Function", f"The function '{function.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")

        self._RULE_REJECT = function
        return function

    async def _RULE_REJECT(self, ctx):
        pass # default

    
    async def _LL_ERR(self, o, ctx, err):
        raise err # default


def cog_command(*, name: String@CogCommandWrapper, rule: CommandRule = DEFAULT_RULE, aliases: list[str] = []) -> CogCommandWrapper:
    """
    Registers a cog command.
    """
    def wrapper(func):
        if not inspect.iscoroutinefunction(func):
            raise Async("Async Function", f"The function '{func.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")
        return CogCommandWrapper(name, func, rule, aliases)

    return wrapper

cog_cmd = cog_command # ~ createAlias

class CogListenerWrapper:
  def __init__(self, event_name: str, func: Callable) -> None:
    self.event = event_name
    self.func = func

  async def emit(self, o: Cog, ctx: type):
    await self.func(o, ctx)
    return 'OK'

def cog_listener(event: str = None) -> Callable:
  if event in ('ready', 'text'):
    raise ClientException('Cogs do not accept the \'ready\' and \'text\' events.\nThe former is unaccepted due to some parameter issues;\nThe latter is due to a conflict would occur when receiving text events & replying to commands.\n\n-> Try modifying the `__init__(self, ...)` function instead.')

  def wrapper(func, *args, **kwargs) -> CogListenerWrapper:
    if not inspect.iscoroutinefunction(func):
      raise Async("Async Function", f"The function '{func.__name__}' should be an async (coroutine) function. Example:\n\nasync def my_function(...)\n\n")
    
    # func.__name__: 'on_text'
    # .split('_'): ['on', 'text']
    # [1]: 'text'
    
    return CogListenerWrapper(event or func.__name__.split('_')[1], func)

  return wrapper

cog_event = cog_listener