# drift_source_sink
Routines to read drifter database and, given a user specified polygon, generates source and sink tracks
Routine to make googlmaps of drifters enimating from or entering into a user-specified polygon using the "gmplot" package which works ok on my linux desktop but I haven't got it to install on my Windows laptop

Requires user to specify box such as decimal degree in the format "gbox=[maxlon, minlon, maxlat, minlat]" as well as how many weeks to run the tracks. I have so far ran this for Stellwagon Bank, Natucket Shoals, and NE Peak boxes and saved results as "sink_person_region.html"
