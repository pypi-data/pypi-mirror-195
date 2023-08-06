import pytest
from print_ext import print
from yaclipy.arg_spec import ArgSpec, ArgType




def test_underscore_args():
    def f(help, h, /, cat__c, *, dog__d, _dont__show): pass
    spec = ArgSpec(f)
    print.pretty(spec)
    names = set()
    for p in spec.params.values():
        names.update(p.aliases)
    
    assert(names == {'cat','c','dog','d','help','h'})



def test_hidden_must_be_keyword():
    def f(_bad): pass
    with pytest.raises(ValueError):
        spec = ArgSpec(f)
