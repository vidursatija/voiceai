#!/bin/bash

program_name="mpris-ctrl"
version=0.0.1
versionDate="2014-10-20"
mp_object="/org/mpris/MediaPlayer2"
executable="$0"


function show-help {
echo "$0 - Control MPRIS Players

USAGE:
$0 [OPTIONS]
$0 PLAYER COMMAND [ARGUMENTS]

OPTIONS:
-h, --help              Show help
-v, --version           Print version information
-l, --list              Lists available NAME targets

COMMANDS (ROOT):
raise                   Raises player window
quit                    Quits player

COMMANDS (PLAYER):
play                    Issues play command
pause                   Issues pause command
stop                    Issues stop command
play-pause              Toggles between playing and pausing
next                    Plays next item in playlist
prev[ious]              Plays previous item in playlist
status                  Displays the status of the player
volume                  Get volume level.
volume [LEVEL]          Set volume level.
                        LEVEL should be in range [0.0, 1.0]

COMMANDS (PLAYLIST):
tracks                  Displays tracks
add-track PATH [PLAY]   Appends file PATH to playlist.
                        PLAY should be one of {true, false(default)}
                        If true: append and skip to this item in the 
playlist.
                        If false, append the item to the playlist.


PLAYER:
Typically this should be the player to control, e.g. 'spotify', 'vlc'.
If this exists as a MPRIS DBus destination of 
org.mpris.MediaPlayer2.[PLAYER],
then everything should work fine.

When using VLC, PLAYER=vlc is valid if you start VLC with 'vlc --control 
dbus'
If not, you have to specify the process ID, and set 
PLAYER=vlc.instance[PID].
For instance, pausing the VLC window with process ID 3300:
  $0 -p vlc.instance3300 pause

To see which PLAYER values are valid, use
  $0 --list


Notes:
This utility relies entirely on the PLAYER implementation of the MPRIS 
DBus
interface. Some commands might not work properly, e.g. spotify ignores 
the
'play' command, does not support org.mpris.MediaPlayer2.PlayList, and 
volume
level is always returned as 0 when queried.

Future improvements:
 - Work around individual player's incomplete support of MPRIS.
   E.g. if PLAYER=spotify COMMAND=play then:
           if PlaybackStatus is 'Pause', issue a PlayPause instead


Mainted at: https://gist.github.com/swarminglogic/??
Author:     Roald Fernandez (github@swarminglogic.com)
Version:    $version ($versionDate)
License:    CC-zero (public domain)
"
    exit $1
}


function list-valid-player-targets {
    echo "$(dbus-send --session --dest=org.freedesktop.DBus \
        --type=method_call --print-reply /org/freedesktop/DBus \
        org.freedesktop.DBus.ListNames | grep org.mpris.MediaPlayer2 |
        awk -F\" '{print $2}' | cut -d '.' -f4- | sort )"
}

# $1 the player name to verify.
function is-valid-player {
    if list-valid-player-targets | grep -qP '^'$1'$' ; then
        return 0
    else
        return 1
    fi
}


function parse-parameters {
    while test $# -gt 0; do
        case "$1" in
            -h|--help)
                showHelp 0 ;;
            -v|--version)
                echo "$program_name $version" ; exit 0 ;;
            -l|--list)
                list-valid-player-targets ; exit 0 ;;
            *)
                player=$1 ; shift
                command=$1 ; shift ;
                leftovers="$@" ; break ;;
        esac
    done
}

# $1 interface_path
# $2 function_name
# $3..# parameters
function dbus-any-command {
    local interface_path=$1
    local function_name=$2
    shift 2
    local parameters="$@"
    dbus-send --print-reply --session \
        --dest=org.mpris.MediaPlayer2.${player} \
        $mp_object ${interface_path}.${function_name} ${parameters}
}

# For dbus-{root,player,tracklist}-command
# $1:function_name
# $2..#:parameters
function dbus-root-command {
    dbus-any-command "org.mpris.MediaPlayer2" "${1}" "${@:2}"
}
function dbus-player-command {
    dbus-any-command "org.mpris.MediaPlayer2.Player" "${1}" "${@:2}"
}
function dbus-tracklist-command {
    dbus-any-command "org.mpris.MediaPlayer2.TrackList" "${1}" "${@:2}"
}


