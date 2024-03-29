import re
import random
import string


# ------------------------------------------------------------

def eliminate_implication(formula):
    equivalent_expression = re.sub(r'(?P<antecedent>[A-Za-z][(A-Za-z)]+)\s*->\s*(?P<consequent>[A-Za-z][(A-Za-z)]+)',
                                   r'(~\1 | \2)', formula)
    return equivalent_expression


# ------------------------------------------------------------
def eliminate_equivalence(formula):
    equivalent_expression = re.sub(r'(?P<antecedent>[A-Za-z][(A-Za-z)]+)\s*<->\s*(?P<consequent>[A-Za-z][(A-Za-z)]+)',
                                   r'(~\1 | \2) & (\1 | ~\2)', formula)

    return equivalent_expression


# ------------------------------------------------------------
def apply_demorgan_law(formula):
    # Pattern for negating conjunction (AND)
    conjunction_pattern = re.compile(r'~\((.*?)\s*&\s*(.*?)\)')
    # Pattern for negating disjunction (OR)
    disjunction_pattern = re.compile(r'~\((.*?)\s*\|\s*(.*?)\)')

    # Replace negated conjunctions and disjunctions
    formula = conjunction_pattern.sub(r'(~\1 | ~\2)', formula)
    formula = disjunction_pattern.sub(r'(~\1 & ~\2)', formula)

    return formula


# ------------------------------------------------------------
def remove_double_negation(formula):
    while '~~' in formula:
        formula = formula.replace('~~', '')
    return formula


# ------------------------------------------------------------
def moving_all_quantifiers_to_the_left(formula):
    regex_pattern = r"For all\s\w|Exist\s\w"
    regex_pattern_FA = r"For all\s\w"
    regex_pattern_EX = r"Exist\s\w"

    matches_FA = re.findall(regex_pattern_FA, formula)
    matches_EX = re.findall(regex_pattern_EX, formula)

    modified_string = re.sub(regex_pattern, "", formula)

    modified_string = ' '.join(matches_FA) + " " + ' '.join(matches_EX) + " " + modified_string

    return modified_string


# ------------------------------------------------------------
def eliminate_existential_quantifiers(formula):
    pattern_EX = re.compile(r'Exist\s+([a-zA-Z]+)\s*')

    modified_string = re.sub(pattern_EX, "", formula)

    pattern_FA = re.compile(r'For\s+all\s+([a-zA-Z]+)\s*')

    # To catch all the variables after 'For all' to add it to the fun
    variables_EX = []
    for match_EX in pattern_EX.finditer(formula):
        variable_EX_tmp = match_EX.group(1)
        variables_EX.append(variable_EX_tmp)

    # To catch all the variables after 'For all' to add it to the fun
    variable_FA = []
    for match in pattern_FA.finditer(formula):
        variable_FA_tmp = match.group(1)
        variable_FA.append(variable_FA_tmp)

    fun = 'f(' + ', '.join(variable_FA) + ')'

    for variable_EX in variables_EX:
        modified_string = re.sub(variable_EX, fun, modified_string)

    return modified_string


# ------------------------------------------------------------
def eliminate_universal_quantifiers(formula):
    pattern = re.compile(r'For\s+all\s+[a-zA-Z]+\s*')
    new_formula = re.sub(pattern, '', formula)

    return new_formula


# ------------------------------------------------------------
def convert_clause(clause):
    split_clause = re.split(r'\s*\&\s+', clause)  # Splitting only at '|'

    pattern = r'(~?[A-Za-z]+\((?:[A-Za-z]+\([^()]*\)|[A-Za-z]+)\))'

    converted_clause = []

    for part in split_clause:
        matches = re.findall(pattern, part)

        match_set = set()

        for match in matches:
            match_set.add(match)

        converted_clause.append(match_set)

    return converted_clause


