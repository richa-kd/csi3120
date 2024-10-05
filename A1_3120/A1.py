import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: Union[str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """
    # TODO
    with open(fp, 'r') as file:
        lines = file.readlines()  
        return [line.strip() for line in lines] 


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    # TODO
    if len(s) > 0 and s[0] in alphabet_chars:
        for c in s:     # Check if all characters in the string are valid
            if c not in var_chars:
                return False
        return True     # If all characters are valid
    return False    


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root: Node):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        indent = '----' * level
        print(f"{indent}{'_'.join(self.root.elem)}")
        for child in self.root.children:     # Recursively print each child with level+1 of indentation
            subtree = ParseTree(child)
            subtree.print_tree(level = level + 1)



def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    s = s_[:]  #  Don't modify the original input string
    # TODO
    tokens = []
    i = 0
    close_pram_to_add = 0
    open_parens_extra = 0
    parentheses_stack = []  # Stack to track open parentheses

    while i < len(s_):
        char = s_[i]

        # Handle lambda expressions
        if char == '\\':
            if i + 1 >= len(s_):  # No variable after '\'
                print(f"Invalid lambda expression at {i}.")
                return False
            if not s_[i + 1].isalpha():  # Invalid variable after '\'
                print(f"Backslashes not followed by a variable name at {i}.")
                return False
            if s_[i + 1].isspace():  # Space after '\'
                print(f"Invalid space inserted after \\ at index {i}.")
                return False
            tokens.append('\\')
            i += 1

        # Handle spaces 
        elif char.isspace():
            i += 1

        # Handle open parentheses
        elif char == '(':
            if i + 1 < len(s_) and s_[i + 1] == ')':  # Empty parentheses
                print(f"Missing expression for parenthesis at index {i}.")
                return False
            tokens.append('(')
            parentheses_stack.append(i) 
            i += 1

        # Handle close parentheses
        elif char == ')':
            tokens.append(')')
            if not parentheses_stack:  # Check for unmatched close parentheses
                print(f"Bracket ) at index: {i} is not matched with an opening bracket '('.")
                return False  # Stop processing invalid input
            parentheses_stack.pop()  # Pop the last open parenthesis
            i += 1

        # Replace dots with open parentheses
        elif char == '.':
            if len(tokens) == 0 or tokens[-1] == '(':  
                print(f"Must have a variable name before character '.' at index {i}.")
                return False
            tokens.append('(')
            close_pram_to_add += 1
            i += 1

        # Handle valid variable names
        elif char in alphabet_chars:
            var = char
            i += 1
            while i < len(s_) and s_[i] in var_chars:
                var += s_[i]
                i += 1
            tokens.append(var)

        # Handle invalid characters
        elif char.isdigit() and len(tokens) == 0:  # Invalid variable starting with digits
            print(f"Error at index {i}, variables cannot begin with digits.")
            return False
        else:
            print(f"Error at index {i} with invalid character '{char}'.")
            return False

    # Check for unmatched opening parentheses
    while parentheses_stack:
        unmatched_index = parentheses_stack.pop()
        print(f"Bracket ( at index: {unmatched_index} is not matched with a closing bracket ')'.")
        return False

    # Check if a lambda expression is incomplete (e.g., \x without an expression)
    if '\\' in tokens and len(tokens) < 3:
        print("Missing complete lambda expression starting at index " + str(tokens.index('\\')) + ".")
        return False

    # Adding the necessary closing parentheses after dots
    if close_pram_to_add != 0:
        for _ in range(close_pram_to_add):
            tokens.append(')')

    
    return tokens

def read_lines_from_txt_check_validity(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).

    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: Union[str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).

    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()


def find_parenthesis_index(tokens: List[str]) -> int:
    """
    Finds the index of the closing bracket that matches the opening bracket in the beginning of the list of tokens.

    Precondition: the first element in the list of tokens must be '('

    :param tokens: A list of token strings
    :return: the index of the matching closing bracket
    :raises ValueError: if there is no such closing bracket
    """
    level = 0
    for i in range(1, len(tokens)):
        if tokens[i] == "(":
            level += 1
        elif tokens[i] == ")":
            if level == 0:
                return i
            else:
                level -= 1
    raise ValueError("no corresponding closing bracket found")

def get_expressions(tokens: List[str]) -> List[tuple[int, List[str]]]:
    """
    Gets a list of 2-tuples of token id and sublist of tokens by partitioning the list of tokens into sublists that
    correspond to a certain type of expression. The type of expression is denoted by a token id as follows:
    - token id = 0: the lambda expression
    - token id = 1: the expression enclosed by 2 brackets
    - token id = 2: the variable expression

    :param tokens: A list of token strings
    :return: a list of 2-tuples of a token id and an expression belonging to a certain id
    """
    output = []
    i = 0
    # rule: <expr> <expr>
    while i < len(tokens):
        # rule: '\' <var> <expr>
        if tokens[i] == "\\":
            output.append((0, tokens[i:])) # take every tokens as a whole lambda expression
            break
        # rule: '(' <expr> ')'
        elif tokens[i] == "(":
            idx = find_parenthesis_index(tokens[i:]) # index of matching ')'
            output.append((1, tokens[i:i+idx+1])) # take every tokens starting from '(' to ')'
            i += idx + 1
        # rule: <var>
        else:
            output.append((2, tokens[i:i+1])) # take only one token as a separate expression
            i += 1
    return output

def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree

    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """
    root = Node(tokens) # start symbol: <expr> - precondition: len(tokens) > 0
    # rule: <expr> <expr>
    expressions = get_expressions(tokens) # get separate expressions (they will be in the same tree level)
    # additional pointer to a node in case of branching out
    subtree = root
    for token_id, expr in expressions:
        # if there are more than 1 expressions, branch out of the root
        if len(expressions) > 1:
            subtree = Node(expr)
            root.add_child_node(subtree)
        # rule: '\' <var> <expr>
        if token_id == 0:
            subtree.add_child_node(Node([expr[0]])) # '\'
            subtree.add_child_node(Node([expr[1]])) # <var>
            for child in get_expressions(expr[2:]): # <expr>
                # the expressions following the lambda will be on the same tree level as '\' and <var>
                subtree.add_child_node(build_parse_tree_rec(child[1]))
        # rule: '(' <expr> ')'
        elif token_id == 1:
            subtree.add_child_node(Node([expr[0]])) # '('
            subtree.add_child_node(build_parse_tree_rec(expr[1:-1])) # <expr>
            subtree.add_child_node(Node([expr[-1]])) # ')'
        # rule: <var> (no need to add any child nodes)
        else:
            pass
    return root

def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens

    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)
