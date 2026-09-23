from langchain.tools import tool
import ast
import operator

def evaluate_expr(node):
    operators = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.BitXor: operator.xor,
        ast.USub: operator.neg
    }
    
    if isinstance(node, ast.Constant): # Python 3.8+
        return node.n
    elif isinstance(node, ast.Num): # Python < 3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        return operators[type(node.op)](evaluate_expr(node.left), evaluate_expr(node.right))
    elif isinstance(node, ast.UnaryOp):
        return operators[type(node.op)](evaluate_expr(node.operand))
    else:
        raise TypeError(node)

@tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    Useful for calculating travel limits, expenses, totals, etc.
    Example expression: '4000 * 5'
    """
    try:
        node = ast.parse(expression, mode='eval').body
        result = evaluate_expr(node)
        return str(result)
    except Exception as e:
        return f"Error in calculation: {str(e)}"
