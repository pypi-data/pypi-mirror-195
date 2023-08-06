def load_profile():
    from scinode.profile import ScinodeProfile
    from mongoengine import connect

    profiles = ScinodeProfile()
    data = profiles.load_activate_profile()
    connect(data["db_name"], host=data["db_address"])
