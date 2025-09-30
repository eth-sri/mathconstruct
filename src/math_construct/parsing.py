import re
from fractions import Fraction
from math_construct.utils import get_depth, latex2sympy_fixed
from sympy import N, Integer

def parse_answer(s: str, primitive_type: type = None):
    s = remove_outer_brackets(normalize_string(s))
    output = ParseList.parse("(" + s + ")", primitive_type=primitive_type)
    if output is None:
        return None
    if len(output) == 1:
        return output[0]
    return output

def match_list_depth(parsed_answer, depth: int = None, primitive_type: type = None):
    depth_parsed = get_depth(parsed_answer)
    if depth_parsed is not None and depth is not None and depth_parsed == depth - 1:
        return [parsed_answer]
    if depth is None:
        return parsed_answer
    if depth > 0 and not isinstance(parsed_answer, list):
        return match_list_depth([parsed_answer], depth, primitive_type)
    if depth == 0 and isinstance(parsed_answer, list):
        if isinstance(parsed_answer[0], list):
            assert len(parsed_answer) == 1
            return match_list_depth(parsed_answer[0], depth, primitive_type)
        elif len(parsed_answer) == 1:
            return parsed_answer[0]
        if primitive_type == str or primitive_type is None:
            return "".join([str(item) for item in parsed_answer])
        raise ValueError(f"Expected a single element, but got '{parsed_answer}'. Failed to match correct depth.")
    elif depth == 0:
        return parsed_answer
    try:
        output_list = [
            match_list_depth(item, depth - 1, primitive_type) for item in parsed_answer
        ]
    except Exception as e:
        raise ValueError(f"Failed to match correct depth {depth} for '{parsed_answer}'")
    return output_list

def normalize_string(s):
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\Bigl", "").replace(r"\Bigr", "").replace(r"\bigl", "").replace(r"\bigr", "")
    s = remove_aligns(s)
    s = s.replace("[", "(")
    s = s.replace("]", ")")
    s = s.replace("\\{", "(") # sets will be converted to lists
    s = s.replace("\\}", ")") # sets will be converted to lists
    s = s.replace("$", "")
    # remove hline and vline
    s = s.replace(r"\hline", "")
    s = s.replace(r"\vline", "")
    s = s.replace(r"\quad", " ")
    s = s.replace("(1mm)", "")
    s = s.replace(",\\,", ",")
    return strip(s)

def remove_outer_brackets(s):
    """
    Removes the outermost matching brackets from the string if they encompass the entire string.
    
    Parameters:
    s (str): The input string potentially wrapped with brackets.
    
    Returns:
    str: The string with the outermost brackets removed if they match and encompass the entire string.
    """
    while True:
        if not s:
            return s
        opening = s[0]
        closing = s[-1]

        if opening == "(" and closing == ")":
            count = 0
            matched = True
            for i, char in enumerate(s):
                if char == opening:
                    count += 1
                elif char == closing:
                    count -= 1
                if count == 0 and i != len(s) - 1:
                    matched = False
                    break

            if matched:
                s = s[1:-1]
                continue
        break

    return s

def remove_aligns(s: str) -> str:
    # This pattern captures:
    #   \begin{align followed by any non-} characters (like align*, alignat, etc.)
    #   then any content (non-greedily) up to
    #   \end{align...} with the same "align" prefix
    pattern = r'\\begin{align[^}]*}(.*?)\\end{align[^}]*}'
    
    # Use a callback to remove '&' from the matched group before returning it
    return re.sub(pattern, lambda m: m.group(1).replace('&', '').replace("\\\\", ""), s, flags=re.DOTALL)



def strip(s: str):
    s = s.strip()
    # be careful with this, it can also remove the "\" in "\begin" if just done with strip
    while s.startswith(r"\n"):
        s = s[2:]
    while s.endswith(r"\n"):
        s = s[:-2]
    while s.startswith("\\ "):
        s = s[2:]
    # if s starts with any thing of the form \\\ and then a bracket, or \\\n and then a bracket, remove it
    while re.match(r"\\{2,}\n?\(", s):
        s = s[3:]
    return s
