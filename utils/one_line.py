import re
string_with_newlines = """
{
                "Myrtle_Warbler(X)": [
                    [
                        "\u00achas_belly_color(X,yellow)"
                    ],
                    [
                        "\u00achas_breast_color(X,yellow)"
                    ],
                    [
                        "\u00achas_nape_color(X,grey)"
                    ],
                    [
                        "has_bill_color(X,black)"
                    ]
                ],
                "Nashville_Warbler(X)": [
                    [
                        "\u00achas_under_tail_color(X,yellow)"
                    ],
                    [
                        "\u00achas_breast_color(X,yellow)"
                    ],
                    [
                        "has_forehead_color(X,grey)"
                    ]
                ],
                "Orange_crowned_Warbler(X)": [
                    [
                        "\u00achas_eye_color(X,black)"
                    ],
                    [
                        "\u00achas_forehead_color(X,grey)"
                    ],
                    [
                        "\u00achas_bill_color(X,black)"
                    ],
                    [
                        "has_forehead_color(X,green)"
                    ],
                    [
                        "\u00achas_leg_color(X,black)"
                    ],
                    [
                        "\u00achas_nape_color(X,grey)"
                    ],
                    [
                        "has_forehead_color(X,buff)"
                    ]
                ]
            }
"""

# Use the replace() method to replace all newline and whitespace characters with a space
one_line_string = string_with_newlines.replace("\n", "").replace("\t", "")
one_line_string = re.sub(r'(?:(?<=[\[|\]|\{|\}\"])\s+)|(?:\s+(?=[\[|\]|\{|\}\"]))', '', one_line_string)

print(one_line_string)
# Output: Thisisastringwithnewlinesandsomewhitespaces
