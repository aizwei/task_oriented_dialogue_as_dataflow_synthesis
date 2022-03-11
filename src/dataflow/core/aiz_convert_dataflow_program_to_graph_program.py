from hashlib import new
from dataflow.core.program import BuildStructOp, CallLikeOp, Expression, Program, ValueOp
from typing import Callable, Dict, List, Tuple
from lispress_to_graph_program import lispress_specific
from lispress_to_graph_program import reset_state, log_state


# Creating some wrapper functions with type declarations so that I can lean on the IDE to remind myself
# what the arguments of each of these functions should be.
CREATE_ARGUMENT_FUNCTION_INDEX = 0
EMPTY_ARGUMENTS_FUNCTION_INDEX = 1
PREPEND_ARGUMENT_FUNCTION_INDEX = 2
ADD_LISPRESS_FUNCTION_FUNCTION_INDEX = 3
def graph_program_create_argument(subtype: int) -> Tuple[str,Tuple[int]]:
    # returns a tuple of the form ('DataNodeId', (4,))
    function: Callable = lispress_specific[CREATE_ARGUMENT_FUNCTION_INDEX]
    return function(subtype)
def graph_program_empty_arguments() -> List:
    function: Callable = lispress_specific[EMPTY_ARGUMENTS_FUNCTION_INDEX]
    return function()
def graph_program_prepend_argument(new_argument_id: Tuple[str,Tuple[int]], existing_arguments_list: List):
    function: Callable = lispress_specific[PREPEND_ARGUMENT_FUNCTION_INDEX]
    return function(new_argument_id, existing_arguments_list)
def graph_program_add_lispress_function(subtype: int, argument_list: List):
    function: Callable = lispress_specific[ADD_LISPRESS_FUNCTION_FUNCTION_INDEX]
    return function(subtype, argument_list)

# we only store numeric values in the graph for now. To store a string, I will hash it, and then
# add hash -> string into this dict. Any numeric argument which is present as a key in this dictionary
# should be assumed to be a hash of the real value, and the string should be used instead when comparing
# to lispress.
hash_to_string: Dict[int, str] = {}

# List of valid functions present in the lispress training data, and thus available to be included in a graph program
action_list = ['']

print(f"Printing action list {action_list}")

# We refer to actions by their index in the action_list when actually passing them as arguments to the add_lispress_function
# method, so we add the function -> index entries to a dictionary for easy lookup.
action_to_id_in_action_list: Dict[str, int] = {action:i for i, action in enumerate(action_list)}
print(f"Printing action to index dict: {action_to_id_in_action_list}")

class GraphProgramStep:
    """
    Dummy class representing a single step in a graph program.
    If this isn't possible, we can make this GraphProgramSegment or something similar,
    and convert each dataflow expression into 1 or more steps within a segment. That
    may make more sense, but if we can add the primitives necessary to make this mapping
    1:1, it may make our lives a lot more straightforward.
    """
    def __init__(self) -> None:
        pass

def convert_build_struct_op(dataflow_expression: Expression) -> GraphProgramStep:
    """
    Convert a dataflow build struct op into a graph program step.
    """
    pass

def convert_call_like_op(dataflow_expression: Expression) -> GraphProgramStep:
    """
    Convert a dataflow call like op into a graph program step.
    """
    pass

def convert_value_op(dataflow_expression: Expression) -> GraphProgramStep:
    """
    Convert a dataflow value op into a graph program step.
    """
    pass


def find_expressions_for_graph_program_step(step: str) -> Expression:
    """
    Convert graph program step into a corresponding dataflow expression.
    """
    pass


if __name__ == "__main__":
    dataflow_program: Program = None # TODO: read in program from file as argument
    print(f"Attempting to convert dataflow program {dataflow_program.expressions_by_id} into a Graph Program!")

    # convert dataflow program to graph program
    graph_program_steps = []
    next_expression: Expression = None
    for expression in dataflow_program.expressions:
        next_expression = expression
        if type(next_expression.op == ValueOp):
            graph_program_steps.append(convert_value_op(dataflow_expression=next_expression))
        elif type(next_expression.op == CallLikeOp):
            graph_program_steps.append(convert_call_like_op(dataflow_expression=next_expression))
        elif type(next_expression.op == BuildStructOp):
            graph_program_steps.append(convert_build_struct_op(dataflow_expression=next_expression))
        else:
            raise Exception(f"Operation type {next_expression.op} not expected!")

    expressions = []
    for step in graph_program_steps:
        next_expressions = find_expressions_for_graph_program_step(step)
        expressions.append(next_expressions)

    resulting_program = Program(expressions=expressions)

    assert resulting_program == dataflow_program, "Programs do not match! Investigate this test case."

    # TODO: write graph_program_steps to file if that assert passes, this appears to be a valid translation
