from pypdf import PdfWriter, PdfReader, Transformation
from copy import deepcopy
import re
import math
import pdfplumber
import click


# === === Constants === ===

# used to space around the extracted texts
FONT_ADJUSTMENTS = 9

# === === --------- === ===


def create_exercise_pdf(input_pdf, splits, template_pdf, file_name="out.pdf"):

    input_reader = PdfReader(input_pdf)
    template_reader = PdfReader(template_pdf)

    exercise_pdf = PdfWriter()
    result_pdf = PdfWriter()


    for page_index, page_splits in enumerate(splits):
        for split_index in range(len(page_splits) + 1):

            from_y = page_splits[split_index - 1] if split_index >= 1 else 0
            to_y = page_splits[split_index] if split_index < len(page_splits) else -1

            exercise_page = input_reader.pages[page_index]

            backup_mediabox_top = exercise_page.mediabox.top
            backup_mediabox_bottom = exercise_page.mediabox.bottom

            page_y_top = exercise_page.mediabox.top - from_y
            page_y_bottom = exercise_page.mediabox.top - to_y if to_y > 0 else 0

            # the top and bottom parameters of the mediabox
            # are both y values where the y axis starts from the bottom
            # and they are absolute to the page
            exercise_page.mediabox.top = page_y_top
            exercise_page.mediabox.bottom = page_y_bottom

            exercise_pdf.add_page(exercise_page)


            exercise_page.mediabox.top = backup_mediabox_top
            exercise_page.mediabox.bottom = backup_mediabox_bottom


    template_page = template_reader.pages[0]


    distances_to_top = []

    for page_splits in splits:
        distances_to_top.append(0)
        distances_to_top += page_splits

    for index, exercise in enumerate(exercise_pdf.pages):
        template_with_exercise = deepcopy(template_page)

        offset = distances_to_top[index]

        # move document up
        move_to_top = Transformation().translate(ty=offset)
        exercise.add_transformation(move_to_top)
        # move mediabox up
        exercise.mediabox.top += offset
        exercise.mediabox.bottom += offset

        template_with_exercise.merge_page(exercise)

        result_pdf.add_page(template_with_exercise)

    with open("./" + file_name, "wb") as fp:
        result_pdf.write(fp)




def get_splits_deprecated(input_pdf, heading_format):

    reader = PdfReader(input_pdf)

    splits = []
    current_page_splits = []
    current_page = 0

    def extract_task_heading(text, cm, tm, font_dict, font_size):
        if re.match(heading_format, text):
            print(text + " ", end="")
            em2 = font_size * 2
            y = tm[5]

            # arbitrary value, had to play around to get something that works
            # the pypdf library cant provide the exact location of the text
            if current_page == 0:
                y += em2
            else:
                y -= em2

            current_page_splits.append(math.floor(y))

    for index, page in enumerate(reader.pages):
        current_page = index
        _ = page.extract_text(visitor_text=extract_task_heading)
        temp = []
        for element in current_page_splits:
            temp.insert(0, element)
        splits.append(temp)
        current_page_splits = []

    # splits = [[300, 1000, 2000, 2500], [100, 300, 600]]
    print(splits)

    return splits

def get_splits(input_pdf, heading_format):
    splits = []
    with pdfplumber.open(input_pdf) as pdf:
        for page in pdf.pages:
            page_splits = []
            for word in page.extract_words():
                text = word["text"]
                y0 = word["top"]

                if re.match(heading_format, text):
                    print(" - " + text)
                    page_splits.append(math.floor(y0) - FONT_ADJUSTMENTS)

            splits.append(page_splits)

    return splits



@click.command()
@click.option('--out', default='out.pdf', help='name of the output file. default will be out.pdf. include the file ending')
@click.option('--format', default=r"[A-Za-z]+[0-9]+\.[0-9]+", help="regex to match the exercises. default will be suitable for tasks in the format LETTER NUMBER DOT NUMBER")
@click.option('--spacing', default=9, help='add some spacing around the exercises. The deafult value should work in most cases')
@click.argument('input_pdf')
@click.argument('template_pdf')
def extract_exercises(out, format, spacing, input_pdf, template_pdf):
    # splits = [[200, 330, 510, 620], [170, 310, 460, 600]]

    FONT_ADJUSTMENTS = spacing
    splits = get_splits(input_pdf, format)
    create_exercise_pdf(input_pdf, splits, template_pdf, out)



if __name__ == "__main__":
    extract_exercises()

