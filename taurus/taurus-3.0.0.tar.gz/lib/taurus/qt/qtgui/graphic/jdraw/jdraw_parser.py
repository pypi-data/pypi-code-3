#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""This module parses jdraw files"""

__all__ = ["parse"]

import os,re,traceback

import ply.lex as lex
import ply.yacc as yacc

from jdraw import *
from taurus.core.util import Logger

tokens = ( 'NUMBER', 'SYMBOL', 'LBRACKET', 'RBRACKET', 'TWOP', 'COMMA',
'JDFILE', 'GLOBAL', 'JDLINE', 'JDRECTANGLE', 'JDROUNDRECTANGLE',
'JDGROUP', 'JDELLIPSE', 'JDBAR', 'JDSWINGOBJECT', 'JDLABEL', 'JDPOLYLINE', 
'JDIMAGE', 'JDAXIS', 'JDSLIDER', 'TEXT', 
'true', 'false',
)

t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_TWOP = r'\:'
t_COMMA = r'\,'

t_TEXT = r'\"[^"]*\"'

reserved = {
'JDFile' : 'JDFILE',
'Global' : 'GLOBAL',
'JDLine' : 'JDLINE',
'JDRectangle' : 'JDRECTANGLE',
'JDRoundRectangle' : 'JDROUNDRECTANGLE',
'JDGroup' : 'JDGROUP',
'JDEllipse' : 'JDELLIPSE',
'JDBar' : 'JDBAR',
'JDSwingObject' : 'JDSWINGOBJECT',
'JDLabel' : 'JDLABEL',
'JDPolyline' : 'JDPOLYLINE',
'JDImage' : 'JDIMAGE',
'JDAxis' : 'JDAXIS',
'JDSlider' : 'JDSLIDER',
'JDSpline' : 'JDSPLINE',
'true' : 'true',
'false' : 'false',

}

def t_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'SYMBOL')    # Check for reserved words
    return t


def t_NUMBER(t):
    r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
    try:
        t.value = float(t.value)
    except:
        t.lexer.log.info("[%d]: Number %s is not valid!" % (t.lineno,t.value))
        t.value = 0
    return t
    
# Ignored characters 
t_ignore = " \t"

def t_newline(t):
    r'\n+' 
    t.lexer.lineno += t.value.count("\n") 
    
def t_error(t): 
    t.lexer.log.info("[%d]: Illegal character '%s'" % (t.lexer.lineno,t.value[0]))
    t.lexer.skip(1)

def p_error(p):
    p.lexer.log.error("[%d]: Syntax error in input [%s]" % (p.lexer.lineno,(str(p))))
    
#-------------------------------------------------------------------------------
# Yacc Starting symbol
#-------------------------------------------------------------------------------
def p_jdfile(p):
    ''' jdfile :  JDFILE SYMBOL LBRACKET global element_list RBRACKET '''
    factory = p.parser.factory
    p[0] = factory.getSceneObj(p[5])
    
    if p[0] is None:
        p.parser.log.info("[%d]: Unable to create Scene" % p.lexer.lineno)
    
def p_jdfile_empty(p):
    ''' jdfile : JDFILE LBRACKET global RBRACKET '''
    factory = p.parser.factory
    p[0] = factory.getSceneObj([])
    
    if p[0] is None:
        p.parser.log.info("[%d]: Unable to create Scene" % p.lexer.lineno)

def p_global(p):
    ''' global : GLOBAL LBRACKET RBRACKET
               | GLOBAL LBRACKET parameter_list RBRACKET'''
    if len(p) == 4:
        p[0] = {}
    else:
        p[0] = p[3]

def p_element_list(p):
    '''element_list : element_list element '''
    if not p[2] is None:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = p[1]

def p_element(p):
    '''element_list : element '''
    p[0] = [p[1]]

