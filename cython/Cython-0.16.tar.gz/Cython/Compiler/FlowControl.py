import cython
cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, ModuleNode=object,
               LetNode=object, LetRefNode=object, TreeFragment=object,
               TemplateTransform=object, EncodedString=object,
               error=object, warning=object, copy=object)

import Builtin
import ExprNodes
import Nodes
from PyrexTypes import py_object_type

from Visitor import TreeVisitor, CythonTransform
from Errors import error, warning, InternalError

class TypedExprNode(ExprNodes.ExprNode):
    # Used for declaring assignments of a specified type without a known entry.
    def __init__(self, type, may_be_none=None):
        self.type = type
        self._may_be_none = may_be_none

    def may_be_none(self):
        return self._may_be_none != False

object_expr = TypedExprNode(py_object_type, may_be_none=True)
object_expr_not_none = TypedExprNode(py_object_type, may_be_none=False)

class ControlBlock(object):
    """Control flow graph node. Sequence of assignments and name references.

       children  set of children nodes
       parents   set of parent nodes
       positions set of position markers

       stats     list of block statements
       gen       dict of assignments generated by this block
       bounded   set  of entries that are definitely bounded in this block

       Example:

        a = 1
        b = a + c # 'c' is already bounded or exception here

        stats = [Assignment(a), NameReference(a), NameReference(c),
                     Assignment(b)]
        gen = {Entry(a): Assignment(a), Entry(b): Assignment(b)}
        bounded = set([Entry(a), Entry(c)])

    """

    def __init__(self):
        self.children = set()
        self.parents = set()
        self.positions = set()

        self.stats = []
        self.gen = {}
        self.bounded = set()

        self.i_input = 0
        self.i_output = 0
        self.i_gen = 0
        self.i_kill = 0
        self.i_state = 0

    def empty(self):
        return (not self.stats and not self.positions)

    def detach(self):
        """Detach block from parents and children."""
        for child in self.children:
            child.parents.remove(self)
        for parent in self.parents:
            parent.children.remove(self)
        self.parents.clear()
        self.children.clear()

    def add_child(self, block):
        self.children.add(block)
        block.parents.add(self)


class ExitBlock(ControlBlock):
    """Non-empty exit point block."""

    def empty(self):
        return False


class AssignmentList:
    def __init__(self):
        self.stats = []


