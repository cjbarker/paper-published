#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********************************************************
# Script validates if paper title was published or not.
#
# Handles rcading input file and checking against
# Google to determine if previously published or not.
# If able to process successfully will print results
# to standard out.
#
# python3 pp.py [<input-file>|<title]>
#
# input-file: XLS or CVS of papers' corresponding titles to search
# title: individual paper title (string) to search on
#
# Example: python3 pp.py "Curing Cancer with Bleach"
#
# If successful exit code is 0
# If fails exit code is > 0
# ********************************************************

import calendar
import csv
import os
import sys
import time
import urllib.parse

import requests
import xlrd
import xlsxwriter as xs
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


def err(msg=None):
    """
    Converts string to bytes & Outputs to stderr
    """
    if not msg:
        return
    msg = msg + "\n"
    os.write(2, msg.encode())


def is_valid_file(fname=None):
    """Validates if file exists"""
    if not fname:
        return False
    fname = fname.strip()
    return os.path.isfile(fname)


def get_page(url=None):
    """HTTP Get request to given URL returns response HTML payload string"""
    result = None
    if not url:
        return result

    # desktop user-agent; expected by google in HTTP header
    headers = {"user-agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers)
    except:  # noqa: E722
        e = sys.exc_info()[0]
        err("Failed connection: " + str(e) + " via URL " + url)
        return result

    # check if valid response
    if resp.status_code != 200:
        err(
            "Failed - unsuccessful response status code: "
            + str(resp.status_code)
            + " via URL "
            + url
        )
        return result

    result = resp.content
    return result


def pubmed_search(paper_title=None):
    """
    Applies a PubMed Central search for a given paper title
    returning list of results key/value of link, title, description
    """
    results = []

    if not paper_title:
        return results

    # extract out top level domain/URL for PMC
    n = 3
    groups = PUBMED_SEARCH_URL.split("/")
    groupings = "/".join(groups[:n]), "/".join(groups[n:])
    pmc_base_url = groupings[0]
    # print(pmc_base_url)

    # encode query string param before search
    params = {"term": paper_title}
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = PUBMED_SEARCH_URL + query
    # print(url)

    response = get_page(url)
    if not response:
        return results

    # parse HTTP response and pull out search results
    soup = BeautifulSoup(response, "html.parser")

    # PMC returns 20 results per page - only pull from first page results
    for r in soup.find_all("div", class_="rslt"):
        title = r.find("div", class_="title")
        anchors = title.find_all("a")
        desc = r.find("div", class_="desc")
        details = r.find("div", class_="details")

        link = pmc_base_url + anchors[0].get("href")
        search_title = title.text
        description = ""
        if desc:
            description = desc.text
        if details:
            description = description + "\n" + details.text

        # Get page results and pull title
        page_title = ""
        page_authors = ""
        response = get_page(link)

        if response:
            # extract title
            page_soup = BeautifulSoup(response, "html.parser")
            soup_title = page_soup.find("h1", class_="content-title")
            if soup_title:
                page_title = soup_title.text

            # extract authors
            metas = page_soup.find_all("meta")
            if metas:
                for meta in metas:
                    if (
                        meta.attrs["content"]
                        and "name" in meta.attrs
                        and meta.attrs["name"] == "citation_authors"
                    ):
                        page_authors = meta.attrs["content"]

        print("Link ", link)
        print("Search Title", search_title)
        print("Page Title " + page_title)
        print("Description", description)
        print("Authors", page_authors, "\n")

        item = {
            "link": link,
            "search_title": search_title,
            "page_title": page_title,
            "description": description,
            "page_authors": page_authors,
        }
        results.append(item)

    return results


def google_search(paper_title=None):
    """
    Applies a google search for a given paper title
    returning list of results key/value of link, title, description
    """
    GOOGLE_SEARCH_URL
    results = []

    if not paper_title:
        return results

    # encode query string param before search
    params = {"q": paper_title}
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = GOOGLE_SEARCH_URL + query
    # print(url)

    response = get_page(url)
    if not response:
        return results

    # parse HTTP response and pull out search results
    soup = BeautifulSoup(response, "html.parser")

    for g in soup.find_all("div", class_="g"):
        anchors = g.find_all("a")
        spans = g.find_all("span", class_="st")
        if anchors and spans:
            link = anchors[0]["href"]
            search_title = g.find("h3").text
            description = spans[0].text
            page_title = ""
            page_authors = ""
            # print("Link ", link)
            # print("Title", title)
            # print("Description", description)
            item = {
                "link": link,
                "search_title": search_title,
                "page_title": page_title,
                "page_authors": page_authors,
                "description": description,
            }
            results.append(item)
    return results


def extract_xlsx(fname=None, search_hdrs=None):
    """
    Reads file contents and returns a list of pairs including
    each manuscript id and corresponding manuscript title.
    """
    results = []

    if fname is None or search_hdrs is None:
        err("Invalid CSV extraction for filename and column headers")
        return results

    # extract corresponding data rows to columns for specific headers
    wb = xlrd.open_workbook(fname)
    ws = wb.sheet_by_index(0)

    # find index headers occur
    headers = []
    for i in range(len(ws.row(0))):
        if ws.row(0)[i].value in search_hdrs:
            item = {"header": ws.row(0)[i].value, "index": i}
            headers.append(item)

    # extract data after first row
    results = []
    for i in range(1, ws.nrows):
        result = {}
        for hdr in headers:
            # print(hdr.get("header"))
            # print(ws.row(i)[hdr.get("index")].value)
            item = {hdr.get("header"): ws.row(i)[hdr.get("index")].value}
            result.update(item)
        results.append(result)

    # print(results)
    return results


def extract_csv(fname=None, search_hdrs=None):
    """
    Reads a CSV file and extracts all rows for column header names requested.
    Returns a list of dictionary with column name and corresponding row value in matrix
    """
    results = []

    if fname is None or search_hdrs is None:
        err("Invalid CSV extraction for filename and column headers")
        return results

    result = {}
    # extract corresponding data rows to columns for specific headers
    with open(fname, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line in reader:
            result = dict((k, line[k]) for k in search_hdrs if k in line)
            # print(result)
            results.append(result)

    return results


# ----------------------------------------------------------------------
# M A I N  L O G I C
# ----------------------------------------------------------------------


def main():
    if len(sys.argv) < 2:
        err("Invalid input arguments: " + sys.argv[0] + " [<input-file>|<paper-title>]")
        sys.exit(1)

    search_records = []
    input = sys.argv[1]

    if is_valid_file(input):
        if input.endswith(".csv"):
            data = extract_csv(input, FILE_SEARCH_HDRS)
        elif input.endswith(".xlsx"):
            data = extract_xlsx(input, FILE_SEARCH_HDRS)
        else:
            err("Unsupport file type - cannot convert: " + input)
            sys.exit(2)
        search_records = data
    else:
        # invalid file not exist - treat cmd line arg as title to search directly via Google
        item = {ID: "NA", AUTHORS: "NA", TYPE: "NA", TITLE: input}
        search_records.append(item)

    # search on title - only initial top 10 results from Google
    hdr_shown = False
    results = []

    # output results to XLSX file named current timestamp
    ts = calendar.timegm(time.gmtime())
    wb = xs.Workbook("paper-published-" + str(ts) + ".xlsx")
    ws = wb.add_worksheet()
    # Add a bold format to use to highlight cells.
    bold = wb.add_format({"bold": True})
    row = 0

    for rec in search_records:
        # print("Searching: " + rec[ID] + "-" + rec[TITLE])
        # results = google_search(rec[TITLE])
        results = pubmed_search(rec[TITLE])
        time.sleep(THROTTLE_SECS)  # avoid being blocked by google - rate limit calls

        # check direct or partial ratio match on title
        for result in results[0:1]:
            if rec[TITLE] in result["search_title"] is False:
                continue

            # validate actual page's title vs. input seach
            direct = fuzz.ratio(rec[TITLE], result["page_title"])
            partial = fuzz.partial_ratio(rec[TITLE], result["page_title"])

            # output results
            if not hdr_shown:
                print(
                    "Paper ID,",
                    "Paper Title,",
                    "Paper Authors, ",
                    "Search Title,",
                    "Result Page Title",
                    "Result Page Authors",
                    "MS Type, ",
                    "Direct Match,",
                    "Partial Match,",
                    "Link, ",
                    "Description",
                )
                ws.write(row, 0, "Paper ID", bold)
                ws.write(row, 1, "Paper Title", bold)
                ws.write(row, 2, "Paper Authors", bold)
                ws.write(row, 3, "Search Title", bold)
                ws.write(row, 4, "Result Page Title", bold)
                ws.write(row, 5, "Result Page Authors", bold)
                ws.write(row, 6, "MS Type", bold)
                ws.write(row, 7, "Direct Match", bold)
                ws.write(row, 8, "Partial Match", bold)
                ws.write(row, 9, "Link", bold)
                ws.write(row, 10, "Description", bold)
                hdr_shown = True

            # ignore search results with poor mathes
            if partial < 60:
                continue

            print(
                '%s,"%s","%s","%s","%s","%s","%s",%.2f,%.2f,%s,%s'
                % (
                    rec[ID],
                    rec[TITLE],
                    rec[AUTHORS],
                    result["search_title"],
                    result["page_title"],
                    result["page_authors"],
                    rec[TYPE],
                    direct,
                    partial,
                    result["link"],
                    result["description"],
                )
            )

            row += 1
            ws.write(row, 0, rec[ID])
            ws.write(row, 1, rec[TITLE])
            ws.write(row, 2, rec[AUTHORS])
            ws.write(row, 3, result["search_title"])
            ws.write(row, 4, result["page_title"])
            ws.write(row, 5, result["page_authors"])
            ws.write(row, 6, rec[TYPE])
            ws.write(row, 7, direct)
            ws.write(row, 8, partial)
            ws.write_url(row, 9, result["link"], string=result["link"])
            ws.write(row, 10, result["description"])

    wb.close()

    sys.exit(0)


# ==========================
# Global Variables
# ==========================
GOOGLE_SEARCH_URL = "https://google.com/search?"
PUBMED_SEARCH_URL = "https://www.ncbi.nlm.nih.gov/pmc/?"  # PMC = PubMed Central
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
)
ID = "Manuscript ID"
TITLE = "Manuscript Title"
AUTHORS = "Author Names"
TYPE = "Manuscript Type"
FILE_SEARCH_HDRS = [ID, TITLE, AUTHORS, TYPE]
THROTTLE_SECS = 1

if __name__ == "__main__":
    main()
    sys.exit(0)
