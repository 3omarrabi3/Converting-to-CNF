import re

def eliminate_implication(formula):
    equivalent_expression = re.sub(r'(?P<antecedent>[A-Za-z][(A-Za-z)]+)\s*->\s*(?P<consequent>[A-Za-z][(A-Za-z)]+)',
                                   r'(~\1 | \2)', formula)
    return equivalent_expression

def eliminate_equivalence(formula):
    equivalent_expression = re.sub(r'(?P<antecedent>[A-Za-z][(A-Za-z)]+)\s*<->\s*(?P<consequent>[A-Za-z][(A-Za-z)]+)',
                                   r'(~\1 | \2) & (\1 | ~\2)', formula)

    return equivalent_expression

def apply_demorgan_law(formula):
    # Pattern for negating conjunction (AND)
    conjunction_pattern = re.compile(r'~\((.*?)\s*&\s*(.*?)\)')
    # Pattern for negating disjunction (OR)
    disjunction_pattern = re.compile(r'~\((.*?)\s*\|\s*(.*?)\)')

    # Replace negated conjunctions and disjunctions
    formula = conjunction_pattern.sub(r'(~\1 | ~\2)', formula)
    formula = disjunction_pattern.sub(r'(~\1 & ~\2)', formula)

    return formula

def remove_double_negation(formula):
    while '~~' in formula:
        formula = formula.replace('~~', '')
    return formula

def moving_all_quantifiers_to_the_left(formula):
     regex_pattern = r"For all\s\w|Exist\s\w"
     regex_pattern_FA = r"For all\s\w"
     regex_pattern_EX = r"Exist\s\w"

     matches_FA = re.findall(regex_pattern_FA, formula)
     matches_EX = re.findall(regex_pattern_EX, formula)

     modified_string = re.sub(regex_pattern, "", formula)

     modified_string = ' '.join(matches_FA) + " " +' '.join(matches_EX) + " " + modified_string

     return modified_string

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

def eliminate_universal_quantifiers(formula):
    pattern = re.compile(r'For\s+all\s+[a-zA-Z]+\s*')
    new_formula = re.sub(pattern, '', formula)

    return new_formula



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


# # Example usage
# clause = "(X(x) | (Y(y)) & (Z(z) | A(w)) & (B(p) | C(q)"
# converted = convert_clause(clause)
# print(converted)

formula = 'For all x (~p(x) | Exist y ((q(x,y) & ~p(y))'
def converting_to_CNF(formula):
    formula = eliminate_implication(formula)
    formula = eliminate_equivalence(formula)
    formula = apply_demorgan_law(formula)
    formula = remove_double_negation(formula)

    formula = moving_all_quantifiers_to_the_left(formula)

    formula = eliminate_existential_quantifiers(formula)
    formula = eliminate_universal_quantifiers(formula)
    # formula = convert_clause(formula)

    return formula

print(converting_to_CNF(formula))

