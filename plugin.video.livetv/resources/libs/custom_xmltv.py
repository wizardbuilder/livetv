import xmltv, os, urllib2, zlib, datetime
from pprint import pprint

basePath = os.getcwd()

#filename = os.path.join(basePath, 'tvguide.xml')
output   = os.path.join(basePath, 'out_tvguide.xml')
guide_sources = ["http://epg.kodi-forum.nl/tvguide.xml"]
available_channels = ["NPO 1 HD", "NPO 2 HD"]


processed_channels = []

def get_remote(src, base=basePath, dest=None):
    filename = src.split('/')[-1]
    if not dest:
        dest = os.path.join(base, src.split('/')[-1])
    f = open(dest, 'wb')
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://thewebsite.com",
        "Connection": "keep-alive" 
        }
    request_src = urllib2.Request(src, headers=request_headers)
    tmpData = urllib2.urlopen(request_src)
    data = tmpData.read()
    if tmpData.info().get('content-encoding') == 'gzip':
        data = zlib.decompress(data, zlib.MAX_WBITS + 16)
    f.write(data)
    f.close()
    if filename.endswith(".gz"):
        import gzip, shutil
        compressed = dest
        extracted  = dest.rstrip(".gz")
        with gzip.open(compressed, 'rb') as f_in, open(extracted, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        filename = extracted
    return filename

def read_epg_data(filename):
    print "Reading EPG data from "+str(filename)
    data = xmltv.read_data(filename)
    return data

def read_epg_channels(filename):
    print "Reading EPG channels from "+str(filename)
    channels = xmltv.read_channels(filename)
    return channels

def read_epg_programmes(filename):
    print "Reading EPG programmes from "+str(filename)
    programmes = xmltv.read_programmes(filename)
    return programmes

def read_all_epg_info(filename):
    data       = read_epg_data(filename)
    channels   = read_epg_channels(filename)
    programmes = read_epg_programmes(filename)
    return data, channels, programmes

def extract_wanted_data(channels, programmes, channel_filter=available_channels):
    wanted_channels   = []
    wanted_programmes = []
    for x in channels:
        if x["id"] in channel_filter:
            wanted_channels.append(x)
    for x in programmes:
        if x["channel"] in channel_filter:
            wanted_programmes.append(x)
    return wanted_channels, wanted_programmes

def write_final_xmltv(channels, programmes, file=output):
    print "Writing new XMLTV file "+str(file)
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    w = xmltv.Writer(encoding="us-ascii",
        date=now,
        source_info_url="http://www.funktronics.ca/python-xmltv",
        source_info_name="Funktronics",
        generator_info_name="python-xmltv",
        generator_info_url="http://www.funktronics.ca/python-xmltv")
    for c in channels:
        print "Adding channel info to new XMLTV:"
        print c
        w.addChannel(c)
    for p in programmes:
        w.addProgramme(p)
    w.write(file, pretty_print=True)

def process_files(sources=guide_sources, base=basePath, refresh_local="false", channel_filter=available_channels):
    refresh_local = (refresh_local != "false")
    # Download files
    xmltv_files = []
    for guide in sources:
        dest = os.path.join(base, guide.split('/')[-1])
        if not os.path.exists(dest):
            refresh_local = True
        if not refresh_local:
            xmltv_files.append(guide.split('/')[-1])
        else:
            print "Getting guide:"
            print guide
            print base
            xmltv_files.append(get_remote(guide, base=base))
    #Process the files for new and wanted data:
    data            = {}
    channels_list   = []
    programmes_list = []
    for file in xmltv_files:
        processing = []
        data, channels, programmes = read_all_epg_info(os.path.join(base,file))
        wanted_channels, wanted_programmes = extract_wanted_data(channels, programmes, channel_filter=channel_filter)
        for chan in wanted_channels:
            if not chan["id"] in processed_channels:
                channels_list.append(chan)
                processing.append(chan["id"])
        for prog in wanted_programmes:
            if not prog["channel"] in processed_channels:
                programmes_list.append(prog)
                processing.append(prog["channel"])
        for x in processing:
            if not x in processed_channels:
                processed_channels.append(x)
    # Create empty channels for all remaining channels that were not found with epg
    for chan in channel_filter:
        if not chan in processed_channels:
            print "Cannot find "+chan+". Adding it to xmltv file with no program available"
            channels_list.append({'url': ['http://kodi.tv/'], 'display-name': [(chan, 'nl')], 'id': chan})
    return data, channels_list, programmes_list

def get_cur_xmltv_data(file=output):
    print "READING XMLTV FILE..."
    print file
    if os.path.exists(file):
        data = read_epg_data(file)
        print data
        return data
    return False



if __name__ == '__main__':
    data, channels, programmes = process_files()
    pprint(data)
    write_final_xmltv(channels, programmes)