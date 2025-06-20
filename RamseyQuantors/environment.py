from pysmt.environment import Environment, push_env
from pysmt.oracles import FreeVarsOracle, QuantifierOracle, SizeOracle, TheoryOracle
from pysmt.walkers import DagWalker
from pysmt.walkers.dag import Walker

from RamseyQuantors.operators import MOD_NODE_TYPE, RAMSEY_NODE_TYPE
from RamseyQuantors.printers import ExtendedSerializer
from RamseyQuantors.substituter import ExtendedMGSubstituter
from RamseyQuantors.walkers import custom_walkers

from .type_checker import ExtendedTypeChecker
from .formula import ExtendedFormulaManager

class RamseyEnvironment(Environment):
    TypeCheckerClass = ExtendedTypeChecker
    FormulaManagerClass = ExtendedFormulaManager
    HRSerializerClass = ExtendedSerializer
    SubstituterClass = ExtendedMGSubstituter

    def __init__(self):
        super().__init__()

        self.add_dynamic_walker_function(RAMSEY_NODE_TYPE, FreeVarsOracle, custom_walkers.free_variables_walk_ramsey)
        self.add_dynamic_walker_function(MOD_NODE_TYPE, FreeVarsOracle, FreeVarsOracle.walk_simple_args)
        self.add_dynamic_walker_function(RAMSEY_NODE_TYPE, QuantifierOracle, QuantifierOracle.walk_true)
        self.add_dynamic_walker_function(MOD_NODE_TYPE, QuantifierOracle, QuantifierOracle.walk_all)
        # No ramsey for theory
        self.add_dynamic_walker_function(MOD_NODE_TYPE, TheoryOracle, custom_walkers.theory_walk_mod)
        self.add_dynamic_walker_function(MOD_NODE_TYPE, SizeOracle, custom_walkers.size_walk_general_delegate)
        self.add_dynamic_walker_function(RAMSEY_NODE_TYPE, SizeOracle, custom_walkers.size_walk_general_delegate)

def push_ramsey():
    env = RamseyEnvironment()
    push_env(env)
