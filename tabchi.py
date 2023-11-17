try:
	import os,re,json,random,aiocron,asyncio
	from telethon.sync import TelegramClient,events,functions,types
except ModuleNotFoundError:
	os.system('pip install --upgrade pip && pip install telethon && pip install asyncio && pip install aiocron && clear')
	os.sys.exit('installed the required packages !')

def get(file):
	with open(file,'r') as r:
		return json.load(r)

def put(file,data):
	with open(file,'w') as w:
		json.dump(data,w)

def font(text):
	if isinstance(text,str):
		text = text.lower()
		return text.translate(text.maketrans('qwertyuiopasdfghjklzxcvbnm-0123456789','ǫᴡᴇʀᴛʏᴜɪᴏᴘᴀsᴅғɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ-𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗'))
	else:
		return None

api_id = 17064702
api_hash = 'f65880b9eededbee85346f874819bbc5'
session = input('enter the session name : ')

bot = TelegramClient(session,api_id,api_hash)

dev = 6663317718

if not os.path.exists('data') or not os.path.isdir('data'):
	os.mkdir('data')

if not os.path.exists(f'data/{session}.json') or not os.path.isfile(f'data/{session}.json'):
	data = {'bot':'on','autojoin':'off','contact':'off','secretary':'off','forward':'off','forwardauthor':'off','forwardtime':10,'forwardid':0,'forwardchat':None,'forwardtype':None,'forwardreply':None,'subscription':30,'admins':[],'groups':[],'secretarytext':[]}
	put(f'data/{session}.json',data)

async def forward_message(to_peer,id,from_peer,reply_text,drop_author):
	message = await bot(functions.messages.ForwardMessagesRequest(from_peer = from_peer,id = [id],to_peer = to_peer,drop_author = drop_author))
	if reply_text:
		await bot.send_message(to_peer,reply_text,reply_to = message.updates[0].id)

forwardtime = get(f'data/{session}.json')['forwardtime']

@aiocron.crontab(f'*/{forwardtime} * * * *')
async def clock():
	data = get(f'data/{session}.json')
	if data['bot'] == 'on' and data['subscription'] != 0:
		if data['forward'] == 'on':
			if data['forwardid'] and data['forwardchat'] and data['forwardtype']:
				i = 0
				async for dialog in bot.iter_dialogs():
					if (data['forwardtype'] == 'privates' and isinstance(dialog.entity,types.User)) or (data['forwardtype'] == 'groups' and isinstance(dialog.entity,types.Chat)) or (data['forwardtype'] == 'super groups' and isinstance(dialog.entity,types.Channel) and dialog.entity.megagroup):
						try:
							await forward_message(dialog.id,data['forwardid'],data['forwardchat'],data['forwardreply'],data['forwardauthor'] == 'off')
							i += 1
						except Exception as e:
							await bot.send_message(dev,font(e))
				await bot.send_message(dev,font(f'Sent to {i} of ' + data['forwardtype'] + ' !'))

@aiocron.crontab(f'12 12 * * *')
async def subscription():
	data = get(f'data/{session}.json')
	if data['subscription'] > 0:
		data['subscription'] -= 1
		put(f'data/{session}.json',data)
	else:
		await bot.send_message(dev,font('The subscription to this tabchi has ended !'))

