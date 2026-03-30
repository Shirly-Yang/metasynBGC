# metasynBGC
This repository currently contains the core Python scripts for a biosynthetic gene cluster (BGC) analysis pipeline.

## Requirements
The pipeline depends on the following tools and environments:
- Python ≥ 3.7
- Recommended packages:
  - tqdm
  - multiprocessing (standard library)
External tools
Make sure the following tools are installed and available in your $PATH:
- Prokka
- Roary
- DIAMOND
- antiSMASH

## Usage
- At present, scripts are intended to be executed as part of a custom workflow.
- Many scripts rely on user-defined file paths. Before running any script, you must modify the paths according to your local environment.
- Absolute paths are currently hardcoded in some scripts.
- Ensure all input files exist before execution.
- Output directories must have write permission.
- Inconsistent paths across scripts may lead to runtime errors.

## Contact
For questions, suggestions, or collaboration, please open an issue or contact the author.
