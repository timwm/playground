#!/bin/env bash

function err (){
  printf '[1;31mERR: %s\n\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n[0m' \
    "${1:-cowardly exiting due to previous errors!}" \
    "EXT: '$EXT'  ${SUFFIX:+SUFFIX: '$SUFFIX'}  EX: '$EX'" \
    "COMPRESSIONS_USED: '$COMPRESSIONS_USED'  ${ARCHIVE:+ARCHIVE: '$ARCHIVE'}" \
    "FILE: '$FILE'" "R: '$R'" "EXTRACT_PD: '$EXTRACT_PD'" \
    "EXTRACT_DIR: '$EXTRACT_DIR'" "DIR: '$DIR'" \
    >/dev/stderr

  test -d "$EXTRACT_DIR" &&rm -r "$EXTRACT_DIR"
  exit $2
}

function log (){
  test -e "$LOG" ||>"$LOG"
  printf '%-13s%-13s%s    |%s\n' "$1" "$2" "$3" "$4" >>"$LOG"
}

function getstats (){
    local STATS_FILE="$1"
    test ! -e "$STATS_FILE" &&err "couldn't get stats file${STATS_FILE:+ \'$STATS_FILE\'}"

    SUM=$(datamash sum 1 sum 2 -W --output-delimiter=',' <"$STATS_FILE")
    printf '\n-------------------------------------------------------\n%s\n-------------------------------------------------------\n'\
	"[1;30m${FILES_COMPRESSED} file(s) (${SUM%,*} bytes) compressed to ${SUM#*,} bytes[0m"
}

function compress (){
  local DIR="$2"
  local ARCHIVE="${1%$EXT}"
  local SUFFIX='.7z'
  I=0
  until test ! -e "${ARCHIVE}$SUFFIX" ;do
    I=$(($I + 1))
    SUFFIX="[$I].7z"
  done


  7z a -m0=lzma2 -mx9 "${ARCHIVE}$SUFFIX" "$DIR/*" ||err "7z compression failed '$1'" "$?"
  STORE_NSZ="$(stat -c '%s' "${ARCHIVE}$SUFFIX")"
  #echo ----------------CMD: rm "$FILE"
  rm "$FILE" ||err "couldn't remove input file: '$FILE'" "$?"

  if test "$SUFFIX" != '.7z'; then
    if test -n "$(diff -s "${ARCHIVE}$SUFFIX" "$ARCHIVE.7z")"; then
      rm "${ARCHIVE}$SUFFIX" ||err "couldn't remove ARCHIVE: '${ARCHIVE}$SUFFIX'" "$?"
      STORE_NSZ=0
    fi
  fi

  log "$STORE_OSZ" "$STORE_NSZ" "${ARCHIVE}$SUFFIX" "$COMPRESSIONS_USED"
}


function uncompress (){

  local DIR="$1"
  if test -d "$DIR"; then

    STORE_FILE='/data/data/com.termux/files/home/.011/011/archives/optimize_storage_by_compresing_zip_to_tar.gz_.bash.store'
    local EXTRACT_DIR="$(mktemp -qd --suffix=".osbczatt7b-extract")" ||err "could not create temporary extraction directory" $?

    oIFS=$IFS
    IFS='
'
    for FILE in $(find -L "$DIR" -type f -iregex '.+\.\(zip\|tar\|\(tar\.\)?\(gz\|xz\|bz2?\)\)$' -exec printf '%s\n' {} \+ 2>/dev/null); do
echo $FILE;echo;continue
      local EX=false
      local STORE_OSZ="$(stat -c '%s' "$FILE")"
      local STORE_NSZ=
      local EXT="$(echo $FILE |grep -io '\.\(zip\|tar\|\(tar\.\)\?\(gz\|xz\|bz2\?\)\)$')"
      COMPRESSIONS_USED="$EXT${R:+ > $COMPRESSIONS_USED}"

      case "${FILE,?}" in
	*.zip )
	  EX=(unzip "$FILE" -d) ;;
	  * )
	    # .bz, .xz, .gz, .tar.xz, etc...
	    EX=(tar -x --file="$FILE" -C) ;;
	  esac

	  "${EX[@]}" "$EXTRACT_DIR" ||err "${EX%% *}: extraction failed '$FILE'"
	  EXTRACT_PD="$EXTRACT_DIR"

# archive might have been compressed with full path eg.
# /path/to/archive.tar extaracts to /path/to/archive
while read -r LINE; do
  if test "${EXTRACT_PD#$EXTRACT_DIR${LINE%/*}}" == "$EXTRACT_PD" -a -d "$EXTRACT_DIR${LINE%/*}" ;then
    EXTRACT_PD="$EXTRACT_DIR${LINE%/*}"
  fi
done < "$STORE_FILE"

# if file had been compressed recursively or multiple times
# decompress it until further no more
test $(ls -a "$EXTRACT_PD" |wc -l) -eq 3 &&
  if test -n "$(echo $EXTRACT_PD/* |grep -io '\.\(zip\|tar\|\(tar\.\)\?\(gz\|xz\|bz2\?\)\)$')"; then
    R="${R:-$FILE}" uncompress "$EXTRACT_PD"
    #echo ..............AFTER UNCOMPRESS: rm -r "$EXTRACT_DIR"
    if test -n "$R"; then
      rm -r $EXTRACT_DIR ||err "couldn't remove EXTRACT_DIR: '$EXTRACT_DIR'" "$?"
    fi
  fi

  if test -z "$R"; then
    compress "$FILE" "$EXTRACT_PD"
    #printf '\n...........AFTER COMPRESSING[0]: rm -r %s\n' $EXTRACT_DIR/* &&
    rm -r $EXTRACT_DIR/* ||err "couldn't remove file in EXTRACT_DIR/*: '$EXTRACT_DIR'" "$?"
    #printf '\n...........AFTER COMPRESSING[1]: rm -r %s\n' "$EXTRACT_PD" &&
    if test "$EXTRACT_PD" != "$EXTRACT_DIR"; then
      rm -r $EXTRACT_PD ||err "couldn't remove EXTRACT_PD: '$EXTRACT_PD'" "$?"
    fi
    FILES_COMPRESSED=$((${FILES_COMPRESSED:-0} + 1))
  else
    FILE="$R"
    return
  fi

done # EOF: for FILE in
IFS=$oIFS

# recover users' ROM

#echo ................LAST: rm -r "$EXTRACT_DIR"
rm -r "$EXTRACT_DIR" ||err "couldn't remove EXTRACT_DIR: '$EXTRACT_DIR'" "$?"
  fi
}


LOG="$(dirname "$0")/osbczatgt7b-extract.store"

uncompress "$1"

getstats "$LOG"
