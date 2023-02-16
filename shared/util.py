"""
Takes a hex value in the form of "0x00" and returns the integer of the same value.
Params:
   hexStr: String - The string of a hex value

 Returns:
   hexInt: Int - The integer value of the hex string
"""
def hexStringToInt(hexStr):
    return int(hexStr, 0)