@bot.on(events.NewMessage())
async def updateMessage(event):
	data = get(f'data/{session}.json')
	text = event.raw_text
	chat_id = event.chat_id
	from_id = event.sender_id
	if from_id == dev or from_id in data['admins'] or chat_id in data['groups']:
		if from_id == dev:
			if match := re.match(r'AddSubscription (\d+)',text):
				time = int(match.group(1))
				data['subscription'] += time
				put(f'data/{session}.json',data)
				await event.reply(font('The subscription of the robot has been successfully increased !'))
			elif match := re.match(r'LowSubscription (\d+)',text):
				time = int(match.group(1))
				data['subscription'] -= time
				put(f'data/{session}.json',data)
				await event.reply(font('The subscription of the robot has been successfully reduced !'))
		if from_id != dev and data['subscription'] == 0:
			return await event.reply(font('Your subscription has ended !'))
		if match := re.match(r'(Bot|Secretary|Contact|AutoJoin|Forward|ForwardAuthor) ([Oo][Nn]|[Oo][Ff][Ff])',text):
			index = match.group(1).lower()
			status = match.group(2).lower()
			data[index] = status
			put(f'data/{session}.json',data)
			await event.reply(font(f'{index} now is {status} !'))
		elif data['bot'] == 'on':
			if text == 'Help':
				await event.reply(f'''
خاموش و روشن کردن ربات :
Bot on | off
خاموش و روشن کردن حالت منشی :
Secretary on | off
خاموش و روشن کردن حالت ذخیره خودکار مخاطب :
Contact on | off
خاموش و روشن کردن حالت عضو شدن خودکار لینک های خصوصی :
AutoJoin on | off
خاموش و روشن کردن فوروارد خودکار :
Forward on | off
فوروارد بدون نقل قول یا با نقل قول :
ForwardAuthor on | off
اطلاع از آنلاین بودن ربات :
Ping
گرفتن اطلاعات ربات :
Info
بدست آوردن اطلاعات یک فرد :
Id (REPLY)
اضافه کردن ادمین به ربات :
AddSudo (ID)
حذف ادمین از ربات :
DeleteSudo (ID)
گرفتن لیست ادمین ها :
SudoList
تغییر نام اکانت :
SetFirstName
تغییر نام خانوادگی اکانت :
SetLastName
تغییر بیوگرافی اکانت :
SetBiography
تغییر یوزرنیم اکانت :
SetUserName
تنظیم عکس برای عکس پروفایل اکانت :
SetPhoto (REPLY)
حذف تمام عکس های پروفایل ربات :
DeletePhoto
اضافه کردن متن منشی رندوم :
AddSecretary (TEXT)
حذف متن منشی :
DeleteSecretary (TEXT)
لیست متن های منشی رندوم :
SecretaryList
استارت کردن ربات :
Start (@username)
عضو شدن در یک گروه یا کانال :
Join (@username)
لفت دادن از یک گروه یا کانال :
Left (@username)
پاکسازی لیست مخاطبین :
CleanContactsList
اشتراک گزاری شماره اکانت :
Share
تنظیم زمان فوروارد خودکار :
ForwardTime (TIME)
اد کردن یه کاربر به همه‌ی گروه ها :
AddAll (REPLY)
فوروارد برای همه :
ForwardAll (REPLY)
فوروارد برای پیوی ها :
ForwardPrivates (REPLY)
فوروارد برای گروه های عادی :
ForwardGroups (REPLY)
فوروارد برای سوپر گروه ها :
ForwardSuperGroups (REPLY)
تنظیم فوروارد خودکار :
SetForward privates | super groups | groups
تنظیم متن ریپلی کردن روی پیام فوروارد شده :
SetForwardReply (REPLY)
حذف متن ریپلی شده روی پیام فوروارد شده :
DeleteForwardReply
اضافه کردن یک گروه به عنوان گروه مدیریت اکانت :
AddGp (IN GROUP)
حذف کردن یک گروه از لیست گروه های مدیریت اکانت :
DeleteGp (IN GROUP)

اشتراک ربات : {data['subscription']}
''')
			elif text == 'Ping':
				await event.reply(font('I am Online !'))
			elif text == 'Info':
				private_chats = 0
				bots = 0
				groups = 0
				broadcast_channels = 0
				admin_in_groups = 0
				creator_in_groups = 0
				admin_in_broadcast_channels = 0
				creator_in_channels = 0
				unread_mentions = 0
				unread = 0
				largest_group_member_count = 0
				largest_group_with_admin = 0
				async for dialog in bot.iter_dialogs():
					entity = dialog.entity
					if isinstance(entity,types.Channel):
						if entity.broadcast:
							broadcast_channels += 1
							if entity.creator or entity.admin_rights:
								admin_in_broadcast_channels += 1
							if entity.creator:
								creator_in_channels += 1
						elif entity.megagroup:
							groups += 1
							if entity.creator or entity.admin_rights:
								admin_in_groups += 1
							if entity.creator:
								creator_in_groups += 1
					elif isinstance(entity,types.User):
						private_chats += 1
						if entity.bot:
							bots += 1
					elif isinstance(entity,types.Chat):
						groups += 1
						if entity.creator or entity.admin_rights:
							admin_in_groups += 1
						if entity.creator:
							creator_in_groups += 1
					unread_mentions += dialog.unread_mentions_count
					unread += dialog.unread_count
				list = f'status !'
				list += f'\nprivate chats : {private_chats}'
				list += f'\nbots : {bots}'
				list += f'\ngroups : {groups}'
				list += f'\nbroadcast channels : {broadcast_channels}'
				list += f'\nadmin in groups : {admin_in_groups}'
				list += f'\ncreator in groups : {creator_in_groups}'
				list += f'\nadmin in broadcast channels : {admin_in_broadcast_channels}'
				list += f'\ncreator in channels : {creator_in_channels}'
				list += f'\nunread mentions : {unread_mentions}'
				list += f'\nunread : {unread}'
				list += f'\nlargest group member count : {largest_group_member_count}'
				list += f'\nlargest group with admin : {largest_group_with_admin}'
				await event.reply(font(list))
			elif match := re.match(r'AddSudo (\d+)',text):
				id = int(match.group(1))
				data['admins'].append(id)
				put(f'data/{session}.json',data)
				await event.respond(font(f'{id} was successfully added to the list of admins !'))
			elif match := re.match(r'DeleteSudo (\d+)',text):
				id = int(match.group(1))
				data['admins'].remove(id)
				put(f'data/{session}.json',data)
				await event.respond(font(f'{id} was successfully removed from the list of admins !'))
			elif text == 'SudoList':
				list = font('Sudo List :')
				for id in data['admins']:
					list += f'\n• [ᴜsᴇʀ](tg://user?id={id})'
				await event.respond(font(list))
			elif text == 'CleanSudoList':
				data['admins'] = []
				put(f'data/{session}.json',data)
			elif match := re.match(r'SetFirstName (.*)',text):
				try:
					await bot(functions.account.UpdateProfileRequest(first_name = match.group(1)))
					await event.reply(font('Your first name has been successfully changed !'))
				except Exception as e:
					await event.reply(font(e))
			elif match := re.match(r'SetLastName (.*)',text):
				try:
					await bot(functions.account.UpdateProfileRequest(last_name = match.group(1)))
					await event.reply(font('Your last name has been successfully changed !'))
				except Exception as e:
					await event.reply(font(e))
			elif match := re.match(r'SetBiography (.*)',text):
				try:
					await bot(functions.account.UpdateProfileRequest(about = match.group(1)))
					await event.reply(font('Your Biography has been successfully changed !'))
				except Exception as e:
					await event.reply(font(e))
			elif match := re.match(r'SetUserName (.*)',text):
				try:
					await bot(functions.account.UpdateUsernameRequest(username = match.group(1)))
					await event.reply(font('Your username has been successfully changed !'))
				except Exception as e:
					await event.reply(font(e))
			elif text == 'DeletePhoto':
				try:
					photos = await bot.get_profile_photos('me')
					for photo in photos:
						await bot(functions.photos.DeletePhotosRequest(id = [types.InputPhoto(id = photo.id,access_hash = photo.access_hash,file_reference = photo.file_reference)]))
					await event.reply(font('All your photos have been deleted !'))
				except Exception as e:
					await event.reply(font(e))
			elif match := re.match(r'AddSecretary (.*)',text):
				if match.group(1) in data['secretarytext']:
					await event.respond(font('This text is already saved !'))
				else:
					data['secretarytext'].append(match.group(1))
					put(f'data/{session}.json',data)
					await event.respond(font('This text has been successfully added !'))
			elif match := re.match(r'DeleteSecretary (.*)',text):
				if match.group(1) in data['secretarytext']:
					data['secretarytext'].remove(match.group(1))
					put(f'data/{session}.json',data)
					await event.respond(font('This text has been successfully removed !'))
				else:
					await event.respond(font('This text does not exist !'))
			elif text == 'SecretaryList':
				list = font('Secretary List :')
				for text in data['secretarytext']:
					list += f'\n• {text}'
				await event.respond(font(list))
			elif match := re.match(r'Start (.*)',text):
				try:
					await bot.send_message(match.group(1),'/start')
					await event.reply(font('The bot started successfully !'))
				except Exception as e:
					await event.reply(font(e))
			elif match := re.match(r'Join (.*)',text):
				invitelink = match.group(1)
				explode = invitelink.split('/')
				if len(explode) > 1:
					try:
						await bot(functions.messages.ImportChatInviteRequest(explode[-1]))
						await event.reply(font('I became a member !'))
					except Exception as e:
						await event.reply(font(e))
				else:
					try:
						await bot(functions.channels.JoinChannelRequest(invitelink))
						await event.reply(font('I became a member !'))
					except Exception as e:
						await event.reply(font(e))
			elif match := re.match(r'Left (.*)',text):
				invitelink = match.group(1)
				explode = invitelink.split('/')
				if len(explode) > 1:
					try:
						group = await client.get_entity(invitelink)
						await bot(functions.messages.DeleteExportedChatInviteRequest(int('-100' + str(group.id))))
						event.reply(font('I became a member !'))
					except Exception as e:
						await event.reply(font(e))
				else:
					try:
						await bot(functions.channels.LeaveChannelRequest(invitelink))
						await event.reply(font('I became a member !'))
					except Exception as e:
						await event.reply(font(e))
			elif text == 'CleanContactsList':
				try:
					contacts = await bot(functions.contacts.GetContactsRequest(hash = 0))
					await bot(functions.contacts.DeleteContactsRequest(id = [contact.id for contact in contacts.users]))
					await event.reply(font('All your contacts have been deleted !'))
				except Exception as e:
					await event.reply(font(e))
			elif text == 'Share':
				me = await bot.get_me()
				await bot.send_file(event.chat_id,types.InputMediaContact(phone_number = me.phone,first_name = me.first_name,last_name = me.last_name or str(),vcard = str()))
			elif match := re.match(r'ForwardTime (\d+)',text):
				time = int(match.group(1))
				clock.spec = f'*/{time} * * * *'
				clock.start()
				data['forwardtime'] = time
				put(f'data/{session}.json',data)
				await event.respond(font(f'The forwarding time was automatically set to {time} minute !'))
			elif text == 'DeleteForwardReply':
				data['forwardreply'] = None
				put(f'data/{session}.json',data)
				await event.reply(font(f'Replay on the forwarded message was successfully deleted !'))
			elif event.is_reply:
				if text == 'Id':
					getMessage = await event.get_reply_message()
					sender = getMessage.sender
					id = sender.id
					first_name = sender.first_name
					last_name = sender.last_name
					username = sender.username
					phone = sender.phone
					list = f'id : {id}'
					list += f'\nfirst name : {first_name}'
					list += f'\nlast name : {last_name}'
					list += f'\nusername : {username}'
					list += f'\nphone : {phone}'
					await event.reply(font(list))
				elif text == 'SetPhoto':
					try:
						message = await event.get_reply_message()
						media = await bot.download_media(message)
						await bot(functions.photos.UploadProfilePhotoRequest(await bot.upload_file(media)))
						os.remove(media)
						await event.reply(font('Your photo has been successfully changed !'))
					except Exception as e:
						await event.reply(font(e))
				elif text == 'AddAll':
					getMessage = await event.get_reply_message()
					id = getMessage.sender.id
					i = 0
					async for dialog in bot.iter_dialogs():
						if isinstance(dialog.entity,types.Chat) or (isinstance(dialog.entity,types.Channel) and dialog.entity.megagroup):
							try:
								await bot(functions.channels.InviteToChannelRequest(dialog.entity,[id]))
								i += 1
							except Exception as e:
								await event.reply(font(e))
					await event.reply(font(f'User {id} was successfully added to {i} groups !'))
				elif text == 'ForwardAll':
					i = 0
					async for dialog in bot.iter_dialogs():
						if isinstance(dialog.entity,(types.Chat,types.User)) or (isinstance(dialog.entity,types.Channel) and dialog.entity.megagroup):
							try:
								await forward_message(dialog.id,event.reply_to_msg_id,event.chat_id,data['forwardreply'],data['forwardauthor'] == 'off')
								i += 1
							except Exception as e:
								await event.reply(font(e))
					await event.reply(font(f'Sent to {i} of groups and super groups and privates !'))
				elif text == 'ForwardPrivates':
					i = 0
					async for dialog in bot.iter_dialogs():
						if isinstance(dialog.entity,types.User):
							try:
								await forward_message(dialog.id,event.reply_to_msg_id,event.chat_id,data['forwardreply'],data['forwardauthor'] == 'off')
								i += 1
							except Exception as e:
								await event.reply(font(e))
					await event.reply(font(f'Sent to {i} of privates !'))
				elif text == 'ForwardGroups':
					i = 0
					async for dialog in bot.iter_dialogs():
						if isinstance(dialog.entity,types.Chat):
							try:
								await forward_message(dialog.id,event.reply_to_msg_id,event.chat_id,data['forwardreply'],data['forwardauthor'] == 'off')
								i += 1
							except Exception as e:
								await event.reply(font(e))
					await event.reply(font(f'Sent to {i} of groups !'))
				elif text == 'ForwardSuperGroups':
					i = 0
					async for dialog in bot.iter_dialogs():
						if isinstance(dialog.entity,types.Channel) and dialog.entity.megagroup:
							try:
								await forward_message(dialog.id,event.reply_to_msg_id,event.chat_id,data['forwardreply'],data['forwardauthor'] == 'off')
								i += 1
							except Exception as e:
								await event.reply(font(e))
					await event.reply(font(f'Sent to {i} of super groups !'))
				elif match := re.match(r'SetForward (privates|super groups|groups)',text):
					data['forwardid'] = event.reply_to_msg_id
					data['forwardchat'] = event.chat_id
					data['forwardtype'] = match.group(1)
					put(f'data/{session}.json',data)
					await event.reply(font('Automatic forwarding has been successfully set !'))
				elif text == 'SetForwardReply':
					getMessage = await event.get_reply_message()
					if getMessage.raw_text:
						data['forwardreply'] = getMessage.raw_text
						put(f'data/{session}.json',data)
						await event.reply(font(f'The replay text was successfully set on the forwarded message !'))
					else:
						await event.reply(font(f'Please only reply to the text message !'))
			elif event.is_group:
				if text == 'AddGp':
					data['groups'].append(int(chat_id))
					put(f'data/{session}.json',data)
					await event.reply(font('This group was added to the list of bot management groups !'))
				elif text == 'DeleteGp':
					data['groups'].remove(int(chat_id))
					put(f'data/{session}.json',data)
					await event.reply(font('This group was removed from the list of bot management groups !'))
				elif text == 'AddContact':
					try:
						contacts = await bot(functions.contacts.GetContactsRequest(hash = 0))
						await bot(functions.channels.InviteToChannelRequest(event.chat_id,[contact.id for contact in contacts.users]))
					except Exception as e:
						await event.reply(font(e))
					await event.reply(font('I added most of my contacts to this group !'))
	elif data['bot'] == 'on' and data['subscription'] != 0:
		if data['secretary'] == 'on' and event.is_private:
			if len(data['secretarytext']) > 0:
				await event.reply(random.choice(data['secretarytext']))
		if data['contact'] == 'on' and event.contact:
			await bot(functions.contacts.AddContactRequest(id = event.contact.user_id,first_name = event.contact.first_name,last_name = event.contact.last_name,phone = event.contact.phone_number,add_phone_privacy_exception = False))
		if data['autojoin'] == 'on':
			if links := re.findall('(?:https?://)?(t|telegram)\.me/(?:\+|joinchat/)([\w\-]+)',text):
				for link in links:
					await bot(functions.messages.ImportChatInviteRequest(link[-1]))

bot.start()
clock.start()
subscription.start()
bot.run_until_disconnected()
asyncio.get_event_loop().run_forever()