#!/bin/env bash

MUSIC_DIR=$HOME/storage/music
PLAYLIST=
PLAYLIST_DIR=$HOME/.011/.011.cfg/cmus_playlists
CMUS_PLAYLIST_DIR=$HOME/.config/cmus/playlists
CMUS_SYMLNKS=0
PLAYLIST_OVERWRITE=0
LN_CMD="ln -si"
WRITE_CMD=': '

mkdir -p "$PLAYLIST_DIR"

function dop(){ 

DIR="$1"
if test -d "$DIR"; then

local PLAYLIST="$PLAYLIST${PLAYLIST:+_}${DIR##*/}"
test -e "$PLAYLIST_DIR/$PLAYLIST" -a $PLAYLIST_OVERWRITE -eq 1 \
    && MSG="WARRNING: playlist '$PLAYLIST' exists, overwrite?" PLAYLIST_OVERWRITE=0 \
    || MSG="INFO: create playlist '$PLAYLIST'?"
test $PLAYLIST_OVERWRITE -eq 1 -o $PLAYLIST_OVERWRITE -eq 0 \
    && read  -p "$MSG [y/N/all/-/none/+/append] " PLAYLIST_OVERWRITE

test $CMUS_SYMLNKS -ne 2 -a $CMUS_SYMLNKS -ne -1 \
    && read  -p "INFO: symlink '$PLAYLIST' in cmus's default playlist directory? [y/N/all/-/none] " CMUS_SYMLNKS

PLAYLIST_OVERWRITE=$(isAnswer "$PLAYLIST_OVERWRITE")
CMUS_SYMLNKS=$(isAnswer "$CMUS_SYMLNKS")

for FILE in "$DIR"/*; do

     if test -d "$FILE"; then

	 dop "$FILE"
	 test $CMUS_SYMLNKS -eq 2 && LN_CMD="ln -sf"
	 test $CMUS_SYMLNKS -gt 0 -a -e "$PLAYLIST_DIR/$PLAYLIST" \
	     && $LN_CMD "$PLAYLIST_DIR/$PLAYLIST" "$CMUS_PLAYLIST_DIR/$PLAYLIST"

	 continue
     fi

     test $PLAYLIST_OVERWRITE -eq 2 -o $PLAYLIST_OVERWRITE -eq 1 \
	 && local WRITE_CMD="echo $FILE >" \
	 || local WRITE_CMD="echo $FILE >>"
     test $PLAYLIST_OVERWRITE -gt 0 -o ! -e "$PLAYLIST_DIR/$PLAYLIST" \
	 && $WRITE_CMD"$PLAYLIST_DIR/$PLAYLIST"
done

fi
}

function isAnswer(){
case "$1" in
    3|+|[aA][pP][pP][eE][nN][dD])
	echo -n 3
	;;
    2|[aA][lL][lL])
	echo -n 2
	;;
    1|[yY]|[yY][eE][sSpP])
	echo -n 1
	;;
    -1|-|[nN][oO][nN][eE])
	echo -n -1
	;;
    0|[nN]|[nN][oO]|[nN][oO][pP]|[nN][oO][pP][eE]) ;&
    *)
	echo -n 0
        ;;
esac
}

dop "$MUSIC_DIR"
