#!/bin/bash
#bash splitpdf.sh inputPdf outputFileName startpage endpage interval
#bash splitpdf.sh dharanikosa_3.pdf dharanikosha 18 262 25
inPDF=$1
outputfolder=$2
startpage=$3
endpage=$4
interval=$5

#mkdir $outputfolder;
for ((i=$startpage; i<$endpage; i=i+$interval))
do
	end=$(( $i+$interval-1 ));
	if [[ $end -gt $endpage ]]
	then
		let end=$endpage;
	fi
	qpdf $1 --pages $1 $i-$end -- splitPdf/"$outputfolder"_"$i"_"$end".pdf;
	echo $i-$end;
done

