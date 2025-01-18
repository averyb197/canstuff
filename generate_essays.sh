#!/bin/bash


MODEL_FILE="models.txt"
N_VALUE=3
GRADES=(6 8 10 12)

for GRADE in "${GRADES[@]}"; do
    OUTPUT_FILE="data/varied_temp_grade${GRADE}_short.json"
    python3 main.py -mf "$MODEL_FILE" -of "$OUTPUT_FILE" -n "$N_VALUE" -g "$GRADE"
done

for GRADE in "${GRADES[@]}"; do
    OUTPUT_FILE="data/varied_temp_grade${GRADE}_long.json"
    python3 main.py -mf "$MODEL_FILE" -of "$OUTPUT_FILE" -n "$N_VALUE" -g "$GRADE" -l "long"
done