class ControlFlow(object):
    """Control-flow graph.

       entry_point ControlBlock entry point for this graph
       exit_point  ControlBlock normal exit point
       block       ControlBlock current block
       blocks      set    children nodes
       entries     set    tracked entries
       loops       list   stack for loop descriptors
       exceptions  list   stack for exception descriptors

    """

    def __init__(self):
        self.blocks = set()
        self.entries = set()
        self.loops = []
        self.exceptions = []

        self.entry_point = ControlBlock()
        self.exit_point = ExitBlock()
        self.blocks.add(self.exit_point)
        self.block = self.entry_point

    def newblock(self, parent=None):
        """Create floating block linked to `parent` if given.

           NOTE: Block is NOT added to self.blocks
        """
        block = ControlBlock()
        self.blocks.add(block)
        if parent:
            parent.add_child(block)
        return block

    def nextblock(self, parent=None):
        """Create block children block linked to current or `parent` if given.

           NOTE: Block is added to self.blocks
        """
        block = ControlBlock()
        self.blocks.add(block)
        if parent:
            parent.add_child(block)
        elif self.block:
            self.block.add_child(block)
        self.block = block
        return self.block

    def is_tracked(self, entry):
        if entry.is_anonymous:
            return False
        if (entry.type.is_array or entry.type.is_struct_or_union or
                entry.type.is_cpp_class):
            return False
        return (entry.is_local or entry.is_pyclass_attr or entry.is_arg or
                entry.from_closure or entry.in_closure or
                entry.error_on_uninitialized)

    def mark_position(self, node):
        """Mark position, will be used to draw graph nodes."""
        if self.block:
            self.block.positions.add(node.pos[:2])

    def mark_assignment(self, lhs, rhs, entry):
        if self.block:
            if not self.is_tracked(entry):
                return
            assignment = NameAssignment(lhs, rhs, entry)
            self.block.stats.append(assignment)
            self.block.gen[entry] = assignment
            self.entries.add(entry)

    def mark_argument(self, lhs, rhs, entry):
        if self.block and self.is_tracked(entry):
            assignment = Argument(lhs, rhs, entry)
            self.block.stats.append(assignment)
            self.block.gen[entry] = assignment
            self.entries.add(entry)

    def mark_deletion(self, node, entry):
        if self.block and self.is_tracked(entry):
            assignment = NameAssignment(node, None, entry)
            self.block.stats.append(assignment)
            self.block.gen[entry] = Uninitialized
            self.entries.add(entry)

    def mark_reference(self, node, entry):
        if self.block and self.is_tracked(entry):
            self.block.stats.append(NameReference(node, entry))
            # Local variable is definitely bound after this reference
            if not node.allow_null:
                self.block.bounded.add(entry)
            self.entries.add(entry)

    def normalize(self):
        """Delete unreachable and orphan blocks."""
        queue = set([self.entry_point])
        visited = set()
        while queue:
            root = queue.pop()
            visited.add(root)
            for child in root.children:
                if child not in visited:
                    queue.add(child)
        unreachable = self.blocks - visited
        for block in unreachable:
            block.detach()
        visited.remove(self.entry_point)
        for block in visited:
            if block.empty():
                for parent in block.parents: # Re-parent
                    for child in block.children:
                        parent.add_child(child)
                block.detach()
                unreachable.add(block)
        self.blocks -= unreachable

    def initialize(self):
        """Set initial state, map assignments to bits."""
        self.assmts = {}

        offset = 0
        for entry in self.entries:
            assmts = AssignmentList()
            assmts.bit = 1 << offset
            assmts.mask = assmts.bit
            self.assmts[entry] = assmts
            offset += 1

        for block in self.blocks:
            for stat in block.stats:
                if isinstance(stat, NameAssignment):
                    stat.bit = 1 << offset
                    assmts = self.assmts[stat.entry]
                    assmts.stats.append(stat)
                    assmts.mask |= stat.bit
                    offset += 1

        for block in self.blocks:
            for entry, stat in block.gen.items():
                assmts = self.assmts[entry]
                if stat is Uninitialized:
                    block.i_gen |= assmts.bit
                else:
                    block.i_gen |= stat.bit
                block.i_kill |= assmts.mask
            block.i_output = block.i_gen
            for entry in block.bounded:
                block.i_kill |= self.assmts[entry].bit

        for assmts in self.assmts.itervalues():
            self.entry_point.i_gen |= assmts.bit
        self.entry_point.i_output = self.entry_point.i_gen

    def map_one(self, istate, entry):
        ret = set()
        assmts = self.assmts[entry]
        if istate & assmts.bit:
            ret.add(Uninitialized)
        for assmt in assmts.stats:
            if istate & assmt.bit:
                ret.add(assmt)
        return ret

    def reaching_definitions(self):
        """Per-block reaching definitions analysis."""
        dirty = True
        while dirty:
            dirty = False
            for block in self.blocks:
                i_input = 0
                for parent in block.parents:
                    i_input |= parent.i_output
                i_output = (i_input & ~block.i_kill) | block.i_gen
                if i_output != block.i_output:
                    dirty = True
                block.i_input = i_input
                block.i_output = i_output


class LoopDescr(object):
    def __init__(self, next_block, loop_block):
        self.next_block = next_block
        self.loop_block = loop_block
        self.exceptions = []


class ExceptionDescr(object):
    """Exception handling helper.

    entry_point   ControlBlock Exception handling entry point
    finally_enter ControlBlock Normal finally clause entry point
    finally_exit  ControlBlock Normal finally clause exit point
    """

    def __init__(self, entry_point, finally_enter=None, finally_exit=None):
        self.entry_point = entry_point
        self.finally_enter = finally_enter
        self.finally_exit = finally_exit

class NameAssignment(object):
    def __init__(self, lhs, rhs, entry):
        if lhs.cf_state is None:
            lhs.cf_state = set()
        self.lhs = lhs
        self.rhs = rhs
        self.entry = entry
        self.pos = lhs.pos
        self.refs = set()
        self.is_arg = False

    def __repr__(self):
        return '%s(entry=%r)' % (self.__class__.__name__, self.entry)

