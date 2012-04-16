# This module is automatically generated from grammar2x.py.templ, 
#      at 2011-07-01 13:23:21.288018, with python 2.7.2 (default, Jun 27 2011, 21:15:33) .
#
# Modified by Daniel Kluev, for Pyjamas project, 2011.
#
# Copyright 2004-2005 Elemental Security, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""This module defines the data structures used to represent a grammar.

These are a bit arcane because they are derived from the data
structures used by Python's 'pgen' parser generator.

There's also a table here mapping operators to their names in the
token module; the Python tokenize module reports all operators as the
fallback token code OP, but the parser needs the actual token code.
"""

class Grammar(object):
    """Pgen parsing tables tables conversion class.

    Once initialized, this class supplies the grammar tables for the
    parsing engine implemented by parse.py.  The parsing engine
    accesses the instance variables directly.  The class here does not
    provide initialization of the tables; several subclasses exist to
    do this (see the conv and pgen modules).

    The instance variables are as follows:

    symbol2number -- a dict mapping symbol names to numbers.  Symbol
                     numbers are always 256 or higher, to distinguish
                     them from token numbers, which are between 0 and
                     255 (inclusive).

    number2symbol -- a dict mapping numbers to symbol names;
                     these two are each other's inverse.

    states        -- a list of DFAs, where each DFA is a list of
                     states, each state is is a list of arcs, and each
                     arc is a (i, j) pair where i is a label and j is
                     a state number.  The DFA number is the index into
                     this list.  (This name is slightly confusing.)
                     Final states are represented by a special arc of
                     the form (0, j) where j is its own state number.

    dfas          -- a dict mapping symbol numbers to (DFA, first)
                     pairs, where DFA is an item from the states list
                     above, and first is a set of tokens that can
                     begin this grammar rule (represented by a dict
                     whose values are always 1).

    labels        -- a list of (x, y) pairs where x is either a token
                     number or a symbol number, and y is either None
                     or a string; the strings are keywords.  The label
                     number is the index in this list; label numbers
                     are used to mark state transitions (arcs) in the
                     DFAs.

    start         -- the number of the grammar's start symbol.

    keywords      -- a dict mapping keyword strings to arc labels.

    tokens        -- a dict mapping token numbers to arc labels.

    """
    symbol2number = {'dotted_as_names': 280, 'import_as_name': 297, 'vfplist': 333, 'try_stmt': 330, 'small_stmt': 318, 'augassign': 264, 'argument': 260, 'or_test': 307, 'import_as_names': 298, 'return_stmt': 313, 'testlist_safe': 328, 'not_test': 304, 'suite': 322, 'listmaker': 303, 'old_test': 306, 'arglist': 259, 'import_from': 299, 'gen_iter': 294, 'break_stmt': 265, 'except_clause': 283, 'comp_if': 268, 'import_stmt': 301, 'parameters': 308, 'continue_stmt': 273, 'shift_expr': 314, 'single_input': 316, 'dotted_as_name': 279, 'testlist_gexp': 327, 'exec_stmt': 284, 'factor': 288, 'test': 324, 'global_stmt': 295, 'subscript': 320, 'vfpdef': 332, 'decorators': 276, 'compound_stmt': 272, 'and_expr': 257, 'yield_stmt': 339, 'dotted_name': 281, 'yield_expr': 338, 'dictsetmaker': 278, 'flow_stmt': 289, 'power': 310, 'print_stmt': 311, 'gen_for': 292, 'subscriptlist': 321, 'testlist': 325, 'comp_op': 270, 'and_test': 258, 'classdef': 266, 'assert_stmt': 262, 'for_stmt': 290, 'stmt': 319, 'lambdef': 302, 'atom': 263, 'funcdef': 291, 'decorated': 274, 'expr_stmt': 286, 'old_lambdef': 305, 'exprlist': 287, 'decorator': 275, 'pass_stmt': 309, 'sliceop': 317, 'comparison': 271, 'term': 323, 'with_item': 335, 'if_stmt': 296, 'arith_expr': 261, 'file_input': 256, 'raise_stmt': 312, 'import_name': 300, 'gen_if': 293, 'expr': 285, 'del_stmt': 277, 'while_stmt': 334, 'varargslist': 331, 'testlist1': 326, 'comp_for': 267, 'eval_input': 282, 'simple_stmt': 315, 'with_stmt': 336, 'xor_expr': 337, 'comp_iter': 269, 'trailer': 329}
    number2symbol = {256: 'file_input', 257: 'and_expr', 258: 'and_test', 259: 'arglist', 260: 'argument', 261: 'arith_expr', 262: 'assert_stmt', 263: 'atom', 264: 'augassign', 265: 'break_stmt', 266: 'classdef', 267: 'comp_for', 268: 'comp_if', 269: 'comp_iter', 270: 'comp_op', 271: 'comparison', 272: 'compound_stmt', 273: 'continue_stmt', 274: 'decorated', 275: 'decorator', 276: 'decorators', 277: 'del_stmt', 278: 'dictsetmaker', 279: 'dotted_as_name', 280: 'dotted_as_names', 281: 'dotted_name', 282: 'eval_input', 283: 'except_clause', 284: 'exec_stmt', 285: 'expr', 286: 'expr_stmt', 287: 'exprlist', 288: 'factor', 289: 'flow_stmt', 290: 'for_stmt', 291: 'funcdef', 292: 'gen_for', 293: 'gen_if', 294: 'gen_iter', 295: 'global_stmt', 296: 'if_stmt', 297: 'import_as_name', 298: 'import_as_names', 299: 'import_from', 300: 'import_name', 301: 'import_stmt', 302: 'lambdef', 303: 'listmaker', 304: 'not_test', 305: 'old_lambdef', 306: 'old_test', 307: 'or_test', 308: 'parameters', 309: 'pass_stmt', 310: 'power', 311: 'print_stmt', 312: 'raise_stmt', 313: 'return_stmt', 314: 'shift_expr', 315: 'simple_stmt', 316: 'single_input', 317: 'sliceop', 318: 'small_stmt', 319: 'stmt', 320: 'subscript', 321: 'subscriptlist', 322: 'suite', 323: 'term', 324: 'test', 325: 'testlist', 326: 'testlist1', 327: 'testlist_gexp', 328: 'testlist_safe', 329: 'trailer', 330: 'try_stmt', 331: 'varargslist', 332: 'vfpdef', 333: 'vfplist', 334: 'while_stmt', 335: 'with_item', 336: 'with_stmt', 337: 'xor_expr', 338: 'yield_expr', 339: 'yield_stmt'}
    states = [[[(1, 0), (2, 1), (3, 0)], [(0, 1)]], [[(38, 1)], [(39, 0), (0, 1)]], [[(40, 1)], [(41, 0), (0, 1)]], [[(42, 1), (43, 2), (44, 3)], [(45, 4)], [(46, 5), (0, 2)], [(45, 6)], [(46, 7), (0, 4)], [(42, 1), (43, 2), (44, 3), (0, 5)], [(0, 6)], [(43, 4), (44, 3)]], [[(45, 1)], [(47, 2), (48, 3), (0, 1)], [(0, 2)], [(45, 2)]], [[(49, 1)], [(30, 0), (37, 0), (0, 1)]], [[(11, 1)], [(45, 2)], [(46, 3), (0, 2)], [(45, 4)], [(0, 4)]], [[(18, 1), (6, 2), (20, 5), (13, 4), (31, 3), (8, 6), (27, 2)], [(18, 1), (0, 1)], [(0, 2)], [(50, 7), (51, 2)], [(52, 2), (53, 8), (54, 8)], [(55, 9), (56, 2)], [(57, 10)], [(51, 2)], [(52, 2)], [(56, 2)], [(8, 2)]], [[(58, 1), (59, 1), (60, 1), (61, 1), (62, 1), (63, 1), (64, 1), (65, 1), (66, 1), (67, 1), (68, 1), (69, 1)], [(0, 1)]], [[(14, 1)], [(0, 1)]], [[(21, 1)], [(27, 2)], [(70, 3), (13, 4)], [(71, 5)], [(52, 6), (72, 7)], [(0, 5)], [(70, 3)], [(52, 6)]], [[(33, 1)], [(73, 2)], [(74, 3)], [(75, 4)], [(76, 5), (0, 4)], [(0, 5)]], [[(35, 1)], [(77, 2)], [(76, 3), (0, 2)], [(0, 3)]], [[(78, 1), (79, 1)], [(0, 1)]], [[(80, 1), (81, 1), (19, 2), (82, 1), (80, 1), (74, 1), (83, 1), (84, 3), (85, 1), (86, 1)], [(0, 1)], [(74, 1)], [(19, 1), (0, 3)]], [[(87, 1)], [(88, 0), (0, 1)]], [[(89, 1), (90, 1), (91, 1), (92, 1), (93, 1), (94, 1), (95, 1), (96, 1)], [(0, 1)]], [[(15, 1)], [(0, 1)]], [[(97, 1)], [(95, 2), (92, 2)], [(0, 2)]], [[(16, 1)], [(98, 2)], [(1, 4), (13, 3)], [(52, 5), (99, 6)], [(0, 4)], [(1, 4)], [(52, 5)]], [[(100, 1)], [(100, 1), (0, 1)]], [[(28, 1)], [(73, 2)], [(0, 2)]], [[(45, 1)], [(70, 2), (79, 3), (46, 4), (0, 1)], [(45, 5)], [(0, 3)], [(45, 6), (0, 4)], [(79, 3), (46, 7), (0, 5)], [(46, 4), (0, 6)], [(45, 8), (0, 7)], [(70, 9)], [(45, 10)], [(46, 7), (0, 10)]], [[(98, 1)], [(101, 2), (0, 1)], [(27, 3)], [(0, 3)]], [[(102, 1)], [(46, 0), (0, 1)]], [[(27, 1)], [(103, 0), (0, 1)]], [[(72, 1)], [(1, 1), (2, 2)], [(0, 2)]], [[(104, 1)], [(45, 2), (0, 1)], [(101, 3), (46, 3), (0, 2)], [(45, 4)], [(0, 4)]], [[(25, 1)], [(87, 2)], [(74, 3), (0, 2)], [(45, 4)], [(46, 5), (0, 4)], [(45, 6)], [(0, 6)]], [[(105, 1)], [(106, 0), (0, 1)]], [[(72, 1)], [(107, 2), (48, 3), (0, 1)], [(72, 4), (54, 4)], [(72, 5), (54, 5)], [(0, 4)], [(48, 3), (0, 5)]], [[(87, 1)], [(46, 2), (0, 1)], [(87, 1), (0, 2)]], [[(108, 2), (30, 1), (5, 1), (37, 1)], [(109, 2)], [(0, 2)]], [[(110, 1), (111, 1), (112, 1), (113, 1), (114, 1)], [(0, 1)]], [[(33, 1)], [(73, 2)], [(74, 3)], [(72, 4)], [(70, 5)], [(71, 6)], [(115, 7), (0, 6)], [(70, 8)], [(71, 9)], [(0, 9)]], [[(7, 1)], [(27, 2)], [(116, 3)], [(70, 4)], [(71, 5)], [(0, 5)]], [[(33, 1)], [(73, 2)], [(74, 3)], [(117, 4)], [(118, 5), (0, 4)], [(0, 5)]], [[(35, 1)], [(77, 2)], [(118, 3), (0, 2)], [(0, 3)]], [[(47, 1), (119, 1)], [(0, 1)]], [[(32, 1), (24, 1)], [(27, 2)], [(46, 1), (0, 2)]], [[(35, 1)], [(45, 2)], [(70, 3)], [(71, 4)], [(115, 5), (120, 1), (0, 4)], [(70, 6)], [(71, 7)], [(0, 7)]], [[(27, 1)], [(101, 2), (0, 1)], [(27, 3)], [(0, 3)]], [[(121, 1)], [(46, 2), (0, 1)], [(121, 1), (0, 2)]], [[(34, 1)], [(98, 2), (103, 3)], [(4, 4)], [(98, 2), (4, 4), (103, 3)], [(122, 5), (42, 5), (13, 6)], [(0, 5)], [(122, 7)], [(52, 5)]], [[(4, 1)], [(123, 2)], [(0, 2)]], [[(124, 1), (125, 1)], [(0, 1)]], [[(22, 1)], [(70, 2), (126, 3)], [(45, 4)], [(70, 2)], [(0, 4)]], [[(45, 1)], [(79, 2), (46, 3), (0, 1)], [(0, 2)], [(45, 4), (0, 3)], [(46, 3), (0, 4)]], [[(19, 1), (127, 2)], [(40, 2)], [(0, 2)]], [[(22, 1)], [(70, 2), (126, 3)], [(77, 4)], [(70, 2)], [(0, 4)]], [[(128, 1), (117, 1)], [(0, 1)]], [[(129, 1)], [(130, 0), (0, 1)]], [[(13, 1)], [(52, 2), (126, 3)], [(0, 2)], [(52, 2)]], [[(29, 1)], [(0, 1)]], [[(131, 1)], [(132, 1), (44, 2), (0, 1)], [(109, 3)], [(0, 3)]], [[(23, 1)], [(45, 2), (133, 3), (0, 1)], [(46, 4), (0, 2)], [(45, 5)], [(45, 2), (0, 4)], [(46, 6), (0, 5)], [(45, 7)], [(46, 8), (0, 7)], [(45, 7), (0, 8)]], [[(17, 1)], [(45, 2), (0, 1)], [(34, 3), (46, 4), (0, 2)], [(45, 5)], [(45, 6)], [(0, 5)], [(46, 3), (0, 6)]], [[(10, 1)], [(72, 2), (0, 1)], [(0, 2)]], [[(134, 1)], [(135, 0), (133, 0), (0, 1)]], [[(136, 1)], [(1, 2), (137, 3)], [(0, 2)], [(136, 1), (1, 2)]], [[(138, 1), (1, 1), (139, 2)], [(0, 1)], [(1, 1)]], [[(70, 1)], [(45, 2), (0, 1)], [(0, 2)]], [[(140, 1), (141, 1), (142, 1), (143, 1), (144, 1), (145, 1), (146, 1), (147, 1), (148, 1)], [(0, 1)]], [[(138, 1), (139, 1)], [(0, 1)]], [[(45, 1), (70, 2), (103, 3)], [(70, 2), (0, 1)], [(149, 4), (45, 5), (0, 2)], [(103, 6)], [(0, 4)], [(149, 4), (0, 5)], [(103, 4)]], [[(150, 1)], [(46, 2), (0, 1)], [(150, 1), (0, 2)]], [[(138, 1), (1, 2)], [(0, 1)], [(151, 3)], [(3, 4)], [(152, 1), (3, 4)]], [[(109, 1)], [(153, 0), (42, 0), (154, 0), (155, 0), (0, 1)]], [[(117, 1), (156, 2)], [(35, 3), (0, 1)], [(0, 2)], [(117, 4)], [(115, 5)], [(45, 2)]], [[(45, 1)], [(46, 2), (0, 1)], [(45, 1), (0, 2)]], [[(45, 1)], [(46, 0), (0, 1)]], [[(45, 1)], [(47, 2), (46, 3), (0, 1)], [(0, 2)], [(45, 4), (0, 3)], [(46, 3), (0, 4)]], [[(77, 1)], [(46, 2), (0, 1)], [(77, 3)], [(46, 4), (0, 3)], [(77, 3), (0, 4)]], [[(13, 1), (103, 2), (31, 3)], [(52, 4), (99, 5)], [(27, 4)], [(157, 6)], [(0, 4)], [(52, 4)], [(51, 4)]], [[(9, 1)], [(70, 2)], [(71, 3)], [(158, 4), (159, 5)], [(70, 6)], [(70, 7)], [(71, 8)], [(71, 9)], [(158, 4), (115, 10), (159, 5), (0, 8)], [(0, 9)], [(70, 11)], [(71, 12)], [(159, 5), (0, 12)]], [[(42, 1), (44, 2), (160, 3)], [(27, 4), (46, 5), (0, 1)], [(27, 6)], [(48, 7), (46, 8), (0, 3)], [(46, 5), (0, 4)], [(27, 9), (44, 2)], [(0, 6)], [(45, 10)], [(42, 1), (44, 2), (160, 3), (0, 8)], [(48, 11), (46, 5), (0, 9)], [(46, 8), (0, 10)], [(45, 4)]], [[(13, 1), (27, 2)], [(161, 3)], [(0, 2)], [(52, 2)]], [[(160, 1)], [(46, 2), (0, 1)], [(160, 1), (0, 2)]], [[(26, 1)], [(45, 2)], [(70, 3)], [(71, 4)], [(115, 5), (0, 4)], [(70, 6)], [(71, 7)], [(0, 7)]], [[(45, 1)], [(101, 2), (0, 1)], [(87, 3)], [(0, 3)]], [[(36, 1)], [(162, 2)], [(70, 3), (46, 1)], [(71, 4)], [(0, 4)]], [[(163, 1)], [(164, 0), (0, 1)]], [[(12, 1)], [(72, 2), (0, 1)], [(0, 2)]], [[(54, 1)], [(0, 1)]]]
    dfas = {256: ([[(1, 0), (2, 1), (3, 0)], [(0, 1)]], {1: 1, 2: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1}), 257: ([[(38, 1)], [(39, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 258: ([[(40, 1)], [(41, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 259: ([[(42, 1), (43, 2), (44, 3)], [(45, 4)], [(46, 5), (0, 2)], [(45, 6)], [(46, 7), (0, 4)], [(42, 1), (43, 2), (44, 3), (0, 5)], [(0, 6)], [(43, 4), (44, 3)]], {5: 1, 6: 1, 8: 1, 42: 1, 44: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 260: ([[(45, 1)], [(47, 2), (48, 3), (0, 1)], [(0, 2)], [(45, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 261: ([[(49, 1)], [(30, 0), (37, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 262: ([[(11, 1)], [(45, 2)], [(46, 3), (0, 2)], [(45, 4)], [(0, 4)]], {11: 1}), 263: ([[(18, 1), (6, 2), (20, 5), (13, 4), (31, 3), (8, 6), (27, 2)], [(18, 1), (0, 1)], [(0, 2)], [(50, 7), (51, 2)], [(52, 2), (53, 8), (54, 8)], [(55, 9), (56, 2)], [(57, 10)], [(51, 2)], [(52, 2)], [(56, 2)], [(8, 2)]], {6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 31: 1}), 264: ([[(58, 1), (59, 1), (60, 1), (61, 1), (62, 1), (63, 1), (64, 1), (65, 1), (66, 1), (67, 1), (68, 1), (69, 1)], [(0, 1)]], {64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 69: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 1}), 265: ([[(14, 1)], [(0, 1)]], {14: 1}), 266: ([[(21, 1)], [(27, 2)], [(70, 3), (13, 4)], [(71, 5)], [(52, 6), (72, 7)], [(0, 5)], [(70, 3)], [(52, 6)]], {21: 1}), 267: ([[(33, 1)], [(73, 2)], [(74, 3)], [(75, 4)], [(76, 5), (0, 4)], [(0, 5)]], {33: 1}), 268: ([[(35, 1)], [(77, 2)], [(76, 3), (0, 2)], [(0, 3)]], {35: 1}), 269: ([[(78, 1), (79, 1)], [(0, 1)]], {33: 1, 35: 1}), 270: ([[(80, 1), (81, 1), (19, 2), (82, 1), (80, 1), (74, 1), (83, 1), (84, 3), (85, 1), (86, 1)], [(0, 1)], [(74, 1)], [(19, 1), (0, 3)]], {83: 1, 74: 1, 80: 1, 81: 1, 82: 1, 19: 1, 84: 1, 85: 1, 86: 1}), 271: ([[(87, 1)], [(88, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 272: ([[(89, 1), (90, 1), (91, 1), (92, 1), (93, 1), (94, 1), (95, 1), (96, 1)], [(0, 1)]], {33: 1, 35: 1, 36: 1, 7: 1, 9: 1, 16: 1, 21: 1, 26: 1}), 273: ([[(15, 1)], [(0, 1)]], {15: 1}), 274: ([[(97, 1)], [(95, 2), (92, 2)], [(0, 2)]], {16: 1}), 275: ([[(16, 1)], [(98, 2)], [(1, 4), (13, 3)], [(52, 5), (99, 6)], [(0, 4)], [(1, 4)], [(52, 5)]], {16: 1}), 276: ([[(100, 1)], [(100, 1), (0, 1)]], {16: 1}), 277: ([[(28, 1)], [(73, 2)], [(0, 2)]], {28: 1}), 278: ([[(45, 1)], [(70, 2), (79, 3), (46, 4), (0, 1)], [(45, 5)], [(0, 3)], [(45, 6), (0, 4)], [(79, 3), (46, 7), (0, 5)], [(46, 4), (0, 6)], [(45, 8), (0, 7)], [(70, 9)], [(45, 10)], [(46, 7), (0, 10)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 279: ([[(98, 1)], [(101, 2), (0, 1)], [(27, 3)], [(0, 3)]], {27: 1}), 280: ([[(102, 1)], [(46, 0), (0, 1)]], {27: 1}), 281: ([[(27, 1)], [(103, 0), (0, 1)]], {27: 1}), 282: ([[(72, 1)], [(1, 1), (2, 2)], [(0, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 283: ([[(104, 1)], [(45, 2), (0, 1)], [(101, 3), (46, 3), (0, 2)], [(45, 4)], [(0, 4)]], {104: 1}), 284: ([[(25, 1)], [(87, 2)], [(74, 3), (0, 2)], [(45, 4)], [(46, 5), (0, 4)], [(45, 6)], [(0, 6)]], {25: 1}), 285: ([[(105, 1)], [(106, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 286: ([[(72, 1)], [(107, 2), (48, 3), (0, 1)], [(72, 4), (54, 4)], [(72, 5), (54, 5)], [(0, 4)], [(48, 3), (0, 5)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 287: ([[(87, 1)], [(46, 2), (0, 1)], [(87, 1), (0, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 288: ([[(108, 2), (30, 1), (5, 1), (37, 1)], [(109, 2)], [(0, 2)]], {37: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 5: 1, 30: 1, 31: 1}), 289: ([[(110, 1), (111, 1), (112, 1), (113, 1), (114, 1)], [(0, 1)]], {17: 1, 10: 1, 12: 1, 14: 1, 15: 1}), 290: ([[(33, 1)], [(73, 2)], [(74, 3)], [(72, 4)], [(70, 5)], [(71, 6)], [(115, 7), (0, 6)], [(70, 8)], [(71, 9)], [(0, 9)]], {33: 1}), 291: ([[(7, 1)], [(27, 2)], [(116, 3)], [(70, 4)], [(71, 5)], [(0, 5)]], {7: 1}), 292: ([[(33, 1)], [(73, 2)], [(74, 3)], [(117, 4)], [(118, 5), (0, 4)], [(0, 5)]], {33: 1}), 293: ([[(35, 1)], [(77, 2)], [(118, 3), (0, 2)], [(0, 3)]], {35: 1}), 294: ([[(47, 1), (119, 1)], [(0, 1)]], {33: 1, 35: 1}), 295: ([[(32, 1), (24, 1)], [(27, 2)], [(46, 1), (0, 2)]], {32: 1, 24: 1}), 296: ([[(35, 1)], [(45, 2)], [(70, 3)], [(71, 4)], [(115, 5), (120, 1), (0, 4)], [(70, 6)], [(71, 7)], [(0, 7)]], {35: 1}), 297: ([[(27, 1)], [(101, 2), (0, 1)], [(27, 3)], [(0, 3)]], {27: 1}), 298: ([[(121, 1)], [(46, 2), (0, 1)], [(121, 1), (0, 2)]], {27: 1}), 299: ([[(34, 1)], [(98, 2), (103, 3)], [(4, 4)], [(98, 2), (4, 4), (103, 3)], [(122, 5), (42, 5), (13, 6)], [(0, 5)], [(122, 7)], [(52, 5)]], {34: 1}), 300: ([[(4, 1)], [(123, 2)], [(0, 2)]], {4: 1}), 301: ([[(124, 1), (125, 1)], [(0, 1)]], {34: 1, 4: 1}), 302: ([[(22, 1)], [(70, 2), (126, 3)], [(45, 4)], [(70, 2)], [(0, 4)]], {22: 1}), 303: ([[(45, 1)], [(79, 2), (46, 3), (0, 1)], [(0, 2)], [(45, 4), (0, 3)], [(46, 3), (0, 4)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 304: ([[(19, 1), (127, 2)], [(40, 2)], [(0, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 305: ([[(22, 1)], [(70, 2), (126, 3)], [(77, 4)], [(70, 2)], [(0, 4)]], {22: 1}), 306: ([[(128, 1), (117, 1)], [(0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 307: ([[(129, 1)], [(130, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 308: ([[(13, 1)], [(52, 2), (126, 3)], [(0, 2)], [(52, 2)]], {13: 1}), 309: ([[(29, 1)], [(0, 1)]], {29: 1}), 310: ([[(131, 1)], [(132, 1), (44, 2), (0, 1)], [(109, 3)], [(0, 3)]], {6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 31: 1}), 311: ([[(23, 1)], [(45, 2), (133, 3), (0, 1)], [(46, 4), (0, 2)], [(45, 5)], [(45, 2), (0, 4)], [(46, 6), (0, 5)], [(45, 7)], [(46, 8), (0, 7)], [(45, 7), (0, 8)]], {23: 1}), 312: ([[(17, 1)], [(45, 2), (0, 1)], [(34, 3), (46, 4), (0, 2)], [(45, 5)], [(45, 6)], [(0, 5)], [(46, 3), (0, 6)]], {17: 1}), 313: ([[(10, 1)], [(72, 2), (0, 1)], [(0, 2)]], {10: 1}), 314: ([[(134, 1)], [(135, 0), (133, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 315: ([[(136, 1)], [(1, 2), (137, 3)], [(0, 2)], [(136, 1), (1, 2)]], {4: 1, 5: 1, 6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 17: 1, 18: 1, 19: 1, 20: 1, 22: 1, 23: 1, 24: 1, 25: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 34: 1, 37: 1}), 316: ([[(138, 1), (1, 1), (139, 2)], [(0, 1)], [(1, 1)]], {1: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1}), 317: ([[(70, 1)], [(45, 2), (0, 1)], [(0, 2)]], {70: 1}), 318: ([[(140, 1), (141, 1), (142, 1), (143, 1), (144, 1), (145, 1), (146, 1), (147, 1), (148, 1)], [(0, 1)]], {4: 1, 5: 1, 6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 17: 1, 18: 1, 19: 1, 20: 1, 22: 1, 23: 1, 24: 1, 25: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 34: 1, 37: 1}), 319: ([[(138, 1), (139, 1)], [(0, 1)]], {4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1}), 320: ([[(45, 1), (70, 2), (103, 3)], [(70, 2), (0, 1)], [(149, 4), (45, 5), (0, 2)], [(103, 6)], [(0, 4)], [(149, 4), (0, 5)], [(103, 4)]], {5: 1, 6: 1, 103: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 70: 1, 37: 1, 30: 1, 31: 1}), 321: ([[(150, 1)], [(46, 2), (0, 1)], [(150, 1), (0, 2)]], {5: 1, 6: 1, 103: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 70: 1, 37: 1, 30: 1, 31: 1}), 322: ([[(138, 1), (1, 2)], [(0, 1)], [(151, 3)], [(3, 4)], [(152, 1), (3, 4)]], {1: 1, 4: 1, 5: 1, 6: 1, 8: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 17: 1, 18: 1, 19: 1, 20: 1, 22: 1, 23: 1, 24: 1, 25: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 34: 1, 37: 1}), 323: ([[(109, 1)], [(153, 0), (42, 0), (154, 0), (155, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 324: ([[(117, 1), (156, 2)], [(35, 3), (0, 1)], [(0, 2)], [(117, 4)], [(115, 5)], [(45, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 325: ([[(45, 1)], [(46, 2), (0, 1)], [(45, 1), (0, 2)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 326: ([[(45, 1)], [(46, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 327: ([[(45, 1)], [(47, 2), (46, 3), (0, 1)], [(0, 2)], [(45, 4), (0, 3)], [(46, 3), (0, 4)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 328: ([[(77, 1)], [(46, 2), (0, 1)], [(77, 3)], [(46, 4), (0, 3)], [(77, 3), (0, 4)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 329: ([[(13, 1), (103, 2), (31, 3)], [(52, 4), (99, 5)], [(27, 4)], [(157, 6)], [(0, 4)], [(52, 4)], [(51, 4)]], {31: 1, 13: 1, 103: 1}), 330: ([[(9, 1)], [(70, 2)], [(71, 3)], [(158, 4), (159, 5)], [(70, 6)], [(70, 7)], [(71, 8)], [(71, 9)], [(158, 4), (115, 10), (159, 5), (0, 8)], [(0, 9)], [(70, 11)], [(71, 12)], [(159, 5), (0, 12)]], {9: 1}), 331: ([[(42, 1), (44, 2), (160, 3)], [(27, 4), (46, 5), (0, 1)], [(27, 6)], [(48, 7), (46, 8), (0, 3)], [(46, 5), (0, 4)], [(27, 9), (44, 2)], [(0, 6)], [(45, 10)], [(42, 1), (44, 2), (160, 3), (0, 8)], [(48, 11), (46, 5), (0, 9)], [(46, 8), (0, 10)], [(45, 4)]], {42: 1, 27: 1, 44: 1, 13: 1}), 332: ([[(13, 1), (27, 2)], [(161, 3)], [(0, 2)], [(52, 2)]], {27: 1, 13: 1}), 333: ([[(160, 1)], [(46, 2), (0, 1)], [(160, 1), (0, 2)]], {27: 1, 13: 1}), 334: ([[(26, 1)], [(45, 2)], [(70, 3)], [(71, 4)], [(115, 5), (0, 4)], [(70, 6)], [(71, 7)], [(0, 7)]], {26: 1}), 335: ([[(45, 1)], [(101, 2), (0, 1)], [(87, 3)], [(0, 3)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 19: 1, 20: 1, 22: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 336: ([[(36, 1)], [(162, 2)], [(70, 3), (46, 1)], [(71, 4)], [(0, 4)]], {36: 1}), 337: ([[(163, 1)], [(164, 0), (0, 1)]], {5: 1, 6: 1, 8: 1, 13: 1, 18: 1, 20: 1, 27: 1, 37: 1, 30: 1, 31: 1}), 338: ([[(12, 1)], [(72, 2), (0, 1)], [(0, 2)]], {12: 1}), 339: ([[(54, 1)], [(0, 1)]], {12: 1})}
    labels = [(0, 'EMPTY'), (4, None), (0, None), (319, None), (1, 'import'), (32, None), (2, None), (1, 'def'), (25, None), (1, 'try'), (1, 'return'), (1, 'assert'), (1, 'yield'), (7, None), (1, 'break'), (1, 'continue'), (50, None), (1, 'raise'), (3, None), (1, 'not'), (26, None), (1, 'class'), (1, 'lambda'), (1, 'print'), (1, 'nonlocal'), (1, 'exec'), (1, 'while'), (1, None), (1, 'del'), (1, 'pass'), (15, None), (9, None), (1, 'global'), (1, 'for'), (1, 'from'), (1, 'if'), (1, 'with'), (14, None), (314, None), (19, None), (304, None), (1, 'and'), (16, None), (260, None), (36, None), (324, None), (12, None), (292, None), (22, None), (323, None), (303, None), (10, None), (8, None), (327, None), (338, None), (278, None), (27, None), (326, None), (46, None), (39, None), (41, None), (47, None), (42, None), (43, None), (37, None), (44, None), (49, None), (45, None), (38, None), (40, None), (11, None), (322, None), (325, None), (287, None), (1, 'in'), (328, None), (269, None), (306, None), (268, None), (267, None), (29, None), (21, None), (28, None), (30, None), (1, 'is'), (31, None), (20, None), (285, None), (270, None), (330, None), (296, None), (290, None), (266, None), (336, None), (334, None), (291, None), (274, None), (276, None), (281, None), (259, None), (275, None), (1, 'as'), (279, None), (23, None), (1, 'except'), (337, None), (18, None), (264, None), (310, None), (288, None), (265, None), (273, None), (312, None), (313, None), (339, None), (1, 'else'), (308, None), (307, None), (294, None), (293, None), (1, 'elif'), (297, None), (298, None), (280, None), (300, None), (299, None), (331, None), (271, None), (305, None), (258, None), (1, 'or'), (263, None), (329, None), (35, None), (261, None), (34, None), (318, None), (13, None), (315, None), (272, None), (289, None), (262, None), (301, None), (309, None), (311, None), (277, None), (284, None), (295, None), (286, None), (317, None), (320, None), (5, None), (6, None), (48, None), (17, None), (24, None), (302, None), (321, None), (283, None), (1, 'finally'), (332, None), (333, None), (335, None), (257, None), (33, None)]
    keywords = {'and': 41, 'elif': 120, 'is': 84, 'global': 32, 'as': 101, 'pass': 29, 'if': 35, 'from': 34, 'raise': 17, 'for': 33, 'except': 104, 'nonlocal': 24, 'finally': 159, 'print': 23, 'import': 4, 'return': 10, 'exec': 25, 'else': 115, 'assert': 11, 'not': 19, 'with': 36, 'class': 21, 'break': 14, 'in': 74, 'yield': 12, 'try': 9, 'while': 26, 'continue': 15, 'del': 28, 'or': 130, 'def': 7, 'lambda': 22}
    tokens = {0: 2, 1: 27, 2: 6, 3: 18, 4: 1, 5: 151, 6: 152, 7: 13, 8: 52, 9: 31, 10: 51, 11: 70, 12: 46, 13: 137, 14: 37, 15: 30, 16: 42, 17: 154, 18: 106, 19: 39, 20: 86, 21: 81, 22: 48, 23: 103, 24: 155, 25: 8, 26: 20, 27: 56, 28: 82, 29: 80, 30: 83, 31: 85, 32: 5, 33: 164, 34: 135, 35: 133, 36: 44, 37: 64, 38: 68, 39: 59, 40: 69, 41: 60, 42: 62, 43: 63, 44: 65, 45: 67, 46: 58, 47: 61, 48: 153, 49: 66, 50: 16}
    symbol2label = {'print_stmt': 144, 'dotted_as_names': 123, 'import_as_name': 121, 'vfplist': 161, 'try_stmt': 89, 'small_stmt': 136, 'augassign': 107, 'argument': 43, 'import_as_names': 122, 'expr_stmt': 148, 'return_stmt': 113, 'not_test': 40, 'flow_stmt': 140, 'except_clause': 158, 'listmaker': 50, 'old_test': 77, 'arglist': 99, 'import_from': 125, 'gen_iter': 118, 'break_stmt': 110, 'del_stmt': 145, 'comp_op': 88, 'raise_stmt': 112, 'atom': 131, 'parameters': 116, 'old_lambdef': 128, 'continue_stmt': 111, 'shift_expr': 38, 'dotted_as_name': 102, 'testlist_gexp': 53, 'exec_stmt': 146, 'factor': 109, 'test': 45, 'testlist_safe': 75, 'subscript': 150, 'vfpdef': 160, 'decorators': 97, 'compound_stmt': 139, 'and_expr': 163, 'dotted_name': 98, 'dictsetmaker': 55, 'yield_expr': 54, 'power': 108, 'simple_stmt': 138, 'gen_for': 47, 'subscriptlist': 157, 'testlist': 72, 'comp_if': 78, 'stmt': 3, 'classdef': 92, 'assert_stmt': 141, 'for_stmt': 91, 'trailer': 132, 'and_test': 129, 'lambdef': 156, 'suite': 71, 'funcdef': 95, 'decorated': 96, 'xor_expr': 105, 'gen_if': 119, 'exprlist': 73, 'decorator': 100, 'pass_stmt': 143, 'sliceop': 149, 'comparison': 127, 'term': 49, 'with_item': 162, 'if_stmt': 90, 'arith_expr': 134, 'global_stmt': 147, 'expr': 87, 'import_name': 124, 'or_test': 117, 'with_stmt': 93, 'while_stmt': 94, 'varargslist': 126, 'testlist1': 57, 'comp_for': 79, 'import_stmt': 142, 'comp_iter': 76, 'yield_stmt': 114}
    start = 256
    opmap = {'>=': 31, '>>': 35, '*=': 39, '<>': 29, '<<': 34, '<=': 30, '%=': 41, '//=': 49, '!=': 29, '%': 24, '^=': 44, '<<=': 45, '&': 19, ')': 8, '(': 7, '+': 14, '*': 16, '-': 15, ',': 12, '/': 17, '.': 23, '>>=': 46, ';': 13, ':': 11, '=': 22, '<': 20, '>': 21, '@': 50, '**=': 47, '==': 28, '|=': 43, '&=': 42, '**': 36, '[': 9, ']': 10, '^': 33, '//': 48, '`': 25, '/=': 40, '-=': 38, '{': 26, '->': 54, '}': 27, '|': 18, '+=': 37, '~': 32}
