from dataflow.core.program import BuildStructOp, CallLikeOp, Expression, Program, ValueOp

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
