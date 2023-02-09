from pyrogram import Client,filters,types
from pyrogram.errors import SessionPasswordNeeded
from os import remove
from DataBase import *

ApiId=int(input("Api Id: "))
ApiHash=input("Api Hash: ")

AntiDeleted=Client("AntiDeleted",ApiId,ApiHash,device_model="Redmi Redmi Note 11 Pro")

StateLogin=AntiDeleted.connect()
if StateLogin == False:
    Phone=input("Phone: ")
    SendLoginCode=AntiDeleted.send_code(Phone)
    CodeLogin=input("Login Code: ")
    try:
        AntiDeleted.sign_in(Phone,SendLoginCode.phone_code_hash,CodeLogin)
    except SessionPasswordNeeded:
        AntiDeleted.check_password(input("Password: "))
    if AntiDeleted.is_connected:
        print("Login succsess :)")
    else:
        print("Login feild :(")
else:
    print("Login Ready !")
AntiDeleted.disconnect()

@AntiDeleted.on_message(filters.me & filters.private)
async def CommandMe(_:AntiDeleted,Message:types.Message):
    try:
        Text=Message.text
        UserId=Message.from_user.id
        UserIdTarget=Message.chat.id
        MessageId=Message.id
        FirstName=Message.chat.first_name
        if Text=="Help":
            await AntiDeleted.edit_message_text(UserId,MessageId,"~ Hi 👻\n\n [🌀] `Deleteon` : Send Pv Target For On Save Deleted Message\n\n[🌀] `Deleteoff` : Send Pv Target For Off Save Deleted Message\n\n[⚠️] And Create Chanell To Name Target For See Deleted Message.")
        if Text=="Deleteon":
            TargetChanellInfo=Fetch_InfoChanell_Target(UserIdTarget)
            await AntiDeleted.delete_messages(UserId,MessageId)
            if TargetChanellInfo==404:
                UserIdChanell=await AntiDeleted.create_channel(FirstName,"[🐈] Github.com/Faridreza\n[🆔] @CaFaR")
                SaveInfoChanell=Insert_InfoChanell_Target(UserIdTarget,UserIdChanell.id)
                if SaveInfoChanell==200:
                    await AntiDeleted.send_message(UserIdChanell.id,"~ Hi 👻\n[⚠️] Target Info:\n  Firstname: {0}\n  UserNumberId: {1} \n\n [🐈] Github.com/Faridreza\n[🆔] @CaFaR".format(FirstName,UserIdTarget))
            else:
                await AntiDeleted.send_message(TargetChanellInfo[0],"~ Hi Chanell Is Ready ⚠️")
        if Text=="Deleteoff":
            await AntiDeleted.delete_messages(UserId,MessageId)
            TargetChanellInfo=Fetch_InfoChanell_Target(UserIdTarget)
            if TargetChanellInfo!=404:
                await AntiDeleted.send_message(TargetChanellInfo[0],"~ Hi Target See Message Off ⚠️")
            Delete_InfoChanell_Target(UserIdTarget)
    except:
        pass
    
def GetTimeAndDate(date)->tuple:
    """return (Time,Date)"""
    DateNowMessage=date.split()
    Time=DateNowMessage[1][:-3]
    Date=DateNowMessage[0]
    return (Time,Date)

@AntiDeleted.on_message(filters.private & filters.text)
async def TargetMessage(_:AntiDeleted,Message:types.Message):
    try:
        Text=Message.text
        UserIdTarget=Message.chat.id
        MessageId=Message.id
        FirstName=Message.chat.first_name
        CheckAny=Fetch_InfoChanell_Target(UserIdTarget)
        if CheckAny!=404:
            TimeDate=GetTimeAndDate(str(Message.date))
            Insert_InfoMessage_Target(UserIdTarget,FirstName,Text,TimeDate[0],TimeDate[1],MessageId)
    except:
        pass


@AntiDeleted.on_message(filters.photo)
async def SaveTimerImgAndVedio(_:AntiDeleted,Message:types.Message):
    try:
        if Message.photo.ttl_seconds:
            CheckAny=Fetch_InfoChanell_Target(Message.from_user.id)
            if CheckAny!=404:
                InfoFile=await AntiDeleted.download_media(Message,"DataFile\\")
                InfoTarget=await AntiDeleted.get_users(Message.from_user.id)
                UserIdTargetChanell=Fetch_InfoChanell_Target(InfoTarget.id)
                if UserIdTargetChanell!=404:
                    if "jpg" in InfoFile:
                        await AntiDeleted.send_media_group(UserIdTargetChanell[0],[types.InputMediaPhoto(InfoFile,caption="Expierd Image Saved 🔐")])
                remove(InfoFile)
    except:
        pass

@AntiDeleted.on_message(filters.video)
async def SaveTimerImgAndVedio(_:AntiDeleted,Message:types.Message):
    try:
        if Message.video.ttl_seconds:
            CheckAny=Fetch_InfoChanell_Target(Message.from_user.id)
            if CheckAny!=404:
                InfoFile=await AntiDeleted.download_media(Message,"DataFile\\")
                InfoTarget=await AntiDeleted.get_users(Message.from_user.id)
                UserIdTargetChanell=Fetch_InfoChanell_Target(InfoTarget.id)
                if UserIdTargetChanell!=404:
                    if "mp4" in InfoFile:                
                        await AntiDeleted.send_media_group(UserIdTargetChanell[0],[types.InputMediaVideo(InfoFile,caption="Expierd Video Saved 🔐")])
                remove(InfoFile)
    except:
        pass

@AntiDeleted.on_deleted_messages()
async def TargetDeletedMessage(_:AntiDeleted,Message:types.Message):
    try:
        for Message in Message:
            GetDeletedMessage=Fetch_InfoMessage_Target(Message.id)
            if GetDeletedMessage!=404:
                InfoTarget=await AntiDeleted.get_users(GetDeletedMessage[1])
                UserIdTargetChanell=Fetch_InfoChanell_Target(InfoTarget.id)
                if UserIdTargetChanell!=404:
                    await AntiDeleted.send_message(UserIdTargetChanell[0],"Find Delete Message👻\n\n[🙋‍♂️] Name: {0}\n[🗓️] Date Time: {1}  {2} \n[🔐] Text: {3}".format(GetDeletedMessage[2],GetDeletedMessage[5],GetDeletedMessage[4],GetDeletedMessage[3]))
    except:
        pass

@AntiDeleted.on_edited_message(filters.private)
async def TargetEditMessage(_:AntiDeleted,Message:types.Message):
    try:
        GetDeletedMessage=Fetch_InfoMessage_Target(Message.id)
        if GetDeletedMessage!=404:
            InfoTarget=await AntiDeleted.get_users(GetDeletedMessage[1])
            UserIdTargetChanell=Fetch_InfoChanell_Target(InfoTarget.id)
            if UserIdTargetChanell!=404 and GetDeletedMessage[3]!=Message.text:
                await AntiDeleted.send_message(UserIdTargetChanell[0],"Find Edit Message👻\n\n[🙋‍♂️] Name: {0}\n[🗓️] Date Time: {1}  {2} \n[✅] Text Original: {3} \n[🔏] Text Edited: {4}".format(GetDeletedMessage[2],GetDeletedMessage[5],GetDeletedMessage[4],GetDeletedMessage[3],Message.text))
    except:
        pass

AntiDeleted.run()