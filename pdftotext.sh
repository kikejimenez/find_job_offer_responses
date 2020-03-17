#!/bin/bash


PARENTDIR=$PWD



function get_txt {
   echo "$TYPE...."
   DATDIR="$PARENTDIR/data/raw/$TYPE"
   mkdir -p $DATDIR
   cd $PARENTDIR/data/$TYPE/pdfs
   for filename in *.pdf;
      do
         mv $filename "pdf_$filename" 
         pdftotext "pdf_$filename" 
      done
      cp $(ls $PARENTDIR/data/$TYPE/pdfs/*.txt) $DATDIR
      cp $(ls $PARENTDIR/data/$TYPE/texts/*.txt) $DATDIR
    
}

TYPE="accept"
get_txt
TYPE="decline"
get_txt