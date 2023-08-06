import re


def validate(citizen_id: str) -> bool:
    # Check type string and only number 13 digits and not start with 0 or 9
    if not isinstance(citizen_id, str) or not re.match('^[0-9]{13}$', citizen_id) or re.match('[09]', citizen_id[0]):
        return False

    # Checksum
    if calculateCheckSum(citizen_id) != citizen_id[12]:
        return False
    return True


def calculateCheckSum(citizen_id: str) -> str:
    sum = 0
    for i in range(12):
        sum += int(citizen_id[i]) * (13 - i)

    return str((11 - sum % 11) % 10)
