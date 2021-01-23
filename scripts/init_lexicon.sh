# Usage - bash init_lexicon.sh book_author
# e.g. - bash init_lexicon.sh abhidhanachintamani_hemchandra
cd ..
mkdir $1
cd $1
mkdir orig
mkdir babylon
mkdir md
mkdir xml
mkdir html
mkdir sample
mkdir json
mkdir slp
mkdir cologne
touch orig/$1_googleocr.txt
cd ../scripts
