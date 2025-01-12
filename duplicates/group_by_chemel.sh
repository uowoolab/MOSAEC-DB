#!/bin/bash

echo "Extracting empirical formulas ..."

for i in *.cif
do
        cf=$(grep '_chemical_formula_sum' $i  | sed 's/_chemical_formula_sum//')
        echo "$i $cf" >> all_formulae.txt
done
cut -d ' ' -f2- all_formulae.txt | sort | uniq -c | sort -gr |  sed 's/^[ ]*//;s/[ ]*$//' > numX_chemform.txt
cut -d ' ' -f2- numX_chemform.txt | sed 's/ //g' | sed "s/'//g"  > unique_empform.txt


echo "Making lists of structures with the same chemical formula ..."
n=1
for line in $(awk '{print$1}' numX_chemform.txt)
do
        i=$(sed -n "${n}p" numX_chemform.txt | cut -d ' ' -f2- )
        ii=$(sed -n "${n}p" unique_empform.txt)
        grep "$i" all_formulae.txt | awk '{print$1}' > $ii.lst
        ((n++))
done

echo "Checking for empirical formula multiples ..."

python multiple_chemform.py unique_empform.txt

echo "Completed"
