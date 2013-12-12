# Playground
Playground is a Gentic Programming framework implemented in Python. Currently
features:

- Genetic Programming in Trees
- Tree Genetic Operators:
    - Selection
        - Roulette wheel selection
        - Tournament selection
    - Crossover
        - One point crossover
    - Mutation
        - Point mutation
        - Hoist mutation
        - Subtree mutation
        - Shrink mutation
        - Expand mutation
- Multicore Evaluation
- JSON config files
- Ability to record evolution process to database (PostgreSQL)


## Requirements

- Python (version 2.7 and higher)


## Optional Requirements

If you want evolution recording (such as fitness/evaluation score vs time):

- PostgreSQL (version 9.3 and higher)
- Psycopg (version 2.5 and higher)


## Licence
LGPL License
Copyright (C) <2013> Chris Choi

This program is free software: you can redistribute it and/or modify it under
the terms of the Lesser GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

[1]: https://travis-ci.org/chutsu/evolve
