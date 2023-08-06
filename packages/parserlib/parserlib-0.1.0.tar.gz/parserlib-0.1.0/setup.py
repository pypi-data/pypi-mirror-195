# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parserlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parserlib',
    'version': '0.1.0',
    'description': 'A Pythonic parser implementation!',
    'long_description': '# parserlib\n\nA Pythonic parser implementation!\n\n\n## Installation\n\n```bash\n    pip install parserlib\n```\n\n\n## Example\n\n```py\n\nfrom parserlib.lexer import Lexer\nfrom parserlib.parser import Rule, ShiftReduceParser\nfrom parserlib.token import Token\n\n\nclass NumberToken(Token):\n    name = "NUMBER"\n    regex = r"\\d+"\n\n\nclass PlusToken(Token):\n    name = "PLUS"\n    regex = r"\\+"\n\n\nclass MinusToken(Token):\n    name = "MINUS"\n    regex = r"-"\n\n\nclass LeftParenthesisToken(Token):\n    name = "LEFT_PARENTHESIS"\n    regex = r"\\("\n\n\nclass RightParenthesisToken(Token):\n    name = "RIGHT_PARENTHESIS"\n    regex = r"\\)"\n\n\nclass AsteriskToken(Token):\n    name = "ASTERISK"\n    regex = r"\\*"\n\n\nclass SlashToken(Token):\n    name = "SLASH"\n    regex = r"/"\n\n\nclass Expression(Rule):\n    pass\n\n\nclass NumberExpression(Expression):\n    def __init__(self, number: NumberToken):\n        self.number = number\n\n    @classmethod\n    def reduce(cls, number: NumberToken) -> Expression:\n        return cls(number)\n\n\nclass ParenthesisExpression(Expression):\n    @classmethod\n    def reduce(\n        cls, _: LeftParenthesisToken, expression: Expression, __: RightParenthesisToken\n    ) -> Expression:\n        return expression\n\n\nclass PlusExpression(Expression):\n    def __init__(self, left: Expression, right: Expression):\n        self.left = left\n        self.right = right\n\n    @classmethod\n    def reduce(cls, left: Expression, _: PlusToken, right: Expression) -> Expression:\n        return cls(left, right)\n\n\nclass MinusExpression(Expression):\n    def __init__(self, left: Expression, right: Expression):\n        self.left = left\n        self.right = right\n\n    @classmethod\n    def reduce(cls, left: Expression, _: MinusToken, right: Expression) -> Expression:\n        return cls(left, right)\n\n\nclass TimesExpression(Expression):\n    def __init__(self, left: Expression, right: Expression):\n        self.left = left\n        self.right = right\n\n    @classmethod\n    def reduce(\n        cls, left: Expression, _: AsteriskToken, right: Expression\n    ) -> Expression:\n        return cls(left, right)\n\n\nclass DivideExpression(Expression):\n    def __init__(self, left: Expression, right: Expression):\n        self.left = left\n        self.right = right\n\n    @classmethod\n    def reduce(cls, left: Expression, _: SlashToken, right: Expression) -> Expression:\n        return cls(left, right)\n\n\nlexer = Lexer(\n    tokens=(\n        NumberToken,\n        PlusToken,\n        MinusToken,\n        LeftParenthesisToken,\n        RightParenthesisToken,\n        AsteriskToken,\n        SlashToken,\n    ),\n    ignore_characters=" \\t",\n)\nparser = ShiftReduceParser(\n    rules=(\n        ParenthesisExpression,\n        PlusExpression,\n        MinusExpression,\n        TimesExpression,\n        DivideExpression,\n        NumberExpression,\n    ),\n    precedence=(\n        (ParenthesisExpression,),\n        (TimesExpression, DivideExpression),\n        (PlusExpression, MinusExpression),\n    ),\n)\ntree = parser.parse(lexer.feed("1 + \\n(2) * 3"))\nprint(tree)\n\n\n```\n',
    'author': 'Nate',
    'author_email': 'minecraftcrusher100@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
