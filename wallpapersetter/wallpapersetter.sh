#!/usr/bin/env bash
# Wallpaper setter

readonly progn=wpsetter
readonly optsfile="${XDG_CONFIG_HOME:-$HOME/.config}"/dmenu/dmenucolors
read -r font < "${XDG_CONFIG_HOME:-$HOME/.config}"/dmenu/font

readonly IMGSIZE=500
readonly IMGDIR="$HOME/Pictures/wallpapers"
readonly THMBDIR="${XDG_CACHE_HOME:-$HOME/.cache}"/wpsetter
readonly lines=25

puts() {
    printf -- "$1\n" "${@:2}"
}

err() { # strings -> stderr
	local msg

	puts "$progn: $1" "${@:2}" >&2
}

create_menu() {

    local key
    shopt -s nullglob
    for key in *; do
        [[ -e $key ]] || continue
        if [[ ! -e $THMBDIR/$key ]]; then
            convert -thumbnail $IMGSIZE "$key" "$THMBDIR/$key"
        fi

        puts 'IMG:%s\t%s' "$THMBDIR/$key" "$key"
    done
}

get_selection() {
    opts+=( -p "Select Wallpaper" )
    create_menu | dmenu "${opts[@]}" -l $lines
}

get_options() {
    if [[ -e "$optsfile" ]]; then
        # Parse optsfile
        if [[ ! "$font" ]]; then
            err "No font found in ${XDG_CONFIG_HOME:-$HOME/.config}/dmenu/font"
        fi
        source "${XDG_CONFIG_HOME:-$HOME/.config}"/dmenu/dmenucolors
    else
        err "No configuration found for dmenu in ${XDG_CONFIG_HOME:-$HOME/.config}/dmenu/dmenucolors"
    fi
}

mkdir -p $THMBDIR
cd $IMGDIR
get_options
declare -A menu image
results="$(get_selection)" || exit 0
setbg $results
