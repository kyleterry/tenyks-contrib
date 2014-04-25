output = "I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux."

def run(data, settings):
    payload = data['payload'].lower()
    if 'linux' in payload and 'gnu' not in payload:
        return output
