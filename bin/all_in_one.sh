#!/bin/bash 

cat ../data/res.out_json_offline | python parse_menu.py > ../data/merge_menu.res 2> ../data/merge_menu.err 
python merge_stat.py > ../data/merge_stat.res 2> ../data/merge_stat.err
