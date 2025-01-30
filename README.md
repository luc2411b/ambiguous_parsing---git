# Ambiguous Sentence Generation

## Overview

This repository contains Python scripts for systematically generating syntactically ambiguous sentences, with their possible interpretations, for linguistic analysis. Used for thesis on human ambiguity resolving.

## Features

- Generates sentence pairs with connective precedence, negation scope, and quantifier scope ambiguities.
- Outputs sentences with possible interpretations in formal and natural language, generated based on pre-defined templates.

## Usage

Run the `generate_pairs.py` script to generate sentence pairs:

This script randomly selects elements from predefined fixtures and outputs generated sentences.

## File Structure

```
.
|-- generate_pairs.py     # Main script for sentence generation
|-- template.py           # Template class for constructing sentences
|-- fixtures/
|   |-- nps.py            # Predefined noun phrases
|   |-- vps.py            # Predefined verb phrases
|-- .gitignore            # Git ignore file
|-- .gitattributes        # Git attributes
```

### Key Components

- `generate_pairs.py`: Main script that constructs ambiguous sentences using predefined templates.
- `template.py`: Defines the `Template` class, which structures and formats generated sentences.
- `fixtures/nps.py`: Contains predefined noun phrases categorized by characteristics (e.g., definite/indefinite, human/non-human).
- `fixtures/vps.py`: Contains predefined verb phrases categorized by action type.

## Contact

For questions or support, contact the repository owner or refer to the thesis documentation.