class ParseObject:
    @classmethod
    def is_at_start(cls, string):
        return False

    @classmethod
    def is_complete(cls, string):
        return string.count("{") == string.count("}") and string.count("(") == string.count(")")

    @classmethod
    def is_finished(cls, string):
        return True
    
    @classmethod
    def parse(cls, string):
        raise NotImplementedError
    
class ParsePrimitive(ParseObject):
    @classmethod
    def parse(cls, string, primitive_type):
        if primitive_type == str:
            return string
        # Integer
        if string.isdigit():
            if primitive_type == Fraction:
                return Fraction(int(string), 1)
            return int(string)
        # Float
        try:
            float_string = float(string)
            if int(float_string) == float_string:
                if primitive_type == Fraction:
                    return Fraction(int(float_string), 1)
                return int(float_string)
            return float_string
        except ValueError:
            pass
        # Expression
        try:
            string_no_eq = string
            if "=" in string_no_eq:
                # rfind is used to remove the last occurence of "="
                string_no_eq = string_no_eq[string_no_eq.rfind("=")+1:]
            float_val = float(N(latex2sympy_fixed(string_no_eq), 101))
            if float_val.is_integer() or float("inf") == float_val or float("-inf") == float_val:
                return int(N(latex2sympy_fixed(string_no_eq), 50001)) # important for large ints
            elif primitive_type == Fraction:
                # get numerator and denominator
                sympy_expression = latex2sympy_fixed(string_no_eq)
                numerator, denominator = sympy_expression.as_numer_denom()
                if not isinstance(numerator, Integer) or not isinstance(denominator, Integer):
                    raise ValueError(f"Expected a primitive fraction, but got '{string}'")
                
                fraction = Fraction(int(numerator), int(denominator))
                if primitive_type != Fraction and fraction.denominator == 1:
                    return fraction.numerator
                return fraction
            return float_val
        except Exception as e:
            if "Expected a primitive fraction" in str(e):
                raise e
            pass
        # String
        if primitive_type not in [str, None]:
            raise ValueError(f"Expected a primitive int/float/parseable LaTeX expression, but got '{string}'")
        return string
        
    @classmethod
    def is_at_start(cls, string):
        return True


class ParseFraction(ParseObject):
    @classmethod
    def is_complete(cls, string):
        if not string.startswith(r"\frac{") and not string.replace(" ", "").startswith(r"-\frac{"):
            return False
        factor, numerator, denominator = cls.search_numerator_and_denominator(string)
        if numerator is None or denominator is None:
            return False
        try:
            float(N(latex2sympy_fixed(numerator), 5000))
            float(N(latex2sympy_fixed(denominator), 5000))
        except:
            return False
        return True
    
    @classmethod
    def search_numerator_and_denominator(cls, s: str):
        factor = 1
        if s.replace(" ", "").startswith(r"-\frac{"):
            factor = -1
        numerator, denominator = None, None
        n_brackets = 0
        start_current = None
        for i, c in enumerate(s):
            if c == "{":
                n_brackets += 1
                if n_brackets == 1:
                    start_current = i
            if c == "}":
                n_brackets -= 1
                if n_brackets == 0:
                    if numerator is None:
                        numerator = s[start_current + 1:i]
                    else:
                        denominator = s[start_current + 1:i]

        if numerator is not None:
            numerator = numerator
        return factor, numerator, denominator
    
    @classmethod
    def is_finished(cls, string):
        # if the second "}" is the last character, then the fraction is finished
        current_brackets = 0
        current_finished = 0
        has_started = False
        for char in string:
            if char == "{":
                current_brackets += 1
                has_started = True
            if char == "}":
                current_brackets -= 1
                has_started = True
            if current_brackets == 0 and has_started:
                current_finished += 1
                has_started = False
        return current_finished == 2 and string.endswith("}")
    
    @classmethod
    def parse(cls, string, primitive_type):
        factor, numerator, denominator = cls.search_numerator_and_denominator(string)
        parsed_numerator = ParsePrimitive.parse(numerator, primitive_type)
        parsed_denominator = ParsePrimitive.parse(denominator, primitive_type)
        try:
            fraction = Fraction(factor * parsed_numerator, parsed_denominator)
            if primitive_type != Fraction and fraction.denominator == 1:
                return fraction.numerator
            return fraction
        except:
            return factor * parsed_numerator / parsed_denominator
    
    @classmethod
    def is_at_start(cls, string):
        return string.startswith(r"\frac{") or string.replace(" ", "").startswith(r"-\frac{")
    
