def get(vk_session, id_group, vk):
    try:
        print('0')
        attachment = ''
        #max_num = vk.photos.get(owner_id=id_group, album_id='wall')['count']
        #print(max_num)
        pictures = vk.photos.get(owner_id=str(id_group), album_id='wall')['ítems']
        buf = []
        for element in pictures:
            buf.append('photo' + str(id_group) + '_' + str(element['id']))
        attachment = ','.join(buf)
        print(attachment)
        return attachment
    except:
        return get(vk_session, id_group, vk)
        #id_group = -202310522