class Argument(NameAssignment):
    def __init__(self, lhs, rhs, entry):
        NameAssignment.__init__(self, lhs, rhs, entry)
        self.is_arg = True

class Uninitialized(object):
    pass

class NameReference(object):
    def __init__(self, node, entry):
        if node.cf_state is None:
            node.cf_state = set()
        self.node = node
        self.entry = entry
        self.pos = node.pos

    def __repr__(self):
        return '%s(entry=%r)' % (self.__class__.__name__, self.entry)


class ControlFlowState(list):
    # Keeps track of Node's entry assignments
    #
    # cf_is_null        [boolean] It is uninitialized
    # cf_maybe_null     [boolean] May be uninitialized
    # is_single         [boolean] Has only one assignment at this point

    cf_maybe_null = False
    cf_is_null = False
    is_single = False

    def __init__(self, state):
        if Uninitialized in state:
            state.discard(Uninitialized)
            self.cf_maybe_null = True
            if not state:
                self.cf_is_null = True
        else:
            if len(state) == 1:
                self.is_single = True
        super(ControlFlowState, self).__init__(state)

    def one(self):
        return self[0]


class GVContext(object):
    """Graphviz subgraph object."""

    def __init__(self):
        self.blockids = {}
        self.nextid = 0
        self.children = []
        self.sources = {}

    def add(self, child):
        self.children.append(child)

    def nodeid(self, block):
        if block not in self.blockids:
            self.blockids[block] = 'block%d' % self.nextid
            self.nextid += 1
        return self.blockids[block]

    def extract_sources(self, block):
        if not block.positions:
            return ''
        start = min(block.positions)
        stop = max(block.positions)
        srcdescr = start[0]
        if not srcdescr in self.sources:
            self.sources[srcdescr] = list(srcdescr.get_lines())
        lines = self.sources[srcdescr]
        return '\\n'.join([l.strip() for l in lines[start[1] - 1:stop[1]]])

    def render(self, fp, name, annotate_defs=False):
        """Render graphviz dot graph"""
        fp.write('digraph %s {\n' % name)
        fp.write(' node [shape=box];\n')
        for child in self.children:
            child.render(fp, self, annotate_defs)
        fp.write('}\n')

    def escape(self, text):
        return text.replace('"', '\\"').replace('\n', '\\n')


class GV(object):
    """Graphviz DOT renderer."""

    def __init__(self, name, flow):
        self.name = name
        self.flow = flow

    def render(self, fp, ctx, annotate_defs=False):
        fp.write(' subgraph %s {\n' % self.name)
        for block in self.flow.blocks:
            label = ctx.extract_sources(block)
            if annotate_defs:
                for stat in block.stats:
                    if isinstance(stat, NameAssignment):
                        label += '\n %s [definition]' % stat.entry.name
                    elif isinstance(stat, NameReference):
                        if stat.entry:
                            label += '\n %s [reference]' % stat.entry.name
            if not label:
                label = 'empty'
            pid = ctx.nodeid(block)
            fp.write('  %s [label="%s"];\n' % (pid, ctx.escape(label)))
        for block in self.flow.blocks:
            pid = ctx.nodeid(block)
            for child in block.children:
                fp.write('  %s -> %s;\n' % (pid, ctx.nodeid(child)))
        fp.write(' }\n')


class MessageCollection:
    """Collect error/warnings messages first then sort"""
    def __init__(self):
        self.messages = []

    def error(self, pos, message):
        self.messages.append((pos, True, message))

    def warning(self, pos, message):
        self.messages.append((pos, False, message))

    def report(self):
        self.messages.sort()
        for pos, is_error, message in self.messages:
            if is_error:
                error(pos, message)
            else:
                warning(pos, message, 2)


