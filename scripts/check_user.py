from load_text import *


def user_is_admin(user_id=None, user_alias=None):
    	
	admins_json = load_json(ADMINS_JSON_FILEPATH)
	admin_dicts = admins_json['admins']

	if user_id:
		return user_id in [admin_dict['user_id'] for admin_dict in admin_dicts]

	elif user_alias:
		return user_alias in [admin_dict['user_alias'] for admin_dict in admin_dicts]

	return None