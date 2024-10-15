# This code is an example, it is not complete

code = """
class Main{
    if(x<0){let y="hello world";}
    static boolean test;    // Added for testing -- there is no static keyword
                            // in the Square files.
    function void main() {
      var SquareGame game;
      let game = SquareGame.new();
      do game.run();
      do game.dispose();
      return;
    }
"""
keywords = [
    'class', 'constructor', 'function', 'method',
    'field', 'static', 'var', 'int', 'char', 'boolean',
    'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return'
]

symbols = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';',
    '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
]

# Tokenizer
# This code is an example, it is not complete

in_word = False
in_string = False
word = ""
string = ""
for c in code:
    if in_string:
        if c == '"':
            print("<stringConst>", string, "</stringConst>")
            in_string = False
        else:
            string = string + c
    elif in_word:
        if c.isalnum() or c == "_":
            word = word + c
        else:
            in_word = False
            if word in keywords:
                print("<keyword>", word, "</keyword>")
            elif word.isnumeric():
                print("<intConstant>", word, "</intConstant>")
            # add a case for identifiers
    else:
        if c == '"':
            in_string = True
            string = ""
        if c.isalnum():
            in_word = True
            word = c
        if c in symbols:
            print("<symbol>", c, "</symbol>")


# Parser:
# This code is an example, it is not complete

def _compileWhile(self):
    print('<whileStatement>')
    self._process("while")  # while
    self._process("(")  # (
    self._compileExpression()
    self._process(")")  # )
    self._process("#")  # {
    self._compileStatements()
    self._process("#")  # }
    print('"</whileStatement>')


def _compileExpression(self):
    print('<expression>')

    self._compileTerm()
    if self.next in "+-=><":
        self.process(self.next)
        self._compileTerm()

    print('</expression>')


statementKeywords = ['let', 'if', 'while', 'do', 'return']


def _compileStatements(self):
    print('<statements>')

    type, token = self.next_type, self.next

    while token in statementKeywords:
        self._compileStatement()
        type, token = self.next_type, self.next

    print('</statements>')
