#!/usr/bin/env tclsh

source "driver.tcl"
source "url.tcl"
driver::read_descr

proc linkout_to_url {article_id type ikey_1 ckey_1 ikey_2 ckey_2} {
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

set types {
ACLANT
ACM
AGU
AIP
APS
AIPP
AZ-UK
AZ-US
AZ-CA
AZ-DE
AZ-FR
AZ-JP
ISBN
IMGS
IMGM
IMGL
AMETS
ANNREV
ANTH
ARXIV
BIOONE
BWELL
BMJJ
CASES
JMEDC
CELL
NAID
CITES
CITESX
IACR
CSDL
CUP
DAUM
DBLP
DEGRUY
DOI
EdIT
EGU
ERIC
FSTMON
HWIRE
HIWIRE
IEEE
RFC
IDRAFT
IJOC
IHC
IBIKE
IOP
IOPDOI
IOS
IUCR
IWAP
JAVMA
JCI
JMLR
JOVE
JSAP
JSTAGE
JSS
JSTR2
LNGV
MALIE
MSCI
MDPI
MPRESS
MITPR
NASA
NATUR
NATPRE
NBER
NEJM
OPNREP
OSA
PCRJ
PENSFT
PION
MUSE
PROLA
PSYCO
PMID
UKPMC
RSC
ROYSOC
SD
EVPII
SCOPUS
SLINK
SPROT
SSRN
TANDF
UCHIC
USENX
UTCSAI
WILEY
WCAT
WBASE
}

foreach linkout $linkouts {
    if { [string length $linkout] == 0 } {
        continue
    }
    set l [split $linkout "|"]
    lassign $l article_id type ikey_1 ckey_1 ikey_2 ckey_2
    set type [string trim $type]
    if { [lsearch $types $type] == -1 } {
        continue
    }
    puts [linkout_to_url $article_id $type $ikey_1 $ckey_1 $ikey_2 $ckey_2]
}

