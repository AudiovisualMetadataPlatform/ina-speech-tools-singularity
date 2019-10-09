#!/usr/bin/env python3

import sys
import json
import os
import subprocess

from segmentation_schema import SegmentationSchema
from inaSpeechSegmenter import Segmenter

def main():
    (input_file, json_file) = sys.argv[1:3]
    
    # Run ina_speech_segmenter on input file
    # the result is a list of tuples
    # each tuple contains:
    # * label in 'Male', 'Female', 'Music', 'NOACTIVITY'
    # * start time of the segment
    # * end time of the segment
    seg = Segmenter()
    segmentation = seg(input_file)

    # Convert the resulting list of tuples to an object for serialization
    seg_schema = convert_to_segmentation_schema(input_file, segmentation)

    # Serialize the json and write it to destination file
    write_output_json(seg_schema, json_file)
    exit(0)

def convert_to_segmentation_schema(filename, segmentation):
    # Create a segmentation object to serialize
    seg_schema = SegmentationSchema(filename)

    # For each segment returned by the ina_speech_segmenter, add 
    # a corresponding segment formatted to json spec
    for segment in segmentation:
        label = get_label(segment[0])
        gender = get_gender(segment[0])
        start = segment[1]
        end = segment[2]
        seg_schema.addSegment(label, gender, start, end)

    return seg_schema

# Recode label values to {speech, music, silence}
def get_label(value):
    if value == "Male" or value == "Female":
        return "speech"
    elif value == "Music":
        return "music"
    elif value == "NOACTIVITY":
        return "silence"

    return value

# Recode gender to {male, female, ""}
def get_gender(value):
    if value == "Male" or value == "Female":
        return value.lower()

    return ""

# Serialize schema obj and write it to output file
def write_output_json(seg_schema, json_file):
    # Serialize the segmentation object
    with open(json_file, 'w') as outfile:
        json.dump(seg_schema, outfile, default=lambda x: x.__dict__)

if __name__ == "__main__":
    if "INASPEECH_OLDPWD" in os.environ:
         os.chdir(os.environ["INASPEECH_OLDPWD"])
    main()