# $1:interface_path
# $2:property_name
function dbus-get-any-property {
    dbus-send --print-reply --session \
        --dest=org.mpris.MediaPlayer2.${player} \
        $mp_object org.freedesktop.DBus.Properties.Get \
        string:"$1" string:"$2"
}

# For dbus-get-{root,player,tracklist}-property
# $1:property_name
function dbus-get-root-property {
    dbus-get-any-property "org.mpris.MediaPlayer2" "${1}"
}
function dbus-get-player-property {
    dbus-get-any-property "org.mpris.MediaPlayer2.Player" "${1}"
}
function dbus-get-tracklist-property {
    dbus-get-any-property "org.mpris.MediaPlayer2.TrackList" "${1}"
}


# $1:interface_path
# $2:property_name
# $3..#:parameters
function dbus-set-any-property {
    local interface_path=$1
    local property_name=$2
    shift 2
    local parameters="$@"
    dbus-send --print-reply --session \
        --dest=org.mpris.MediaPlayer2.${player} \
        $mp_object org.freedesktop.DBus.Properties.Set \
        string:"$interface_path" string:"$property_name" "$parameters"
}

# For dbus-set-{root,player,tracklist}-property
# $1:property_name
# $2..#:parameters
function dbus-set-root-property {
    dbus-set-any-property "org.mpris.MediaPlayer2" "${1}" "${@:2}"
}
function dbus-set-player-property {
    dbus-set-any-property "org.mpris.MediaPlayer2.Player" "${1}" "${@:2}"
}
function dbus-set-tracklist-property {
    dbus-set-any-property "org.mpris.MediaPlayer2.TrackList" "${1}" "${@:2}"
}


function execute-command {
    case $1 in
        raise)
            dbus-root-command Raise       > /dev/null ;;
        quit)
            dbus-root-command Quit        > /dev/null ;;
        play)
            dbus-player-command Play      > /dev/null ;;
        pause)
            dbus-player-command Pause     > /dev/null ;;
        stop)
            dbus-player-command Stop      > /dev/null ;;
        play-pause)
            dbus-player-command PlayPause > /dev/null ;;
        next)
            dbus-player-command Next      > /dev/null ;;
        prev|previous)
            dbus-player-command Previous  > /dev/null ;;
        volume)
            set -- $@
            if [ $# -eq 2 ] ; then
                dbus-set-player-property Volume variant:double:$2 
>/dev/null
            else
                dbus-get-player-property Volume | grep double | awk '{print $3}'
            fi
            ;;
        status)
            status=$(dbus-get-player-property PlaybackStatus)
            <<<"$status" grep string | awk -F\" '{print $2}'
            ;;
        tracks)
            tracks=$(dbus-get-tracklist-property Tracks)
            <<<"$tracks" grep object | awk -F\" '{print $2}'
            ;;
        add-track)
            set -- $@
            play=false
            [ $# -ge 2 ] && file="$2"
            [ $# -eq 3 ] && play="$3"
            absolute_file=$(dirname $(readlink -e "$file"))/$(basename 
"$file")
            lastTrack=$($executable $player tracks | tail -n 1)
            [ -z "$lastTrack" ] && 
lastTrack="/org/mpris/MediaPlayer2/TrackList/NoTrack"
            if [ -f "$absolute_file" ] ; then
                dbus-tracklist-command AddTrack 
string:"file://${absolute_file}" \
                    objpath:$lastTrack \
                    boolean:$play > /dev/null
            fi
            ;;
        *)
            echo "'$1' is not a valid command"
            exit 1
            ;;
    esac
}


# Parse parameters, or exit with help if none
if [ $# -gt 0 ] ; then parse-parameters "$@" ; else
    echo "Error: Missing parameters" >&2
    show-help 1
fi


# Validate the specified player
if ! is-valid-player "$player" ; then
    echo "PLAYER '$player' is not a valid MPRIS target."
    echo "List of valid MPRIS targets: "
    list-valid-player-targets
    exit 1
fi

execute-command "$command" "$leftovers"
