def print_cyara_star():
    # Define the ASCII art for each letter
    # Each list must have the same number of rows (5 in this case)
    letters = {
        'C': [
            "  *** ",
            " * * ",
            " * ",
            " * * ",
            "  *** "
        ],
        'y': [
            "* * ",
            "* * ",
            " **** ",
            "    * ",
            " **** "
        ],
        'a': [
            "  *** ",
            "     * ",
            "  **** ",
            " * * ",
            "  **** "
        ],
        'r': [
            " * ** ",
            " ** * ",
            " * ",
            " * ",
            " * "
        ]
    }

    # Define the sequence of characters to print
    word = ['C', 'y', 'a', 'r', 'a']

    # Iterate through each of the 5 rows
    for i in range(5):
        row_string = ""
        for char in word:
            # Add the specific row of the current letter plus spacing
            row_string += letters[char] + "  "
        print(row_string)

if __name__ == "__main__":
    print_cyara_star()