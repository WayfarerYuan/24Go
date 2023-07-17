from flask import Flask, render_template, request

app = Flask(__name__)

def dfs(nums, target, expression, current_val, index, solutions):
    if index == len(nums):
        if abs(current_val - target) < 1e-6:  # Allow for floating point imprecision
            solutions.append(expression)
        return

    num = nums[index]

    # Addition operation
    dfs(nums, target, f"({expression} + {num})", current_val + num, index + 1, solutions)

    # Subtraction operation (try both orders)
    dfs(nums, target, f"({expression} - {num})", current_val - num, index + 1, solutions)
    dfs(nums, target, f"({num} - {expression})", num - current_val, index + 1, solutions)

    # Multiplication operation
    dfs(nums, target, f"({expression} * {num})", current_val * num, index + 1, solutions)

    # Division operation (try both orders, avoid division by zero)
    if num != 0:
        dfs(nums, target, f"({expression} / {num})", current_val / num, index + 1, solutions)
    if current_val != 0:
        dfs(nums, target, f"({num} / {expression})", num / current_val, index + 1, solutions)



def calculate24(nums):
    solutions = []
    dfs(nums, 24, str(nums[0]), nums[0], 1, solutions)
    return solutions


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nums = [int(num) for num in request.form.values()]
        solutions = calculate24(nums)
        return render_template('solutions.html', solutions=solutions)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

