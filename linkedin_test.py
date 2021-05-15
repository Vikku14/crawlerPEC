from linkedin_api import Linkedin

# Authenticate using any Linkedin account credentials
api = Linkedin('viveksharma.mtcse19@pec.edu.in', 'vivek@pec')

# GET a profile
profile = api.get_profile('pooja-sareen-23874151')
print(profile)
# GET a profiles contact info
# contact_info = api.get_profile_contact_info('billy-g')
# print(contact_info)
