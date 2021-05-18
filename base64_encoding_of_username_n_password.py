import base64

userName = "vivek"
password = "vivek*******"
auth = base64.b64encode(("%s:%s" % ( userName, password )).encode("utf-8"))

print(auth)