class ParseList(ParseObject):
    @classmethod
    def is_at_start(cls, string):
        return string.startswith(r"(")
    
    @classmethod
    def is_finished(cls, string):
        # safe condition for finishing a list
        return string.strip().strip(",").endswith(")")
    
    @classmethod
    def is_complete(cls, string):
        return string.count("(") == string.count(")")
    
    @classmethod
    def never_zero_count(cls, string):
        # says wheter count "(" - count ")" for every string[:i] is never zero
        count = 0
        ever_zero = False
        for char in string:
            if char == "(":
                count += 1
            if char == ")":
                count -= 1
            if count == 0:
                ever_zero = True
        return not ever_zero

    
    @classmethod
    def parse(cls, string, delimiter=[r"\n", ","], primitive_type=None, depth=0):
        if isinstance(delimiter, str):
            delimiter = [delimiter]
        output = []
        if not string.startswith("("):
            return None
        string = string.strip().strip(",")
        if cls.never_zero_count(string[:-1]):
            string = string[1:-1]
        string = strip(string)
        used_delim = delimiter[0]
        for delim in delimiter:
            if delim in string:
                comma_separated = string.split(delim)
                used_delim = delim
                break
        while len(string) > 0:
            previous_string = string
            comma_separated = string.split(used_delim)
            allowed_objects = [ParseList, ParseMatrix, ParseFraction, ParsePrimitive]
            if depth > 50:
                allowed_objects = [ParseMatrix, ParseFraction, ParsePrimitive]
            for obj in allowed_objects:
                if obj.is_at_start(strip(string)):
                    current_index = 1
                    while not obj.is_complete(strip(used_delim.join(comma_separated[:current_index]))) or \
                        not obj.is_finished(strip(used_delim.join(comma_separated[:current_index]))):
                        current_index += 1
                        if current_index >= len(comma_separated):
                            break
                    if not obj.is_complete(strip(used_delim.join(comma_separated[:current_index]))) or \
                        not obj.is_finished(strip(used_delim.join(comma_separated[:current_index]))):
                        continue
                    
                    if obj == ParseList:
                        parsed = obj.parse(strip(used_delim.join(comma_separated[:current_index])), 
                                            primitive_type=primitive_type, depth=depth+1)
                    else:
                        parsed = obj.parse(strip(used_delim.join(comma_separated[:current_index])), 
                                    primitive_type=primitive_type)
                    output.append(parsed)
                    string = strip(used_delim.join(comma_separated[current_index:]))
                    break
            if previous_string == string:
                if depth > 50:
                    raise ValueError(f"Failed to parse '{string}'")
                return None
        return output

class ParseMatrix(ParseObject):
    @classmethod
    def is_valid(cls, string):
        pass

    @classmethod
    def is_complete(cls, string):
        return string.count("{") == string.count("}") and string.count("\\end{") == string.count("\\begin{")

    @classmethod
    def is_at_start(cls, string):
        return re.match(r'\\begin{.*matrix}', string) or re.match(r"^\\begin{array}", string)
    
    @classmethod
    def parse(cls, string, primitive_type):
        if "array" in string:
            match = re.search(r'\\begin{array}({[^}]*})*(.*?)\\end{array}', string, re.DOTALL)
            content = match.group(2).strip() if match else None
            while content.startswith("}"):
                content = content[1:]
        else:
            match = re.search(r'\\begin{.*matrix}(.*?)\\end{.*matrix}', string, re.DOTALL)
            content = match.group(1).strip() if match else None
        if not content:
            return None
        rows = [row.strip() for row in content.split('\\\\')]
        rows = [row for row in rows if len(row) > 0]
        parse_rows = []
        for row in rows:
            row_parse = row.strip().strip(",")
            row_parse = "(" + row_parse + ")"
            parse_rows.append(row_parse)
        rows = [ParseList.parse(row, delimiter=["&", r"\n", ","], primitive_type=primitive_type) for row in parse_rows]
        if all([len(row) == 1 for row in rows]):
            return [row[0] for row in rows]
        return rows

