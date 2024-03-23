#!/bin/env bash

# Reduce audio file sizes using ffmpeg
# only need to set SRC and DEST variables appropriately

trap "printf '\n\n...exiting\n';exit" INT

SRC="/storage/emulated/0/Xender/audio"
DEST="${SRC}.compressed"

mkdir -p "$DEST"

I=1;

oIFS=$IFS;
IFS=$(echo -en "\n\b");

for f in $SRC/*; do
    file="${f##*/}";
    #printf '\n\n%s\n' "[ $I ] compressing: $file";
    echo $f
    ffmpeg -i "$f" -acodec libvorbis -vn -b:a 48k -ar 44100 -ac 1 "$DEST/${file%.*}.ogg";
    I=$(($i + 1));
done
printf "\ncompressed $I file(s) from $SRC to $DEST\n\n";

read -p "clear SRC directory, replacing any DEST files bigger than SRC files: " answer
case $answer in
    [yY]|[yY][eE]|[yY][eE][sSpP]) 
	for f in $SRC/*; do
	    file="${f##*/}";
	    test -f "$DEST/${file%.*}.ogg" || continue;
	    src_size=$(wc -c "$f"|awk '{printf $1}');
	    dest_size=$(wc -c "$DEST/${file%.*}.ogg"|awk '{printf $1}');
	    if [[ $src_size -lt $dest_size ]]; then
		rm "$DEST/${file%.*}.ogg";
		mv "$f" "$DEST/$file";
	    else
		rm "$f"
	    fi
	done
	rmdir "$SRC";
    ;;
esac

IFS=$oIFS;
