from pysmt.shortcuts import *
import RamseyQuantors.smtlib.parser

def Ramsey(vv1, vv2, formula):
    """
    Shorthand for creating a Ramsey quantifier node:
        Ramsey(vv1, vv2). formula

    Args:
        vv1 (Sequence[FNode]): First group of bound variables.
        vv2 (Sequence[FNode]): Second group of bound variables.
        formula (FNode): Boolean formula over bound variables.

    Returns:
        FNode: A RAMSEY quantifier node, as produced by the environment's FormulaManager.
    """
    fm = get_env().formula_manager
    return fm.Ramsey(vv1, vv2, formula)

def Mod(left, right):
    r""".. math:: l % r """
    return get_env().formula_manager.Mod(left, right)


def read_smtlib(fname):
    """Reads the SMT formula from the given file.

    This supports compressed files, if the fname ends in .bz2 .

    :param fname: Specify the filename
    :returns: An SMT formula
    :rtype: FNode
    """

    return RamseyQuantors.smtlib.parser.get_formula_fname(fname)

