# --------------------------------------------------
# Copyright The IETF Trust 2011, All Rights Reserved
# --------------------------------------------------

import copy
import codecs
import string
import datetime
import lxml
import xml2rfc.log
import xml2rfc.utils


class _RfcItem:
    """ A unique ID object for an anchored RFC element.
    
        Anchored elements are the following: Automatic sections, user (middle)
        sections, paragraphs, references, appendices, figures, and tables.
        
        RfcItems are collected into an index list in the base writer
    """
    def __init__(self, autoName, autoAnchor, counter='', title='', anchor='',
                 toc=True, level=1):
        self.counter = str(counter)
        self.autoName = autoName
        self.autoAnchor = autoAnchor
        self.title = title
        self.anchor = anchor
        self.toc = toc
        self.level = level
        self.page = 0    # This will be set after buffers are complete!


class _IrefItem:
    """ A unique ID object for an iref element """
    def __init__(self, anchor=None):
        self.pages = []
        self.subitems = {}
        self.anchor = anchor


class RfcWriterError(Exception):
    """ Exception class for errors during document writing """
    def __init__(self, msg):
        self.msg = msg


class BaseRfcWriter:
    """ Base class for all writers

        All public methods need to be overridden for a writer implementation.
    """

    # -------------------------------------------------------------------------
    # Attribute default values
    #
    # These will mainly come into play if DTD validation was disabled, and
    # processing that happens to rely on DTD populated attributes require a lookup
    defaults = {
        'section_toc':              'default',
        'xref_pageno':              'false',
        'xref_format':              'default',
        'iref_primary':             'false',
        'spanx_style':              'emph',
        'figure_suppress-title':    'false',
        'figure_title':             '',
        'figure_align':             'left',
        'vspace_blanklines':        0,
        'table_suppress-title':     'false',
        'table_title':              '',
        'table_align':              'center',
        'table_style':              'full',
        'ttcol_align':              'left',
        'references_title':         'References',
        'ipr':                      'trust200902',
        'submissionType':           'IETF',
        'consensus':                'no',
    }

    # -------------------------------------------------------------------------
    # Boilerplate text
    boilerplate = {}

    # Document stream names
    boilerplate['document_stream'] = {}
    boilerplate['document_stream']['IETF'] = \
        'Internet Engineering Task Force (IETF)'
    boilerplate['document_stream']['IAB'] = \
        'Internet Architecture Board (IAB)'
    boilerplate['document_stream']['IRTF'] = \
        'Internet Research Task Force (IRTF)'
    boilerplate['document_stream']['independent'] = \
        'Independent Submission'

    # Draft workgroup name
    boilerplate['draft_workgroup'] = 'Network Working Group'

    # Category names
    boilerplate['std'] = 'Standards Track'
    boilerplate['bcp'] = 'Best Current Practice'
    boilerplate['exp'] = 'Experimental Protocol'
    boilerplate['info'] = 'Informational'
    boilerplate['historic'] = 'Historic'

    # Series type
    boilerplate['series_name'] = {}
    boilerplate['series_name']['std'] = 'STD'
    boilerplate['series_name']['bcp'] = 'BCP'
    boilerplate['series_name']['info'] = 'FYI'

    # ISSN
    boilerplate['issn'] = '2070-1721'

    # 'Status of this Memo' boilerplate for RFCs
    boilerplate['status'] = {
        'std': {},
        'bcp': {},
        'exp': {},
        'info': {},
        'historic': {},
    }

    # Paragraph 1
    boilerplate['status']['std']['p1'] = \
        'This is an Internet Standards Track document.'
    boilerplate['status']['bcp']['p1'] = \
        'This memo documents an Internet Best Current Practice.'
    boilerplate['status']['exp']['p1'] = \
        'This document is not an Internet Standards Track specification; ' \
        'it is published for examination, experimental implementation, and ' \
        'evaluation.'
    boilerplate['status']['info']['p1'] = \
        'This document is not an Internet Standards Track specification; ' \
        'it is published for informational purposes.'
    boilerplate['status']['historic']['p1'] = \
        'This document is not an Internet Standards Track specification; ' \
        'it is published for the historical record.'

    # Paragraph 2 header
    boilerplate['status']['exp']['p2'] = \
        'This document defines an Experimental Protocol for the Internet ' \
        'community.'
    boilerplate['status']['historic']['p2'] = \
        'This document defines a Historic Document for the Internet ' \
        'community.'

    # Paragraph 2 body
    boilerplate['status']['IETF'] = \
        'This document is a product of the Internet Engineering Task Force ' \
        '(IETF).  It has been approved for publication by the Internet ' \
        'Engineering Steering Group (IESG).'
    boilerplate['status']['IETF_consensus'] = \
        'This document is a product of the Internet Engineering Task Force ' \
        '(IETF).  It represents the consensus of the IETF community.  It has ' \
        'received public review and has been approved for publication by ' \
        'the Internet Engineering Steering Group (IESG).'
    boilerplate['status']['IRTF'] = \
        'This document is a product of the Internet Research Task Force ' \
        '(IRTF).  The IRTF publishes the results of Internet-related ' \
        'research and development activities.  These results might not be ' \
        'suitable for deployment.'
    boilerplate['status']['IRTF_workgroup'] = \
        'This RFC represents the individual opinion(s) ' \
        'of one or more members of the %s Research Group of the Internet ' \
        'Research Task Force (IRTF).'
    boilerplate['status']['IRTF_workgroup_consensus'] = \
        'This RFC represents the consensus of the ' \
        '%s Research Group of the Internet Research Task Force (IRTF).'
    boilerplate['status']['IAB'] = \
        'This document is a product of the Internet Architecture Board ' \
        '(IAB) and represents information that the IAB has deemed valuable ' \
        'to provide for permanent record.'
    boilerplate['status']['independent'] = \
        'This is a contribution to the RFC Series, independently of any ' \
        'other RFC stream.  The RFC Editor has chosen to publish this ' \
        'document at its discretion and makes no statement about its value ' \
        'for implementation or deployment.'

    # Paragraph 2 last sentence
    boilerplate['status']['p2end_ietf_std'] = \
        'Further information on Internet Standards is available ' \
        'in Section 2 of RFC 5741.'
    boilerplate['status']['p2end_ietf_bcp'] = \
        'Further information on BCPs is available in Section 2 of RFC 5741.'
    boilerplate['status']['p2end_ietf_other'] = \
        'Not all documents approved by the IESG are a candidate for any ' \
        'level of Internet Standard; see Section 2 of RFC 5741.'
    boilerplate['status']['p2end_other'] = \
        'Documents approved for publication by the %s are not a ' \
        'candidate for any level of Internet Standard; see Section 2 of RFC ' \
        '5741.'

    # Paragraph 3
    boilerplate['status']['p3'] = \
        'Information about the current status of this document, any errata, ' \
        'and how to provide feedback on it may be obtained at ' \
        'http://www.rfc-editor.org/info/rfc%s.'

    # 'Status of this Memo' boilerplate for drafts
    boilerplate['status']['draft'] = \
       ['Internet-Drafts are working documents of the Internet Engineering ' \
       'Task Force (IETF).  Note that other groups may also distribute ' \
       'working documents as Internet-Drafts.  The list of current Internet- ' \
       'Drafts is at http://datatracker.ietf.org/drafts/current/.',

       'Internet-Drafts are draft documents valid for a maximum of six months ' \
       'and may be updated, replaced, or obsoleted by other documents at any ' \
       'time.  It is inappropriate to use Internet-Drafts as reference ' \
       'material or to cite them other than as "work in progress."']
    boilerplate['draft_expire'] = \
       'This Internet-Draft will expire on %s.'

    # IPR status boilerplate
    boilerplate['ipr_200902_status'] = \
        'This Internet-Draft is submitted in full conformance ' \
        'with the provisions of BCP 78 and BCP 79.'
    boilerplate['ipr_200811_status'] = \
        'This Internet-Draft is submitted to IETF in full conformance ' \
        'with the provisions of BCP 78 and BCP 79.'
    
    # Copyright boilerplate
    boilerplate['base_copyright_header'] = \
        'Copyright (c) %s IETF Trust and the persons identified as the ' \
        'document authors.  All rights reserved.'
    boilerplate['base_copyright_body'] = \
        'This document is subject to BCP 78 and the IETF Trust\'s Legal ' \
        'Provisions Relating to IETF Documents ' \
        '(http://trustee.ietf.org/license-info) in effect on the date of ' \
        'publication of this document.  Please review these documents ' \
        'carefully, as they describe your rights and restrictions with respect ' \
        'to this document.'

    # IPR values which append things to copyright
    boilerplate['ipr_200902_copyright_ietfbody'] = \
        'Code Components extracted from this document must ' \
        'include Simplified BSD License text as described in Section 4.e of ' \
        'the Trust Legal Provisions and are provided without warranty as ' \
        'described in the Simplified BSD License.'
    boilerplate['ipr_noModification_copyright'] = \
        'This document may not be modified, and derivative works of it may ' \
        'not be created, except to format it for publication as an RFC or ' \
        'to translate it into languages other than English.'
    boilerplate['ipr_noDerivatives_copyright'] = \
        'This document may not be modified, and derivative works of it may ' \
        'not be created, and it may not be published except as an ' \
        'Internet-Draft.'
    boilerplate['ipr_pre5378Trust200902_copyright'] = \
        'This document may contain material from IETF Documents or IETF ' \
        'Contributions published or made publicly available before ' \
        'November 10, 2008.  The person(s) controlling the copyright in some ' \
        'of this material may not have granted the IETF Trust the right to ' \
        'allow modifications of such material outside the IETF Standards ' \
        'Process. Without obtaining an adequate license from the person(s) ' \
        'controlling the copyright in such materials, this document may not ' \
        'be modified outside the IETF Standards Process, and derivative ' \
        'works of it may not be created outside the IETF Standards Process, ' \
        'except to format it for publication as an RFC or to translate it ' \
        'into languages other than English.'

    # Any extra boilerplate
    boilerplate['iprnotified'] = \
        'The IETF has been notified of intellectual property rights ' \
        'claimed in regard to some or all of the specification contained ' \
        'in this document.  For more information consult the online list ' \
        'of claimed rights.'
    
    # Stream approvers
    approvers = {
        'IAB': 'IAB',
        'IRTF': 'IRSG',
        'independent': 'RFC Editor',
    }

    # Valid IPR attributes
    supported_ipr = [
        'trust200902',
        'noModificationTrust200902',
        'noDerivativesTrust200902',
        'pre5378Trust200902',
        'trust200811',
        'noModificationTrust200811',
        'noDerivativesTrust200811',
    ]

    # -------------------------------------------------------------------------

    def __init__(self, xmlrfc, quiet=False, verbose=False):
        self.quiet = quiet
        self.verbose = verbose
        self.expire_string = ''
        self.ascii = False

        # We will refer to the XmlRfc document root as 'r'
        self.xmlrfc = xmlrfc
        self.r = xmlrfc.getroot()
        self.pis = xmlrfc.getpis()

        # Document counters
        self.ref_start = 1
        self.figure_count = 0
        self.table_count = 0

        # Set RFC number and draft flag
        self.rfcnumber = self.r.attrib.get('number', '')
        self.draft = bool(not self.rfcnumber)
        
        # Used for two-pass indexing
        self.indexmode = False

        # Item Indicies
        self._index = []
        self._iref_index = {}
        
    def _make_iref(self, item, subitem=None, anchor=None):
        """ Create an iref ID object if it doesnt exist yet """
        last = None
        if item not in self._iref_index:
            self._iref_index[item] = _IrefItem()
            last = self._iref_index[item]
        if subitem and subitem not in self._iref_index[item].subitems:
            self._iref_index[item].subitems[subitem] = _IrefItem()
            last = self._iref_index[item].subitems[subitem]
        if last and anchor:
            last.anchor = anchor

    def _indexParagraph(self, counter, p_counter, anchor=None, toc=False):
        counter = str(counter)  # This is the section counter
        p_counter = str(p_counter)  # This is the paragraph counter
        autoName = 'Section ' + counter + ', Paragraph ' + p_counter
        autoAnchor = 'rfc.section.' + counter + '.p.' + p_counter
        item = _RfcItem(autoName, autoAnchor, anchor=anchor, toc=toc)
        self._index.append(item)
        return item

    def _indexSection(self, counter, title=None, anchor=None, toc=True, \
                      level=1, appendix=False):
        counter = str(counter)
        if appendix:
            autoName = 'Appendix ' + counter
            autoAnchor = 'rfc.appendix.' + counter
        else:
            autoName = 'Section ' + counter
            autoAnchor = 'rfc.section.' + counter
        item = _RfcItem(autoName, autoAnchor, counter=counter, title=title, \
                       anchor=anchor, toc=toc, level=level)
        self._index.append(item)
        return item

    def _indexReferences(self, counter, title=None, anchor=None, toc=True, \
                         subCounter=0, level=1):
        if subCounter < 1:
            autoName = 'References'
            autoAnchor = 'rfc.references'
        else:
            subCounter = str(subCounter)
            autoName = 'References ' + subCounter
            autoAnchor = 'rfc.references.' + subCounter
        item = _RfcItem(autoName, autoAnchor, counter=counter, title=title, \
                       anchor=anchor, toc=toc, level=level)
        self._index.append(item)
        return item
    
    def _indexFigure(self, counter, title=None, anchor=None, toc=False):
        counter = str(counter)
        autoName = 'Figure ' + counter
        autoAnchor = 'rfc.figure.' + counter
        item = _RfcItem(autoName, autoAnchor, title=title, anchor=anchor, \
                       toc=toc)
        self._index.append(item)
        return item
        
    def _indexTable(self, counter, title=None, anchor=None, toc=False):
        counter = str(counter)
        autoName = 'Table ' + counter
        autoAnchor = 'rfc.table.' + counter
        item = _RfcItem(autoName, autoAnchor, title=title, anchor=anchor, \
                       toc=toc)
        self._index.append(item)
        return item

    def _getTocIndex(self):
        return [item for item in self._index if item.toc]
        
    def _getItemByAnchor(self, anchor):
        for item in self._index:
            if item.autoAnchor == anchor or item.anchor == anchor:
                return item
        return None
    
    def _validate_ipr(self):
        """ Ensure the application has boilerplate for the ipr attribute given """
        ipr = self.r.attrib.get('ipr', self.defaults['ipr'])
        if not ipr in self.supported_ipr:
            raise RfcWriterError('No boilerplate text available for '
            'ipr: \'%s\'.  Acceptable values are: ' % ipr + \
            ', '.join(self.supported_ipr))
    
    def _format_date(self):
        """ Fix the date data """
        today = datetime.date.today()
        date = self.r.find('front/date')
        if date is not None:
            year = date.attrib.get('year', '')
            month = date.attrib.get('month', '')
            # If year is this year, and month not specified, use current date
            if not year or (year == str(today.year) and not month) or \
                           (year == str(today.year) and month == str(today.month)):
                # Set everything to today
                date.attrib['year'] = today.strftime('%Y')
                date.attrib['month'] = today.strftime('%B')
                date.attrib['day'] = today.strftime('%d')
        
        # Setup the expiration string for drafts as published date + six months
        if self.draft:
            date = self.r.find('front/date')
            if date is not None:
                month = date.attrib.get('month', '')
                year = date.attrib.get('year', '')
                day = date.attrib.get('day', '1')  # Default to first of month
                if month and year:
                    try:
                        start_date = datetime.datetime.strptime(year + month + day, \
                                                                '%Y%B%d')
                        expire_date = start_date + datetime.timedelta(183)
                        self.expire_string = expire_date.strftime('%B %d, %Y')
                    except ValueError:
                        pass
                elif not year:
                    # Warn about no date
                    xml2rfc.log.warn('No date specified for document.')

    def _prepare_top_left(self):
        """ Returns a lines of lines for the top left header """
        lines = []
        # Document stream / workgroup
        if self.draft:
            workgroup = self.r.find('front/workgroup')
            if workgroup is not None and workgroup.text:
                lines.append(workgroup.text)
            else:
                lines.append(self.boilerplate['draft_workgroup'])
        else:
            # Determine 'workgroup' from submissionType
            subtype = self.r.attrib.get('submissionType', 
                                         self.defaults['submissionType'])
            docstream = self.boilerplate['document_stream'].get(subtype)
            lines.append(docstream)

        # RFC number
        if not self.draft:
            lines.append('Request for Comments: ' + self.rfcnumber)
        else:
            lines.append('Internet-Draft')

        # Series number
        category = self.r.attrib.get('category', '')
        seriesNo = self.r.attrib.get('seriesNo')
        if seriesNo is not None and category in self.boilerplate['series_name']:
            lines.append('%s: %s' % (self.boilerplate['series_name'][category], 
                                     seriesNo))

        # RFC relation notice
        approved_text = self.draft and '(if approved)' or ''
        updates = self.r.attrib.get('updates')
        if updates:
            lines.append('Updates: %s %s' % (updates, approved_text))
        obsoletes = self.r.attrib.get('obsoletes')
        if obsoletes:
            lines.append('Obsoletes: %s %s' % (obsoletes, approved_text))

        # Cateogory
        if category:
            cat_text = self.boilerplate[category]
            if self.draft:
                lines.append('Intended status: ' + cat_text)
            else:
                lines.append('Category: ' + cat_text)
        else:
            xml2rfc.log.warn('No category specified for document.')

        # Expiration notice for drafts
        if self.expire_string:
            lines.append('Expires: ' + self.expire_string)

        # ISSN identifier
        if not self.draft:
            lines.append('ISSN: %s' % self.boilerplate['issn'])

        # Strip any whitespace from XML to make header as neat as possible
        lines = map(string.strip, lines)
        return lines

    def _prepare_top_right(self):
        """ Returns a list of lines for the top right header """
        lines = []
        # Render author?
        authorship = self.pis.get('authorship', 'yes')
        if authorship == 'yes':
            # Keep track of previous organization and remove if redundant.
            last_org = None
            for author in self.r.findall('front/author'):
                role = author.attrib.get('role', '')
                if role == 'editor':
                    role = ', Ed.'
                initials = author.attrib.get('initials', '')
                # Append a dot if it doesnt already exist
                if initials and not initials.endswith('.'):
                    initials = initials + '.'
                lines.append(initials + ' ' + author.attrib.\
                             get('surname', '') + role)
                organization = author.find('organization')
                if organization is not None:
                    abbrev = organization.attrib.get('abbrev')
                    org_result = None
                    if abbrev:
                        org_result = abbrev
                    elif organization.text:
                        org_result = organization.text
                    if org_result:
                        if org_result == last_org:
                            # Remove redundant organization
                            lines.remove(last_org)
                        last_org = org_result
                        lines.append(org_result)

        date = self.r.find('front/date')
        if date is not None:
            year = date.attrib.get('year', '')
            month = date.attrib.get('month', '')
            day = date.attrib.get('day', '')
            if month:
                month = month + ' '
            if day:
                day = day + ', '
            lines.append(month + day + year)
            # Strip any whitespace from XML to make header as neat as possible
            lines = map(string.strip, lines)
        return lines

    def _write_figure(self, figure):
        """ Writes <figure> elements """
        align = figure.attrib.get('align', self.defaults['figure_align'])
        self.figure_count += 1
        anchor = figure.attrib.get('anchor')
        title = figure.attrib.get('title', self.defaults['figure_title'])
    
        if self.indexmode:
            # Add figure to the index, inserting any anchors necessary
            self._indexFigure(self.figure_count, anchor=anchor, title=title)
        else:
            # Insert anchor(s) for the figure
            self.insert_anchor('#rfc.figure.' + str(self.figure_count))
            if (anchor):
                self.insert_anchor('#' + anchor)
    
            # Write preamble
            preamble = figure.find('preamble')
            if preamble is not None:
                self.write_t_rec(preamble, align=align)
    
            # Write figure with optional delimiter
            delimiter = self.pis.get('artworkdelimiter', None)
            artwork = figure.find('artwork')
            # artwork_align = artwork.attrib.get('align', align)
            # Explicitly use figure alignment
            artwork_align = align
            blanklines = int(self.pis.get('artworklines', 0))
            self.write_raw(figure.find('artwork').text, align=artwork_align, \
                           blanklines=blanklines, delimiter=delimiter)
    
            # Write postamble
            postamble = figure.find('postamble')
            if postamble is not None:
                self.write_t_rec(postamble, align=align)
    
            # Write label if PI figurecount = yes
            if self.pis.get('figurecount', 'no') == 'yes':
                title = figure.attrib.get('title', '')
                if title:
                    title = ': ' + title
                self.write_label('Figure ' + str(self.figure_count) + title, \
                                type='figure')

    def _write_table(self, table):
        """ Writes <texttable> elements """
        align = table.attrib.get('align', self.defaults['table_align'])
        self.table_count += 1
        anchor = table.attrib.get('anchor')
        title = table.attrib.get('title', self.defaults['table_title'])
        
        if self.indexmode:
            # Add table to the index, inserting any anchors necessary
            self._indexTable(self.table_count, anchor=anchor, title=title)
        else:
            # Insert anchor(s) for the table
            self.insert_anchor('#rfc.table.' + str(self.table_count))
            if (anchor):
                self.insert_anchor('#' + anchor)
    
            # Write preamble
            preamble = table.find('preamble')
            if preamble is not None:
                self.write_t_rec(preamble, align=align)
    
            # Write table
            self.draw_table(table, table_num=self.table_count)
    
            # Write postamble
            postamble = table.find('postamble')
            if postamble is not None:
                self.write_t_rec(postamble, align=align)
    
            # Write label if PI tablecount = yes
            if self.pis.get('tablecount', 'no') == 'yes':
                title = table.attrib.get('title', '')
                if title:
                    title = ': ' + title
                self.write_label('Table ' + str(self.table_count) + title, \
                                 type='table')
    
    def _index_t_rec(self, element):
        """ Traverse a <t> element only performing indexing operations """
        

    def _write_section_rec(self, section, count_str, appendix=False, \
                           level=0):
        """ Recursively writes <section> elements 
        
            We use the self.indexmode flag to determine whether or not we
            render actual text at this point or just lookup header information
            to construct the index
        """
        if level > 0:
            anchor = section.attrib.get('anchor')
            title = section.attrib.get('title')
            include_toc = section.attrib.get('toc', self.defaults['section_toc']) != 'exclude' \
                          and (not appendix or self.pis.get('tocappendix', \
                                                            'yes') == 'yes')
            if self.indexmode:
                # Add section to the index
                self._indexSection(count_str, title=title, anchor=anchor,
                                   toc=include_toc, level=level,
                                   appendix=appendix)
            else:
                # Write the section heading
                aa_prefix = appendix and 'rfc.appendix.' or 'rfc.section.'
                self.write_heading(title, bullet=count_str + '.',
                                   autoAnchor=aa_prefix + count_str,
                                   anchor=anchor, level=level)
        else:
            # Must be <middle> or <back> element -- no title or index.
            count_str = ''

        p_count = 1  # Paragraph counter
        for element in section:
            # Check for a PI
            if element.tag is lxml.etree.PI:
                self.xmlrfc.parse_pi(element)
            # Write elements in XML document order
            if element.tag == 't':
                anchor = element.attrib.get('anchor')
                if self.indexmode:
                    self._indexParagraph(count_str, p_count, anchor=anchor)
                autoAnchor = 'rfc.section.' + count_str + '.p.' + str(p_count)
                self.write_t_rec(element, autoAnchor=autoAnchor)
                p_count += 1
            elif element.tag == 'figure':
                self._write_figure(element)
            elif element.tag == 'texttable':
                self._write_table(element)

        s_count = 1  # Section counter
        
        # Append a dot to separate sub counters
        if count_str:
            count_str += '.'

        # Recurse on sections
        for child_sec in section.findall('section'):
            if appendix == True and not count_str:
                # Use an alphabetic counter for first-level appendix
                self._write_section_rec(child_sec, 'Appendix ' + \
                                        string.uppercase[s_count - 1] + '',
                                        level=level + 1, appendix=True)
            else:
                # Use a numeric counter
                self._write_section_rec(child_sec, count_str + str(s_count), 
                                        level=level + 1, appendix=appendix)

            s_count += 1

        # Set the ending index number so we know where to begin references
        if count_str == '' and appendix == False:
            self.ref_start = s_count

    def _write_status_section(self):
        """ Writes the 'Status of this Memo' section """

        self.write_heading('Status of this Memo', autoAnchor='rfc.status')
        if not self.draft:  #RFC
            # Status boilerplate is determined by category/submissionType/consensus
            category = self.r.attrib.get('category', 'none')
            stream = self.r.attrib.get('submissionType', 
                                       self.defaults['submissionType'])
            consensus = self.r.attrib.get('consensus',
                                          self.defaults['consensus'])
            workgroup = ''
            wg_element = self.r.find('front/workgroup')
            if wg_element is not None and wg_element.text:
                workgroup = wg_element.text

            # Write first paragraph
            if category in self.boilerplate['status']:
                self.write_paragraph(self.boilerplate['status'][category]\
                                     .get('p1', ''))
            
            # Build second paragraph
            p2 = []
            if category in self.boilerplate['status']:
                p2.append(self.boilerplate['status'][category].get('p2', ''))
            if stream == 'IETF':
                if consensus == 'yes':
                    p2.append(self.boilerplate['status']['IETF_consensus'])
                else:
                    p2.append(self.boilerplate['status']['IETF'])
            elif stream == 'IRTF':
                p2.append(self.boilerplate['status']['IRTF'])
                if workgroup:
                    if consensus == 'yes':
                        p2.append(self.boilerplate['status']['IRTF_workgroup_consensus'] \
                                  % workgroup)
                    else:
                        p2.append(self.boilerplate['status']['IRTF_workgroup'] \
                                  % workgroup)
            else:
                p2.append(self.boilerplate['status'].get(stream, ''))

            # Last sentence of p2
            if stream == 'IETF' and category == 'std':
                p2.append(self.boilerplate['status']['p2end_ietf_std'])
            elif stream == 'IETF' and category == 'bcp':
                p2.append(self.boilerplate['status']['p2end_ietf_bcp'])
            elif stream == 'IETF':
                p2.append(self.boilerplate['status']['p2end_ietf_other'])
            else:
                p2.append(self.boilerplate['status']['p2end_other'] \
                          % self.approvers.get(stream, ''))

            # Write second paragraph
            self.write_paragraph('  '.join(p2))
            
            # Write third paragraph
            self.write_paragraph(self.boilerplate['status']['p3'] % self.rfcnumber)

        else:  # Draft
            # Start by checking for an ipr header
            ipr = self.r.attrib.get('ipr', self.defaults['ipr'])
            if '200902' in ipr:
                self.write_paragraph(self.boilerplate['ipr_200902_status'])
            elif '200811' in ipr:
                self.write_paragraph(self.boilerplate['ipr_200811_status'])

            # Write the standard draft status
            for par in self.boilerplate['status']['draft']:
                self.write_paragraph(par)

            # Write expiration string, if it was generated
            if self.expire_string:
                self.write_paragraph( \
                    self.boilerplate['draft_expire'] % self.expire_string)
    
    def _write_copyright(self):
        """ Writes the 'Copyright' section """
        self.write_heading('Copyright Notice', autoAnchor='rfc.copyrightnotice')

        # Write header line with year
        date = self.r.find('front/date')
        year = ''
        if date is not None:
            year = date.attrib.get('year', '')
        self.write_paragraph(self.boilerplate['base_copyright_header'] % year)

        # Write next paragraph which may be modified by ipr
        ipr = self.r.attrib.get('ipr', self.defaults['ipr'])
        body = self.boilerplate['base_copyright_body']
        if '200902' in ipr and self.r.attrib.get('submissionType', 
                                   self.defaults['submissionType']) == 'IETF':
            body += '  ' + self.boilerplate['ipr_200902_copyright_ietfbody']
        self.write_paragraph(body)
        
        # Write any additional paragraphs
        if 'noModification' in ipr:
            self.write_paragraph(self.boilerplate['ipr_noModification_copyright'])
        elif 'noDerivatives' in ipr:
            self.write_paragraph(self.boilerplate['ipr_noDerivatives_copyright'])
        elif ipr == 'pre5378Trust200902':
            self.write_paragraph(self.boilerplate['ipr_pre5378Trust200902_copyright'])

    def _run(self, indexmode=False):
        self.indexmode = indexmode
        # Reset document counters
        self.ref_start = 1
        self.figure_count = 0
        self.table_count = 0

        if not self.indexmode:
            # Format the date properly
            self._format_date()
            
            # Do any pre processing necessary, such as inserting metadata
            self.pre_processing()

            # Block header
            topblock = self.pis.get('topblock', 'yes')
            if topblock == 'yes':
                self.write_top(self._prepare_top_left(), \
                                   self._prepare_top_right())

            # Title & Optional docname
            title = self.r.find('front/title')
            if title is not None:
                docName = self.r.attrib.get('docName', None)
                self.write_title(title.text, docName)

            # Abstract
            abstract = self.r.find('front/abstract')
            if abstract is not None:
                self.write_heading('Abstract', autoAnchor='rfc.abstract')
                for t in abstract.findall('t'):
                    self.write_t_rec(t)

            # Optional notified boilerplate
            if self.pis.get('iprnotified', 'no') == 'yes':
                self.write_paragraph(BaseRfcWriter.boilerplate['iprnotified'])

            # Optional notes
            for note in self.r.findall('front/note'):
                self.write_heading(note.attrib.get('title', 'Note'))
                for t in note.findall('t'):
                    self.write_t_rec(t)
            
            # Verify that 'ipr' attribute is valid before continuing
            self._validate_ipr()
            
            # "Status of this Memo" section
            self._write_status_section()

            # Copyright section
            self._write_copyright()

            # Insert the table of contents marker at this position
            toc_enabled = self.pis.get('toc', 'no')
            if toc_enabled == 'yes':
                self.insert_toc()
        
        # ENDIF indexmode

        # Middle sections
        middle = self.r.find('middle')
        if middle is not None:
            self._write_section_rec(middle, None)

        # References sections
        # Treat references as nested only if there is more than one
        ref_counter = str(self.ref_start)
        references = self.r.findall('back/references')
        # Write root level references header
        ref_title = self.pis.get('refparent', self.defaults['references_title'])
        if self.indexmode:
            self._indexReferences(ref_counter, title=ref_title)
        else:
            self.write_heading(ref_title, bullet=ref_counter + '.', \
                               autoAnchor='rfc.references')
        if len(references) > 1:
            for i, reference_list in enumerate(references):
                ref_newcounter = ref_counter + '.' + str(i + 1)
                ref_title = reference_list.attrib.get('title',
                                        self.defaults['references_title'])
                if self.indexmode:
                    self._indexReferences(ref_newcounter, title=ref_title, \
                                          subCounter=i+1, level=2)
                else:
                    autoAnchor = 'rfc.references.' + str(i + 1)
                    self.write_heading(ref_title, bullet=ref_newcounter + '.',\
                                       autoAnchor=autoAnchor, level=2)
                    self.write_reference_list(reference_list)
        elif len(references) == 1 and not self.indexmode:
            self.write_reference_list(references[0])

        # Appendix sections
        back = self.r.find('back')
        if back is not None:
            self._write_section_rec(back, None, appendix=True)

        # Index section, disable if there are no irefs
        if len(self._iref_index) > 0:
            if self.indexmode:
                # Add explicitly to index
                title = 'Index'
                autoAnchor = 'rfc.index'
                item = _RfcItem(title, autoAnchor, title=title)
                self._index.append(item)
            else:
                self.insert_iref_index()

        # Authors addresses section
        authors = self.r.findall('front/author')
        autoAnchor = 'rfc.authors'
        if len(authors) > 1:
            title = "Authors' Addresses"
        else:
            title = "Author's Address"
        if self.indexmode:
            # Add explicitly to index
            item = _RfcItem(title, autoAnchor, title=title)
            self._index.append(item)
        else:
            self.write_heading(title, autoAnchor=autoAnchor)
            for author in authors:
                self.write_address_card(author)

        # Primary buffer is finished -- apply any post processing
        if not self.indexmode:
            self.post_processing()
        
    def write(self, filename, tmpfile=None):
        """ Public method to write the RFC document to a file. """
        # If the ascii flag is enabled, replace unicode with ascii in the tree
        if self.ascii:
            xml2rfc.utils.safeReplaceUnicode(self.r)

        # Make two passes over the document, the first pass we run in
        # 'index mode' to construct the internal index and other things, 
        # the second pass will assemble a buffer and render the actual text
        self._run(indexmode=True)
        self._run(indexmode=False)

        # Finished processing, write to file
        # Override file with keyword argument if passed in, ignoring filename.
        # Warning -- make sure file is open and ready for writing!
        if not tmpfile:
            if self.ascii:
                file = open(filename, 'w')
            else:
                # Open as unicode
                file = codecs.open(filename, 'w', encoding='utf-8')
            self.write_to_file(file)
            file.close()
        else:
            self.write_to_file(tmpfile)

        if not self.quiet and filename:
            xml2rfc.log.write('Created file', filename)

    # -----------------------------------------
    # Base writer interface methods to override
    # -----------------------------------------

    def insert_toc(self):
        """ Marks the current buffer position to insert ToC at """
        raise NotImplementedError('insert_toc() needs to be overridden')
    
    def insert_iref_index(self):
        """ Marks the current buffer position to insert the index at """
        raise NotImplementedError('insert_iref_index() needs to be ' \
                                  'overridden')

    def write_raw(self, text, indent=3, align='left', blanklines=0, \
                  delimiter=None):
        """ Writes a block of text that preserves all whitespace """
        raise NotImplementedError('write_raw() needs to be overridden')

    def write_label(self, text, type='figure'):
        """ Writes a table or figure label """
        raise NotImplementedError('write_label() needs to be overridden')

    def write_title(self, title, docName=None):
        """ Writes the document title """
        raise NotImplementedError('write_title() needs to be overridden')

    def write_heading(self, text, bullet='', autoAnchor=None, anchor=None, \
                      level=1):
        """ Writes a section heading """
        raise NotImplementedError('write_heading() needs to be overridden')

    def write_paragraph(self, text, align='left', autoAnchor=None):
        """ Writes a paragraph of text """
        raise NotImplementedError('write_paragraph() needs to be'\
                                  ' overridden')

    def write_t_rec(self, t, align='left', autoAnchor=None):
        """ Recursively writes <t> elements """
        raise NotImplementedError('write_t_rec() needs to be overridden')

    def write_top(self, left_header, right_header):
        """ Writes the main document header

            Takes two list arguments, one for each margin, and combines them
            so that they exist on the same lines of text
        """
        raise NotImplementedError('write_top() needs to be overridden')

    def write_address_card(self, author):
        """ Writes the address information for an <author> element """
        raise NotImplementedError('write_address_card() needs to be ' \
                                  'overridden')

    def write_reference_list(self, list):
        """ Writes a <references> element """
        raise NotImplementedError('write_reference_list() needs to be ' \
                                  'overridden')

    def insert_anchor(self, text):
        """ Inserts a document anchor for internal links """
        raise NotImplementedError('insert_anchor() needs to be overridden')

    def draw_table(self, table, table_num=None):
        """ Draws a formatted table from a <texttable> element

            For HTML nothing is really 'drawn' since we can use <table>
        """
        raise NotImplementedError('draw_table() needs to be overridden')

    def pre_processing(self):
        """ First method that is called before traversing the XML RFC tree """
        raise NotImplementedError('pre_processing() needs to be overridden')

    def post_processing(self):
        """ Last method that is called after traversing the XML RFC tree """
        raise NotImplementedError('post_processing() needs to be overridden')

    def write_to_file(self, file):
        """ Writes the finished buffer to a file """
        raise NotImplementedError('write_to_file() needs to be overridden')