def check_definitions(flow, compiler_directives):
    flow.initialize()
    flow.reaching_definitions()

    # Track down state
    assignments = set()
    # Node to entry map
    references = {}
    assmt_nodes = set()

    for block in flow.blocks:
        i_state = block.i_input
        for stat in block.stats:
            i_assmts = flow.assmts[stat.entry]
            state = flow.map_one(i_state, stat.entry)
            if isinstance(stat, NameAssignment):
                stat.lhs.cf_state.update(state)
                assmt_nodes.add(stat.lhs)
                i_state = i_state & ~i_assmts.mask
                if stat.rhs:
                    i_state |= stat.bit
                else:
                    i_state |= i_assmts.bit
                assignments.add(stat)
                stat.entry.cf_assignments.append(stat)
            elif isinstance(stat, NameReference):
                references[stat.node] = stat.entry
                stat.entry.cf_references.append(stat)
                stat.node.cf_state.update(state)
                if not stat.node.allow_null:
                    i_state &= ~i_assmts.bit
                state.discard(Uninitialized)
                for assmt in state:
                    assmt.refs.add(stat)

    # Check variable usage
    warn_maybe_uninitialized = compiler_directives['warn.maybe_uninitialized']
    warn_unused_result = compiler_directives['warn.unused_result']
    warn_unused = compiler_directives['warn.unused']
    warn_unused_arg = compiler_directives['warn.unused_arg']

    messages = MessageCollection()

    # assignment hints
    for node in assmt_nodes:
        if Uninitialized in node.cf_state:
            node.cf_maybe_null = True
            if len(node.cf_state) == 1:
                node.cf_is_null = True
            else:
                node.cf_is_null = False
        else:
            node.cf_is_null = False
            node.cf_maybe_null = False

    # Find uninitialized references and cf-hints
    for node, entry in references.iteritems():
        if Uninitialized in node.cf_state:
            node.cf_maybe_null = True
            if not entry.from_closure and len(node.cf_state) == 1:
                node.cf_is_null = True
            if node.allow_null or entry.from_closure or entry.is_pyclass_attr:
                pass # Can be uninitialized here
            elif node.cf_is_null:
                if (entry.type.is_pyobject or entry.type.is_unspecified or
                        entry.error_on_uninitialized):
                    messages.error(
                        node.pos,
                        "local variable '%s' referenced before assignment"
                        % entry.name)
                else:
                    messages.warning(
                        node.pos,
                        "local variable '%s' referenced before assignment"
                        % entry.name)
            elif warn_maybe_uninitialized:
                messages.warning(
                    node.pos,
                    "local variable '%s' might be referenced before assignment"
                    % entry.name)
        else:
            node.cf_is_null = False
            node.cf_maybe_null = False

    # Unused result
    for assmt in assignments:
        if (not assmt.refs and not assmt.entry.is_pyclass_attr
            and not assmt.entry.in_closure):
            if assmt.entry.cf_references and warn_unused_result:
                if assmt.is_arg:
                    messages.warning(assmt.pos, "Unused argument value '%s'" %
                                     assmt.entry.name)
                else:
                    messages.warning(assmt.pos, "Unused result in '%s'" %
                                     assmt.entry.name)
            assmt.lhs.cf_used = False

    # Unused entries
    for entry in flow.entries:
        if (not entry.cf_references and not entry.is_pyclass_attr
            and not entry.in_closure):
            if entry.is_arg:
                if warn_unused_arg:
                    messages.warning(entry.pos, "Unused argument '%s'" %
                                     entry.name)
            else:
                if warn_unused:
                    messages.warning(entry.pos, "Unused entry '%s'" %
                                     entry.name)
            entry.cf_used = False

    messages.report()

    for node in assmt_nodes:
        node.cf_state = ControlFlowState(node.cf_state)
    for node in references:
        node.cf_state = ControlFlowState(node.cf_state)


class AssignmentCollector(TreeVisitor):
    def __init__(self):
        super(AssignmentCollector, self).__init__()
        self.assignments = []

    def visit_Node(self):
        self.visitchildren(self)

    def visit_SingleAssignmentNode(self, node):
        self.assignments.append((node.lhs, node.rhs))

    def visit_CascadedAssignmentNode(self, node):
        for lhs in node.lhs_list:
            self.assignments.append((lhs, node.rhs))


