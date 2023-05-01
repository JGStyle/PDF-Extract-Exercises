# PDF Exercise extractor

this tool is meant to make working with exercise pdfs easier
often times as a student you will receive a pdf with exercises to work through
however the creators of the pdf did not put any space around the exercises
so working on these exercises on for example an iPad is a hassle

This tool will take a pdf as input, recognize the exercises and then write
a new pdf where each exercise is on a single page with some space around it

The tool is command line based

## Example

I have included one example file in the project with the corresponding out.pdf
the pdf was generated with the command
`extract.py blatt-aufg.pdf a4_dotted.pdf`

## Remarks

- It is recommended to keep the template.pdf with the same dimensions as the input.pdf
- You can use this for any exercise pdf, just provide a regex pattern to match the exercise names. You do not need to know regex - just use https://regex-generator.olafneumann.org/?
- if the spacing for the tasks is a bit of you can enter some special spacing

## help:

In case you do not remember the cli options, just type
`extract.py --help`


```
Usage: extract.py [OPTIONS] INPUT_PDF TEMPLATE_PDF

Options:
  --out TEXT         location where the generated pdf should be put
  --format TEXT      regex to match the exercises. default will be suitable
                     for tasks in the format LETTER NUMBER DOT NUMBER
  --spacing INTEGER  add some spacing around the exercises. The deafult value
                     should work in most cases
  --help             Show this message and exit.

```
