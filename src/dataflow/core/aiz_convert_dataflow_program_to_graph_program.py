from hashlib import new
from dataflow.core.program import BuildStructOp, CallLikeOp, Expression, Program, ValueOp
from typing import Callable, Dict, List, Tuple
from lispress_to_graph_program import *
from lispress_to_graph_program import reset_state, log_state
from dataflow.core.dialogue import Dialogue, Turn
from dataflow.core.lispress import Lispress, lispress_to_program, parse_lispress, render_pretty
from dataflow.core.program import BuildStructOp, ValueOp, CallLikeOp, Expression, Program

from dataflow.core.io_utils import load_jsonl_file
import os
import json
import argparse

STRING_DATA_NODE_SUBTYPE = 2
NUMERIC_DATA_NODE_SUBTYPE = 1
EMPTY_DATA_NODE_SUBTYPE = 0

EMPTY_DATA_NODE_DUMMY_VALUE = -1 # required because we dont have support for creating an argument with no value yet, this value means the data node is an output data node

# Creating some wrapper functions with type declarations so that I can lean on the IDE to remind myself
# what the arguments of each of these functions should be.
CREATE_ARGUMENT_FUNCTION_INDEX = 0
EMPTY_ARGUMENTS_FUNCTION_INDEX = 1
PREPEND_ARGUMENT_FUNCTION_INDEX = 2
ADD_LISPRESS_FUNCTION_FUNCTION_INDEX = 3
def graph_program_create_argument(subtype: int, value: int) -> Tuple[str,Tuple[int]]:
    # returns a tuple of the form ('DataNodeId', (4,))
    function: Callable = lispress_specific[CREATE_ARGUMENT_FUNCTION_INDEX]
    return function(subtype, value)
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
action_list = ['Tomorrow', 'Yield']

print(f"Printing action list {action_list}")

# We refer to actions by their index in the action_list when actually passing them as arguments to the add_lispress_function
# method, so we add the function -> index entries to a dictionary for easy lookup.
action_to_id_in_action_list: Dict[str, int] = {action:i for i, action in enumerate(action_list)}
print(f"Printing action to index dict: {action_to_id_in_action_list}")

# dictionary which maps dataflow node ids to graph program node arguments
# For value ops, which just create an argument, the id of the node in dataflow
# is the key, and the generated argument in the graph is the value.
# For build struct ops and call like ops, the id of the node in dataflow 
# is still the key, but the value is the generated_argument of the output node in the graph.
# This gets a little confusing because the single buildstructop nodes in 
# dataflow actually map to multiple nodes in our representation, but in those 
# cases it is always the OUTPUT data node of the corresponding action which will
# be returned here.
dataflow_node_ids_to_graph_program_node_ids: Dict[int, Tuple[str,Tuple[int]]] = {}

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

def convert_dataflow_argument_string_to_value(dataflow_arg_id:str) -> int:
    """
    They give argument id lists like this:
    arg_ids=['[1]', '[3]']
    Each element in this list is a string, I just want the numeric value
    Decode the json, grab the only element, will make this more robust if I encounter
    an example with multiple elements in a single string
    """
    return json.loads(dataflow_arg_id)[0]
    

def convert_build_struct_op(dataflow_expression: Expression) -> GraphProgramStep:
    """
    Convert a dataflow build struct op into a graph program step.
    """
    print(f"converting build struct op {dataflow_expression}")
    action_name = dataflow_expression.op.op_schema
    action_id = action_to_id_in_action_list[action_name]
    # we always want an output node, and that will be the last argument, so add it to the arguments list first
    output_data_node_arg = graph_program_create_argument(subtype=EMPTY_DATA_NODE_SUBTYPE, value=EMPTY_DATA_NODE_DUMMY_VALUE)
    graph_program_arguments_list = graph_program_prepend_argument(new_argument_id=output_data_node_arg, existing_arguments_list=[])

    # update the map of dataflow node ids to graph program arguments
    dataflow_node_ids_to_graph_program_node_ids[dataflow_expression.id] = output_data_node_arg

    if dataflow_expression.arg_ids:
        for input_node_id in reversed(dataflow_expression.arg_ids):
            node_id_int: int = convert_dataflow_argument_string_to_value(input_node_id)
            graph_program_argument = dataflow_node_ids_to_graph_program_node_ids[input_node_id]
            graph_program_arguments_list = graph_program_prepend_argument(new_argument_id=graph_program_argument, existing_arguments_list=graph_program_arguments_list)

    graph_program_add_lispress_function(subtype=action_id, argument_list=graph_program_arguments_list)
    log_state(str(os.path.realpath(".")))
    print(f"logged state after adding lispress function for build struct op")

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

