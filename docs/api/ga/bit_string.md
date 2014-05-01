# playground.ga.bit_string

**Classes**:
- BitString(object)


## BitString(object)

    Attributes:

        bit_string_id (int):
            bit string id

        score (float):
            fitness score

        gnome (list):
            list containing the solution

        length (int):
            length of the gnome

    Constructor:

        BitString()


**Methods**:
- valid()
- equals(target)
- to_dict()


### valid()
Boolean function to test whether the bit string is valid.

    Returns:
        True or False


### equals(target)
Boolean function to test whether the `BitString` in question has the same gnome
as `target`.

    Returns:
        True or False


### to_dict()
Converts the `BitString` object attributes to dictionary

    Returns:

        Dictionary containing:
            - id
            - score
            - genome
            - length
