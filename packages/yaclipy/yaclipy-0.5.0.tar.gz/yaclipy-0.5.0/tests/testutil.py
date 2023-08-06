from print_ext import print
from yaclipy.cmd_dfn import CmdDfn, SubCmds
from yaclipy.exceptions import CallError
from yaclipy.arg_spec import ArgSpec


def exe(fn, args, **incoming):
    try:
        return CmdDfn('main', fn)(incoming, args.split(' ') if args else [])
    except CallError as e:
        print('\vspec\v')
        print.pretty(e.spec)
        raise e


def bind_kw(fn, args):
    return bind(fn, args)[1]

def bind_pos(fn, args):
    return bind(fn, args)[0]

def bind(fn, args):
    try:
        dfn = ArgSpec(fn)
        spec = dfn({}, args.split(' ') if args else [])
        
        print('--------- bound')
        print.pretty(spec)
        print.pretty(spec.argv)
        assert(not spec.errors)
        return spec.args, [(k,spec.kwargs[k]) for k in sorted(spec.kwargs)], spec.argv
    except CallError as e:
        print('\vspec\v')
        print.pretty(e.spec)
        raise e