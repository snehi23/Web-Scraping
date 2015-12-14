# Web-Scraping
Web scraping (web harvesting or web data extraction) is a computer software technique of extracting information from websites.

ASNs (Autonomous System Numbers) are one of the building blocks of the
Internet. This project is to create a mapping from each ASN in use to the
company that owns it. For example, ASN 36375 is used by the University of
Michigan - http://bgp.he.net/AS36375
 
The site http://bgp.he.net/ has lots of useful information about ASNs. 
Starting at http://bgp.he.net/report/world crawl and scrape the linked country
reports to make a structure mapping each ASN to info about that ASN.
Sample structure:
  {3320: {'Country': 'DE',
  'Name': 'Deutsche Telekom AG',
  'Routes v4': 13547,
  'Routes v6': 268},
  36375: {'Country': 'US',
  'Name': 'University of Michigan',
  'Routes v4': 14,
  'Routes v6': 1}}
