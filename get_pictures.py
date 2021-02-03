def get(vk_session, session, id_group, vk):
    attachments = []
    from vk_api import VkUpload
    upload = VkUpload(vk_session)
    image_url = 'Ссылка на картинку'
    image = session.get(image_url, stream=True)
    photo = upload.photo_messages(photos=image.raw)[0]
    attachments.append(
        'photo{}_{}'.format(photo['owner_id'], photo['id'])
    )
    attachment = ','.join(attachments)

