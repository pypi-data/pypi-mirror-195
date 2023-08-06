import glob
import json
import os
import shutil
import re
from lxml import etree
import glob
NEW_ROOT_PATH = "/Users/shareit/work/shareit/wagb/DecodeCode/WhatsApp_v2.22.22.80"
OLD_ROOT_PATH = "/Users/shareit/work/shareit/wa_diff_gb/wa_diff_gbv17"
# 查找对应关系


def get_all_x_files(root):
    return glob.glob(root+"/smali*/X/*.smali", recursive=True)


def get_file_by_name(root, name):
    return glob.glob(root+"/smali*/**/"+name+".smali", recursive=True)


def get_RequestPermissionActivity(root):
    return get_file_by_name(root, "RequestPermissionActivity")


def get_ViewProfilePhoto(root):
    return get_file_by_name(root, "ViewProfilePhoto")


def get_PaymentCustomInstructionsBottomSheet(root):
    return get_file_by_name(root, "PaymentCustomInstructionsBottomSheet")


def get_AppBarLayout(root):
    return get_file_by_name(root, "AppBarLayout")

def get_PaymentView(root):
    return get_file_by_name(root, "PaymentView")


def get_ProfileActivity(root):
    return get_file_by_name(root, "ProfileActivity")

def get_096(root):
    return get_file_by_string(root,'"Could not inflate Behavior subclass "')

def get_1IB(root):
    return get_file_by_string(root,'"msgstore/edit/revoke "')


regex_list = [
    {"\.method public constructor \<init\>\(Landroid\/content\/Context\;Landroid\/graphics\/Typeface\;Lcom\/gbwhatsapp\/TextData\;LX\/\w*\;LX\/\w*\;LX\/\w*\;Ljava\/lang\/String\;\)V": get_all_x_files},
    {"\.method public \w*\(LX\/\w*\;LX\/\w*\;LX\/\w*\;Ljava\/lang\/String\;Ljava\/util\/List\;Ljava\/util\/List\;ZZ\)V": get_all_x_files},
    {"\.method public \w*\(LX\/\w*\;LX\/\w*\;LX\/\w*\;LX\/\w*\;LX\/\w*\;Ljava\/lang\/String\;Ljava\/util\/List\;Ljava\/util\/List\;ZZZ.*": get_all_x_files},
    {"\.method public \w*\(Lorg\/whispersystems\/jobqueue\/Job\;\)V": get_all_x_files},
    {"\.method public static \w*\(Landroid\/content\/Context\;Landroid\/graphics\/Paint\;LX\/\w*\;Ljava\/lang\/CharSequence\;\)Ljava\/lang\/CharSequence\;": get_all_x_files},
    {"\.method public \w*\(Landroid\/content\/Context\;LX\/\w*\;IZ\)I": get_all_x_files},
    {"\.method public \w*\(Landroid\/content\/Context\;Ljava\/lang\/String\;\)LX\/\w*\;": get_all_x_files},
    {"\.method public constructor \<init\>\(LX\/\w*\;LX\/\w*\;LX\/\w*\;LX\/\w*\;Ljava\/io\/File\;Ljava\/io\/File\;IIJJ\)V": get_all_x_files},
    {"\.method public \w*\(LX\/\w*\;\)V": get_AppBarLayout},
    {"\.method public static \w*\(Landroid\/content\/Context\;II\)Landroid\/graphics\/drawable\/Drawable\;": get_all_x_files},
    {"\.method public abstract \w*\(Lcom\/gbwhatsapp\/conversationslist\/ViewHolder\;LX\/\w*\;I\)V": get_all_x_files},
    {"\.method public \w*\(Landroid\/app\/Activity\;LX\/\w*\;LX\/\w*\;LX\/\w*\;Ljava\/lang\/String\;Ljava\/util\/List\;Ljava\/util\/List\;IZZ\)V": get_all_x_files},
    {"\.method public abstract \w*\(Landroid\/graphics\/Bitmap\;Landroid\/view\/View\;LX\/\w*\;\)V": get_all_x_files},
    {"\.field public \w*\:Lcom\/gbwhatsapp\/TextData\;": get_all_x_files},
    {"\.method public \w*\(Landroid\/view\/View\;Landroid\/view\/View\;Landroidy\/coordinatorlayout\/widget\/CoordinatorLayout\;IIII\)V": get_all_x_files},
    {"\.method public static \w*\(Landroid\/app\/Activity\;LX\/\w*\;\[Ljava\/lang\/String\;III.*": get_RequestPermissionActivity},
    {"check\-cast v0\, LX\/\w*\;": get_PaymentCustomInstructionsBottomSheet},
    {"\.super LX\/\w*\;": get_ViewProfilePhoto},
    {"\.method public \w*\(LX\/\w*\;\)V": get_096},
    {"\.method public \w*\(LX\/\w*\;Z\)V": get_1IB},
    {"invoke\-virtual \{\w*\, \w*\}\, LX\/\w*\;\-\>\w*\(F\)V": get_PaymentView},
    {"invoke\-virtual \{v0\}\, LX\/\w*\;\-\>A00\(\)Z": get_ProfileActivity},
    {"\.method public abstract \w*\(Ljava\/lang\/String\;Ljava\/util\/concurrent\/BlockingQueue\;IIIJ\)Ljava\/util\/concurrent\/ThreadPoolExecutor\;": get_all_x_files},
]


