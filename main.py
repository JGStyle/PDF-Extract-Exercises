from pypdf import PdfWriter, PdfReader, Transformation
from copy import deepcopy
import math
from itertools import chain

# === === Constants === ===

project_dir = "/Users/jgs/Developer/Projekte/PDFsplit"

# === === --------- === ===


def create_exercise_pdf(input_pdf, splits, template_pdf, out_dir, file_name="out.pdf"):

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
            # and they are absolute to the document
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

        print("ex#" + str(index) + " d@" + str(distances_to_top[index]))

        move_to_top = Transformation().translate(ty=distances_to_top[index])

        exercise.add_transformation(move_to_top)
        template_with_exercise.merge_page(exercise)

        result_pdf.add_page(template_with_exercise)

    with open(out_dir + "/" + file_name, "wb") as fp:
        result_pdf.write(fp)



def get_splits(input_pdf):
    # TODO

    # splits = [[300, 1000, 2000, 2500], [100, 300, 600]]
    splits = [[200, 330, 530, 620], [200, 330, 530, 620]]

    return splits


if __name__ == "__main__":

    input_pdf = project_dir + "/in/blatt-aufg.pdf"
    template_pdf = project_dir + "/templates/a4_dotted.pdf"
    out_dir = project_dir + "/out"

    
    splits = get_splits(input_pdf)

    create_exercise_pdf(input_pdf, splits, template_pdf, out_dir)
    




