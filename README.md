# expert_system
Project of School42

A backward-chaining inference engine.

## Example of input

```
A => B
B | E => C + D
=A
?DC
```
what should be read as
```
A implies B
B or E implies C and D
initially A is true
what is D and C ?
```
expert system processes such input and answers
the given question

### Facts
`A,B,C,D,E ...` are facts.
Facts can be `false` or `true`,
by default all facts are `false`

### Operators
`|,+,^` are logical operators `or`,`and`,`xor` respectively

### Implication
`=>` is an implication that can change facts
if left hand side of `=>` is true then right hand
side is also true (each rhs fact will be set as `true`)
if it's `false`, rhs will remain unchanged

### Comments
Inline/line comments are also allowed.
`Comment` must start with `#` symbol,
everything from it and to the end of line
will be ignored by expert system

## Big O notation
1. Build a graph: `O(N^3)`
2. Resolve a graph: `O(|V| + |E|)`

where `N` is a number of rules, `(V,E)` is a number of vertices and edges
respectively

## How to run:
```
python3.6 -m expert_system.main <filepath>
```

## How to test:
```
python3.6 -m unittest
```
