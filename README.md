HyFi
====

HyFi (Hyphen Fixer) is a tool to fix the hyphenation at the end of lines in text imported from PDF files and similar sources.

**Features**

* Joins words at the end and beginning of lines, where the end-word is hyphenated.
* Checks a dictionary to ensure the joined word is valid English. If the word isn't recognized, a warning is issued and the word isn't joined.
* Provides an option to output unrecognized words, along with their potential corrected form, to a file for later review.
* Allows for user-defined rules to be specified for unrecognized words, which are then applied in the joining process.

## Installation

HyFi is designed to run on Linux machines. Follow the steps below to install it:

1. Copy the hyfi.py file to your bin directory:

```bash
cp hyfi.py ~/bin/
```

2. Make sure the file is executable. You can do this using the chmod command:

```bash
chmod +x ~/bin/hyfi.py
```

After these steps, you should be able to run the hyfi.py command from any location in your command line terminal.

## Command Line Interface (CLI)

The general usage of HyFi's CLI is as follows. The CLI accepts options and arguments to customize its behavior.

### Basic CLI usage

```
hyfi.py [-h] [-o OUTPUT] [-u UNRECOGNIZED_PAIRS] [-r REPLACEMENT_RULES] [INPUT]
```

**Arguments**

INPUT: The text file to process. If not specified, input is taken from stdin.

**Options**

* -h, --help: Show a help message and exit.
* -o OUTPUT, --output OUTPUT: The path to the output text file. If not specified, output is written to stdout.
* -u UNRECOGNIZED_PAIRS, --unrecognized-pairs UNRECOGNIZED_PAIRS: Output unrecognized words and their potential correction to a file.
* -r REPLACEMENT_RULES, --replacement-rules REPLACEMENT_RULES: Specify a file containing user-defined replacement rules.

### Usage Examples

**Simple Usage**

In this usage scenario, words that would issue warnings are ignored.

```bash
$ hyfi input.txt -o output.txt
```

This command reads from the input.txt file, corrects hyphenated end-words and writes the output to output.txt.
Save unrecognized words and use them as custom rules

In this usage scenario, unrecognized words are saved and then edited by the user to create a set of custom rules.

```bash
$ hyfi input.txt -o output.txt -u unrecognized.txt
```

This command saves the unrecognized words and their potential correction to unrecognized.txt. After this, the user manually edits the unrecognized.txt file to remove unwanted entries.

```bash
$ hyfi input.txt -o output.txt -r unrecognized.txt
```

This command uses the user-edited unrecognized.txt as a set of custom rules. With these rules, the command corrects hyphenated end-words while taking into account the user's edits.

## Acknowledgments

I would like to express my deep gratitude to OpenAI's ChatGPT. The major parts of this tool's codebase and its user guide were written by ChatGPT. While its contributions can't currently be recognized formally in terms of copyright, I believe it's important to acknowledge the significant role it played in the development of HyFi. Its ability to understand complex requirements, propose solutions, and even generate high-quality, runnable code is genuinely impressive. I look forward to seeing what AI can do in the future for the world of software development.