def find_by_regex_list():
    for regex in regex_list:
        for key, value in regex.items():
            find_by_regex(key, value)


def find_by_regex(regex, get_file_func):
    old_line = ""
    old_file = ""
    for file in get_file_func(OLD_ROOT_PATH):
        with open(file, "r") as f:
            for line in f.readlines():
                if (re.match(regex, line.strip()) != None):
                    old_line = line
                    old_file = file
                    break
    for file in get_file_func(NEW_ROOT_PATH):
        with open(file, "r") as f:
            for line in f.readlines():
                if (re.match(regex, line.strip()) != None and old_file!=""):
                    x_dict[get_x_name_by_file(
                        old_file)] = get_x_name_by_file(file)
                    print(f"通过{regex}找到{get_x_name_by_file(old_file)}=={get_x_name_by_file(file)}")
                    old_arr = get_x(old_line)
                    arr = get_x(line)
                    for i in range(0, len(old_arr)):
                        x_dict[old_arr[i]] = arr[i]


# 解析public
def parse_public(root):
    public = root+"/res/values/public.xml"
    tree = etree.parse(public)
    dict = {}
    for child in tree.getroot():
        if (child.tag == "public" and "id" in child.attrib):
            name = child.attrib['name']
            id = child.attrib['id']
            type = child.attrib['type']
            if (type not in dict):
                dict[type] = []
            dict[type].append({"name": name, "id": id})
    return dict


def get_file_by_string(root,s):
    """通过字符串查找对应的文件"""
    target_file = None
    for file in glob.glob(root+"/"+"smali*/**/*.smali",recursive=True):
        with open(file,'r') as f:
            if s in f.read():
                target_file = file
                break
    return [target_file]

def get_ids(root):
    """获取id和文件的映射关系"""
    dict = {}
    files = get_all_files(root)
    for file in files:
        content = ""
        with open(file, 'r') as f:
            content = f.read()
            l = re.findall(r'0x7f\w{6}', content)
            for item in l:
                if (item not in dict):
                    dict[item] = set()
                dict[item].add(file)
    print("id个数："+str(len(dict)))
    dict = {k: v for k, v in dict.items() if len(v) == 1}
    print("过滤id个数："+str(len(dict)))
    new_dict = {}
    for key, value in dict.items():
        new_dict[key] = list(value)[0]
    return new_dict


def get_strings(root):
    """获取id和文件的映射关系"""
    dict = {}
    files = get_all_files(root)
    for file in files:
        content = ""
        with open(file, 'r') as f:
            content = f.read()
            l = re.findall(r'".*"', content)
            for item in l:
                if (item not in dict):
                    dict[item] = set()
                dict[item].add(file)
    print("字符串个数："+str(len(dict)))
    dict = {k: v for k, v in dict.items() if len(v) == 1}
    print("过滤之后字符串个数："+str(len(dict)))
    new_dict = {}
    for key, value in dict.items():
        new_dict[key] = list(value)[0]
    return new_dict


def get_id(ids, name, type):
    """"""
    id = "0x7f000000"
    l = list(filter(lambda x: x["name"] == name, ids[type]))
    if (len(l) > 0):
        id = l[0]["id"]
    return id


def get_all_files(root):
    return glob.glob(root+"/smali*/X/*.smali", recursive=True)


