#!/usr/bin/env python

import re, sys, urllib2

# error messages (taken from iop.py)
ERR_STR_PREFIX = 'status\terr\t'
ERR_STR_FETCH = 'Unable to fetch the page: '
ERR_STR_TRY_AGAIN = 'The server may be down.  Please try later.'
ERR_STR_NO_DOI = 'No document object identifier found on the page: '
ERR_STR_NO_BIBTEX = 'No BibTeX entry found for the DOI: '
ERR_STR_NO_URL = 'No URL found in the BibTeX entry for the DOI: '
ERR_STR_REPORT = 'Please report the error to plugins@citeulike.org.'

# read url from std input
url = sys.stdin.readline()

# get rid of the newline at the end
url = url.strip()

# we'll be given a url of the form http://prola.aps.org/abstract/PRA/v18/i3/p787_1
#  http://prola.aps.org/abstract/journal/volume/issue/page
# the ris resource is located at http://prola.aps.org/export/___/v__/i__/p__?type=ris
# use type=bibtex for bibtex 
# should we prefer one to the other?

address = url.split('abstract')[1]

risurl = 'http://prola.aps.org/export' + address + '?type=ris'
try:
	f = urllib2.urlopen(risurl);
except:
	print ERR_STR_PREFIX + ERR_STR_FETCH + risurl + '.  ' + ERR_STR_TRY_AGAIN
	sys.exit(1)
ris = f.read()

#okay so that handles most of it  but we still need to get the actual title of the journal,
# and we need to find the abstract if it has one.
absurl = 'http://prola.aps.org/abstract' + address
try:
	f = urllib2.urlopen(absurl)
except:
	print ERR_STR_PREFIX + ERR_STR_FETCH + absurl + '.  ' + ERR_STR_TRY_AGAIN
	sys.exit(1)
content = f.read()

match = re.search(r"""<div class="aps-abstractbox"><p>(.*)</p></div>""", content, re.DOTALL)
abstract = ''
if match:
	# strip HTML tags (taken from iop.py)
	from sgmllib import SGMLParser
	class XMLJustText (SGMLParser):
		just_text = ''
		def handle_data (self,data):
			self.just_text = self.just_text + ' ' + data

	parser = XMLJustText()
	parser.feed(match.group(1))
	abstract = parser.just_text.replace(',',';').strip()

match2 = re.search(r"""span class="aps-boldfont">DOI:</span>(.*?)<br/>""", content, re.DOTALL)
if not match2:
	print ERR_STR_PREFIX + ERR_STR_NO_DOI + absurl + '.  ' + ERR_STR_REPORT
	sys.exit(1)
doi = match2.group(1).strip()

#We can look at the 3 letter code in the address to get the journal name.
	
journalmap = {'PRA' : 'Physical Review A',
              'PRB' : 'Physical Review B',
              'PRC' : 'Physical Review C',
              'PRD' : 'Physical Review D',
              'PRE' : 'Physical Review E',
              'PRL' : 'Physical Review Letters',
              'PRI' : 'Physical Review (Series I)',
              'PR/'  : 'Physical Review',
              'RMP' : 'Reviews of Modern Physics'
             }
journal = journalmap[address[1:4]]
 
print 'begin_tsv'
print 'journal\t' + journal
if abstract:
	print 'abstract\t' + abstract
print "linkout\tPROLA\t\t%s\t\t" % (address[1:])
print "linkout\tDOI\t\t%s\t\t" % (doi)
print 'doi\t' + doi
print 'end_tsv'
print 'begin_ris'
print ris
print 'end_ris'
print 'status\tok'
	