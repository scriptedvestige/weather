# NWS Forecast Scraper

This is currently a very rough start of a new project.  This system will ingest weather forecast data from NWS for multiple zones as well as observation data from one of the zones then save the parsed data from the API response to a database.

I'm currently in build and test mode, and this is far from complete.

The purpose of this standalone system is that the database will be a single source of truth for multiple projects.  One of those projects is my Daily Briefing system.  Once this system is functional, I'll point the weather module of the Daily Briefing system to pull from the appropriate table in the database.

The second project that will feed on this data will be launching in the spring.  Stay tuned!