string_list = [
    '"CachedMessageStore/fillMessageFromExtraTables"',
    '"messagethumbcache/construct "',
    '", autoDownloadLimit="',
    '"sys-msg/number-change/new-jid-null-override"',
    '"MessageUtil/isValidIncomingUrl/error invalid host on received media url; url="',
    '"Could not inflate Behavior subclass "',
    '"This Activity already has an action bar supplied by the window decor. Do not request Window.FEATURE_SUPPORT_ACTION_BAR and set windowActionBar to false in your theme to use a Toolbar instead."',
    '"wa-shared-preferences/set-backup-timestamp last successful backup timestamp is set to "',
    '"isRecyclable decremented below 0: unmatched pair of setIsRecyable() calls for "',
    '"ViewHolder views must not be attached when created. Ensure that you are not passing \\\'true\\\' to the attachToRoot parameter of LayoutInflater.inflate(..., boolean attachToRoot)"',
    '"Added View has RecyclerView as parent but view is not a real child. Unfiltered index:"',
    '"wa-shared-preferences/get-backup-freq"',
    '"app/has-google-maps-v2 am=false"',
    '"conversation/setuppreview/share-failed"',
    '"ID does not reference a View inside this Activity"',
    '"subgroup has to have a linked parent group jid"',
    '"ConversationRow/onReactionViewClicked null message reactions."',
    '"; rowIds="',
    '", remote_jid="',
    '"videotranscoder/transcode/decoder color format for Huaiwei is VideoFrameConverter.FRAMECONV_COLOR_FORMAT_NV12"',
    '"transcodeutils/isEligibleForMp4Check exception"',
    '"dialogtoast/update-progress-message/dialog-type-not-progress-dialog/ \\\""',
    '"fmessageio/prepareFolder/mkdirs failed: "',
    '"verifynumber/requestcode/invalid-country \\\'"',
    '"contact-mgr-db/unable to get all individual chats"',
    '" that was not found in the set of active Fragments "',
    '"msgstore/setchatunseen/nochat/"',
    '"msgstore/reset-show-group-description/no chat "',
    '"Bad id: "',
    '"Insufficient number of bitmaps to combine"',
    '"app/send-presence-subscription jid="',
    '"msgstore/edit/revoke "',
    '"participant_jids"',
    '"Profile Pictures"',
    '"composerThumbCache"',
    '".Shared"',
    '"externalfilevalidator/file read error: "',
    '"mediafileutils/readablefilename/"',
    '"app/progress-spinner/remove dt="',
    '"should not be run in main thread"',
    '"file-utils/truncate-from-end compressedFile:"',
    '"chat-settings-store/set-underlying-message-tone-to-default updated message tone to default"',
    '"memanager/setMyLidDeviceJid/invalid_jid_error"',
    '"conversations/delete/group:"',
    '".sizeOf() is reporting inconsistent results!"',
    '"msgstore/setchatunseen/nochat/"',
    '"mock_acs_reqeust"',
    '" not attached to a context."',
    '"jid: %s deleted:%d muteEndTime:%d showNotificationWhenMuted:%b useCustomNotification:%b messageTone:%s messageVibrate:%s messagePopup:%s messageLight:%s callTone:%s callVibrate:%s statusMuted:%b pinned:%b pinned_time:%d lowPriorityNotifications:%b mediaVisibility:%d muteReactions:%b autoMutedStatus: %d"',
]


def find_by_string():
    old_strings = get_strings(OLD_ROOT_PATH)
    new_strings = get_strings(NEW_ROOT_PATH)
    for s in string_list:
        if(s in old_strings and s in new_strings):
            old_file = old_strings[s]
            new_file = new_strings[s]
            x_dict[get_x_name_by_file(old_file)] = get_x_name_by_file(new_file)


id_list = [
    {
        "type": "drawable",
        "name": "ic_status_revoked"
    },
    {
        "type": "id",
        "name": "coordinator"
    },
    {
        "type": "id",
        "name": "menuitem_share_third_party"
    },
    {
        "type": "drawable",
        "name": "my_status_add_button"
    },      {
        "type": "drawable",
        "name": "ic_voip_chatlist_joinable_voice"
    },
    {
        "type": "id",
        "name": "menuitem_contactqr_revoke"
    },     {
        "type": "string",
        "name": "conversation_contact_online"
    },     {
        "type": "drawable",
        "name": "ic_voip_chatlist_joinable_voice"
    },     {
        "type": "string",
        "name": "conversation_header_pushname"
    },
]


def find_by_id():
    """通过id查找"""
    old_res_dict = parse_public(OLD_ROOT_PATH)
    old_ids = get_ids(OLD_ROOT_PATH)
    new_res_dict = parse_public(NEW_ROOT_PATH)
    new_ids = get_ids(NEW_ROOT_PATH)
    for id in id_list:
        old_id = get_id(old_res_dict, id["name"], id["type"])
        new_id = get_id(new_res_dict, id["name"], id["type"])
        if (old_id in old_ids and new_id in new_ids):
            x_dict[get_x_name_by_file(old_ids[old_id])] = get_x_name_by_file(
                new_ids[new_id])
        else:
            print(f"未找到{id}")


