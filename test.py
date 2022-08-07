def extract_txt_metadata(txt, search_doi=True, search_fulltext=False, max_query_words=200, scholar=False):
    """extract metadata from text, by parsing and doi-query, or by fulltext query in google scholar
    """
    assert search_doi or search_fulltext, 'no search criteria specified for metadata'

    bibtex = None

    if search_doi:
        try:
            logger.debug('parse doi')
            doi = parse_doi(txt)
            logger.info('found doi:'+doi)
            logger.debug('query bibtex by doi')
            bibtex = fetch_bibtex_by_doi(doi)
            logger.debug('doi query successful')

        except DOIParsingError as error:
            logger.debug(u'doi parsing error: '+str(error))

        except DOIRequestError as error:
            return '''@misc{{{doi},
             doi = {{{doi}}},
             url = {{http://dx.doi.org/{doi}}},
            }}'''.format(doi=doi)

        except ValueError as error:
            raise
            # logger.debug(u'failed to obtained bibtex by doi search: '+str(error))

    if search_fulltext and not bibtex:
        logger.debug('query bibtex by fulltext')
        query_txt = query_text(txt, max_query_words)
        if scholar:
            bibtex = fetch_bibtex_by_fulltext_scholar(query_txt)
        else:
            bibtex = fetch_bibtex_by_fulltext_crossref(query_txt)
        logger.debug('fulltext query successful')

    if not bibtex:
        raise ValueError('failed to extract metadata')

    return bibtex 