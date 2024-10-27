import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        """ Convert the Node to a dictionary for JSON serialization. """
        return {
            'node_type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

def validate_rule_string(rule_string):
    """ Validate the rule string format """
    # Enhanced regex pattern to allow for nested conditions and various operators
    pattern = r'^(\s*\(*\s*[\w]+\s*([<>]=?|!=|=)\s*[\w.]+\s*\)*\s*)((\s*(AND|OR)\s*)(\s*\(*\s*[\w]+\s*([<>]=?|!=|=)\s*[\w.]+\s*\)*\s*))*$'
    
    if not re.match(pattern, rule_string):
        raise ValueError("Invalid rule string format. Ensure proper usage of operators and parentheses.")

def create_rule(rule_string):
    validate_rule_string(rule_string)
    
    # Improved parsing logic to handle nested conditions
    rule_string = rule_string.strip()
    if 'AND' in rule_string:
        left_part, right_part = rule_string.split(' AND ', 1)
        return Node('operator', create_rule(left_part), create_rule(right_part), 'AND')
    elif 'OR' in rule_string:
        left_part, right_part = rule_string.split(' OR ', 1)
        return Node('operator', create_rule(left_part), create_rule(right_part), 'OR')
    else:
        # Parse the conditions
        condition = rule_string.strip('() ')
        return Node('operand', value=condition)

import re

def evaluate_rule(node, data):
    if node.type == 'operand':
        # Assuming condition is of the form "age > 30"
        attr, operator, value = re.split(r'\s*(>=|<=|!=|>|<|=)\s*', node.value)
        attr = attr.strip()
        value = value.strip().strip('"')  # Remove quotes for string comparison

        if attr not in data:
            raise ValueError(f"Attribute '{attr}' not found in data.")
        
        # Determine type of data[attr] and value
        try:
            if isinstance(data[attr], int) or isinstance(data[attr], float):
                # Convert value to a number if possible
                value = float(value)
            else:
                # Keep value as a string if it cannot be converted to a number
                value = str(value)
        except ValueError:
            pass  # Keep value as a string if it cannot be converted to a number

        # Perform the comparison based on the operator
        if operator == '>':
            return data[attr] > value
        elif operator == '<':
            return data[attr] < value
        elif operator == '=':
            return data[attr] == value
        elif operator == '>=':
            return data[attr] >= value
        elif operator == '<=':
            return data[attr] <= value
        elif operator == '!=':
            return data[attr] != value
    elif node.type == 'operator':
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
    return False



def combine_rules(rule_strings):
    """ Combine a list of rule strings into a single AST. """
    if not rule_strings:
        return None

    # Create a list to hold the AST nodes for each rule
    ast_nodes = []
    
    for rule in rule_strings:
        try:
            ast_nodes.append(create_rule(rule))
        except ValueError as e:
            print(f"Error creating rule for '{rule}': {e}")

    # If there's only one rule, return it as the root
    if len(ast_nodes) == 1:
        return ast_nodes[0]

    # Count the frequency of AND and OR operators
    and_count = sum(1 for rule in rule_strings if 'AND' in rule)
    or_count = len(rule_strings) - and_count  # Total rules minus AND rules

    # Combine rules based on the most frequent operator
    if and_count >= or_count:
        # Combine using AND
        root = ast_nodes[0]
        for node in ast_nodes[1:]:
            root = Node('operator', root, node, 'AND')
    else:
        # Combine using OR
        root = ast_nodes[0]
        for node in ast_nodes[1:]:
            root = Node('operator', root, node, 'OR')

    return root

def modify_rule(ast, new_condition):
    # Modify the AST: Create a new operator node and return the new condition directly
    return create_rule(new_condition)


def ast_to_string(node):
    if node.type == 'operand':
        return node.value
    elif node.type == 'operator':
        left = ast_to_string(node.left)
        right = ast_to_string(node.right)
        return f'({left} {node.value} {right})'

