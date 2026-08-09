from collections.abc import Callable


class Calculator:
    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        postfix = self._infix_to_postfix(tokens)
        return self._evaluate_postfix(postfix)

    def _infix_to_postfix(self, tokens: list[str]) -> list[str]:
        output: list[str] = []
        operators: list[str] = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    output.append(operators.pop())
                operators.append(token)
            else:
                output.append(token)

        while operators:
            output.append(operators.pop())

        return output

    def _evaluate_postfix(self, tokens: list[str]) -> float:
        values: list[float] = []

        for token in tokens:
            if token in self.operators:
                b = values.pop()
                a = values.pop()
                values.append(self.operators[token](a, b))
            else:
                values.append(float(token))

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]