class ControlFlowAnalysis(CythonTransform):
    in_inplace_assignment = False

    def visit_ModuleNode(self, node):
        self.gv_ctx = GVContext()

        # Set of NameNode reductions
        self.reductions = set()

        self.env_stack = []
        self.env = node.scope
        self.stack = []
        self.flow = ControlFlow()
        self.visitchildren(node)

        check_definitions(self.flow, self.current_directives)

        dot_output = self.current_directives['control_flow.dot_output']
        if dot_output:
            annotate_defs = self.current_directives['control_flow.dot_annotate_defs']
            fp = open(dot_output, 'wt')
            try:
                self.gv_ctx.render(fp, 'module', annotate_defs=annotate_defs)
            finally:
                fp.close()
        return node

    def visit_FuncDefNode(self, node):
        for arg in node.args:
            if arg.default:
                self.visitchildren(arg)
        self.visitchildren(node, attrs=('decorators',))
        self.env_stack.append(self.env)
        self.env = node.local_scope
        self.stack.append(self.flow)
        self.flow = ControlFlow()

        # Collect all entries
        for entry in node.local_scope.entries.values():
            if self.flow.is_tracked(entry):
                self.flow.entries.add(entry)

        self.mark_position(node)
        # Function body block
        self.flow.nextblock()

        for arg in node.args:
            self.visit(arg)
        if node.star_arg:
            self.flow.mark_argument(node.star_arg,
                                    TypedExprNode(Builtin.tuple_type,
                                                  may_be_none=False),
                                    node.star_arg.entry)
        if node.starstar_arg:
            self.flow.mark_argument(node.starstar_arg,
                                    TypedExprNode(Builtin.dict_type,
                                                  may_be_none=False),
                                    node.starstar_arg.entry)
        self.visit(node.body)
        # Workaround for generators
        if node.is_generator:
            self.visit(node.gbody.body)

        # Exit point
        if self.flow.block:
            self.flow.block.add_child(self.flow.exit_point)

        # Cleanup graph
        self.flow.normalize()
        check_definitions(self.flow, self.current_directives)
        self.flow.blocks.add(self.flow.entry_point)

        self.gv_ctx.add(GV(node.local_scope.name, self.flow))

        self.flow = self.stack.pop()
        self.env = self.env_stack.pop()
        return node

    def visit_DefNode(self, node):
        node.used = True
        return self.visit_FuncDefNode(node)

    def visit_GeneratorBodyDefNode(self, node):
        return node

    def visit_CTypeDefNode(self, node):
        return node

    def mark_assignment(self, lhs, rhs=None):
        if not self.flow.block:
            return
        if self.flow.exceptions:
            exc_descr = self.flow.exceptions[-1]
            self.flow.block.add_child(exc_descr.entry_point)
            self.flow.nextblock()

        if not rhs:
            rhs = object_expr
        if lhs.is_name:
            if lhs.entry is not None:
                entry = lhs.entry
            else:
                entry = self.env.lookup(lhs.name)
            if entry is None: # TODO: This shouldn't happen...
                return
            self.flow.mark_assignment(lhs, rhs, entry)
        elif isinstance(lhs, ExprNodes.SequenceNode):
            for arg in lhs.args:
                self.mark_assignment(arg)
        else:
            self.visit(lhs)

        if self.flow.exceptions:
            exc_descr = self.flow.exceptions[-1]
            self.flow.block.add_child(exc_descr.entry_point)
            self.flow.nextblock()

    def mark_position(self, node):
        """Mark position if DOT output is enabled."""
        if self.current_directives['control_flow.dot_output']:
            self.flow.mark_position(node)

    def visit_FromImportStatNode(self, node):
        for name, target in node.items:
            if name != "*":
                self.mark_assignment(target)
        self.visitchildren(node)
        return node

    def visit_AssignmentNode(self, node):
        raise InternalError, "Unhandled assignment node"

    def visit_SingleAssignmentNode(self, node):
        self.visit(node.rhs)
        self.mark_assignment(node.lhs, node.rhs)
        return node

    def visit_CascadedAssignmentNode(self, node):
        self.visit(node.rhs)
        for lhs in node.lhs_list:
            self.mark_assignment(lhs, node.rhs)
        return node

    def visit_ParallelAssignmentNode(self, node):
        collector = AssignmentCollector()
        collector.visitchildren(node)
        for lhs, rhs in collector.assignments:
            self.visit(rhs)
        for lhs, rhs in collector.assignments:
            self.mark_assignment(lhs, rhs)
        return node

    def visit_InPlaceAssignmentNode(self, node):
        self.in_inplace_assignment = True
        self.visitchildren(node)
        self.in_inplace_assignment = False
        self.mark_assignment(node.lhs, node.create_binop_node())
        return node

    def visit_DelStatNode(self, node):
        for arg in node.args:
            if arg.is_name:
                entry = arg.entry or self.env.lookup(arg.name)
                if entry.in_closure or entry.from_closure:
                    error(arg.pos,
                          "can not delete variable '%s' "
                          "referenced in nested scope" % entry.name)
                # Mark reference
                self.visit(arg)
                self.flow.mark_deletion(arg, entry)
        return node

    def visit_CArgDeclNode(self, node):
        entry = self.env.lookup(node.name)
        if entry:
            may_be_none = not node.not_none
            self.flow.mark_argument(node, TypedExprNode(entry.type, may_be_none), entry)
        return node

    def visit_NameNode(self, node):
        if self.flow.block:
            entry = node.entry or self.env.lookup(node.name)
            if entry:
                self.flow.mark_reference(node, entry)

                if entry in self.reductions and not self.in_inplace_assignment:
                    error(node.pos,
                          "Cannot read reduction variable in loop body")

        return node

    def visit_StatListNode(self, node):
        if self.flow.block:
            for stat in node.stats:
                self.visit(stat)
                if not self.flow.block:
                    stat.is_terminator = True
                    break
        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        self.mark_position(node)
        return node

    def visit_IfStatNode(self, node):
        next_block = self.flow.newblock()
        parent = self.flow.block
        # If clauses
        for clause in node.if_clauses:
            parent = self.flow.nextblock(parent)
            self.visit(clause.condition)
            self.flow.nextblock()
            self.visit(clause.body)
            if self.flow.block:
                self.flow.block.add_child(next_block)
        # Else clause
        if node.else_clause:
            self.flow.nextblock(parent=parent)
            self.visit(node.else_clause)
            if self.flow.block:
                self.flow.block.add_child(next_block)
        else:
            parent.add_child(next_block)

        if next_block.parents:
            self.flow.block = next_block
        else:
            self.flow.block = None
        return node

    def visit_WhileStatNode(self, node):
        condition_block = self.flow.nextblock()
        next_block = self.flow.newblock()
        # Condition block
        self.flow.loops.append(LoopDescr(next_block, condition_block))
        self.visit(node.condition)
        # Body block
        self.flow.nextblock()
        self.visit(node.body)
        self.flow.loops.pop()
        # Loop it
        if self.flow.block:
            self.flow.block.add_child(condition_block)
            self.flow.block.add_child(next_block)
        # Else clause
        if node.else_clause:
            self.flow.nextblock(parent=condition_block)
            self.visit(node.else_clause)
            if self.flow.block:
                self.flow.block.add_child(next_block)
        else:
            condition_block.add_child(next_block)

        if next_block.parents:
            self.flow.block = next_block
        else:
            self.flow.block = None
        return node

    def visit_ForInStatNode(self, node):
        condition_block = self.flow.nextblock()
        next_block = self.flow.newblock()
        # Condition with iterator
        self.flow.loops.append(LoopDescr(next_block, condition_block))
        self.visit(node.iterator)
        # Target assignment
        self.flow.nextblock()
        self.mark_assignment(node.target)

        # Body block
        if isinstance(node, Nodes.ParallelRangeNode):
            # In case of an invalid
            self._delete_privates(node, exclude=node.target.entry)

        self.flow.nextblock()
        self.visit(node.body)
        self.flow.loops.pop()

        # Loop it
        if self.flow.block:
            self.flow.block.add_child(condition_block)
        # Else clause
        if node.else_clause:
            self.flow.nextblock(parent=condition_block)
            self.visit(node.else_clause)
            if self.flow.block:
                self.flow.block.add_child(next_block)
        else:
            condition_block.add_child(next_block)

        if next_block.parents:
            self.flow.block = next_block
        else:
            self.flow.block = None
        return node

    def _delete_privates(self, node, exclude=None):
        for private_node in node.assigned_nodes:
            if not exclude or private_node.entry is not exclude:
                self.flow.mark_deletion(private_node, private_node.entry)

    def visit_ParallelRangeNode(self, node):
        reductions = self.reductions

        # if node.target is None or not a NameNode, an error will have
        # been previously issued
        if hasattr(node.target, 'entry'):
            self.reductions = set(reductions)

            for private_node in node.assigned_nodes:
                private_node.entry.error_on_uninitialized = True
                pos, reduction = node.assignments[private_node.entry]
                if reduction:
                    self.reductions.add(private_node.entry)

            node = self.visit_ForInStatNode(node)

        self.reductions = reductions
        return node

    def visit_ParallelWithBlockNode(self, node):
        for private_node in node.assigned_nodes:
            private_node.entry.error_on_uninitialized = True

        self._delete_privates(node)
        self.visitchildren(node)
        self._delete_privates(node)

        return node

    def visit_ForFromStatNode(self, node):
        condition_block = self.flow.nextblock()
        next_block = self.flow.newblock()
        # Condition with iterator
        self.flow.loops.append(LoopDescr(next_block, condition_block))
        self.visit(node.bound1)
        self.visit(node.bound2)
        if node.step:
            self.visit(node.step)
        # Target assignment
        self.flow.nextblock()
        self.mark_assignment(node.target)

        # Body block
        self.flow.nextblock()
        self.visit(node.body)
        self.flow.loops.pop()
        # Loop it
        if self.flow.block:
            self.flow.block.add_child(condition_block)
        # Else clause
        if node.else_clause:
            self.flow.nextblock(parent=condition_block)
            self.visit(node.else_clause)
            if self.flow.block:
                self.flow.block.add_child(next_block)
        else:
            condition_block.add_child(next_block)

        if next_block.parents:
            self.flow.block = next_block
        else:
            self.flow.block = None
        return node

    def visit_LoopNode(self, node):
        raise InternalError, "Generic loops are not supported"

    def visit_WithTargetAssignmentStatNode(self, node):
        self.mark_assignment(node.lhs, node.rhs)
        return node

    def visit_WithStatNode(self, node):
        self.visit(node.manager)
        self.visit(node.enter_call)
        self.visit(node.body)
        return node

    def visit_TryExceptStatNode(self, node):
        # After exception handling
        next_block = self.flow.newblock()
        # Body block
        self.flow.newblock()
        # Exception entry point
        entry_point = self.flow.newblock()
        self.flow.exceptions.append(ExceptionDescr(entry_point))
        self.flow.nextblock()
        ## XXX: links to exception handling point should be added by
        ## XXX: children nodes
        self.flow.block.add_child(entry_point)
        self.visit(node.body)
        self.flow.exceptions.pop()

        # After exception
        if self.flow.block:
            if node.else_clause:
                self.flow.nextblock()
                self.visit(node.else_clause)
            if self.flow.block:
                self.flow.block.add_child(next_block)

        for clause in node.except_clauses:
            self.flow.block = entry_point
            if clause.pattern:
                for pattern in clause.pattern:
                    self.visit(pattern)
            else:
                # TODO: handle * pattern
                pass
            entry_point = self.flow.newblock(parent=self.flow.block)
            self.flow.nextblock()
            if clause.target:
                self.mark_assignment(clause.target)
            self.visit(clause.body)
            if self.flow.block:
                self.flow.block.add_child(next_block)

        if self.flow.exceptions:
            entry_point.add_child(self.flow.exceptions[-1].entry_point)

        if next_block.parents:
            self.flow.block = next_block
        else:
            self.flow.block = None
        return node

    def visit_TryFinallyStatNode(self, node):
        body_block = self.flow.nextblock()

        # Exception entry point
        entry_point = self.flow.newblock()
        self.flow.block = entry_point
        self.visit(node.finally_clause)

        if self.flow.block and self.flow.exceptions:
            self.flow.block.add_child(self.flow.exceptions[-1].entry_point)

        # Normal execution
        finally_enter = self.flow.newblock()
        self.flow.block = finally_enter
        self.visit(node.finally_clause)
        finally_exit = self.flow.block

        descr = ExceptionDescr(entry_point, finally_enter, finally_exit)
        self.flow.exceptions.append(descr)
        if self.flow.loops:
            self.flow.loops[-1].exceptions.append(descr)
        self.flow.block = body_block
        ## XXX: Is it still required
        body_block.add_child(entry_point)
        self.visit(node.body)
        self.flow.exceptions.pop()
        if self.flow.loops:
            self.flow.loops[-1].exceptions.pop()

        if self.flow.block:
            self.flow.block.add_child(finally_enter)
            if finally_exit:
                self.flow.block = self.flow.nextblock(parent=finally_exit)
            else:
                self.flow.block = None
        return node

    def visit_RaiseStatNode(self, node):
        self.mark_position(node)
        self.visitchildren(node)
        if self.flow.exceptions:
            self.flow.block.add_child(self.flow.exceptions[-1].entry_point)
        self.flow.block = None
        return node

    def visit_ReraiseStatNode(self, node):
        self.mark_position(node)
        if self.flow.exceptions:
            self.flow.block.add_child(self.flow.exceptions[-1].entry_point)
        self.flow.block = None
        return node

    def visit_ReturnStatNode(self, node):
        self.mark_position(node)
        self.visitchildren(node)

        for exception in self.flow.exceptions[::-1]:
            if exception.finally_enter:
                self.flow.block.add_child(exception.finally_enter)
                if exception.finally_exit:
                    exception.finally_exit.add_child(self.flow.exit_point)
                break
        else:
            if self.flow.block:
                self.flow.block.add_child(self.flow.exit_point)
        self.flow.block = None
        return node

    def visit_BreakStatNode(self, node):
        if not self.flow.loops:
            #error(node.pos, "break statement not inside loop")
            return node
        loop = self.flow.loops[-1]
        self.mark_position(node)
        for exception in loop.exceptions[::-1]:
            if exception.finally_enter:
                self.flow.block.add_child(exception.finally_enter)
                if exception.finally_exit:
                    exception.finally_exit.add_child(loop.next_block)
                break
        else:
            self.flow.block.add_child(loop.next_block)
        self.flow.block = None
        return node

    def visit_ContinueStatNode(self, node):
        if not self.flow.loops:
            #error(node.pos, "continue statement not inside loop")
            return node
        loop = self.flow.loops[-1]
        self.mark_position(node)
        for exception in loop.exceptions[::-1]:
            if exception.finally_enter:
                self.flow.block.add_child(exception.finally_enter)
                if exception.finally_exit:
                    exception.finally_exit.add_child(loop.loop_block)
                break
        else:
            self.flow.block.add_child(loop.loop_block)
        self.flow.block = None
        return node

    def visit_ComprehensionNode(self, node):
        if node.expr_scope:
            self.env_stack.append(self.env)
            self.env = node.expr_scope
        # Skip append node here
        self.visit(node.target)
        self.visit(node.loop)
        if node.expr_scope:
            self.env = self.env_stack.pop()
        return node

    def visit_ScopedExprNode(self, node):
        if node.expr_scope:
            self.env_stack.append(self.env)
            self.env = node.expr_scope
        self.visitchildren(node)
        if node.expr_scope:
            self.env = self.env_stack.pop()
        return node

    def visit_PyClassDefNode(self, node):
        self.visitchildren(node, attrs=('dict', 'metaclass',
                                        'mkw', 'bases', 'class_result'))
        self.flow.mark_assignment(node.target, object_expr_not_none,
                                  self.env.lookup(node.name))
        self.env_stack.append(self.env)
        self.env = node.scope
        self.flow.nextblock()
        self.visitchildren(node, attrs=('body',))
        self.flow.nextblock()
        self.env = self.env_stack.pop()
        return node

    def visit_AmpersandNode(self, node):
        if node.operand.is_name:
            # Fake assignment to silence warning
            self.mark_assignment(node.operand)
        self.visitchildren(node)
        return node
