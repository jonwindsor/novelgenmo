import random
import re

#Weasyprint import/installation
!pip install weasyprint==52.5
import markdown
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration

#Markovify import/instillation
!pip install markovify
import markovify

#Gutenberg novel import
with open("/content/junglebook") as f:
  text = f.read()
  
#Markovify Code / by Zach Whalen
ngrams = []

for b in range(len(text) - 4):
  ngrams.append(text[b:b+4])

random.shuffle(ngrams)
seed = random.choice(ngrams)

new_text = seed

for i in range(50000):
  for n in ngrams:
    if (n[:3] == new_text[-3:]):
      new_text += n[-1]
      ngrams.remove(n)

print(new_text)

#PDF HTML Preliminary Code / by Zach Whalen
novel = """

# Surelephaniwake
### By Jonathan Windsor
---
"""

# How about 10 chapters of 5000 words each

for c in range(1,10):

  # Add a chapter title
  novel += f"## Chapter {c}\n"

  # Add the word "HA" 5000 times
  for w in range(5000):
    novel += text
    if (random.randrange(10) < 2):
      novel += random.choice(['. ', ' -- ','? ',', and ','. ','! ','.\n\n'])


  novel += "\n\n\n\n\n\n"

html = markdown.markdown(novel)

# Prepares WeasyPrint / by Zach Whalen
font_config = FontConfiguration()
rendered_html = HTML(string=html)

# The following bit of CSS formats the content of the pages, adding
# page numbers. Here's a good overview of the options:
# https://www.quackit.com/css/at-rules/css_page_at-rule.cfm 

css = CSS(string='''
@import url('https://fonts.googleapis.com/css2?family=Festive&display=swap');

@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300&display=swap');
body {
font-family: 'Merriweather', serif;
}

hr {
  break-after: recto; 
}

h1 {
  font-size: 50pt;
  text-align:center;
  margin-top: 3in;
  font-family: 'Festive',cursive;
}
h2{
  break-before: recto;
  font-family: 'Festive',cursive;
}

h3 {
  font-size: 20pt;
  text-align:center;
}

/* set the basic page geometry and start the incrementer */
@page {
  font-family: 'Merriweather', serif;
  margin: 1in;
  size: letter;
  counter-increment: page;
  @bottom-center {
    content: "Surelephaniwake";
    text-align:center;
    font-style: italic;
    color: #666666;
  }
}

/* print the page number on the bottom-right of recto pages */
@page :right {
  @bottom-right{
    content: "[" counter(page) "]";
    text-align:right;
    color: #666666;
    visibility: invisible;
  }
}

/* print the page number on the bottom-left of verso pages */
@page :left {
  @bottom-left{
    content: "[" counter(page) "]";
    text-align:left;
    color: #666666;
  }
}

/* blank the footer on the first page */
@page:first{
  @bottom-left {content: ""}
  @bottom-right {content: ""}
  @bottom-center {content: ""}
}


''', font_config=font_config)

rendered_html.write_pdf('/content/sample.pdf', stylesheets=[css],font_config=font_config)
