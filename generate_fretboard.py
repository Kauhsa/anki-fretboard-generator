class HorizontalPositionCalculator:
    def __init__(self, first_fret_width):
        self.first_fret_width = first_fret_width

    def fret(self, fret_number):
        """
        Return the position of the given fret number.
        """

        # https://en.wikipedia.org/wiki/Twelfth_root_of_two
        fret_multiplier = 1 / (2 ** (1 / 12))

        # https://en.wikipedia.org/wiki/Geometric_series
        return self.first_fret_width * (
            (1 - fret_multiplier**fret_number) / (1 - fret_multiplier)
        )

    def marker(self, fret_number):
        # The position of the marker is exactly between previous and current fret.
        return (self.fret(fret_number - 1) + self.fret(fret_number)) / 2


class VerticalPositionCalculator:
    def __init__(self, string_height, string_count):
        self.string_height = string_height
        self.string_count = string_count

    def string(self, string_number):
        return string_number * self.string_height + (self.string_height / 2)

    def neck_height(self):
        return self.string_height * self.string_count


def generate_fretboard_svg(
    fret_count=21,
    first_fret_width=50,
    background="#F0D9B5",
    string_widths=[4, 3, 2.5, 2],
    highlight_position=(1, 2),
):
    """
    Generate a fretboard SVG image with the given number of strings and frets.
    """

    svg_xml_template = """
    <svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
        <rect id="neck" width="{width}" height="{height}" fill="{background}" />
        <g id="markers">
            {markers}
        </g>
        <g id="frets">
            {frets}
        </g>
        <g id="strings">
            {strings}
        </g>
        <g id="highlight">
            {highlight}
        </g>
    </svg>
    """

    strings_template = """
    <line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#888" stroke-width="{stroke_width}" />
    """

    frets_template = """
    <line x1="{x}" y1="0" x2="{x}" y2="{height}" stroke="black" stroke-width="1" />
    """

    marker_template = """
    <circle cx="{x}" cy="{y}" r="5" stroke="black" stroke-width="1" fill="white" />
    """

    highlight_template = """
    <circle cx="{x}" cy="{y}" r="7.5" fill="red" />
    """

    string_height = 20
    horizontal_pos = HorizontalPositionCalculator(first_fret_width)
    vertical_pos = VerticalPositionCalculator(string_height, len(string_widths))
    neck_height = vertical_pos.neck_height()
    total_width = horizontal_pos.fret(fret_count)

    strings = ""
    for i, stroke_width in enumerate(string_widths):
        y = vertical_pos.string(i)
        strings += strings_template.format(
            y=y, width=total_width, stroke_width=stroke_width
        )

    frets = ""
    for i in range(1, fret_count):
        x = horizontal_pos.fret(i)
        frets += frets_template.format(x=x, height=neck_height)

    markers = ""
    for i in range(1, fret_count):
        x = horizontal_pos.marker(i)
        has_single_marker = i % 12 in [3, 5, 7, 9]
        has_double_marker = i % 12 == 0

        if has_single_marker:
            y = neck_height / 2
            markers += marker_template.format(x=x, y=y)
        elif has_double_marker:
            y1 = neck_height * (1 / 4)
            y2 = neck_height * (3 / 4)
            markers += marker_template.format(x=x, y=y1)
            markers += marker_template.format(x=x, y=y2)

    highlight = ""
    if highlight_position:
        highlight_x = horizontal_pos.marker(highlight_position[0])
        highlight_y = vertical_pos.string(highlight_position[1])
        highlight = highlight_template.format(x=highlight_x, y=highlight_y)

    return svg_xml_template.format(
        width=total_width,
        height=neck_height,
        strings=strings,
        frets=frets,
        highlight=highlight,
        markers=markers,
        background=background,
    )


if __name__ == "__main__":
    print(generate_fretboard_svg())