x_dict = {
    "LX/4oF;":"LX/5PR;",
    "LX/1Z0;":"LX/1eC;",
    "LX/1LS;":"LX/1Rs;",
    "LX/1Z2;":"LX/1eE;",
    "LX/1Fw;":"LX/1Nt;",
    "LX/1dS;":"LX/1YJ;",
    "LX/0lT;":"LX/0qS;",
    "LX/07X;":"LX/07m;",
    "LX/05R;":"LX/05e;",
    "LX/4jx;":"LX/5Iw;",
    "LX/4TVV;":"LX/4TVV;",
}


def get_x(s):
    return re.findall("LX\/\w*\;", s)


def get_x_name_by_file(file):
    file = file[file.rindex('/')+1:]
    file = file[:file.index(".")]
    return f"LX/{file};"


def find():
    find_by_regex_list()
    find_by_id()
    find_by_string()


def search_x():
    """搜索老版本的x"""
    d={}
    for dir in smali_dirs:
        for file in glob.glob(OLD_ROOT_PATH+dir+"**/*.smali", recursive=True):
            with open(file, 'r') as f:
                l = re.findall(r'LX/\w*;', f.read())
                for i in l:
                    if i not in d:
                        d[i]=[]
                    d[i].append(file)

    return d

smali_dirs = [
    "/smali_classes5/",
    "/smali_classes6/",
    "/smali_classes7/",
]

def search_method():
    d=[]
    for dir in smali_dirs:
        for file in glob.glob(NEW_ROOT_PATH+dir+"**/*.smali", recursive=True):
            with open(file, 'r') as f:
                l = re.findall(r'LX/\w*\;\-\>\w*\(.*\).*', f.read())
                for i in l:
                    if i not in d:
                        d.append(i)

    return d

def replace_x():
    for dir in smali_dirs:
        for file in glob.glob(NEW_ROOT_PATH+dir+"**/*.smali", recursive=True):
            with open(file, 'r') as f:
                content = f.read()
                for key,value in x_dict.items():
                    content = content.replace(key,value)
            with open(file,"w") as f:
                f.write(content)
    pass

def replace_method():
    dict = {}
    methods = search_method()
    for i in methods:
        x = i.split("->")[0]
        x = x[x.index("/")+1:-1]
        method = i.split("->")[1]
        old = method[:method.index("(")]
        method = method[method.index("("):]
        files = glob.glob(NEW_ROOT_PATH+"/smali*/X/"+x+"*.smali")
        if(len(files)==1):
            with open (files[0],"r") as f:
                l = []
                for line in f.readlines():
                    if(method in line and ".method" in line):
                        line =line.split(" ")[-1]
                        line = line[:line.index("(")]
                        l.append(line)
                if(len(l)==1):
                    if(old!=l[0]):
                        dict[i]=i.replace(old,l[0])
                elif(len(l)>1):
                    print(l)
                    print(f"匹配到多个方法{i}")

        else:
            print("存在多个文件")
    for dir in smali_dirs:
        for file in glob.glob(NEW_ROOT_PATH+dir+"**/*.smali", recursive=True):
            with open(file, 'r') as f:
                content = f.read()
                for key,value in dict.items():
                    content = content.replace(key,value)
            with open(file,"w") as f:
                    f.write(content)

def replace_field():
    pass

def copy_file():
    for dir in smali_dirs:
        if(not os.path.isdir(NEW_ROOT_PATH+dir)):
            shutil.copytree(OLD_ROOT_PATH+dir,NEW_ROOT_PATH+dir)


if __name__ == "__main__":
    copy_file()
    old_x_dict = search_x()
    find()
    count = 0
    for key,value in old_x_dict.items():
        if(key not in x_dict):
            count+=1
            print(f"未找到{key} {value}")
    print(f"个数为{count}")
    """有些value值和key值相同所以会导致重复替换 比如{A:B,B:C} A先替换为了B，然后B又替换成了C 如果调换顺序就不会发行该种情况
    从字典中移除再添加进行顺序调整"""
    temp_dict = {}
    for key,value in x_dict.items():
        if(value in x_dict):

            temp_dict[key] = value
            print(f"key = {key} value = {value}")
    for key,value in temp_dict.items():
        x_dict.pop(key)
        x_dict[key] = value
    print(x_dict)
    if(count==0):
        replace_x()
        replace_method()
