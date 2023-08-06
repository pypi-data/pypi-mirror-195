import re
import dill
import inspect

from nctoolkit.session import session_info


def split_equation(mystr):
    return re.split("[-+^!=*/(&|)\[\]]", mystr)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def between_brackets(s):
    return s[s.find("(") + 1 : s.find(")")]


def find_parens(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "[":
            pstack.append(i)
        elif c == "]":
            toret[pstack.pop()] = i

    return toret


def find_parens2(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "{":
            pstack.append(i)
        elif c == "}":
            toret[pstack.pop()] = i

    return toret


def find_parens3(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "(":
            pstack.append(i)
        elif c == ")":
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


phen_funs = ["min", "max", "mean", "median"]

# split using all possible mathematical operators
def split1(mystr):
    return re.split("([+-/*()<>=])", mystr)


def is_lambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


pattern = re.compile(":\w*")


def bloom_start(self, drop=False, **kwargs):
    """
    Create new variables
    Existing columns that are re-assigned will be overwritten.

    Parameters
    ----------
    drop : bool
        Set to True if you want existing variables to be removed once the new ones have been created.
        Defaults to False.

        should evaluate to a numeric. New variables are calculated for each grid cell and time step.
    **kwargs : dict of {str: callable}
        New variable names are keywords. All terms in the equation given by the lamda function
        should evaluate to a numeric. New variables are calculated for each grid cell and time step.
    Notes
    -----
    Operations are carried out in the order give. So if a new variable is created in the first argument,
    it can then be used in following arguments.

    """
    frame = inspect.currentframe()

    if not isinstance(drop, bool):
        raise ValueError("drop is not boolean!")

    if len(kwargs) == 0:
        raise ValueError("Please provide assignments!")

    for k, v in kwargs.items():
        if is_lambda(v) is False:
            raise ValueError("Please check everything is a lambda function!")
        lambdas = v

    for k, v in kwargs.items():
        if is_lambda(v) is True:
            break
    lambdas = v

    # now, we need to parse things.

    interactive = False
    if session_info["interactive"]:
        import readline

        if readline.get_current_history_length() > 0:
            interactive = True

    if interactive:
        import readline

        start = [
            str(readline.get_history_item(i + 1))
            for i in range(readline.get_current_history_length())
        ][-1]
    else:
        start = lambdas
        try:
            start = inspect.getsourcelines(start)[0][0].replace("\n", "").strip()
        except:
            start = dill.source.getsource(start).replace("\n", "").strip()

    # we now need to figure out if what we have is one line

    if ".bloom_start(" not in start:
        raise ValueError("Please write assign methods as single line!")

    try:
        find_parens3(start)
    except:
        raise ValueError("Please write assign methods as single line!")

    start = start[start.find("(") + 1 : -1]

    pattern1 = re.compile("drop\s*=\s*(True|False)")
    y = pattern1.search(start)
    if y is not None:
        y = y.group()
        start = start.replace(y, "").strip()

    start = start.strip()
    start = start.replace(" or ", " | ")
    start = start.replace(" and ", " & ")

    if "%" in start:
        raise ValueError("assign does not yet accept %")

    if "//" in start:
        raise ValueError("assign does not yet accept //")

    if start.endswith(","):
        start = start[:-1]

    pattern1 = re.compile("\s*:")

    for tt in pattern1.findall(start):
        start = start.replace(tt, ": ")

    if start.startswith(","):
        start = start[1:]
    start = start.strip()

    pattern1 = re.compile(",\s,")
    y = pattern1.search(start)
    if y is not None:
        y = y.group()
        start = start.replace(y, " , ").strip()

    start = start.replace("  ", " ")
    pattern1 = re.compile(",\s*\w+\s*=\s*lambda")

    for x in pattern1.finditer(start):
        index = x.span()[0]
        start = start[:index] + ";" + start[index + 1 :]

    command = list()
    starts = start

    pattern_missing = re.compile("lambda\s*:")
    if pattern_missing.search(start) is not None:
        raise ValueError("Ensure lambda functions of the form 'lambda x:'")

    for start in starts.split(";"):

        patternl = re.compile("lambda \w*:")
        lambda_value = patternl.findall(start)[0][-2]

        start = (
            " ".join(split1(start))
            .replace("  ", " ")
            .replace(" ( ", "(")
            .replace(" . ", ".")
        )

        # run equations first.
        # key here is that equation can only pure pure python or pure cdo

        check_them = True
        while check_them:
            check_start = start
            pars = find_parens(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                check_them = False

        while True:
            check_start = start
            pars = find_parens2(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                break

        start = start.replace(";", " ; ").replace("  ", " ")

        # tidy functions

        start = start.replace(" [", "[").replace("(", "( ").replace(" . ", ".")

        # pattern to identify functions
        fun_pattern = re.compile("[a-zA-Z\_][a-zA-Z\_z.0-9]*\(")

        for x in fun_pattern.findall(start):

            check = True
            while check:
                x_terms = re.finditer(x.replace("(", "\\(").replace("[", "\\["), start)

                terminate = len(
                    re.findall(x.replace("(", "\\(").replace("[", "\\["), start)
                )

                if terminate == 0:
                    check = False

                tracker = 0
                for y in x_terms:
                    if x in start:
                        old_start = start
                        start_parens = find_parens3(start)
                        x_term = (
                            x + start[y.span()[1] : start_parens[y.span()[1] - 1] + 1]
                        )
                        try:
                            new_x = eval(x_term, globals(), frame.f_back.f_locals)
                            if not isinstance(new_x, str):
                                if is_number(str(new_x)):
                                    start = start.replace(
                                        x_term, str(new_x).replace(" ", "")
                                    )
                            if start != old_start:
                                break
                        except:
                            odllan = "nothing"
                    tracker += 1
                    if tracker == terminate:
                        check = False

        terms = list(
            set(
                [
                    x
                    for x in start.replace(" . ", ".").split(" ")
                    if x.endswith("(") and len(x) > 1
                ]
            )
        )

        for x in terms:
            if ("[" in x and f"{lambda_value}." in x) is False:
                if fun_pattern.search(x) is not None:

                    fix = True
                    n = 0
                    n_limit = start.count("x")
                    while fix:
                        for y in re.finditer(
                            x.replace("(", "\\(").replace("[", "\\["), start
                        ):
                            if len(y.group()) > 0:
                                old_start = start
                                start_parens = find_parens3(start)
                                x_term = (
                                    x
                                    + start[
                                        y.span()[1] : start_parens[y.span()[1] - 1] + 1
                                    ]
                                )
                                start = start.replace(x_term, x_term.replace(" ", ""))
                                if old_start != start:
                                    break
                        n += 1

                        if n > n_limit:
                            fix = False

        error_message = None

        for x in start.split(" "):
            if "(" in x:
                x_fun = x.split("(")[0]
                pattern1 = re.compile("[A-Za-z0-9\\.\\_]*")
                if fun_pattern.match(x) is not None:
                    # if pattern1.findall(x_fun)[0] == x_fun:
                    try:
                        # need to tweak this so that it captures the output and returns an appropriate error
                        new_x = eval(x, globals(), frame.f_back.f_locals)
                        if isinstance(new_x, str):
                            error_message = f"{x} evaluates to a string!"
                            raise ValueError(f"{x} evaluates to a string")
                        if is_number(str(new_x)) is False:
                            error_message = f"{x} does not evaluate to numeric!"
                            raise ValueError(f"{x} does not evaluate to numeric!")

                        new_start = ""
                        for y in start.split(" "):
                            if y != x:
                                new_start += " " + y
                            else:
                                new_start += " " + str(new_x)
                        start = new_start
                        error_message = None

                    except:

                        if x_fun in phen_funs:
                            x_term = between_brackets(x)

                            if (f"{lambda_value}." in x_term) is False:
                                raise ValueError(
                                    f"Error for {x}: nctoolkit functions must take dataset variables as args!"
                                )
                            if x_fun == "timestep":
                                start = start.replace(x, "(" + x + "-1)")
                            if x_fun in ["cell_area", "longitude", "latitude"]:
                                if len(split_equation(x_term)) > 1:
                                    raise ValueError(
                                        f"{x_fun} can only take a single dataset variable as an argument!"
                                    )

                        else:
                            x_term = between_brackets(x)
                            if f"{lambda_value}." in x_term:
                                possible = find_possible(x_fun)
                                if possible is not None:
                                    raise ValueError(
                                        f"{x_fun} is not an assignment function. Did you mean {possible}?"
                                    )

                            if f"{lambda_value}." in x_term:
                                raise ValueError(
                                    f"{x_fun} is not an assignment function"
                                )
                            else:
                                raise ValueError(f"{x} cannot be evaluated!")

        start = (
            " ".join(split1(start))
            .replace("  ", " ")
            .replace(" ( ", "(")
            .replace(" . ", ".")
        )

        start = start.replace(";", " ; ").replace("  ", " ").replace(") ", ")")

        # put spaces round lambda x: etc.
        pattern1 = re.compile("lambda [a-zA-Z\_][a-zA-Z\_z0-9]*\:")
        for x in pattern1.findall(start):
            start = start.replace(x, x + " ")
        rtart = start.replace("  ", " ")

        terms = (
            start.replace(" . ", ".")
            .replace(") ", ")")
            .replace(") ", ")")
            .replace("  ", " ")
            .split(" ")
        )

        for x in terms:
            if "[" in x:
                if f"{lambda_value}." in x:
                    raise ValueError(f"{x} is not valid syntax")
                try:
                    new_term = eval(x, globals(), frame.f_back.f_locals)
                except:
                    raise ValueError(f"{x} is not available!")
                if not isinstance(new_term, (int, float)):
                    type(new_term)
                ):
                    raise ValueError(f"{x} does not evaluate to numeric!")

                new_start = ""
                for y in start.split(" "):
                    if y != x:
                        new_start += " " + y
                    else:
                        new_start += " " + str(new_term)
                start = new_start

        terms = start.split(" ")

        for x in terms:
            if "{" in x:
                if f"{lambda_value}." in x:
                    raise ValueError(f"{x} is not valid syntax")
                try:
                    new_term = eval(x, globals(), frame.f_back.f_locals)
                except:
                    raise ValueError(f"{x} is not available!")
                if not isinstance(new_term, (int, float)):
                    type(new_term)
                ):
                    raise ValueError(f"{x} does not evaluate to numeric!")

                new_start = ""
                for y in start.split(" "):
                    if y != x:
                        new_start += " " + y
                    else:
                        new_start += " " + str(new_term)
                start = new_start

        # fix powers

        if "^" in start:
            raise ValueError("^ is not valid syntax. Please use **")

        start = start.replace("* ", "*").replace("**", "^")

        start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

        start = start.replace("|", "||")
        start = start.replace("&", "&&")

        # we need to be able to identify lambdas and get rid of them
        # start = start.replace("=", "= ")
        start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

        # We now need to tidy up each element

        start = " ".join(split1(start))
        start = start.replace("  ", " ")
        start = start.replace(" (", "(").replace(" . ", ".")
        terms = start.split(" ")

        error_message = None

        for i in range(2, len(terms)):
            if (
                terms[i].isidentifier()
                and terms[i] != "lambda"
                and terms[min(i + 1, len(terms) - 1)] != lambda_value
            ):
                term = terms[i]

                if term in frame.f_back.f_locals:
                    try:
                        new_term = eval(term, globals(), frame.f_back.f_locals)
                        if isinstance(new_term, str):
                            error_message = f"{term} does not evaluate to a numeric!"
                            raise ValueError(f"{term} does not evaluate to a numeric!")

                        if is_number(str(new_term)) is False:
                            error_message = f"{term} does not evaluate to a numeric!"
                            raise ValueError(f"{term} does not evaluate to a numeric!")

                        new_start = ""
                        for y in start.split(" "):
                            if y != term:
                                new_start += " " + y
                            else:
                                new_start += " " + str(new_term)
                        start = new_start
                    except:
                        raise ValueError(f"{term} is not available!")
                else:
                    raise ValueError(f"{term} is not available!")

        start = " ".join(split1(start))

        new_start = []

        def new_split(mystr):
            return re.split("([+-/*()&|<>=!^])", mystr)

        for tt in start.split(";"):

            tt_frag = []
            l_pattern = re.compile("lambda (\w*):")
            l_string = l_pattern.findall(tt)[0]
            tt1 = tt.replace(f"lambda {l_string}:", " ")
            tt1 = re.sub(" ", "", tt1)
            tt1 = " ".join(new_split(tt1)).replace(" . ", ".")
            tt1 = re.sub(" +", " ", tt1)

            for ss in tt1.split(" "):
                if ss.startswith(f"{l_string}."):
                    tt_frag.append(ss.replace(f"{l_string}.", ""))
                else:
                    tt_frag.append(ss)

            tt_frag = " ".join(tt_frag)
            new_start.append(tt_frag)

        start = ";".join(new_start)
        start = " ".join(split1(start))

        start = start.replace(" lambda ", " ").replace(" ", "")

        # We need to fix pow functions potentially. Though, it might be better to stick with ^

        start = " ".join(split1(start))

        def new_split(mystr):
            return re.split("([+-/*()&|<>=!^])", mystr)

        y = " ".join(new_split(start))
        z = y.split(" = ")[1]
        total = 0
        for w in (z.replace(" (", "(")).split(" "):
            if w.strip().isidentifier():
                total += 1
        if total == 0:
            raise ValueError("Formula does not use any dataset variables!")

        command.append(start)

    command = ";".join(command).replace(" ", "")

    def split_this(mystr):
        return re.split("([+-/*()<>|&=])", mystr)

    command = " ".join(split_this(command)).replace(" . ", ".").replace(";", " ; ")

    for term in command.split(" "):

        if "." in term:
            pattern1 = re.compile(r"[a-zA-Z]")
            if len(pattern1.findall(term)) > 0:
                if term.split(".")[0] in frame.f_back.f_locals:
                    try:
                        new_term = eval(term, globals(), frame.f_back.f_locals)
                        if isinstance(new_term, str):
                            raise ValueError(f"{new_term} is not numeric!")
                        if is_number(str(new_term)) is False:
                            raise ValueError(f"{new_term} is not numeric!")
                        new_start = ""
                        for y in command.split(" "):
                            if y != term:
                                new_start += " " + y
                            else:
                                new_start += " " + str(new_term)
                        command = new_start
                    except:
                        raise ValueError(f"{term} is not available!")
                else:
                    raise ValueError(f"{term} is not available!")

    command = command.replace(" ", "")

    del frame

    # create the cdo call and run it
    if drop is False:
        cdo_command = f"cdo -aexpr,'{command}'"
    else:
        cdo_command = f"cdo -expr,'{command}'"

    # at this point, we need to generate a new datasets with the min, max values etc.
    #
    # gg/
    #
    # would be
    # data = nc.open_data()
    #

    # run_this(cdo_command, self, output="ensemble")
