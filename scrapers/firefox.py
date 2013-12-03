#!/usr/bin/env python2

import platform
import os
import sqlite3 as sql

class FirefoxScraper(object):
    def __init__(self):
        (result, paths) = self.config_path(platform.system(), platform.release())
        if result:
            #TODO actually handle multiple profiles
            srcConn = sql.connect("%s/%s" % (paths[0], "places.sqlite"))
            self.visitsCur = srcConn.cursor()

            srcConn = sql.connect("%s/%s" % (paths[0], "downloads.sqlite"))
            self.dlCur = srcConn.cursor()
            self.ready = True
        else:
            self.ready = False

    
    def isReady(self):
        return self.ready


    def config_path(self, platform, release):
        """ 
        returns (false, errMsg) if (platform, release browser) not supported
        returns (true, paths) otherwise

        Add to this function as we support more platforms and browsers
        TODO: test on machines other than Ubuntu
        """
        paths = []
        error = ""

        if platform == "Linux":
            profiles_path = "%s/.mozilla/firefox" % os.environ["HOME"]
            for prof_dir in os.listdir(profiles_path):
                db_path = "%s/%s" % (profiles_path, prof_dir)
                if(os.access("%s/%s" % (db_path, "places.sqlite"), os.R_OK) \
                and os.access("%s/%s" % (db_path, "downloads.sqlite"), os.R_OK)):
                    paths.append(db_path)
        #elif platform == "Darwin":
            #path = ("/Users/%s/Library/Application Support" \
            #        + "/Google/Chrome/Default") \
            #        % os.environ["USER"]
        #elif platform == "Windows" and release == "XP":
            #path = "C:\\Documents and Settings\\%s" \
            #        + "\\Local Settings\\Application Data" \
            #        + "\\Google\\Chrome\\User Data\\Default" \
            #        % os.environ["USERNAME"]
        #elif platform == "Windows" and release == "Vista":
            #path = "C:\\Users\\%s\\AppData\\Local" \
            #        + "\\Google\\Chrome\\User Data\\Default" \
            #        % os.environ["USERNAME"]
        else:
            error = "Your platform, %s %s, is not supported" \
                    % (platform, release)

        if paths != []:
            return (True, paths)
        else:
            return (False, error)


    def scrape_visits(self):
        for (id, url, visit_time) in \
            self.visitsCur.execute(\
                    """select hv.id, p.url, hv.visit_date
                       from moz_places as p
                       inner join moz_historyvisits as hv
                       on p.id=hv.place_id
                       """): 
            new_time = (visit_time) / 1000000
            yield (id, url, new_time, None, "firefox")

        return

    def scrape_downloads(self):
        for (id, path) in self.dlCur.execute(\
                """select id,target from moz_downloads"""):
            yield (id, path.replace("file://", ""), "firefox")

        return
