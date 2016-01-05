#!/usr/bin/env tclsh

source "driver.tcl"
source "url.tcl"
driver::read_descr

proc linkout_to_url {linkout} {
    set l [split $linkout "|"]
    lassign $l article_id type ikey_1 ckey_1 ikey_2 ckey_2
    set type [string trim $type]
    lassign [driver::format_linkout_$type $type [string trim $ikey_1] [string trim $ckey_1] [string trim $ikey_2] [string trim $ckey_2]] descr link
    return [list $article_id $link]
}

#set linkout "43|HWIRE |295|www.sciencemag.org|5560|1664"
#puts [linkout_to_url $linkout]
#exit

set fname [lindex $argv 0]
set fd [open $fname]
set linkouts [split [read $fd] "\n"]
close $fd;

foreach linkout $linkouts {
    if { [string length $linkout] == 0 } {
        break
    }
    puts [linkout_to_url $linkout]
}

