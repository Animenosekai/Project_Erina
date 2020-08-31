"""
Anime Episode Number Extraction for the Erina Project

@author: Anime no Sekai
Idea from aniep.js by soruly (done in a completly different way though)
Erina Project - 2020
"""

import re
import filecenter

def kanjis_to_digit(kanjis):
    '''
    Translate kanjis number to digits from 0 to 100.\n
    i.e.  三十二 ==> 32
    '''
    if kanjis == '百':
        return '100'
    kanjis_to_digit_data = {
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '十': 1,
    }
    unwanted = ['第', '話', '集', '话', '回', '夜', ' ']
    for kanji in unwanted:
        kanjis = kanjis.replace(kanji, '')
    kanjis = kanjis.replace('第', '').replace('話', '')
    digits = ''
    for character_number, _ in enumerate(kanjis):
        if character_number + 1 == len(kanjis) and kanjis[character_number] == '十':
            if digits == '':
                digits = '10'
            else:
                digits = digits + '0'
        elif kanjis[character_number] == '十':
            if digits == '':
                digits = digits + str(kanjis_to_digit_data[kanjis[character_number]])
            else:
                pass
        else:
            digits = digits + str(kanjis_to_digit_data[kanjis[character_number]])
    return digits

def episode_from_filename(filename, anime_title='', list_of_alternative_titles=[]):
    """
    Extracting an anime episode number from a filename.

    Erina Project\n
    © Anime no Sekai - 2020
    """
    # removing the file extension
    file_extension = filecenter.extension_from_base(filename)
    episode = filename.replace(file_extension, '')

    # replacing the title by nothing
    episode = episode.replace(anime_title, '')

    # replacing alternative titles by nothing
    for title in list_of_alternative_titles:
        episode = episode.replace(title, '')
    
    # data
    list_of_anime_raw_team = ['Ohys-Raws', 'Abystoma', 'VCB-Studio', 'Snow-Raws', 'Fullmetal', 'Shark-Raws', 'FY-Raws', 'LowPower-Raws', 'Moe-Raws', 'Moozzi2', 'JKG', 'Okay-Raws', 'Centaurea-Raws', 'Anime Land', 'Cornflower Studio', 'BeatZ', 'jibaketa', 'Pandoratv-raws', 'FumeiRaws', 'Chilled', 'Renascent', 'UCCUSS', 'ReinForce', '◯PMan', 'PPP-Raws', 'Squirrel', 'YuushaNi', 'meow', 'tribute', 'tG1R0', 'Kentaraws', 'hworm', 'Bastard-Raws', 'DDD', 'Beatrice-Raws', 'TardRaws', 'KTXP', 'Leopard-Raws']
    list_of_unwanted_digits = ['1280x720', '720', '1280', '1920', '1080', '1920x1080', 'x264', '10 bits', 'bs11', '720p', '1080p', '10bits', 'x265', 'x.265', 'x.264', 'x2', 'x1', 'x3', 'hi10p', '10p', 'eac3', '10bit', '10 bit', '110c26b0', '640x480', '640', '480', '480p', 'yuv420p10', 'p10', '420', 'h265', 'h264', '1920x1036', '1036', 'mpeg2', 'mpeg4', '1440', '1440x1080', 'ac3', '486p', 'Part 1', 'Part 2', 'Part 3', 'Part 4', 'Part 5', 'Part 6', 'Part 7', 'Part 8', 'Part 9', 'Part 10', 'of 1', 'of 2', 'of 3', 'of 4', 'of 5', 'of 6', 'of 7', 'of 8', 'of 9', 'of 10', ]
    video_extensions = ['arcut', 'prproj', 'aep', 'wot', 'swf', 'pz', 'dmx', 'mkv', 'psv', 'sfd', 'piv', 'fcp', 'mp4', 'rmvb', 'veg', 'sfvidcap', 'ncor', 'vem', 'd2v', 'wmmp', 'm1v', 'viv', 'izz', 'ale', 'cpvc', 'mpv', 'ser', 'bk2', 'jtv', 'webm', 'meta', 'aec', 'wlmp', 'mswmm', 'msdvd', 'rec', 'bik', 'dcr', 'scm', 'mxf', 'srt', 'wpl', 'scm', 'dir', 'dzm', 'fbr', 'db2', 'str', 'vtt', 'dcr', 'amc', 'dmsm', 'rcd', 'wmv', 'aepx', '3gp', 'mj2', 'dpa', 'camproj', 'vob', 'vp6', 'mpeg', 'bin', 'ts', 'mpv2', 'mk3d', 'm15', 'sbt', 'pac', 'ifo', 'hdmov', 'mp4infovid', 'video', 'avi', 'vid', 'mani', 'asf', 'swi', 'photoshow', 'kdenlive', 'ssf', 'trec', 'pns', 'mvd', 'psh', 'rms', 'trp', 'dat', 'aaf', 'aegraphic', 'amx', 'flv', 'mpg', 'gts', 'zmv', 'ismv', '3gp2', 'flc', 'vpj', 'vsp', 'usm', 'siv', 'rum', 'mpeg4', 'm2ts', 'tvshow', 'swt', 'wvm', '264', 'mse', 'evo', 'rcut', 'rm', 'dxr', 'mts', 'cine', 'wp3', 'f4p', 'avchd', 'gvi', 'sbk', 'm2t', 'pds', 'scc', 'mproj', 'dv4', 'mvp', 'pmf', 'mp4v', 'vro', 'playlist', 'dmsm3d', 'dream', 'mob', 'tpd', 'aqt', 'dzt', 'ivr', 'rdb', 'smv', 'tix', 'dav', 'mnv', 'movie', '264', 'm2p', 'mmv', 'm4v', 'mov', 'cpi', 'gfp', 'dzp', 'stx', 'h264', 'dvr', '3g2', 'ircp', 'avv', 'screenflow', 'cst', 'axv', 'vc1', 'qtch', 'lvix', 'inp', 'awlive', 'ffd', 'camv', 'bnp', 'izzy', 'avb', 'wcp', 'fbr', 'mys', 'm75', 'dmb', 'avs', 'vr', 'sbz', 'zm3', 'mpe', 'camrec', 'xvid', 'ogv', 'vp3', 'mp2v', '3mm', '60d', 'tp', 'dash', 'hevc', 'bsf', 'kmv', 'f4v', 'bu', 'yuv', 'vgz', 'psb', '3gpp', 'exo', 'wm', 'g2m', 'vep', 'osp', 'ddat', 'spl', '890', 'bdmv', 'dvr-ms', 'dv', 'r3d', 'jdr', 'sfera', 'ism', 'mvp', 'xml', 'moi', 'mvex', 'sqz', 'hdv', 'dck', 'int', 'jss', 'qtl', 'smk', 'n3r', 'dnc', 'm4u', '3gpp2', 'aetx', 'rsx', 'tsp', 'mp21', 'rmd', 'mgv', 'lrv', 'rv', 'divx', 'k3g', 'ogx', 'f4m', 'mtv', 'lrec', 'wmd', 'clpi', 'roq', 'cme', 'snagproj', 'mve', 'bdt3', 'g64', '3p2', 'lsx', 'mpeg2', 'vcr', 'flic', 'dv-avi', 'rmp', 'qtz', 'tvs', 'fli', 'm2a', 'tsv', 'mpeg1', 'xesc', 'vcpf', 'moov', 'ivf', 'tdt', 'v264', 'ced', 'dmsd', 'f4f', 'wmx', 'dpg', 'nfv', 'wvx', 'ogm', 'xmv', 'wxp', 'irf', 'arf', 'nvc', '787', 'wtv', 'ajp', 'ftc', 'mpl', 'mjp', 'bdm', 'asx', 'tivo', 'theater', 'dvx', 'd3v', 'vivo', 'cvc', 'm4e', 'ssm', 'mjpg', 'nsv', 'msh', 'm21', 'ave', 'vse', 'imovielibrary', 'movie', 'avp', 'san', 'bvr', 'jmv', 'otrkey', 'dvdmedia', 'mpsub', 'crec', 'tda3mt', 'avd', 'nuv', 'vlab', 'pgi', 'rcrec', 'smil', 'wfsp', 'sec', 'zeg', 'prel', 'vcv', 'vbc', 'sdv', 'rvid', 'vdr', 'ttxt', 'g64x', 'sedprj', 'orv', 'rvl', 'plproj', 'jts', 'mpgindex', 'xlmv', 'ismc', 'cmproj', 'prtl', 'ppj', 'cmmtpl', 'pxv', 'fpdx', 'tod', 'evo', 'zm1', 'zm2', 'flh', 'gom', 'axm', 'm21', 'mt2s', 'gifv', 'mvc', 'y4m', 'box', 'gxf', 'par', 'edl', 'w32', 'rmd', 'm2v', 'mod', 'amv', 'qt', 'xel', 'av', 'viewlet', 'qtm', 'yog', 'am', 'wsve', 'thp', 'pvr', 'clk', 'vp7', 'pssd', 'bmk', 'tpr', 'fcproject', 'gcs', 'm1pg', 'seq', 'vdx', 'aet', 'vdo', 'fcarch', 'blz', 'byu', 'sec', 'vfw', 'mpl', 'tvlayer', 'bmc', 'vs4', 'proqc', 'imovieproj', 'scn', 'anim', 'mpg4', 'mpls', 'smi', 'modd', 'hkm', 'tp0', 'nut', 'cmrec', 'gl', 'qsv', 'rmv', 'mqv', 'cmmp', 'usf', 'aecap', 'ismclip', 'pro', 'imovieproject', 'dmss', 'iva', 'bix', 'ffm', 'xej', 'insv', 'svi', 'xfl', 'rcproject', 'ezt', 'vf', 'mpg2', 'ivs', 'lsf', 'fvt', 'cip', 'imoviemobile', 'fbz', 'dce', 'avm', 'exp', 'stl', 'vix', 'tdx', 'eyetv', 'ravi', 'avs', 'moff', 'smi', 'mp21', 'gvp', 'vfz', 'rp', 'bik2', 'pjs', 'bdt2', 'qtindex', 'mxv', 'rts', 'cx3', 'dmsd3d', 'ktn', 'pro4dvd', 'pro5dvd', 'mvb', 'mvy', 'dad', 'mjpeg', 'tvrecording', 'anx', 'ntp', 'vmlf', 'avr', 'wgi', 'pva', 'dif', 'mpf', 'eye', 'tid', 'vmlt', 'sml', 'dlx', 'flx', 'bs4', 'cmv', 'jnr', 'vsh', 'av3', 'avc', 'grasp', 'vft', 'cel', 'pmv', 'dsy', 'rts']
    ### this list of video extensions comes from my python module filecenter.
    audio_extensions = ['sdt', 'amxd', 'minigsf', 'nbs', 'fev', 'pcg', 'mp3', 'flp', 'rns', 'ply', 'rgrp', 'bun', '4mp', 'apl', 'band', 'aimppl', 'wow', '5xe', 'ust', 'xfs', 'nkm', 'dm', 'mui', 'mscx', 'nki', 'rex', 'l', 'flac', 'sfk', 'm4r', 'sf2', 'bww', 'toc', 'ovw', 'omx', 'mmlp', 'mti', 'sng', 'phy', 'rmj', 'qcp', 'ftmx', 'pek', 'h5b', 'vsq', 'h5s', 'vpw', 'omg', 'cgrp', 'vyf', 'f4a', 'bidule', 'isma', 'mtm', 'caff', 'wus', 'efs', 'trak', 'igp', 'gsf', 'itls', 'wproj', 'rol', 'sbi', 'sds', 'dsm', 'slp', 'zpa', 'afc', 'dmse', 'dmsa', 'mdr', 'cwb', 'omf', 'syw', 'sngx', 'gsm', 'sph', 'mmpz', 'als', 'dtm', 'aup', 'm3u', 'dff', 'vdj', 'gp5', 'wfp', 'mka', 'mid', 'uax', 'asd', 'vlc', 'aud', 'ang', 'tg', 'saf', 'sdat', 'wav', 'flm', 'abm', 'dcf', 'sty', 'w01', 'ogg', 'mscz', 'dsf', 'midi', 'sfpack', 'oma', 'alc', 'rip', 'sfl', 'act', 'm4a', 'copy', 'kt3', 'uni', 'acd-zip', 'mtf', 'pla', 'wpk', 'emx', 'pcast', 'ckb', 'sgp', 'mux', 'm3u8', 'ac3', 'rx2', 'vsqx', 'gpk', 'ptx', 'sesx', 'ftm', 'frg', 'sd', 'uw', 'pandora', 'cdo', 'q1', 'ram', 'stm', 'logic', 'oga', 'mo3', 'emd', 'wax', 'acm', 'ds', 'wma', 'pts', 'dct', 'iti', 'ptt', 's3i', 'ncw', 'kmp', 'sd', 'vgm', 'ins', 'rmx', 'cwt', 'f32', 'mpu', 'akp', 'vag', 's3m', 'pkf', '3ga', 'bnk', 'sib', 'rso', 'aac', 'aif', 'mtp', 'amr', 'abc', 'cdr', 'aa3', 'acd', 'opus', 'at3', 'b4s', 'wrk', 'vmd', '669', 'dfc', 'ins', 'mus', 'syx', 'xspf', 'dra', 'vqf', 'svd', 'caf', 'mod', 'gbs', 'cda', 'vox', 'iff', 'odm', 'mmm', 'mx3', 'acp', 'lof', 'mx5template', 'wvc', 'amf', 'rcy', 'ppcx', 'h0', 'sbg', 'rta', 'ssnd', 'nml', 'nkx', 'wfm', 'gpbank', 'cdda', 'sseq', 'agm', 'vpl', 'dtshd', 'mbr', 'bdd', 'sxt', 'g726', 'emp', 'ptxt', 'psm', 'logicx', 'rti', 'ptm', 'wave', 'conform', 'cwp', 'sng', 'mxl', 'aob', 'mpa', 'mogg', 'med', 'a2m', 'aiff', 'wtpt', 'bwg', 'cidb', 'cts', 'm4b', 'gpx', 'fsb', 'sns', 'vip', 'wpp', 'ra', 'shn', 'xm', 'smf', 'nwc', 'wve', 'okt', 'yookoo', 'ics', 'w64', 'syh', 'gsflib', 'zvd', 'pk', 'nra', 'xa', 'nrt', 'fpa', 'sou', 'miniusf', 'xrns', 'aa', 'wem', 'dss', 'csh', 'dig', 'fdp', 'tak', 'cpr', 'musx', 'mus', 'swa', 'npl', 'tak', 'igr', 'aria', 'uwf', 'agr', 'dvf', 'mpga', 'lwv', 'mpdp', 'mx5', 'myr', 'mu3', 'krz', 'rsn', 'smp', 'nvf', 'wv', 'kar', 'u', 'peak', 'nkc', 'ape', 'brstm', 'acd-bak', 'cfa', 'dls', 'dts', 'vpm', 'mmf', 'sc2', 'hbe', 'vmo', 'pca', 'g721', 'stap', 'gig', 'ssm', 'vc3', 'fzv', 'lso', 'mdc', 'fzf', 'ds2', 'm5p', 'efv', 'nsa', 'pna', 'usflib', 'wfb', 'obw', 'ab', 'ntn', 'sppack', 'narrative', 'gbproj', 'amz', 'jam', 'cdlx', 'note', 'au', 'raw', 'k26', 'mt2', 'ksc', 'rmi', 'voxal', 'smp', 'sprg', 'sseq', 'h4b', 'm4p', 'msmpl_bank', 'hsb', 'groove', 'esps', 'psf', 'sma', 'sap', 'ftm', 'dcm', 'efk', 'drg', 'bwf', 'hca', 'efq', 'f2r', 'koz', 'koz', 'tta', 'wut', 'xmu', 'song', 'ma1', 'cws', 'sfz', 'f3r', 'seq', 'aax', 'vb', 'mxmf', 'ksf', '5xb', 'rfl', 'mts', 'ots', 'mmp', 'a2b', '8svx', 'adt', 'ptf', 'nmsv', 'mpc', 'pno', 'usf', 'avastsounds', 'pac', 'rng', 'adg', 'xmf', 'syn', 'ove', 'snd', 'vpr', 'adv', 'vrf', 'sbk', 'voc', 'dmc', 'prg', 'r1m', 'rbs', 'psy', 'expressionmap', 'vtx', 'ovw', 'dewf', 'la', '5xs', 'its', 'mp2', 'g723', 'all', 'slx', 'fsc', 'ppc', 'vgz', 's3z', 'rvx', 'kpl', 'bap', 'mgv', 'ult', 'zpl', 'nkb', 'a2i', 'pho', 'aifc', 'stx', 'kfn', 'psf1', 'mux', 'vap', 'h5e', 'adts', 'f64', 'sd2f', 'snd', 'dwd', 'wfd', 'ofr', 'rbs', 'sfs', 'efa', 'sfap0', 'mx4', 'wtpl', 'wwu', 'td0', 'minipsf2', 'psf2', 'ariax', 'iaa', 'xsp', 'rts', 'nks', 'fsm', 'ses', 'smpx', 'ams', 'svx', 'df2', 'ay', 'rax', 'exs', 'pvc', 'cpt', 'mte', 'ckf', 'dmf', 'scs11', 'ptcop', 'jspf', 'sd2', 'ams', 'hdp', 'cel', 'snd', 'txw', 'minipsf', 'vmf', 'msv', 'pbf', 'vmf']
    ### this list of audio extensions comes from my python module filecenter.
    list_of_years = [1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050]
    
    # lowercase everything for a more efficient search
    episode = episode.lower()
    
    # iterating and replacing by nothing content of lists
    for team in list_of_anime_raw_team:
        episode = episode.replace(team.lower(), '')
    for unwanted in list_of_unwanted_digits:
        episode = episode.replace(unwanted, '')
    for extension in video_extensions:
        episode = episode.replace(extension, '')
    for extension in audio_extensions:
        episode = episode.replace(extension, '')
    for year in list_of_years:
        episode = episode.replace(str(year), '')

    types = ['OVA','OAD','SP','OP','ED','NCOP','NCED','EX','CM','PV','Preview','Yokoku','メニュー','Menu','エンディング','Movie', '予告', 'OPENING', 'opening', 'Opening', 'ENDING', 'Ending', 'ending']

    found_type = ''
    for element in types:
        if element.lower() in episode:
            found_type = element
            break

    # deleting everything other than digit
    episode = re.sub('[^0123456789一二三四五六七八九十]', '', episode)
    episode_without_kanjis = re.sub('[^0123456789]', '', episode)
    episode_without_digits = re.sub('[^一二三四五六七八九十]', '', episode)

    if len(episode_without_digits) != 0 and len(episode_without_kanjis) == 0:
        episode = str(kanjis_to_digit(episode_without_digits))

    if found_type != '':
        episode = str(found_type) + ' ' + str(episode)

    if episode == '':
        return '0'

    return episode
    
