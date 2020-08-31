def return_data():
    data = {
        0 : "HMagazines",
        2 : "HGame CG",
        3 : "DoujinshiDB",
        5 : "Pixiv Images",
        8 : "Nico Nico Seiga",
        9 : "Danbooru",
        10 : "Drawr Images",
        11 : "Nijie Images",
        12 : "Yandere",
        13 : "Openingsmoe",
        15 : "Shutterstock",
        16 : "FAKKU",
        18 : "HMisc",
        19 : "TwoDMarket",
        20 : "MediBang",
        21 : "Anime",
        22 : "HAnime",
        23 : "Movies",
        24 : "Shows",
        25 : "Gelbooru",
        26 : "Konachan",
        27 : "SankakuChannel",
        28 : "AnimePicturesnet",
        29 : "E621net",
        30 : "IdolComplex",
        31 : "Bcynet Illust",
        32 : "Bcynet Cosplay",
        33 : "PortalGraphicsnet",
        34 : "DeviantArt",
        35 : "Pawoonet",
        36 : "Madokami",
        37 : "MangaDex",
        38 : "HMisc EHentai",
        999 : "ALL"
    }
    return data

def index_to_db(index):
    return return_data()[int(index)]