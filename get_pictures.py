def get(vk_session, session, id_group, vk):
    attachments = []
    from vk_api import VkUpload
    upload = VkUpload(vk_session)
    image_url = 'https://i.pinimg.com/736x/77/42/8e/77428e14118bffd18623e30be8f6afca.jpg'
    image = session.get(image_url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments.append(
        'photo{}_{}'.format(photo['owner_id'], photo['id'])
    )
    attachment = ','.join(attachments)
    return attachment