def main(dataflow_dialogues_dir: str, subsets: List[str], outdir: str):
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for subset in subsets:
        dataflow_dialogues = list(
            load_jsonl_file(
                data_jsonl=os.path.join(
                    dataflow_dialogues_dir, f"{subset}.dataflow_dialogues.jsonl"
                ),
                cls=Dialogue,
                unit=" dialogues",
            )
        )
        first: Dialogue = dataflow_dialogues[0]
        print(f"dialogue looks like this {first} \n")
        for turn in first.turns:
            turn: Turn
            print(f"printing turn: {turn.lispress}")
            dataflow_program: Program = turn.program()
            print(f"Attempting to convert dataflow program {dataflow_program.expressions_by_id} into a Graph Program! \n")

            graph_name = "output_graph_" + str(first.dialogue_id) + "_" + str(turn.turn_index)
            reset_state(graph_name, action_list)

            # convert dataflow program to graph program
            next_expression: Expression = None
            for expression in dataflow_program.expressions:
                print(f"\n CONVERTING EXPRESSION {expression} of type {type(expression.op)}")
                next_expression = expression
                if type(next_expression.op) == ValueOp:
                    convert_value_op(dataflow_expression=next_expression)
                elif type(next_expression.op) == CallLikeOp:
                    convert_call_like_op(dataflow_expression=next_expression)
                elif type(next_expression.op) == BuildStructOp:
                    convert_build_struct_op(dataflow_expression=next_expression)
                else:
                    raise Exception(f"Operation type {next_expression.op} not expected!")



def add_arguments(argument_parser: argparse.ArgumentParser) -> None:
    argument_parser.add_argument(
        "--dataflow_dialogues_dir", help="the dataflow dialogues data directory"
    )
    argument_parser.add_argument(
        "--subset", nargs="+", default=[], help="the subset to be analyzed"
    )
    argument_parser.add_argument("--outdir", help="the output directory")

if __name__ == "__main__":
    cmdline_parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    add_arguments(cmdline_parser)
    args = cmdline_parser.parse_args()
    # dataflow_program: Program = None # TODO: read in program from file as argument
    # print(f"Attempting to convert dataflow program {dataflow_program.expressions_by_id} into a Graph Program!")

    # # convert dataflow program to graph program
    # graph_program_steps = []
    # next_expression: Expression = None
    # for expression in dataflow_program.expressions:
    #     next_expression = expression
    #     if type(next_expression.op == ValueOp):
    #         graph_program_steps.append(convert_value_op(dataflow_expression=next_expression))
    #     elif type(next_expression.op == CallLikeOp):
    #         graph_program_steps.append(convert_call_like_op(dataflow_expression=next_expression))
    #     elif type(next_expression.op == BuildStructOp):
    #         graph_program_steps.append(convert_build_struct_op(dataflow_expression=next_expression))
    #     else:
    #         raise Exception(f"Operation type {next_expression.op} not expected!")

    # # convert back to lispress to verify
    # expressions = []
    # for step in graph_program_steps:
    #     next_expressions = find_expressions_for_graph_program_step(step)
    #     expressions.append(next_expressions)

    # resulting_program = Program(expressions=expressions)

    # assert resulting_program == dataflow_program, "Programs do not match! Investigate this test case."

    # TODO: write graph_program_steps to file if that assert passes, this appears to be a valid translation
    main(
        dataflow_dialogues_dir=args.dataflow_dialogues_dir,
        subsets=args.subset,
        outdir=args.outdir,
    )
    # reset_state("first_program", ["PleasantryCalendar"])
    # add_success = graph_program_add_lispress_function(subtype=0, argument_list=graph_program_empty_arguments)
    # log_state(str(os.path.realpath(".")))
