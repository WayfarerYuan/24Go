from flask import Flask, render_template, request, redirect, url_for
import itertools
import re

app = Flask(__name__)

def standardize(solution):
    def sort_expr(match):
        expr = match.group(0)
        numbers = sorted(re.findall(r"\d+", expr))
        return "+".join(numbers) if "+" in expr else "*".join(numbers)
    return re.sub(r"\d+( [+*] \d+)+", sort_expr, solution)

def calculate24(nums):
    solutions = set()
    for num_permutation in itertools.permutations(nums):
        for op_permutation in itertools.product('+-*/', repeat=3):
            formula = f"({num_permutation[0]}{op_permutation[0]}{num_permutation[1]}){op_permutation[1]}{num_permutation[2]}{op_permutation[2]}{num_permutation[3]}"
            try:
                if abs(eval(formula) - 24.0) < 1e-6:  # Allow for floating point imprecision
                    formula = standardize(formula)
                    if formula not in solutions:
                        solutions.add(formula)
                        yield formula
            except ZeroDivisionError:
                pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nums = [int(num) for num in request.form.values()]
        solutions = list(calculate24(nums))
        return render_template('solutions.html', solutions=solutions)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)