def p_single_element(p):
    '''element : obj LBRACKET RBRACKET
               | obj LBRACKET parameter_list RBRACKET'''
    
    #elems = None
    if len(p) == 4:
        p[3] = {}
    
    # determine the model name 
    name = p[3].get('name')
    
    #change name: if item has no name it should take the name of its nearest-named-parent
    keywords = ['JDGroup']+[n.replace('JD','') for n in reserved]
    if not name or name in keywords:
        p[3]['name'] = name = ""
        #print '\t name is empty, checking stack: %s' % [str(s) for s in reversed(p.parser.modelStack)]
        for model in reversed(p.parser.modelStack):
            if model and model not in keywords:
                p[3]['name'] = name = model
                break
    
    extension = p[3].get("extensions")     
    if p.parser.modelStack2:
        if extension is None:
            p[3]["extensions"]=p.parser.modelStack2[0]
        elif len(p.parser.modelStack2)==2:
            extension.update(p.parser.modelStack2[0])
            p[3]["extensions"] = extension

    # create the corresponding element
    factory = p.parser.factory
    ret = factory.getObj(p[1],p[3])
 
    if ret is None:
        p.parser.log.info("[%d]: Unable to create obj '%s'" % (p.lexer.lineno,p[1]))
    
    # clear the model stack 
    # if name:
    p.parser.modelStack.pop()
    if extension:
        p.parser.modelStack2.pop()

    #extension = p[3].get("extensions") 
    p[0] = ret
    
def p_obj(p):
    '''obj : JDLINE
           | JDRECTANGLE
           | JDROUNDRECTANGLE
           | JDGROUP
           | JDELLIPSE
           | JDBAR
           | JDSWINGOBJECT
           | JDLABEL
           | JDPOLYLINE
           | JDIMAGE
           | JDAXIS
           | JDSLIDER'''
    p[0] = p[1]

def p_parameter_list(p):
    '''parameter_list : parameter_list parameter'''
    p[0] = p[1]
    p[0].update(p[2])

def p_parameter(p):
    '''parameter_list : parameter'''
    p[0] = p[1] 
                           
def p_single_parameter(p):
    '''parameter : SYMBOL TWOP param_value'''
    if p[1] == 'name':
       # if p[3]:
       p.parser.modelStack.append(p[3])
    if p[1] == 'extensions':
        p.parser.modelStack2.append(p[3])
    p[0] = { p[1] : p[3] }

def p_complex_parameter(p):
    '''parameter : SYMBOL TWOP LBRACKET RBRACKET
                 | SYMBOL TWOP LBRACKET parameter_list RBRACKET
                 | SYMBOL TWOP LBRACKET element_list RBRACKET'''
    if len(p) == 5:
        p[4] = []
    p[0] = { p[1] : p[4] }
    if p[1] == 'extensions':
        p.parser.modelStack2.append(p[4])

def p_param_value_number_list(p):
    '''param_value : value_list '''
    if len(p[1]) == 1:
        p[0] = p[1][0]
    else:
        p[0] = p[1]

def p_value_list(p):
    ''' value_list : value_list COMMA value '''
    p[0] = p[1] + [p[3]]

def p_value_list_value(p):
    ''' value_list : value '''
    p[0] = [p[1]]

def p_value_number(p):
    '''value : NUMBER'''
    p[0] = p[1]

def p_value_text(p):
    '''value : TEXT'''
    p[0] = p[1].strip('"')
    
def p_value_bool(p):
    '''value : true
             | false'''
    p[0] = p[1] == 'true'

def parse(filename,factory):
    l = lex.lex()
    p = yacc.yacc()
    p.factory = factory
    p.modelStack = []
    p.modelStack2 = []
    p.log = Logger('JDraw Parser')
    l.log = p.log
    res = None
    try:
        filename = os.path.realpath(filename)
        f = open(filename)
        res = yacc.parse(f.read())
    except:
        p.log.warning("Failed to parse %s" % filename)
        #p.log.traceback()
        p.log.warning(traceback.format_exc())
    return res
    
#if __name__ == '__main__':
#    res = parse("jd1.jdw",jdraw.JDrawTaurusGraphicsFactory(self))

