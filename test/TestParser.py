import re

class TestParserError(Exception):
    pass

class TestParser:
    """This class gives more flexibility to tests.
       It allows to change initial facts and 
       questions, gives expected values for specified
       facts. This is achieved via specific syntax
       in comment lines

       Example:

       A => B
       B | K => C + D

       =K
       ?D

       #=AR +MT -SO

       Notice:
           Input should be valid for expert system
       What does really important it's the last line
       "#=AR +MT -SO" it changes initial facts to AR
       and says that test should expect MT as True,
       while SO as False, MT and SO also become
       questions in parse() output:

       A => B
       B | K => C + D

       =AR
       ?MTSO

       #=AR +MT -SO

       also there'll be info about what facts should be false
       and what true after processing such input by expert
       system
    """

    _defines_format = r'(?m)^=[A-Z]*$'
    _questions_format = r'(?m)^\?[A-Z]+$'
    _cmnt_format = r'(?m)^#(?P<defines>=[A-Z]*)'
    _cmnt_format += r'( \+(?P<pos>[A-Z]+))?'
    _cmnt_format += r'( -(?P<neg>[A-Z]+))?$'

    @classmethod
    def parse(cls, content):
        """parse(content) -> generator which
           generates (text, pos, neg) for every
           comment line in input with specified format as below.
           'text' is multiline string
           (modified input), 'pos' is list of
           facts that should to be true and
           'neg' which is a list of facts
           that should to be false.

           a simplified syntax is:
           #=[A-Z]* \+[A-Z]+ -[A-Z]+

           It's allowed to specify only - or + facts
           but if both are absent TestParserError
           is raised
        """
        for match in re.finditer(cls._cmnt_format, content):
            new_defines = match.group('defines')
            pos = match.group('pos')
            neg = match.group('neg')
            if not pos and not neg:
                raise TestParserError('+ or - facts must be defined')
            new_questions = '?' + (pos or '') + (neg or '')
            imds = re.sub(cls._defines_format, new_defines, content) 
            imds = re.sub(cls._questions_format, new_questions, imds)
            yield (imds, pos, neg)
