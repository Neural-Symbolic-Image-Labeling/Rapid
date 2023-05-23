import re
string_with_newlines = """
{
  "downtown(X)": [
    [
      "building(X,B)",
      "pavement(X,E)"
    ],
    [
      "building(X,B)",
      "buildings(X,F)"
    ],
    [
      "building(X,B)",
      "window(X,A)"
    ],
    [
      "street(X,C)",
      "pavement(X,E)"
    ],
    [
      "man(X,D)"
    ]
  ],
  "highway(X)": [
    [
      "car(X,D)",
      "¬building(X,B)",
      "¬mountain(X,C)",
      "¬pavement(X,I)"
    ],
    [
      "color(H,green)"
    ],
    [
      "color(D,white)",
      "¬street(X,E)",
      "¬mountain(X,C)"
    ],
    [
      "bridge(X,J)"
    ],
    [
      "color(F,white)",
      "color(G,black)"
    ],
    [
      "color(A,white)",
      "car(X,D)"
    ]
  ],
  "mountain road(X)": [
    [
      "mountain(X,C)",
      "color(A,blue)"
    ],
    [
      "¬car(X,D)",
      "¬building(X,B)",
      "¬pavement(X,F)",
      "¬tracks(X,H)"
    ],
    [
      "clouds(X,G)",
      "line(X,E)"
    ]
  ]
}
"""

# Use the replace() method to replace all newline and whitespace characters with a space
one_line_string = string_with_newlines.replace("\n", "").replace("\t", "")
one_line_string = re.sub(r'(?:(?<=[\[|\]|\{|\}\"])\s+)|(?:\s+(?=[\[|\]|\{|\}\"]))', '', one_line_string)

print(one_line_string)
# Output: Thisisastringwithnewlinesandsomewhitespaces
