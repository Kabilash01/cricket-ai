#!/bin/bash
# Run the Cricket AI pipeline with proper Python path

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add src directory to PYTHONPATH
export PYTHONPATH="${SCRIPT_DIR}/src:${PYTHONPATH}"

# Run the pipeline
python "${SCRIPT_DIR}/src/pipeline/realtime_pipeline.py" "$@"
