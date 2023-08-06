import phonenumbers


def is_valid(phone_number):
        try:
            parsed_number = phonenumbers.parse(str(phone_number), "TZ")
            print(parsed_number)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False 