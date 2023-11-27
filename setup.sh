#!/bin/bash

while read LIST; do
  python -m spacy download "$LIST";
done < spacy_model_list.txt