# ------------------------------------------------------------
def replace_variables(match):
    statements = match.group(0)
    variables = re.findall(r'\b\w\(([^)]*)\)', statements)
    unique_var = ''.join(random.choices(string.ascii_lowercase, k=1))  # Generate a unique letter for this group
    replaced_statement = statements
    unique_var_map = {}  # Store the unique variable assigned to each original variable
    for var in variables:
        if '(' in var:  # Check if the variable contains parentheses, indicating it's a function call
            function_name, argument = var.split('(',  maxsplit=1)  # Split the function call into function name and argument
            inner_variables = re.findall(r'\b\w+\b', argument)  # Find all simple variables in the function argument
            replaced_argument = ''
            for inner_var in inner_variables:
                if inner_var in unique_var_map:
                    replaced_argument += inner_var[:1]  # Use the same unique variable
                else:
                    replaced_var = unique_var
                    for i, letter in enumerate(inner_var, start=0):
                        if letter != unique_var:
                            break
                        replaced_var += letter
                    replaced_argument += replaced_var
                    unique_var_map[inner_var] = replaced_argument[ :1]  # Store the unique variable for this original variable
                replaced_argument += ', '  # Add comma and space for multiple variables
            replaced_argument = replaced_argument.rstrip(', ')  # Remove the trailing comma and space
            replaced_var = f"{function_name}({replaced_argument}"  # Reconstruct the function call
        else:
            replaced_var = unique_var  # Replace simple variables with the unique letter
        replaced_statement = replaced_statement.replace(var[:5], replaced_var[:5], 1)  # Replace only the first occurrence
    return replaced_statement


# ------------------------------------------------------------
def converting_to_CNF(formula):
    formula = eliminate_implication(formula)
    formula = eliminate_equivalence(formula)
    formula = remove_double_negation(formula)
    formula = apply_demorgan_law(formula)
    formula = moving_all_quantifiers_to_the_left(formula)
    formula = eliminate_existential_quantifiers(formula)
    formula = eliminate_universal_quantifiers(formula)
    formula = convert_clause(formula)
    input_statements = str(formula)
    result = re.sub(r'\{[^{}]*\}', replace_variables, input_statements)

    return result


formula1 = ('For all x Exist y (P(x) -> Q(y))')
formula2 = ('For all x (P(x) <-> Q(x))')
formula3 = ('For all x ~(P(x) | Q(x))')
formula4 = ('For all x ~~(P(x) | Q(x))')
formula5 = ('For all x ~~(P(x) | Q(x)) & For all y ~(P(y) | Q(y))')
formula6 = ('For all x (P(x) | Q(x)) & Exist y (P(x) | Q(y))')
formula7 = ('For all x (~P(x) | Q(x))')
formula8 = ('For all x Exist y ~(P(x) | Q(y))')
formula9 = ('For all x ~(P(x) & Q(x))')
formula10 = ('For all x (~P(x) | ~Q(x)) & Exist y ((Z(x) <-> C(y)) & For all z (P(x) -> R(z))')
formula11 = ('For all x (~P(x) | ~Q(x)) & Exist y ((Z(x) | ~C(y)) & For all z (P(x) -> R(z)) & Exist g (P(x) -> R(g))')

print("Test Cases To Convert to CNF")
print("\n------------ Test Cases For Formula 1 ------------")
print(converting_to_CNF(formula1))
print("\n------------ Test Cases For Formula 2 ------------")
print(converting_to_CNF(formula2))
print("\n------------ Test Cases For Formula 3 ------------")
print(converting_to_CNF(formula3))
print("\n------------ Test Cases For Formula 4 ------------")
print(converting_to_CNF(formula4))
print("\n------------ Test Cases For Formula 5 ------------")
print(converting_to_CNF(formula5))
print("\n------------ Test Cases For Formula 6 ------------")
print(converting_to_CNF(formula6))
print("\n------------ Test Cases For Formula 7 ------------")
print(converting_to_CNF(formula7))
print("\n------------ Test Cases For Formula 8 ------------")
print(converting_to_CNF(formula8))
print("\n------------ Test Cases For Formula 9 ------------")
print(converting_to_CNF(formula9))
print("\n------------ Test Cases For Formula 10 ------------")
print(converting_to_CNF(formula10))
print("\n------------ Test Cases For Formula 11 ------------")
print(converting_to_CNF(formula11))

