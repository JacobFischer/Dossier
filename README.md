# Dossier
The auto-doc manager for Cadre projects

![{Cadre}](http://i.imgur.com/17wwI3f.png)

All inspiration taken from [MST's SIG-GAME framework](https://github.com/siggame), and most of the terminology is assuming some familiarity with it as this is a spiritual successor to it.

This could be thought of as a glorified bash script. In fact it very well could have been written in bash, I just like python more.

All Cadre projects that use an auto doc system should have a `_dossier.data` file which instructs this script how to build and run it's auto-doc system.

## How To Run

`
python main.py -i ../directory/to/search ../another/one/ ../etc -o ../where/you/want/the/output
`

If an error occurs it should be printed to the console with some information about why the error occured.

## Purpose

The primary purpose is so that the html docs can be easily generated with one command. Just like Creer generates code, this generates docs, though it uses popular document generators in the process.
